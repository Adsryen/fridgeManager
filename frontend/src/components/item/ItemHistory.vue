<template>
  <div class="item-history">
    <div class="history-header">
      <div class="header-tabs">
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'history' }"
          @click="activeTab = 'history'"
        >
          <i class="fas fa-history"></i>
          <span>操作历史</span>
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'deleted' }"
          @click="activeTab = 'deleted'"
        >
          <i class="fas fa-trash-restore"></i>
          <span>已删除</span>
        </button>
      </div>
    </div>

    <!-- 操作历史 -->
    <div v-if="activeTab === 'history'" class="history-content">
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <span>加载中...</span>
      </div>
      
      <div v-else-if="histories.length === 0" class="empty-state">
        <i class="fas fa-history"></i>
        <h4>暂无历史记录</h4>
        <p>该冰箱还没有任何操作记录</p>
      </div>
      
      <div v-else class="history-list">
        <div 
          v-for="history in histories" 
          :key="history._id"
          class="history-item"
        >
          <div class="history-icon">
            <i :class="getActionIcon(history.action)"></i>
          </div>
          <div class="history-content">
            <div class="history-main">
              <span class="action-text">{{ getActionText(history.action) }}</span>
              <span class="item-name">{{ history.item_data.Name || history.item_data.name }}</span>
              <span v-if="history.quantity_change" class="quantity-change">
                ({{ history.quantity_change > 0 ? '+' : '' }}{{ history.quantity_change }})
              </span>
            </div>
            <div class="history-meta">
              <span class="username">{{ history.username }}</span>
              <span class="time">{{ formatTime(history.created_at) }}</span>
            </div>
            <div v-if="history.reason" class="history-reason">
              {{ history.reason }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 已删除物品 -->
    <div v-if="activeTab === 'deleted'" class="deleted-content">
      <div v-if="loadingDeleted" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i>
        <span>加载中...</span>
      </div>
      
      <div v-else-if="deletedItems.length === 0" class="empty-state">
        <i class="fas fa-trash"></i>
        <h4>暂无已删除物品</h4>
        <p>该冰箱没有已删除的物品</p>
      </div>
      
      <div v-else class="deleted-list">
        <div 
          v-for="item in deletedItems" 
          :key="item._id"
          class="deleted-item"
        >
          <div class="item-info">
            <div class="item-main">
              <span class="item-name">{{ item.item_data.Name || item.item_data.name }}</span>
              <span class="item-quantity">{{ item.item_data.Num || item.item_data.num }}个</span>
            </div>
            <div class="item-meta">
              <span class="deleted-by">由 {{ item.username }} 删除</span>
              <span class="deleted-time">{{ formatTime(item.created_at) }}</span>
            </div>
          </div>
          <button 
            class="restore-btn"
            @click="handleRestore(item)"
            :disabled="restoring"
          >
            <i class="fas fa-undo"></i>
            <span>恢复</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as itemHistoryApi from '@/api/itemHistory'

interface Props {
  fridgeId: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  restored: []
}>()

const activeTab = ref<'history' | 'deleted'>('history')
const histories = ref<any[]>([])
const deletedItems = ref<any[]>([])
const loading = ref(false)
const loadingDeleted = ref(false)
const restoring = ref(false)

// 加载历史记录
const loadHistory = async () => {
  loading.value = true
  try {
    const response = await itemHistoryApi.getFridgeHistory(props.fridgeId, 50)
    if (response.success) {
      histories.value = response.data || []
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载历史记录失败')
  } finally {
    loading.value = false
  }
}

// 加载已删除物品
const loadDeletedItems = async () => {
  loadingDeleted.value = true
  try {
    const response = await itemHistoryApi.getDeletedItems(props.fridgeId, 20)
    if (response.success) {
      deletedItems.value = response.data || []
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载已删除物品失败')
  } finally {
    loadingDeleted.value = false
  }
}

// 恢复物品
const handleRestore = async (item: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要恢复物品"${item.item_data.Name || item.item_data.name}"吗？`,
      '确认恢复',
      {
        confirmButtonText: '恢复',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    restoring.value = true
    const response = await itemHistoryApi.restoreItem(item._id)
    if (response.success) {
      ElMessage.success('物品恢复成功')
      // 重新加载数据
      await loadDeletedItems()
      await loadHistory()
      emit('restored')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '恢复失败')
    }
  } finally {
    restoring.value = false
  }
}

// 获取操作图标
const getActionIcon = (action: string) => {
  const icons: Record<string, string> = {
    created: 'fas fa-plus text-success',
    updated: 'fas fa-edit text-primary',
    deleted: 'fas fa-trash text-danger',
    taken_out: 'fas fa-arrow-up text-warning',
    restored: 'fas fa-undo text-info'
  }
  return icons[action] || 'fas fa-circle'
}

// 获取操作文本
const getActionText = (action: string) => {
  const texts: Record<string, string> = {
    created: '添加了',
    updated: '更新了',
    deleted: '删除了',
    taken_out: '取出了',
    restored: '恢复了'
  }
  return texts[action] || '操作了'
}

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 小于1分钟
  if (diff < 60000) {
    return '刚刚'
  }
  
  // 小于1小时
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  }
  
  // 小于1天
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  }
  
  // 小于7天
  if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  }
  
  // 超过7天显示具体日期
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 监听标签切换
watch(activeTab, (newTab) => {
  if (newTab === 'history' && histories.value.length === 0) {
    loadHistory()
  } else if (newTab === 'deleted' && deletedItems.value.length === 0) {
    loadDeletedItems()
  }
})

onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.item-history {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.history-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}

.header-tabs {
  display: flex;
  gap: 8px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  color: var(--text-secondary);
}

.tab-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.history-content,
.deleted-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

.history-list,
.deleted-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.history-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.history-content {
  flex: 1;
  min-width: 0;
}

.history-main {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.action-text {
  font-size: 14px;
  color: var(--text-secondary);
}

.item-name {
  font-weight: 600;
  color: var(--text-primary);
}

.quantity-change {
  font-size: 12px;
  color: var(--text-secondary);
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.history-reason {
  margin-top: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  font-style: italic;
}

.deleted-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-main {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.item-name {
  font-weight: 600;
  color: var(--text-primary);
}

.item-quantity {
  font-size: 12px;
  color: var(--text-secondary);
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.restore-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--success-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 12px;
}

.restore-btn:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.restore-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.text-success { color: var(--success-color); }
.text-primary { color: var(--primary-color); }
.text-danger { color: var(--danger-color); }
.text-warning { color: var(--warning-color); }
.text-info { color: var(--info-color); }
</style>