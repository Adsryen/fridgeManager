<template>
  <div class="home-page">
    <!-- 顶部导航栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <img src="/images/ice-box.png" alt="冰箱图标">
          </div>
          <div class="app-name">{{ currentFridge?.name || '冰箱管理' }}</div>
        </div>
        <div class="header-right">
          <button class="icon-btn" @click="handleToggleTheme" :class="{ rotating: isRotating }">
            <i :class="currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="mobile-content">
      <!-- 统计卡片 -->
      <div class="stats-container">
        <div class="stat-card" @click="showAllItems">
          <div class="stat-icon total">
            <i class="fas fa-box"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ itemStore.items.length }}</div>
            <div class="stat-label">全部</div>
          </div>
        </div>
        <div class="stat-card" @click="showExpiringSoon">
          <div class="stat-icon warning">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ itemStore.expiringItems.length }}</div>
            <div class="stat-label">即将过期</div>
          </div>
        </div>
        <div class="stat-card" @click="showExpired">
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
          <div 
            v-for="fridge in fridgeStore.myFridges" 
            :key="fridge._id"
            class="fridge-tab"
            :class="{ active: fridgeStore.currentFridgeId === fridge._id }"
            @click="switchFridge(fridge._id)"
          >
            <i class="fas fa-home"></i>
            <span>{{ fridge.name }}</span>
          </div>
          <div 
            v-for="fridge in fridgeStore.sharedFridges" 
            :key="fridge._id"
            class="fridge-tab"
            :class="{ active: fridgeStore.currentFridgeId === fridge._id }"
            @click="switchFridge(fridge._id)"
          >
            <i class="fas fa-users"></i>
            <span>{{ fridge.name }}</span>
          </div>
          <div class="fridge-tab add-fridge" @click="showFridgeSelector">
            <i class="fas fa-plus-circle"></i>
            <span>添加冰箱</span>
          </div>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="mobile-search">
        <div class="search-input-wrapper">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            v-model="itemStore.searchKeyword"
            placeholder="搜索物品..."
          >
          <button 
            v-if="itemStore.searchKeyword" 
            class="clear-btn" 
            @click="itemStore.searchKeyword = ''"
          >
            <i class="fas fa-times-circle"></i>
          </button>
        </div>
      </div>

      <!-- 主体内容区域：左侧边栏 + 右侧列表 -->
      <div class="content-with-sidebar">
        <!-- 左侧边栏 -->
        <div class="sidebar">
          <button 
            class="sidebar-item" 
            :class="{ active: currentPlace === 'all' }"
            @click="filterByPlace('all')"
          >
            <i class="fas fa-th"></i>
            <span>全部</span>
          </button>
          <button 
            class="sidebar-item" 
            :class="{ active: currentPlace === 'cold' }"
            @click="filterByPlace('cold')"
          >
            <i class="fas fa-temperature-low"></i>
            <span>冷藏</span>
            <span class="sidebar-badge">{{ getPlaceCount('cold') }}</span>
          </button>
          <button 
            class="sidebar-item" 
            :class="{ active: currentPlace === 'frozen' }"
            @click="filterByPlace('frozen')"
          >
            <i class="fas fa-snowflake"></i>
            <span>冷冻</span>
            <span class="sidebar-badge">{{ getPlaceCount('frozen') }}</span>
          </button>
          <button 
            class="sidebar-item" 
            :class="{ active: currentPlace === 'normal' }"
            @click="filterByPlace('normal')"
          >
            <i class="fas fa-home"></i>
            <span>室温</span>
            <span class="sidebar-badge">{{ getPlaceCount('normal') }}</span>
          </button>
        </div>

        <!-- 右侧物品列表 -->
        <div class="main-list-area">
          <ItemList />
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <nav class="mobile-bottom-nav">
      <button class="nav-item active">
        <i class="fas fa-snowflake"></i>
        <span>冰箱</span>
      </button>
      <button class="nav-item add-btn" @click="showAddItem">
        <div class="add-icon">
          <i class="fas fa-plus"></i>
        </div>
      </button>
      <button class="nav-item" @click="showUserMenu">
        <i class="fas fa-user"></i>
        <span>我的</span>
        <span v-if="user" class="nav-badge" :class="user.is_admin ? 'admin' : 'user'">
          {{ user.is_admin ? '管理员' : '私人' }}
        </span>
        <span v-else class="nav-badge guest">游客</span>
      </button>
    </nav>

    <!-- 用户菜单抽屉 -->
    <div class="drawer-overlay" :class="{ active: userMenuVisible }" @click="userMenuVisible = false">
      <div class="drawer-content" @click.stop>
        <div class="drawer-header">
          <h5>个人中心</h5>
          <button class="close-btn" @click="userMenuVisible = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="drawer-body">
          <div class="user-info-card">
            <div class="user-avatar">
              <i class="fas fa-user"></i>
            </div>
            <div class="user-details">
              <div class="user-name-large">{{ user?.username || '未登录' }}</div>
              <div class="user-status">{{ user?.email || '' }}</div>
            </div>
          </div>
          <div class="menu-list">
            <router-link v-if="user" to="/profile" class="menu-item" @click="userMenuVisible = false">
              <i class="fas fa-user-circle"></i>
              <span>个人资料</span>
              <i class="fas fa-chevron-right"></i>
            </router-link>
            <router-link v-if="user?.is_admin" to="/admin" class="menu-item" @click="userMenuVisible = false">
              <i class="fas fa-cog"></i>
              <span>系统管理</span>
              <i class="fas fa-chevron-right"></i>
            </router-link>
            <router-link v-if="user" to="/family" class="menu-item" @click="userMenuVisible = false">
              <i class="fas fa-users"></i>
              <span>家庭管理</span>
              <i class="fas fa-chevron-right"></i>
            </router-link>
            <button v-if="user" class="menu-item danger" @click="handleLogout">
              <i class="fas fa-sign-out-alt"></i>
              <span>退出登录</span>
              <i class="fas fa-chevron-right"></i>
            </button>
            <router-link v-if="!user" to="/login" class="menu-item" @click="userMenuVisible = false">
              <i class="fas fa-sign-in-alt"></i>
              <span>登录</span>
              <i class="fas fa-chevron-right"></i>
            </router-link>
            <router-link v-if="!user" to="/register" class="menu-item" @click="userMenuVisible = false">
              <i class="fas fa-user-plus"></i>
              <span>注册</span>
              <i class="fas fa-chevron-right"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加物品抽屉 -->
    <div class="drawer-overlay" :class="{ active: addItemVisible }" @click="addItemVisible = false">
      <div class="drawer-content full-height" @click.stop>
        <div class="drawer-header">
          <h5>添加物品</h5>
          <button class="close-btn" @click="addItemVisible = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="drawer-body">
          <ItemForm @success="handleAddSuccess" @cancel="addItemVisible = false" />
        </div>
      </div>
    </div>

    <!-- 冰箱选择器抽屉 -->
    <div class="drawer-overlay" :class="{ active: fridgeSelectorVisible }" @click="fridgeSelectorVisible = false">
      <div class="drawer-content" @click.stop>
        <div class="drawer-header">
          <h5>选择冰箱</h5>
          <button class="close-btn" @click="fridgeSelectorVisible = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="drawer-body">
          <FridgeSelector @close="fridgeSelectorVisible = false" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useFridgeStore } from '@/stores/fridge'
import { useItemStore } from '@/stores/item'
import { useTheme } from '@/composables/useTheme'
import ItemList from '@/components/item/ItemList.vue'
import ItemForm from '@/components/item/ItemForm.vue'
import FridgeSelector from '@/components/fridge/FridgeSelector.vue'
import type { Item } from '@/types/models'

const router = useRouter()
const userStore = useUserStore()
const fridgeStore = useFridgeStore()
const itemStore = useItemStore()
const { currentTheme, toggleTheme } = useTheme()

// 状态
const userMenuVisible = ref(false)
const addItemVisible = ref(false)
const fridgeSelectorVisible = ref(false)
const isRotating = ref(false)
const currentPlace = ref('all')

// 计算属性
const user = computed(() => userStore.user)
const currentFridge = computed(() => {
  const allFridges = [...fridgeStore.myFridges, ...fridgeStore.sharedFridges]
  return allFridges.find(f => f._id === fridgeStore.currentFridgeId)
})

// 获取指定位置的物品数量
const getPlaceCount = (place: string) => {
  return itemStore.items.filter((item: Item) => item.place === place).length
}

// 显示用户菜单
const showUserMenu = () => {
  userMenuVisible.value = true
}

// 显示添加物品
const showAddItem = () => {
  addItemVisible.value = true
}

// 显示冰箱选择器
const showFridgeSelector = () => {
  fridgeSelectorVisible.value = true
}

// 切换冰箱
const switchFridge = async (fridgeId: string) => {
  try {
    await fridgeStore.switchFridge(fridgeId)
    await itemStore.loadItems()
    ElMessage.success('已切换冰箱')
  } catch (error) {
    console.error('[首页] 切换冰箱失败', error)
  }
}

// 按位置过滤
const filterByPlace = (place: string) => {
  currentPlace.value = place
  if (place === 'all') {
    itemStore.filterPlace = null
  } else {
    itemStore.filterPlace = place
  }
}

// 显示所有物品
const showAllItems = () => {
  itemStore.filterPlace = null
  itemStore.filterType = null
  currentPlace.value = 'all'
}

// 显示即将过期物品
const showExpiringSoon = () => {
  ElMessage.info('即将过期物品筛选功能开发中...')
}

// 显示已过期物品
const showExpired = () => {
  ElMessage.info('已过期物品筛选功能开发中...')
}

// 切换主题
const handleToggleTheme = async () => {
  isRotating.value = true
  await toggleTheme()
  
  setTimeout(() => {
    isRotating.value = false
  }, 600)
}

// 处理添加成功
const handleAddSuccess = () => {
  addItemVisible.value = false
  ElMessage.success('添加成功')
  itemStore.loadItems()
}

// 处理登出
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消
  }
}

// 初始化
onMounted(async () => {
  // 初始化用户状态
  userStore.initFromStorage()
  
  // 加载数据
  try {
    await Promise.all([
      fridgeStore.loadFridges(),
      itemStore.loadItems()
    ])
  } catch (error) {
    console.error('[首页] 加载数据失败', error)
  }
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: var(--bg-color);
}

/* 响应式布局 */
@media (min-width: 769px) {
  .home-page {
    max-width: 768px;
    margin: 0 auto;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }
}
</style>
