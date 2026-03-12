 ，<template>
  <div class="home-page">
    <!-- 顶部导航栏 -->
    <div class="mobile-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <img src="/images/ice-box.png" alt="冰箱图标" />
          </div>
          <div class="app-name">冰箱里面还有啥</div>
        </div>
        <div class="header-right">
          <button class="icon-btn" @click="toggleDarkMode" title="切换深色模式">
            <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="mobile-content">
      <!-- 统计卡片 -->
      <div class="stats-container">
        <div class="stat-card" @click="filterByStatus('all')">
          <div class="stat-icon total">
            <i class="fas fa-box"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ itemStore.itemCount }}</div>
            <div class="stat-label">全部</div>
          </div>
        </div>
        <div class="stat-card" @click="filterByStatus('expiring')">
          <div class="stat-icon warning">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ itemStore.expiringItems.length }}</div>
            <div class="stat-label">即将过期</div>
          </div>
        </div>
        <div class="stat-card" @click="filterByStatus('expired')">
          <div class="stat-icon danger">
            <i class="fas fa-times-circle"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ itemStore.expiredItems.length }}</div>
            <div class="stat-label">已过期</div>
          </div>
        </div>
      </div>

      <!-- 冰箱选择器 -->
      <div class="fridge-selector-container">
        <div class="fridge-selector-scroll">
          <!-- 公共冰箱 -->
          <button
            class="fridge-tab"
            :class="{ active: fridgeStore.currentFridgeId === 'public' }"
            @click="switchFridge('public')"
            style="z-index: 1000; position: relative;"
          >
            <i class="fas fa-users"></i>
            <span>公共冰箱</span>
            <span v-if="getPublicItemCount() > 0" class="fridge-badge" style="z-index: 1001;">{{ getPublicItemCount() }}</span>
          </button>
          <!-- 我的冰箱 -->
          <button
            v-for="fridge in fridgeStore.myFridges"
            :key="fridge._id"
            class="fridge-tab"
            :class="{ active: fridgeStore.currentFridgeId === fridge._id }"
            @click="switchFridge(fridge._id)"
            style="z-index: 1000; position: relative;"
          >
            <i class="fas fa-snowflake"></i>
            <span>{{ fridge.name }}</span>
            <span v-if="fridge.item_count > 0" class="fridge-badge" style="z-index: 1001;">{{ fridge.item_count }}</span>
          </button>
          <!-- 家庭共享冰箱 -->
          <button
            v-for="fridge in fridgeStore.sharedFridges"
            :key="fridge._id"
            class="fridge-tab shared-fridge"
            :class="{ active: fridgeStore.currentFridgeId === fridge._id }"
            @click="switchFridge(fridge._id)"
            style="z-index: 1000; position: relative;"
          >
            <i class="fas fa-share-alt"></i>
            <div class="fridge-info">
              <span class="fridge-name">{{ fridge.name }}（{{ fridge.owner_username }}）</span>
            </div>
            <span v-if="fridge.item_count > 0" class="fridge-badge" style="z-index: 1001;">{{ fridge.item_count }}</span>
          </button>
          <button class="fridge-tab add-fridge" @click="$router.push('/fridge')" style="z-index: 1000; position: relative;">
            <i class="fas fa-plus"></i>
            <span>管理冰箱</span>
          </button>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="mobile-search">
        <div class="search-input-wrapper">
          <i class="fas fa-search"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索物品..."
            @input="handleSearch"
          />
          <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>

      <!-- 主体内容：左侧边栏 + 右侧列表 -->
      <div class="content-with-sidebar">
        <!-- 左侧边栏 -->
        <div class="sidebar">
          <button
            class="sidebar-item"
            :class="{ active: currentView === 'all' }"
            @click="currentView = 'all'"
          >
            <i class="fas fa-th-large"></i>
            <span>全部</span>
          </button>
          <button
            class="sidebar-item"
            :class="{ active: currentView === 'cold' }"
            @click="currentView = 'cold'"
          >
            <i class="fas fa-temperature-low"></i>
            <span>冷藏</span>
            <span v-if="getCategoryCount('cold')" class="sidebar-badge">
              {{ getCategoryCount('cold') }}
            </span>
          </button>
          <button
            class="sidebar-item"
            :class="{ active: currentView === 'frozen' }"
            @click="currentView = 'frozen'"
          >
            <i class="fas fa-snowflake"></i>
            <span>冷冻</span>
            <span v-if="getCategoryCount('frozen')" class="sidebar-badge">
              {{ getCategoryCount('frozen') }}
            </span>
          </button>
          <button
            class="sidebar-item"
            :class="{ active: currentView === 'room' }"
            @click="currentView = 'room'"
          >
            <i class="fas fa-home"></i>
            <span>室温</span>
            <span v-if="getCategoryCount('room')" class="sidebar-badge">
              {{ getCategoryCount('room') }}
            </span>
          </button>
        </div>

        <!-- 右侧物品列表 -->
        <div class="main-list-area">
          <div v-if="itemStore.loading" class="loading-state">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>
          <div v-else-if="filteredItems.length === 0" class="empty-state">
            <i class="fas fa-inbox"></i>
            <h4>暂无物品</h4>
            <p>点击下方 + 按钮添加物品</p>
          </div>
          <div v-else class="mobile-items-container">
            <div
              v-for="item in filteredItems"
              :key="item._id"
              class="mobile-item-card"
              :class="{
                expired: isExpired(item),
                'expiring-soon': isExpiringSoon(item)
              }"
            >
              <div class="item-card-main">
                <div class="item-card-header">
                  <div class="item-emoji">{{ getItemEmoji(item.type) }}</div>
                  <div class="item-name-info">
                    <h3>{{ item.name }}</h3>
                  </div>
                </div>
                <div class="item-card-body">
                  <div class="item-info-row-group">
                    <span class="item-info-inline">
                      <i class="fas fa-map-marker-alt"></i>
                      {{ getPlaceLabel(item.place) }}
                    </span>
                    <span class="item-info-inline">
                      <i class="fas fa-calendar-alt"></i>
                      {{ formatDate(item.expire_date) }}
                    </span>
                    <span class="item-info-inline">
                      <i class="fas fa-boxes"></i>
                      ×{{ item.num }}
                    </span>
                  </div>
                  <div class="item-bottom-row">
                    <div
                      class="item-expiry-status"
                      :class="{
                        fresh: !isExpired(item) && !isExpiringSoon(item),
                        warning: isExpiringSoon(item),
                        danger: isExpired(item)
                      }"
                    >
                      <span>{{ getExpiryText(item) }}</span>
                    </div>
                    <button class="item-action-btn take-out" @click="takeOutItem(item)" title="取出">
                      <i class="fas fa-hand-holding"></i>
                    </button>
                    <button class="item-action-btn edit" @click="editItem(item)" title="编辑">
                      <i class="fas fa-edit"></i>
                    </button>
                  </div>
                </div>
              </div>
              <div class="item-card-actions">
                <button class="item-action-btn delete" @click="deleteItem(item)" title="删除">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部分类标签 -->
    <div class="category-tags-container">
      <div class="category-tags-scroll">
        <button
          v-for="cat in categories"
          :key="cat.value"
          class="category-tag"
          :class="{ active: selectedCategory === cat.value }"
          @click="selectedCategory = cat.value"
        >
          <span class="category-tag-icon">{{ cat.emoji }}</span>
          <span class="category-tag-name">{{ cat.label }}</span>
          <span v-if="getCategoryCount(cat.value)" class="category-tag-count">
            {{ getCategoryCount(cat.value) }}
          </span>
        </button>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <div class="mobile-bottom-nav">
      <button class="nav-item" :class="{ active: $route.path === '/' }" @click="$router.push('/')">
        <i class="fas fa-home"></i>
        <span>首页</span>
      </button>
      <button class="nav-item" :class="{ active: $route.path === '/fridge' }" @click="$router.push('/fridge')">
        <i class="fas fa-snowflake"></i>
        <span>冰箱</span>
      </button>
      <button class="nav-item add-btn" @click="handleAddClick">
        <div class="add-icon">
          <i class="fas fa-plus"></i>
        </div>
      </button>
      <button class="nav-item" :class="{ active: $route.path === '/family' }" @click="$router.push('/family')">
        <i class="fas fa-users"></i>
        <span>家庭</span>
      </button>
      <button class="nav-item" :class="{ active: $route.path === '/profile' }" @click="$router.push('/profile')">
        <i class="fas fa-user"></i>
        <span>我的</span>
        <span v-if="!userStore.isLoggedIn" class="nav-badge guest">游客</span>
        <span v-else-if="userStore.isAdmin" class="nav-badge admin">管理员</span>
        <span v-else class="nav-badge user">私人</span>
      </button>
    </div>

    <!-- 取出物品对话框 -->
    <Drawer v-model="showTakeOutDialog" title="取出物品">
      <TakeOutDialog
        v-if="currentItem"
        :item-id="currentItem._id"
        :item-name="currentItem.name"
        :current-num="currentItem.num"
        @confirm="handleTakeOutConfirm"
        @cancel="showTakeOutDialog = false"
      />
    </Drawer>

    <!-- 编辑物品表单 -->
    <Drawer v-model="showEditForm" title="编辑物品">
      <ItemEditForm
        v-if="currentItem"
        :item="currentItem"
        @success="handleEditSuccess"
        @cancel="showEditForm = false"
      />
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, inject } from 'vue'
import { useItemStore } from '../stores/item'
import { useFridgeStore } from '../stores/fridge'
import { useUserStore } from '../stores/user'
import { useTheme } from '../composables/useTheme'
import Drawer from '../components/common/Drawer.vue'
import TakeOutDialog from '../components/item/TakeOutDialog.vue'
import ItemEditForm from '../components/item/ItemEditForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Item } from '../types/models'
import { updateItem as updateItemApi, deleteItem as deleteItemApi } from '../api/item'

const itemStore = useItemStore()
const fridgeStore = useFridgeStore()
const userStore = useUserStore()
const { isDark, toggleTheme } = useTheme()

// 注入全局添加方法
const openGlobalAddMenu = inject('openGlobalAddMenu') as () => void

const searchQuery = ref('')
const currentView = ref('all')
const selectedCategory = ref('all')
const showTakeOutDialog = ref(false)
const showEditForm = ref(false)
const currentItem = ref<Item | null>(null)

const categories = [
  { value: 'all', label: '全部', emoji: '📦' },
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

const filteredItems = computed(() => {
  let items = itemStore.items

  // 按存储位置过滤
  if (currentView.value !== 'all') {
    const viewPlace = currentView.value === 'frozen' ? 'frozer' : currentView.value
    items = items.filter(item => {
      const itemPlace = item.place === 'frozen' ? 'frozer' : item.place
      return itemPlace === viewPlace
    })
  }

  // 按分类过滤
  if (selectedCategory.value !== 'all') {
    items = items.filter(item => item.type === selectedCategory.value)
  }

  // 按搜索关键词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item => item.name.toLowerCase().includes(query))
  }

  return items
})

const toggleDarkMode = async () => {
  await toggleTheme()
}

const switchFridge = async (fridgeId: string) => {
  await fridgeStore.switchFridge(fridgeId)
  await itemStore.loadItems()
}

const filterByStatus = (status: string) => {
  // 可以添加状态过滤逻辑
  console.log('Filter by status:', status)
}

const handleSearch = () => {
  // 搜索已通过 computed 实现
}

const clearSearch = () => {
  searchQuery.value = ''
}

const getCategoryCount = (category: string) => {
  if (category === 'all') return itemStore.items.length
  
  return itemStore.items.filter(item => {
    // 如果是存储位置过滤
    if (category === 'cold' || category === 'frozen' || category === 'frozer' || category === 'room' || category === 'normal') {
      const itemPlace = item.place === 'frozen' ? 'frozer' : item.place
      const catPlace = category === 'frozen' ? 'frozer' : category
      return itemPlace === catPlace
    }
    // 如果是类型过滤
    return item.type === category
  }).length
}

const getPlaceLabel = (place: string) => {
  const labels: Record<string, string> = {
    cold: '冷藏室',
    frozen: '冷冻室',
    frozer: '冷冻室',
    room: '室温区',
    normal: '室温区'
  }
  return labels[place] || place
}

const getPublicItemCount = () => {
  // 使用冰箱store的方法获取公共冰箱的物品数量
  return fridgeStore.getFridgeItemCount('public')
}

const getItemEmoji = (type: string) => {
  const emojiMap: Record<string, string> = {
    vegetable: '🥬',
    vegetables: '�',
    fruit: '🍎',
    fruits: '🍎',
    meat: '🥩',
    seafood: '🐟',
    diary: '🥛',
    dairy: '🥛',
    beverage: '🥤',
    drinks: '🥤',
    egg: '🥚',
    bread: '🍞',
    frozen: '🍦',
    sauce: '🍯',
    snack: '🍿',
    other: '📦'
  }
  return emojiMap[type] || '📦'
}

const isExpired = (item: any) => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const expireDate = new Date(item.expire_date)
  expireDate.setHours(0, 0, 0, 0)
  return expireDate < now
}

const isExpiringSoon = (item: any) => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const threeDaysLater = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
  const expireDate = new Date(item.expire_date)
  expireDate.setHours(0, 0, 0, 0)
  return expireDate >= now && expireDate <= threeDaysLater
}

const getExpiryText = (item: any) => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const expireDate = new Date(item.expire_date)
  expireDate.setHours(0, 0, 0, 0)
  const daysUntilExpiry = Math.floor((expireDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  if (daysUntilExpiry < 0) {
    return `已过期 ${Math.abs(daysUntilExpiry)} 天`
  } else if (daysUntilExpiry === 0) {
    return '今天过期'
  } else if (daysUntilExpiry <= 3) {
    return `还剩 ${daysUntilExpiry} 天`
  } else {
    return `还剩 ${daysUntilExpiry} 天`
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${month}-${day}`
}

const takeOutItem = (item: Item) => {
  currentItem.value = item
  showTakeOutDialog.value = true
}

const handleTakeOutConfirm = async (quantity: number) => {
  if (!currentItem.value) return

  const item = currentItem.value
  const remainingQty = item.num - quantity

  try {
    if (remainingQty === 0) {
      // 删除物品
      await deleteItemApi(item._id)
      ElMessage.success(`已取出 ${quantity} 个并移除`)
    } else {
      // 更新数量
      await updateItemApi(item._id, { quantity: remainingQty })
      if (remainingQty === 0) {
        ElMessage.success(`已取出 ${quantity} 个，卡片已保留`)
      } else {
        ElMessage.success(`已取出 ${quantity} 个，剩余 ${remainingQty} 个`)
      }
    }
    await itemStore.loadItems()
  } catch (error: any) {
    console.error('取出物品失败:', error)
    ElMessage.error(error.message || '操作失败')
  } finally {
    showTakeOutDialog.value = false
    currentItem.value = null
  }
}

const editItem = (item: Item) => {
  currentItem.value = item
  showEditForm.value = true
}

const handleEditSuccess = () => {
  showEditForm.value = false
  currentItem.value = null
  itemStore.loadItems()
}

const deleteItem = async (item: Item) => {
  try {
    await ElMessageBox.confirm(`确定要删除"${item.name}"吗？`, '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await itemStore.deleteItem(item._id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const handleAddClick = () => {
  // 调用全局添加方法
  openGlobalAddMenu()
}

onMounted(async () => {
  console.log('[首页] 组件挂载，开始加载数据')
  try {
    await Promise.all([
      fridgeStore.loadFridges(),
      itemStore.loadItems()
    ])
    console.log('[首页] 数据加载完成')
  } catch (error) {
    console.error('[首页] 加载数据失败', error)
  }
})
</script>

<style scoped>
.home-page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
