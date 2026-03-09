<template>
  <div class="item-edit-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label><i class="fas fa-tag"></i> 物品名称</label>
        <input
          v-model="formData.name"
          type="text"
          class="form-input"
          placeholder="请输入物品名称"
          required
        />
      </div>

      <div class="form-group">
        <label><i class="fas fa-calendar-alt"></i> 过期日期</label>
        <input
          v-model="formData.expire_date"
          type="date"
          class="form-input"
          required
        />
      </div>

      <div class="form-group">
        <label><i class="fas fa-map-marker-alt"></i> 存放位置</label>
        <div class="radio-group">
          <label class="radio-item">
            <input v-model="formData.place" type="radio" value="cold" />
            <span class="radio-label">
              <i class="fas fa-temperature-low"></i>
              冷藏室
            </span>
          </label>
          <label class="radio-item">
            <input v-model="formData.place" type="radio" value="frozer" />
            <span class="radio-label">
              <i class="fas fa-snowflake"></i>
              冷冻室
            </span>
          </label>
          <label class="radio-item">
            <input v-model="formData.place" type="radio" value="room" />
            <span class="radio-label">
              <i class="fas fa-home"></i>
              室温区
            </span>
          </label>
        </div>
      </div>

      <div class="form-group">
        <label><i class="fas fa-boxes"></i> 数量</label>
        <input
          v-model.number="formData.num"
          type="number"
          class="form-input"
          min="0"
          required
        />
      </div>

      <div class="form-group">
        <label><i class="fas fa-th-large"></i> 物品分类</label>
        <div class="category-grid">
          <button
            v-for="cat in categories"
            :key="cat.value"
            type="button"
            class="category-item"
            :class="{ selected: formData.type === cat.value }"
            @click="formData.type = cat.value"
          >
            <span class="category-emoji">{{ cat.emoji }}</span>
            <span class="category-name">{{ cat.label }}</span>
          </button>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="handleCancel">取消</button>
        <button type="submit" class="btn-primary" :disabled="loading">
          <i class="fas fa-save"></i>
          {{ loading ? '保存中...' : '保存' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { Item } from '@/types/models'
import { updateItem } from '@/api/item'

interface Props {
  item: Item
}

const props = defineProps<Props>()
const emit = defineEmits<{
  success: []
  cancel: []
}>()

const loading = ref(false)

const categories = [
  { value: 'vegetable', label: '蔬菜', emoji: '🥬' },
  { value: 'fruit', label: '水果', emoji: '🍎' },
  { value: 'meat', label: '肉类', emoji: '🥩' },
  { value: 'seafood', label: '海鲜', emoji: '🐟' },
  { value: 'diary', label: '乳制品', emoji: '🥛' },
  { value: 'beverage', label: '饮料', emoji: '🥤' },
  { value: 'egg', label: '蛋豆类', emoji: '🥚' },
  { value: 'bread', label: '面包', emoji: '🍞' },
  { value: 'frozen', label: '冷冻食品', emoji: '🍦' },
  { value: 'sauce', label: '酱料', emoji: '🍯' },
  { value: 'snack', label: '零食', emoji: '🍿' },
  { value: 'other', label: '其他', emoji: '📦' }
]

const formData = reactive({
  name: '',
  expire_date: '' as string,
  place: 'cold' as 'cold' | 'frozer' | 'room',
  num: 1,
  type: 'other'
})

const handleCancel = () => {
  emit('cancel')
}

const handleSubmit = async () => {
  if (loading.value) return

  loading.value = true
  try {
    const response = await updateItem(props.item._id, {
      name: formData.name,
      quantity: formData.num,
      expire_date: formData.expire_date,
      place: formData.place,
      type: formData.type
    })

    if (response.success) {
      ElMessage.success('更新成功')
      emit('success')
    } else {
      ElMessage.error(response.error || '更新失败')
    }
  } catch (error: any) {
    console.error('更新物品失败:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 填充表单数据
  formData.name = props.item.name
  const expireDate = props.item.expire_date || new Date().toISOString()
  formData.expire_date = (expireDate.includes('T') ? expireDate.split('T')[0] : expireDate) as string
  formData.place = props.item.place === 'frozen' ? 'frozer' : props.item.place as any
  formData.num = props.item.num
  formData.type = props.item.type
})
</script>

<style scoped>
.item-edit-form {
  padding: 0;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.form-group label i {
  margin-right: 6px;
  color: var(--primary-color);
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 15px;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.radio-group {
  display: flex;
  gap: 12px;
}

.radio-item {
  flex: 1;
  cursor: pointer;
}

.radio-item input[type='radio'] {
  display: none;
}

.radio-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 12px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
  transition: all 0.2s;
}

.radio-item input[type='radio']:checked + .radio-label {
  border-color: var(--primary-color);
  background: var(--primary-light);
  color: var(--primary-color);
}

.radio-label i {
  font-size: 24px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:hover {
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.category-item.selected {
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.category-emoji {
  font-size: 28px;
}

.category-name {
  font-size: 12px;
  color: var(--text-primary);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  height: 44px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: var(--bg-tertiary);
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary i {
  margin-right: 6px;
}
</style>
