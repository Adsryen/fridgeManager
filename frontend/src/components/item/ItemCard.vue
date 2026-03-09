<template>
  <div class="item-card" :class="statusClass">
    <div class="item-icon">
      <i :class="typeIcon"></i>
    </div>
    <div class="item-info">
      <div class="item-name">{{ item.name }}</div>
      <div class="item-details">
        <span class="item-quantity">
          <i class="fas fa-box"></i>
          {{ item.num }}{{ item.unit || '个' }}
        </span>
        <span class="item-place">
          <i :class="placeIcon"></i>
          {{ placeText }}
        </span>
      </div>
      <div class="item-expire">
        <i class="fas fa-calendar-alt"></i>
        <span>{{ expireText }}</span>
        <span v-if="status !== 'normal'" class="expire-badge" :class="status">
          {{ statusText }}
        </span>
      </div>
    </div>
    <div class="item-actions">
      <button class="action-btn edit" @click="handleEdit">
        <i class="fas fa-edit"></i>
      </button>
      <button class="action-btn delete" @click="handleDelete">
        <i class="fas fa-trash-alt"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Item } from '@/types/models'

interface Props {
  item: Item
  status?: 'expired' | 'expiring' | 'normal'
}

const props = withDefaults(defineProps<Props>(), {
  status: 'normal'
})

const emit = defineEmits<{
  edit: [item: Item]
  delete: [item: Item]
}>()

// 计算属性

// 状态样式类
const statusClass = computed(() => {
  return `status-${props.status}`
})

// 状态文本
const statusText = computed(() => {
  switch (props.status) {
    case 'expired':
      return '已过期'
    case 'expiring':
      return '即将过期'
    default:
      return ''
  }
})

// 类型图标
const typeIcon = computed(() => {
  const typeIcons: Record<string, string> = {
    '蔬菜': 'fas fa-carrot',
    '水果': 'fas fa-apple-alt',
    '肉类': 'fas fa-drumstick-bite',
    '饮料': 'fas fa-glass-whiskey',
    '调味品': 'fas fa-pepper-hot',
    '面包糕点': 'fas fa-bread-slice',
    '乳制品': 'fas fa-cheese',
    '海鲜': 'fas fa-fish',
    '速食': 'fas fa-pizza-slice',
    '其他': 'fas fa-box'
  }
  return typeIcons[props.item.type] || 'fas fa-box'
})

// 存放位置图标
const placeIcon = computed(() => {
  const placeIcons: Record<string, string> = {
    'cold': 'fas fa-snowflake',
    'frozen': 'fas fa-icicles',
    'normal': 'fas fa-temperature-high'
  }
  return placeIcons[props.item.place] || 'fas fa-box'
})

// 存放位置文本
const placeText = computed(() => {
  const placeTexts: Record<string, string> = {
    'cold': '冷藏',
    'frozen': '冷冻',
    'normal': '常温'
  }
  return placeTexts[props.item.place] || '未知'
})

// 过期日期文本
const expireText = computed(() => {
  const expireDate = new Date(props.item.expire_date)
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  expireDate.setHours(0, 0, 0, 0)
  
  const diffTime = expireDate.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return `已过期 ${Math.abs(diffDays)} 天`
  } else if (diffDays === 0) {
    return '今天过期'
  } else if (diffDays === 1) {
    return '明天过期'
  } else if (diffDays <= 3) {
    return `${diffDays} 天后过期`
  } else {
    return expireDate.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  }
})

// 事件处理
const handleEdit = () => {
  emit('edit', props.item)
}

const handleDelete = () => {
  emit('delete', props.item)
}
</script>

<style scoped>
.item-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 2px solid var(--border-color);
  transition: all 0.3s;
}

.item-card:active {
  transform: scale(0.98);
}

.item-card.status-expired {
  border-color: var(--danger-color);
  background: rgba(239, 68, 68, 0.05);
}

.item-card.status-expiring {
  border-color: var(--warning-color);
  background: rgba(245, 158, 11, 0.05);
}

/* 物品图标 */
.item-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  flex-shrink: 0;
}

.status-expired .item-icon {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.status-expiring .item-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

/* 物品信息 */
.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-details {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.item-details span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.item-details i {
  font-size: 12px;
}

.item-expire {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.item-expire i {
  font-size: 12px;
}

.expire-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 4px;
}

.expire-badge.expired {
  background: var(--danger-color);
  color: white;
}

.expire-badge.expiring {
  background: var(--warning-color);
  color: white;
}

/* 操作按钮 */
.item-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.edit {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.action-btn.edit:active {
  background: rgba(59, 130, 246, 0.2);
  transform: scale(0.95);
}

.action-btn.delete {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.action-btn.delete:active {
  background: rgba(239, 68, 68, 0.2);
  transform: scale(0.95);
}
</style>
