<template>
  <div class="item-form">
    <form @submit.prevent="handleSubmit">
      <!-- 物品名称 -->
      <div class="form-group">
        <label><i class="fas fa-tag"></i> 物品名称</label>
        <input
          v-model="formData.name"
          type="text"
          class="mobile-input"
          placeholder="例如：牛奶、苹果..."
          required
        />
      </div>

      <!-- 到期日期 -->
      <div class="form-group">
        <label><i class="fas fa-calendar-alt"></i> 到期日期</label>
        <div class="date-picker-custom">
          <input
            v-model="formData.expire_date"
            type="date"
            class="date-input-hidden"
            required
            @change="updateDateDisplay"
          />
          <div class="date-display-area" @click="focusDateInput">
            <i class="fas fa-calendar-alt date-display-icon"></i>
            <span
              class="date-display-text"
              :class="{ 'has-value': formData.expire_date }"
            >
              {{ dateDisplayText }}
            </span>
          </div>
        </div>
        <div class="date-shortcuts">
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(3)">
            3天后
          </button>
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(7)">
            1周后
          </button>
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(14)">
            2周后
          </button>
        </div>
        <div class="date-shortcuts">
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(30)">
            1月后
          </button>
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(60)">
            2月后
          </button>
          <button type="button" class="date-shortcut-btn" @click="setDateShortcut(90)">
            3月后
          </button>
        </div>
      </div>

      <!-- 数量 -->
      <div class="form-group">
        <label><i class="fas fa-boxes"></i> 数量</label>
        <input
          v-model.number="formData.quantity"
          type="number"
          class="mobile-input"
          min="1"
          required
        />
      </div>

      <!-- 存放位置 -->
      <div class="form-group">
        <label><i class="fas fa-map-marker-alt"></i> 存放位置</label>
        <div class="place-selector">
          <label class="place-option">
            <input v-model="formData.place" type="radio" value="cold" />
            <div class="place-card">
              <i class="fas fa-temperature-low"></i>
              <span>冷藏室</span>
            </div>
          </label>
          <label class="place-option">
            <input v-model="formData.place" type="radio" value="frozer" />
            <div class="place-card">
              <i class="fas fa-snowflake"></i>
              <span>冷冻室</span>
            </div>
          </label>
          <label class="place-option">
            <input v-model="formData.place" type="radio" value="room" />
            <div class="place-card">
              <i class="fas fa-home"></i>
              <span>室温区</span>
            </div>
          </label>
        </div>
      </div>

      <!-- 类别 -->
      <div class="form-group">
        <label>
          <i class="fas fa-layer-group"></i> 类别
          <span class="text-muted">(单选)</span>
        </label>
        <div class="category-grid">
          <div
            v-for="cat in categories"
            :key="cat.value"
            class="category-item"
            :class="{ selected: formData.type === cat.value }"
            @click="formData.type = cat.value"
          >
            <span class="emoji">{{ cat.emoji }}</span>
            <span class="text">{{ cat.label }}</span>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="handleCancel">取消</button>
        <button type="submit" class="btn-primary" :disabled="loading">
          <i class="fas fa-check"></i>
          {{ loading ? '添加中...' : '添加' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { addItem } from '@/api/item'
import { useFridgeStore } from '@/stores/fridge'

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const fridgeStore = useFridgeStore()
const loading = ref(false)

const categories = [
  { value: 'vegetable', label: '蔬菜', emoji: '🥬' },
  { value: 'fruit', label: '水果', emoji: '🍎' },
  { value: 'seafood', label: '海鲜', emoji: '🐟' },
  { value: 'meat', label: '肉类', emoji: '🥩' },
  { value: 'beverage', label: '饮料', emoji: '🥤' },
  { value: 'diary', label: '乳制品', emoji: '🥛' },
  { value: 'egg', label: '蛋豆类', emoji: '🥚' },
  { value: 'bread', label: '面包', emoji: '🍞' },
  { value: 'frozen', label: '冷冻食品', emoji: '🍦' },
  { value: 'sauce', label: '酱料', emoji: '🍯' },
  { value: 'snack', label: '零食', emoji: '🍿' },
  { value: 'other', label: '其他', emoji: '📦' }
]

const formData = reactive({
  name: '',
  quantity: 1,
  expire_date: '',
  place: 'cold' as 'cold' | 'frozer' | 'room',
  type: 'other'
})

const dateDisplayText = computed(() => {
  if (!formData.expire_date) {
    return '点击选择日期'
  }
  const date = new Date(formData.expire_date)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}年${month}月${day}日`
})

const focusDateInput = () => {
  const input = document.querySelector('.date-input-hidden') as HTMLInputElement
  if (input) {
    input.focus()
    input.click()
  }
}

const updateDateDisplay = () => {
  // 日期显示会自动更新
}

const setDateShortcut = (days: number) => {
  const date = new Date()
  date.setDate(date.getDate() + days)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  formData.expire_date = `${year}-${month}-${day}`
}

const handleCancel = () => {
  emit('cancel')
}

const handleSubmit = async () => {
  if (loading.value) return

  // 验证表单
  if (!formData.name || !formData.expire_date || !formData.type) {
    ElMessage.error('请填写完整信息')
    return
  }

  loading.value = true
  try {
    const response = await addItem({
      name: formData.name,
      quantity: formData.quantity,
      expire_date: formData.expire_date,
      place: formData.place,
      type: formData.type,
      fridge_id: fridgeStore.currentFridgeId
    })

    if (response.success) {
      ElMessage.success('添加成功')
      // 重置表单
      formData.name = ''
      formData.quantity = 1
      formData.expire_date = ''
      formData.place = 'cold'
      formData.type = 'other'
      emit('success')
    } else {
      ElMessage.error(response.error || '添加失败')
    }
  } catch (error: any) {
    console.error('添加物品失败:', error)
    ElMessage.error(error.message || '添加失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.item-form {
  padding: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-group label i {
  color: var(--primary-color);
}

.text-muted {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 400;
}

.mobile-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-bg);
  color: var(--text-primary);
  transition: all 0.3s;
}

.mobile-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 日期选择器 */
.date-picker-custom {
  position: relative;
  margin-bottom: 8px;
}

.date-input-hidden {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  width: 0;
  height: 0;
}

.date-display-area {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-bg);
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-display-area:active {
  transform: scale(0.98);
  border-color: var(--primary-color);
}

.date-display-icon {
  color: var(--primary-color);
  font-size: 18px;
}

.date-display-text {
  flex: 1;
  color: var(--text-secondary);
}

.date-display-text.has-value {
  color: var(--text-primary);
  font-weight: 500;
}

.date-shortcuts {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.date-shortcut-btn {
  flex: 1;
  padding: 8px 12px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.date-shortcut-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.date-shortcut-btn:active {
  transform: scale(0.95);
}

/* 位置选择器 */
.place-selector {
  display: flex;
  gap: 12px;
}

.place-option {
  flex: 1;
  cursor: pointer;
}

.place-option input {
  display: none;
}

.place-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: var(--bg-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  transition: all 0.3s;
}

.place-option input:checked + .place-card {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-color: transparent;
}

.place-card i {
  font-size: 24px;
}

.place-card span {
  font-size: 13px;
  font-weight: 500;
}

/* 类别网格 */
.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  background: var(--bg-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:active {
  transform: scale(0.95);
}

.category-item.selected {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-color: transparent;
}

.category-item .emoji {
  font-size: 32px;
}

.category-item .text {
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

/* 表单操作按钮 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-color);
  color: var(--text-primary);
}

.btn-secondary:active {
  transform: scale(0.98);
  background: var(--border-color);
}
</style>
