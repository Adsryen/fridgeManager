<template>
  <button
    class="voice-btn"
    :class="{ recording: isRecording, processing: isProcessing }"
    @click="toggleRecording"
    :disabled="isProcessing"
    :title="isRecording ? '停止录音' : '语音输入'"
  >
    <i v-if="!isRecording && !isProcessing" class="fas fa-microphone"></i>
    <i v-if="isRecording" class="fas fa-stop"></i>
    <i v-if="isProcessing" class="fas fa-spinner fa-spin"></i>
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as itemApi from '@/api/item'

const emit = defineEmits<{
  textRecognized: [text: string]
}>()

const isRecording = ref(false)
const isProcessing = ref(false)
const mediaRecorder = ref<MediaRecorder | null>(null)
const audioChunks = ref<Blob[]>([])

// 开始/停止录音
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

// 开始录音
const startRecording = async () => {
  try {
    // 请求麦克风权限
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // 创建 MediaRecorder
    const recorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm'
    })
    
    audioChunks.value = []
    
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    recorder.onstop = async () => {
      // 停止所有音频轨道
      stream.getTracks().forEach(track => track.stop())
      
      // 处理录音数据
      await processAudio()
    }
    
    recorder.start()
    mediaRecorder.value = recorder
    isRecording.value = true
    
    ElMessage.info('开始录音...')
  } catch (error: any) {
    console.error('启动录音失败:', error)
    
    if (error.name === 'NotAllowedError') {
      ElMessage.error('请允许使用麦克风权限')
    } else if (error.name === 'NotFoundError') {
      ElMessage.error('未找到麦克风设备')
    } else {
      ElMessage.error('启动录音失败')
    }
  }
}

// 停止录音
const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}

// 处理音频数据
const processAudio = async () => {
  if (audioChunks.value.length === 0) {
    ElMessage.warning('未录制到音频')
    return
  }
  
  isProcessing.value = true
  
  try {
    // 创建音频 Blob
    const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
    
    // 转换为 WAV 格式（如果需要）
    const wavBlob = await convertToWav(audioBlob)
    
    // 转换为 Base64
    const base64Audio = await blobToBase64(wavBlob)
    
    // 调用语音识别 API
    const response = await itemApi.voiceToText(base64Audio)
    
    if (response.success && response.data?.text) {
      const text = response.data.text.trim()
      
      if (text) {
        ElMessage.success('识别成功')
        emit('textRecognized', text)
      } else {
        ElMessage.warning('未识别到内容')
      }
    } else {
      ElMessage.error('识别失败，请重试')
    }
  } catch (error: any) {
    console.error('处理音频失败:', error)
    ElMessage.error(error.response?.data?.error || '识别失败，请重试')
  } finally {
    isProcessing.value = false
    audioChunks.value = []
  }
}

// 转换为 WAV 格式
const convertToWav = async (blob: Blob): Promise<Blob> => {
  // 简化版本：直接返回原始 blob
  // 实际项目中可能需要使用 Web Audio API 进行格式转换
  return blob
}

// Blob 转 Base64
const blobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => {
      const result = reader.result as string
      resolve(result)
    }
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}
</script>

<style scoped>
.voice-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-color);
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 16px;
}

.voice-btn:hover {
  background: var(--border-color);
  color: var(--text-primary);
}

.voice-btn.recording {
  background: var(--danger-color);
  color: white;
  animation: pulse 1.5s infinite;
}

.voice-btn.processing {
  background: var(--primary-color);
  color: white;
}

.voice-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}
</style>
