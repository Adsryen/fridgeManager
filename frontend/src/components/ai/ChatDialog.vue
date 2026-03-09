<template>
  <div class="chat-dialog">
    <!-- 聊天历史 -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-avatar">
          <i :class="message.role === 'user' ? 'fas fa-user' : 'fas fa-robot'"></i>
        </div>
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="message assistant">
        <div class="message-avatar">
          <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
          <div class="message-text">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 识别的物品列表 -->
      <div v-if="parsedItems.length > 0" class="items-preview">
        <div class="items-header">
          <h4>识别到 {{ parsedItems.length }} 个物品</h4>
        </div>
        <div class="items-list">
          <div
            v-for="(item, index) in parsedItems"
            :key="index"
            class="item-preview-card"
          >
            <div class="item-info">
              <div class="item-name">{{ item.name }}</div>
              <div class="item-details">
                {{ item.quantity }}{{ item.unit }} · {{ item.expire_date }} · {{ item.place }}
              </div>
            </div>
          </div>
        </div>
        <div class="items-actions">
          <button class="btn-secondary" @click="clearParsedItems">
            取消
          </button>
          <button class="btn-primary" @click="confirmAddItems" :disabled="adding">
            <i class="fas fa-check"></i>
            {{ adding ? '添加中...' : '确认添加' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input-area">
      <div class="input-actions">
        <button class="btn-icon" @click="clearHistory" title="清空历史">
          <i class="fas fa-trash"></i>
        </button>
        <VoiceInput @text-recognized="handleVoiceText" />
      </div>
      <div class="input-wrapper">
        <textarea
          v-model="inputMessage"
          class="chat-input"
          placeholder="告诉我你要添加什么物品..."
          rows="1"
          @keydown.enter.exact.prevent="sendMessage"
          @input="autoResize"
          ref="inputRef"
        ></textarea>
        <button
          class="btn-send"
          @click="sendMessage"
          :disabled="!inputMessage.trim() || loading"
        >
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as itemApi from '@/api/item'
import { useFridgeStore } from '@/stores/fridge'
import type { ChatMessage } from '@/types/models'
import VoiceInput from './VoiceInput.vue'

const emit = defineEmits<{
  success: []
}>()

const fridgeStore = useFridgeStore()

const messages = ref<ChatMessage[]>([])
const inputMessage = ref('')
const loading = ref(false)
const adding = ref(false)
const parsedItems = ref<Array<{
  name: string
  quantity: number
  unit?: string
  expire_date: string
  place: string
  type: string
}>>([])

const messagesContainer = ref<HTMLElement>()
const inputRef = ref<HTMLTextAreaElement>()

// 加载聊天历史
const loadChatHistory = async () => {
  try {
    const response = await itemApi.getChatHistory()
    if (response.success && response.data) {
      messages.value = response.data.map((msg: any) => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp || new Date().toISOString()
      }))
      scrollToBottom()
    }
  } catch (_error) {
    console.error('加载聊天历史失败:', _error)
  }
}

// 发送消息
const sendMessage = async () => {
  const text = inputMessage.value.trim()
  if (!text || loading.value) return
  
  // 添加用户消息
  const userMessage: ChatMessage = {
    role: 'user',
    content: text,
    timestamp: new Date().toISOString()
  }
  messages.value.push(userMessage)
  inputMessage.value = ''
  loading.value = true
  
  // 重置 textarea 高度
  if (inputRef.value) {
    inputRef.value.style.height = 'auto'
  }
  
  scrollToBottom()
  
  try {
    // 调用 AI 对话接口（SSE 流式）
    const response = await fetch('/item/ai-chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        messages: messages.value.map(m => ({
          role: m.role,
          content: m.content
        }))
      })
    })
    
    if (!response.ok) {
      throw new Error('请求失败')
    }
    
    // 创建 AI 消息
    const aiMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString()
    }
    messages.value.push(aiMessage)
    
    // 读取 SSE 流
    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    
    if (!reader) {
      throw new Error('无法读取响应流')
    }
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          
          try {
            const json = JSON.parse(data)
            
            if (json.content) {
              // 追加内容
              aiMessage.content += json.content
              scrollToBottom()
            }
            
            if (json.done) {
              // 流结束，尝试解析 JSON 物品数据
              parseItemsFromMessage(aiMessage.content)
              break
            }
            
            if (json.error) {
              ElMessage.error(json.error)
              break
            }
          } catch (_e) {
            // 忽略解析错误
          }
        }
      }
    }
  } catch (error: any) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败，请重试')
    // 移除失败的消息
    messages.value.pop()
  } finally {
    loading.value = false
  }
}

// 从消息中解析物品数据
const parseItemsFromMessage = (content: string) => {
  try {
    // 查找 JSON 代码块
    const jsonMatch = content.match(/```json\s*(\{[\s\S]*?\})\s*```/)
    if (jsonMatch && jsonMatch[1]) {
      const jsonData = JSON.parse(jsonMatch[1])
      if (jsonData.items && Array.isArray(jsonData.items)) {
        parsedItems.value = jsonData.items.map((item: any) => ({
          name: item.name || '',
          quantity: item.quantity || 1,
          unit: item.unit || '个',
          expire_date: item.expire_date || '',
          place: item.place || 'cold',
          type: item.type || '其他'
        }))
        scrollToBottom()
      }
    }
  } catch (_error) {
    console.error('解析物品数据失败:', _error)
  }
}

// 确认添加物品
const confirmAddItems = async () => {
  if (parsedItems.value.length === 0) return
  
  adding.value = true
  
  try {
    const response = await itemApi.batchAddItems(
      parsedItems.value,
      fridgeStore.currentFridgeId
    )
    
    if (response.success && response.data) {
      const { added, failed, total } = response.data
      
      if (failed > 0) {
        ElMessage.warning(`成功添加 ${added}/${total} 个物品`)
      } else {
        ElMessage.success(`成功添加 ${added} 个物品`)
      }
      
      clearParsedItems()
      emit('success')
    } else {
      ElMessage.error('添加失败，请重试')
    }
  } catch (error: any) {
    console.error('批量添加失败:', error)
    ElMessage.error(error.response?.data?.error || '添加失败，请重试')
  } finally {
    adding.value = false
  }
}

// 清除解析的物品
const clearParsedItems = () => {
  parsedItems.value = []
}

// 清空聊天历史
const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空聊天历史吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await itemApi.clearChatHistory()
    if (response.success) {
      messages.value = []
      parsedItems.value = []
      ElMessage.success('已清空聊天历史')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空历史失败:', error)
      ElMessage.error('清空失败，请重试')
    }
  }
}

// 处理语音识别文本
const handleVoiceText = (text: string) => {
  inputMessage.value = text
  nextTick(() => {
    autoResize()
  })
}

// 格式化消息（支持 Markdown）
const formatMessage = (content: string) => {
  // 简单的 Markdown 格式化
  let formatted = content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
  
  // 移除 JSON 代码块（已经显示在物品预览中）
  formatted = formatted.replace(/```json[\s\S]*?```/g, '')
  
  return formatted
}

// 格式化时间
const formatTime = (timestamp?: string) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 自动调整 textarea 高度
const autoResize = () => {
  if (inputRef.value) {
    inputRef.value.style.height = 'auto'
    inputRef.value.style.height = inputRef.value.scrollHeight + 'px'
  }
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动
watch(() => messages.value.length, () => {
  scrollToBottom()
})

onMounted(() => {
  loadChatHistory()
})
</script>

<style scoped>
.chat-dialog {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.message.assistant .message-avatar {
  background: var(--bg-color);
  color: var(--primary-color);
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: 12px 12px 4px 12px;
}

.message.assistant .message-text {
  background: var(--bg-color);
  color: var(--text-primary);
  border-radius: 12px 12px 12px 4px;
}

.message-time {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 0 4px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: var(--text-secondary);
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.items-preview {
  background: var(--card-bg);
  border: 2px solid var(--primary-color);
  border-radius: 12px;
  padding: 16px;
  margin-top: 8px;
}

.items-header h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--primary-color);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.item-preview-card {
  background: var(--bg-color);
  border-radius: 8px;
  padding: 12px;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.item-details {
  font-size: 13px;
  color: var(--text-secondary);
}

.items-actions {
  display: flex;
  gap: 8px;
}

.chat-input-area {
  border-top: 1px solid var(--border-color);
  padding: 12px;
  background: var(--card-bg);
}

.input-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.btn-icon {
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
}

.btn-icon:hover {
  background: var(--border-color);
  color: var(--text-primary);
}

.input-wrapper {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  padding: 10px 14px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 15px;
  background: var(--bg-color);
  color: var(--text-primary);
  resize: none;
  max-height: 120px;
  overflow-y: auto;
  font-family: inherit;
}

.chat-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-send {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-send:not(:disabled):active {
  transform: scale(0.95);
}
</style>
