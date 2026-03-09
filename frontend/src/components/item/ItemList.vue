<template>
  <div class="item-list-container">
    <!-- 搜索和过滤 -->
    <ItemFilter />

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="skeleton-list">
        <div v-for="i in 3" :key="i" class="skeleton-item">
          <div class="skeleton-avatar"></div>
          <div class="skeleton-content">
            <div class="skeleton-title"></div>
            <div class="skeleton-text"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 物品列表 -->
    <div v-else-if="filteredItems.length > 0" class="item-list">
      <!-- 过期物品 -->
      <div v-if="expiredItems.length > 0" class="item-section">
        <div class="section-header expired">
          <i class="fas fa-exclamation-circle"></i>
          <span>已过期 ({{ expiredItems.length }})</span>
        </div>
        <div class="section-content">
          <ItemCard
            v-for="item in expiredItems"
            :key="item._id"
            :item="item"
            status="expired"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>

      <!-- 即将过期物品 -->
      <div v-if="expiringItems.length > 0" class="item-section">
        <div class="section-header expiring">
          <i class="fas fa-clock"></i>
          <span>即将过期 ({{ expiringItems.length }})</span>
        </div>
        <div class="section-content">
          <ItemCard
            v-for="item in expiringItems"
            :key="item._id"
            :item="item"
            status="expiring"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>

      <!-- 正常物品 -->
      <div v-if="normalItems.length > 0" class="item-section">
        <div class="section-header normal">
          <i class="fas fa-check-circle"></i>
          <span>正常 ({{ normalItems.length }})</span>
        </div>
        <div class="section-content">
          <ItemCard
            v-for="item in normalItems"
            :key="item._id"
            :item="item"
            status="normal"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-inbox"></i>
      </div>
      <div class="empty-text">
        <p class="empty-title">暂无物品</p>
        <p class="empty-desc">点击下方"添加"按钮添加物品</p>
      </div>
    </div>

    <!-- 编辑物品抽屉 -->
    <div class="drawer-overlay" :class="{ active: editDrawerVisible }" @click="editDrawerVisible = false">
      <div class="drawer-content full-height" @click.stop>
        <div class="drawer-header">
          <h5>编辑物品</h5>
          <button class="close-btn" @click="editDrawerVisible = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="drawer-body">
          <ItemForm
            v-if="editingItem"
            :item="editingItem"
            mode="edit"
            @success="handleEditSuccess"
            @cancel="editDrawerVisible = false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useItemStore } from '@/stores/item'
import type { Item } from '@/types/models'
import ItemCard from './ItemCard.vue'
import ItemFilter from './ItemFilter.vue'
import ItemForm from './ItemForm.vue'

const itemStore = useItemStore()

// 状态
const editDrawerVisible = ref(false)
const editingItem = ref<Item | null>(null)

// 计算属性
const loading = computed(() => itemStore.loading)
const filteredItems = computed(() => itemStore.filteredItems)
const expiredItems = computed(() => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  return filteredItems.value.filter(item => {
    const expireDate = new Date(item.expire_date)
    expireDate.setHours(0, 0, 0, 0)
    return expireDate < now
  })
})
const expiringItems = computed(() => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const threeDaysLater = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
  return filteredItems.value.filter(item => {
    const expireDate = new Date(item.expire_date)
    expireDate.setHours(0, 0, 0, 0)
    return expireDate >= now && expireDate <= threeDaysLater
  })
})
const normalItems = computed(() => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const threeDaysLater = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
  return filteredItems.value.filter(item => {
    const expireDate = new Date(item.expire_date)
    expireDate.setHours(0, 0, 0, 0)
    return expireDate > threeDaysLater
  })
})

// 处理编辑
const handleEdit = (item: Item) => {
  editingItem.value = item
  editDrawerVisible.value = true
}

// 处理删除
const handleDelete = async (item: Item) => {
  try {
    await ElMessageBox.confirm(`确定要删除"${item.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await itemStore.deleteItem(item._id)
    if (response.success) {
      ElMessage.success('删除成功')
    } else {
      ElMessage.error(response.error || '删除失败')
    }
  } catch {
    // 用户取消
  }
}

// 处理编辑成功
const handleEditSuccess = () => {
  editDrawerVisible.value = false
  editingItem.value = null
  ElMessage.success('更新成功')
  itemStore.loadItems()
}
</script>

<style scoped>
.item-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 加载状态 */
.loading-container {
  padding: 20px;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: var(--border-color);
}

.skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-title {
  width: 60%;
  height: 16px;
  border-radius: 4px;
  background: var(--border-color);
}

.skeleton-text {
  width: 40%;
  height: 14px;
  border-radius: 4px;
  background: var(--border-color);
}

/* 物品列表 */
.item-list {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px;
}

.item-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.section-header.expired {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.section-header.expiring {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-color);
}

.section-header.normal {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.empty-icon i {
  font-size: 40px;
  color: var(--text-secondary);
}

.empty-text {
  text-align: center;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
