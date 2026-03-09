<template>
  <div class="take-out-dialog">
    <div class="take-out-info">
      <h4>{{ itemName }}</h4>
      <p>当前数量：{{ currentNum }}</p>
    </div>
    <div class="form-group">
      <label><i class="fas fa-boxes"></i> 取出数量</label>
      <div class="quantity-selector">
        <button type="button" class="qty-btn minus" @click="adjustQuantity(-1)">
          <i class="fas fa-minus"></i>
        </button>
        <input
          v-model.number="quantity"
          type="number"
          class="qty-input"
          :min="1"
          :max="currentNum"
          @input="validateQuantity"
        />
        <button type="button" class="qty-btn plus" @click="adjustQuantity(1)">
          <i class="fas fa-plus"></i>
        </button>
      </div>
      <div class="qty-shortcuts">
        <button type="button" class="qty-shortcut-btn" @click="setQuantity(1)">1个</button>
        <button
          v-if="currentNum >= 2"
          type="button"
          class="qty-shortcut-btn"
          @click="setQuantity(Math.floor(currentNum / 2))"
        >
          半数
        </button>
        <button type="button" class="qty-shortcut-btn" @click="setQuantity(currentNum)">
          全部
        </button>
      </div>
    </div>
    <div class="form-actions">
      <button type="button" class="btn-secondary" @click="handleCancel">取消</button>
      <button type="button" class="btn-primary" @click="handleConfirm">
        <i class="fas fa-check"></i> 确认取出
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Props {
  itemId: string
  itemName: string
  currentNum: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  confirm: [quantity: number]
  cancel: []
}>()

const quantity = ref(1)

const adjustQuantity = (delta: number) => {
  const newVal = quantity.value + delta
  if (newVal >= 1 && newVal <= props.currentNum) {
    quantity.value = newVal
  }
}

const setQuantity = (val: number) => {
  quantity.value = val
}

const validateQuantity = () => {
  if (quantity.value < 1) {
    quantity.value = 1
  } else if (quantity.value > props.currentNum) {
    quantity.value = props.currentNum
  }
}

const handleCancel = () => {
  emit('cancel')
}

const handleConfirm = async () => {
  if (!quantity.value || quantity.value < 1) {
    ElMessage.error('请输入有效的数量')
    return
  }

  if (quantity.value > props.currentNum) {
    ElMessage.error('取出数量不能超过当前数量')
    return
  }

  const remainingQty = props.currentNum - quantity.value

  if (remainingQty === 0) {
    try {
      await ElMessageBox.confirm(
        '取出后数量为0，是否删除该物品卡片？\n\n点击"确定"删除卡片\n点击"取消"保留卡片（数量为0）',
        '提示',
        {
          confirmButtonText: '删除卡片',
          cancelButtonText: '保留卡片',
          type: 'warning'
        }
      )
      // 用户选择删除
      emit('confirm', quantity.value)
    } catch {
      // 用户选择保留（数量为0）
      emit('confirm', quantity.value)
    }
  } else {
    emit('confirm', quantity.value)
  }
}
</script>

<style scoped>
.take-out-dialog {
  padding: 0;
}

.take-out-info {
  margin-bottom: 24px;
  text-align: center;
}

.take-out-info h4 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.take-out-info p {
  font-size: 14px;
  color: var(--text-secondary);
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

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.qty-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.qty-btn:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.qty-btn:active {
  transform: scale(0.95);
}

.qty-input {
  flex: 1;
  height: 40px;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.qty-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.qty-shortcuts {
  display: flex;
  gap: 8px;
}

.qty-shortcut-btn {
  flex: 1;
  height: 36px;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  border-radius: 6px;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.qty-shortcut-btn:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
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

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-primary i {
  margin-right: 6px;
}
</style>
