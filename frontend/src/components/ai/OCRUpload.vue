<template>
  <div class="ocr-upload">
    <!-- 上传区域 -->
    <div class="upload-area" v-if="!imagePreview">
      <div class="upload-icon">
        <i class="fas fa-camera"></i>
      </div>
      <p class="upload-text">拍照或选择图片识别物品</p>
      <div class="upload-buttons">
        <label class="btn-upload">
          <i class="fas fa-camera"></i>
          拍照
          <input
            type="file"
            accept="image/*"
            capture="environment"
            @change="handleImageSelect"
            style="display: none"
          />
        </label>
        <label class="btn-upload">
          <i class="fas fa-image"></i>
          选择图片
          <input
            type="file"
            accept="image/*"
            @change="handleImageSelect"
            style="display: none"
          />
        </label>
      </div>
    </div>

    <!-- 图片预览 -->
    <div class="image-preview" v-if="imagePreview && !recognizing">
      <img :src="imagePreview" alt="预览图片" />
      <div class="preview-actions">
        <button class="btn-secondary" @click="resetUpload">
          <i class="fas fa-redo"></i>
          重新选择
        </button>
        <button class="btn-primary" @click="startRecognition">
          <i class="fas fa-magic"></i>
          开始识别
        </button>
      </div>
    </div>

    <!-- 识别中 -->
    <div class="recognizing-state" v-if="recognizing">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
      </div>
      <p>正在识别中...</p>
    </div>

    <!-- 识别结果 -->
    <div class="recognition-results" v-if="recognizedItems.length > 0 && !recognizing">
      <div class="results-header">
        <h4>识别结果（{{ recognizedItems.length }}个物品）</h4>
        <button class="btn-text" @click="resetUpload">
          <i class="fas fa-redo"></i>
          重新识别
        </button>
      </div>

      <div class="items-list">
        <div
          v-for="(item, index) in recognizedItems"
          :key="index"
          class="item-card"
        >
          <div class="item-header">
            <span class="item-number">{{ index + 1 }}</span>
            <button class="btn-remove" @click="removeItem(index)">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="item-form">
            <div class="form-row">
              <label>名称</label>
              <input
                v-model="item.name"
                type="text"
                class="mobile-input"
                placeholder="物品名称"
              />
            </div>
            <div class="form-row-group">
              <div class="form-row">
                <label>数量</label>
                <input
                  v-model.number="item.quantity"
                  type="number"
                  class="mobile-input"
                  placeholder="数量"
                  min="1"
                />
              </div>
              <div class="form-row">
                <label>单位</label>
                <input
                  v-model="item.unit"
                  type="text"
                  class="mobile-input"
                  placeholder="单位"
                />
              </div>
            </div>
            <div class="form-row">
              <label>过期日期</label>
              <input
                v-model="item.expire_date"
                type="date"
                class="mobile-input"
              />
            </div>
            <div class="form-row-group">
              <div class="form-row">
                <label>存放位置</label>
                <select v-model="item.place" class="mobile-input">
                  <option value="cold">冷藏</option>
                  <option value="frozen">冷冻</option>
                  <option value="normal">常温</option>
                </select>
              </div>
              <div class="form-row">
                <label>类型</label>
                <select v-model="item.type" class="mobile-input">
                  <option value="蔬菜">蔬菜</option>
                  <option value="水果">水果</option>
                  <option value="肉类">肉类</option>
                  <option value="饮料">饮料</option>
                  <option value="调味品">调味品</option>
                  <option value="面包糕点">面包糕点</option>
                  <option value="乳制品">乳制品</option>
                  <option value="其他">其他</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="results-actions">
        <button class="btn-secondary" @click="resetUpload">
          取消
        </button>
        <button class="btn-primary" @click="confirmAdd" :disabled="adding">
          <i class="fas fa-check"></i>
          {{ adding ? '添加中...' : `添加 ${recognizedItems.length} 个物品` }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as itemApi from '@/api/item'
import { useFridgeStore } from '@/stores/fridge'

const emit = defineEmits<{
  success: []
  close: []
}>()

const fridgeStore = useFridgeStore()

const imagePreview = ref<string>('')
const imageData = ref<string>('')
const recognizing = ref(false)
const adding = ref(false)
const recognizedItems = ref<Array<{
  name: string
  quantity: number
  unit?: string
  expire_date: string
  place: string
  type: string
}>>([])

// 处理图片选择
const handleImageSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // 检查文件大小（限制 5MB）
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }
  
  // 读取文件并转换为 Base64
  const reader = new FileReader()
  reader.onload = (e) => {
    const result = e.target?.result as string
    imagePreview.value = result
    imageData.value = result
  }
  reader.onerror = () => {
    ElMessage.error('读取图片失败')
  }
  reader.readAsDataURL(file)
  
  // 重置 input
  target.value = ''
}

// 开始识别
const startRecognition = async () => {
  if (!imageData.value) {
    ElMessage.error('请先选择图片')
    return
  }
  
  recognizing.value = true
  
  try {
    const response = await itemApi.ocrRecognize(imageData.value, false)
    
    if (response.success && response.data) {
      const result = response.data
      
      if (result.items && result.items.length > 0) {
        // 处理识别结果，确保所有字段都有默认值
        const defaultExpireDate = getDefaultExpireDate()
        recognizedItems.value = result.items.map(item => ({
          name: item.name || '',
          quantity: Number((item as any).quantity || item.num || 1),
          unit: item.unit || '个',
          expire_date: (item.expire_date || defaultExpireDate) as string,
          place: (item.place as string) || 'cold',
          type: item.type || '其他'
        }))
        
        ElMessage.success(`识别成功！找到 ${result.items.length} 个物品`)
      } else {
        ElMessage.warning('未识别到物品信息，请重新拍照或手动添加')
        resetUpload()
      }
    } else {
      ElMessage.error('识别失败，请重试')
      resetUpload()
    }
  } catch (error: any) {
    console.error('OCR 识别失败:', error)
    ElMessage.error(error.response?.data?.error || '识别失败，请重试')
    resetUpload()
  } finally {
    recognizing.value = false
  }
}

// 获取默认过期日期（7天后）
const getDefaultExpireDate = () => {
  const date = new Date()
  date.setDate(date.getDate() + 7)
  return date.toISOString().split('T')[0]
}

// 移除物品
const removeItem = (index: number) => {
  recognizedItems.value.splice(index, 1)
  if (recognizedItems.value.length === 0) {
    resetUpload()
  }
}

// 确认添加
const confirmAdd = async () => {
  // 验证所有物品
  const invalidItems = recognizedItems.value.filter(
    item => !item.name || !item.expire_date || !item.place || !item.type
  )
  
  if (invalidItems.length > 0) {
    ElMessage.error('请填写完整的物品信息')
    return
  }
  
  adding.value = true
  
  try {
    const response = await itemApi.batchAddItems(
      recognizedItems.value,
      fridgeStore.currentFridgeId
    )
    
    if (response.success && response.data) {
      const { added, failed, total } = response.data
      
      if (failed > 0) {
        ElMessage.warning(`成功添加 ${added}/${total} 个物品`)
      } else {
        ElMessage.success(`成功添加 ${added} 个物品`)
      }
      
      emit('success')
      emit('close')
      resetUpload()
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

// 重置上传
const resetUpload = () => {
  imagePreview.value = ''
  imageData.value = ''
  recognizing.value = false
  adding.value = false
  recognizedItems.value = []
}
</script>

<style scoped>
.ocr-upload {
  padding: 20px;
}

.upload-area {
  text-align: center;
  padding: 40px 20px;
}

.upload-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: var(--bg-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: var(--primary-color);
}

.upload-text {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.upload-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-upload {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-upload:active {
  transform: scale(0.98);
}

.image-preview {
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.preview-actions {
  display: flex;
  gap: 12px;
}

.recognizing-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  font-size: 48px;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.recognizing-state p {
  font-size: 16px;
  color: var(--text-secondary);
}

.recognition-results {
  max-height: 60vh;
  overflow-y: auto;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.results-header h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.btn-text {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.item-card {
  background: var(--bg-color);
  border-radius: 12px;
  padding: 16px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-number {
  width: 28px;
  height: 28px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.btn-remove {
  width: 28px;
  height: 28px;
  background: var(--danger-color);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-row-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.results-actions {
  display: flex;
  gap: 12px;
  position: sticky;
  bottom: 0;
  background: var(--card-bg);
  padding: 16px 0;
}
</style>
