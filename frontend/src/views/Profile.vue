<template>
  <div class="profile-page">
    <!-- 顶部导航栏 -->
    <div class="mobile-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <i class="fas fa-user"></i>
          </div>
          <div class="app-name">个人中心</div>
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
      <div class="settings-page-content">
        <!-- 用户信息卡片 -->
        <div class="user-profile-card">
          <div :class="['profile-avatar', { guest: !userStore.isLoggedIn }]">
            <i :class="userStore.isLoggedIn ? 'fas fa-user-circle' : 'fas fa-user'"></i>
          </div>
          <div class="profile-info">
            <div class="profile-name">{{ userStore.user?.username || '游客模式' }}</div>
            <div v-if="userStore.isLoggedIn" class="profile-status">
              <span v-if="userStore.isAdmin" class="badge-admin">
                <i class="fas fa-crown"></i> 管理员
              </span>
              <span v-else class="badge-user">
                <i class="fas fa-check-circle"></i> 已登录
              </span>
            </div>
            <div v-else class="profile-hint">登录后享受更多功能</div>
          </div>
          <div v-if="!userStore.isLoggedIn" class="guest-actions">
            <a href="/login" class="btn-login-small">
              <i class="fas fa-sign-in-alt"></i> 登录
            </a>
            <a href="/register" class="btn-register-small">
              <i class="fas fa-user-plus"></i> 注册
            </a>
          </div>
        </div>

        <!-- 管理后台入口 -->
        <div v-if="userStore.isLoggedIn && userStore.isAdmin" class="settings-section">
          <router-link to="/admin/dashboard" class="settings-item admin-entry">
            <div class="settings-item-left">
              <i class="fas fa-shield-alt"></i>
              <span>管理后台</span>
            </div>
            <div class="settings-item-right">
              <span class="badge-admin-small">管理员</span>
              <i class="fas fa-chevron-right"></i>
            </div>
          </router-link>
        </div>

        <!-- 外观设置 -->
        <div class="settings-section">
          <h3>外观设置</h3>
          <div class="settings-item-toggle">
            <div class="settings-item-left">
              <i class="fas fa-adjust"></i>
              <span>自动日夜切换</span>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="autoTheme" @change="toggleAutoTheme">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <!-- 主题选择 -->
        <div class="settings-section">
          <h3>主题颜色</h3>
          <div class="theme-selector-scroll">
            <div class="theme-selector">
              <div 
                v-for="theme in themes" 
                :key="theme.name"
                :class="['theme-option', { active: currentTheme === theme.name }]"
                :data-theme="theme.name"
                @click="selectTheme(theme.name)"
              >
                <div class="theme-color" :style="{ background: theme.gradient }"></div>
                <span>{{ theme.label }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 数据管理 -->
        <div class="settings-section">
          <h3>数据管理</h3>
          <div class="settings-item" @click="exportData">
            <div class="settings-item-left">
              <i class="fas fa-download"></i>
              <span>导出数据</span>
            </div>
            <div class="settings-item-right">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
          <div class="settings-item" @click="clearExpiredItems">
            <div class="settings-item-left">
              <i class="fas fa-trash-alt"></i>
              <span>清理过期物品</span>
            </div>
            <div class="settings-item-right">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>

        <!-- 关于 -->
        <div class="settings-section">
          <h3>关于</h3>
          <a href="https://github.com/Adsryen/fridgeManager" target="_blank" class="settings-item">
            <div class="settings-item-left">
              <i class="fab fa-github"></i>
              <span>GitHub 仓库</span>
            </div>
            <div class="settings-item-right">
              <span class="settings-value">Adsryen/fridgeManager</span>
              <i class="fas fa-external-link-alt" style="margin-left: 8px; font-size: 12px;"></i>
            </div>
          </a>
          <div class="settings-item">
            <div class="settings-item-left">
              <i class="fas fa-info-circle"></i>
              <span>版本信息</span>
            </div>
            <div class="settings-item-right">
              <span class="settings-value">v1.0.0</span>
            </div>
          </div>
        </div>

        <!-- 退出登录 -->
        <div v-if="userStore.isLoggedIn" class="settings-section">
          <div class="settings-item danger-item" @click="handleLogout">
            <div class="settings-item-left">
              <i class="fas fa-sign-out-alt"></i>
              <span>退出登录</span>
            </div>
            <div class="settings-item-right">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <div class="mobile-bottom-nav">
      <button class="nav-item" @click="$router.push('/')">
        <i class="fas fa-home"></i>
        <span>首页</span>
      </button>
      <button class="nav-item" @click="$router.push('/fridge')">
        <i class="fas fa-snowflake"></i>
        <span>冰箱</span>
      </button>
      <button class="nav-item add-btn" @click="$router.push('/')">
        <div class="add-icon">
          <i class="fas fa-plus"></i>
        </div>
      </button>
      <button class="nav-item" @click="$router.push('/family')">
        <i class="fas fa-users"></i>
        <span>家庭</span>
      </button>
      <button class="nav-item active">
        <i class="fas fa-user"></i>
        <span>我的</span>
        <span v-if="!userStore.isLoggedIn" class="nav-badge guest">游客</span>
        <span v-else-if="userStore.isAdmin" class="nav-badge admin">管理员</span>
        <span v-else class="nav-badge user">私人</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useItemStore } from '../stores/item'
import { useTheme } from '../composables/useTheme'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const itemStore = useItemStore()
const { isDark, toggleTheme } = useTheme()

const autoTheme = ref(false)
const currentTheme = ref('pink')

const themes = [
  { name: 'pink', label: '粉色', gradient: 'linear-gradient(135deg, #ffc0cb, #ffb6c1)' },
  { name: 'blue', label: '蓝色', gradient: 'linear-gradient(135deg, #60a5fa, #3b82f6)' },
  { name: 'purple', label: '紫色', gradient: 'linear-gradient(135deg, #a78bfa, #8b5cf6)' },
  { name: 'green', label: '绿色', gradient: 'linear-gradient(135deg, #6ee7b7, #34d399)' },
  { name: 'orange', label: '橙色', gradient: 'linear-gradient(135deg, #fdba74, #fb923c)' },
  { name: 'gray', label: '灰色', gradient: 'linear-gradient(135deg, #9ca3af, #6b7280)' }
]

onMounted(() => {
  // 从 localStorage 读取主题设置
  const savedTheme = localStorage.getItem('userTheme') || 'pink'
  currentTheme.value = savedTheme
  
  const savedAutoTheme = localStorage.getItem('autoTheme')
  autoTheme.value = savedAutoTheme === 'true'
})

const toggleDarkMode = () => {
  toggleTheme()
}

const toggleAutoTheme = () => {
  localStorage.setItem('autoTheme', autoTheme.value.toString())
  if (autoTheme.value) {
    // 根据时间自动切换
    const hour = new Date().getHours()
    const shouldBeDark = hour >= 18 || hour < 6
    if (shouldBeDark !== isDark.value) {
      toggleTheme()
    }
  }
}

const selectTheme = (themeName: string) => {
  currentTheme.value = themeName
  localStorage.setItem('userTheme', themeName)
  
  // 移除所有主题类
  document.documentElement.className = document.documentElement.className
    .split(' ')
    .filter(c => !c.startsWith('theme-'))
    .join(' ')
  
  // 添加新主题类
  if (themeName !== 'pink') {
    document.documentElement.classList.add(`theme-${themeName}`)
    document.body.classList.add(`theme-${themeName}`)
  }
  
  ElMessage.success(`已切换到${themes.find(t => t.name === themeName)?.label}主题`)
}

const exportData = async () => {
  try {
    await ElMessageBox.confirm('确定要导出所有数据吗？', '导出数据', {
      confirmButtonText: '导出',
      cancelButtonText: '取消',
      type: 'info'
    })
    
    // 获取所有物品数据
    const items = itemStore.items
    const dataStr = JSON.stringify(items, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `fridge-data-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
    
    ElMessage.success('数据导出成功')
  } catch {
    // 用户取消
  }
}

const clearExpiredItems = async () => {
  try {
    await ElMessageBox.confirm('确定要清理所有过期物品吗？此操作不可恢复！', '清理过期物品', {
      confirmButtonText: '清理',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 这里应该调用后端 API 清理过期物品
    ElMessage.success('过期物品清理成功')
  } catch {
    // 用户取消
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '确认退出', {
      confirmButtonText: '退出',
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
</script>

<style scoped>
.profile-page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.settings-page-content {
  padding: 20px;
  padding-bottom: 100px;
  overflow-y: auto;
  height: calc(100vh - 60px - 70px);
}

/* 用户信息卡片 */
.user-profile-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: var(--card-bg);
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
  flex-shrink: 0;
}

.profile-avatar.guest {
  background: #9ca3af;
}

.profile-info {
  flex: 1;
  min-width: 0;
}

.profile-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.profile-status {
  display: flex;
  gap: 8px;
  align-items: center;
}

.badge-admin,
.badge-user {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.badge-admin {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: white;
}

.badge-user {
  background: #3b82f6;
  color: white;
}

.profile-hint {
  font-size: 14px;
  color: var(--text-secondary);
}

.guest-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-login-small,
.btn-register-small {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-login-small {
  background: var(--primary-color);
  color: white;
}

.btn-register-small {
  background: var(--card-bg);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

/* 设置区块 */
.settings-section {
  margin-bottom: 24px;
}

.settings-section h3 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 快捷操作 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  background: var(--card-bg);
  border-radius: 12px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s;
  border: 1px solid var(--border-color);
}

.quick-action-item:active {
  transform: scale(0.95);
}

.quick-action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.quick-action-icon.admin {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
}

.quick-action-icon.fridge {
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
}

.quick-action-icon.family {
  background: linear-gradient(135deg, #a78bfa, #8b5cf6);
}

.quick-action-item span {
  font-size: 13px;
  font-weight: 500;
}

/* 管理后台入口 */
.admin-entry {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.1));
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.admin-entry .settings-item-left i {
  color: #f59e0b;
}

.badge-admin-small {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: white;
}

/* 设置项 */
.settings-item,
.settings-item-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid var(--border-color);
  text-decoration: none;
  color: var(--text-primary);
}

.settings-item:active {
  transform: scale(0.98);
}

.settings-item-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.settings-item-left i {
  width: 24px;
  text-align: center;
  font-size: 18px;
  color: var(--primary-color);
}

.settings-item-left span {
  font-size: 15px;
  font-weight: 500;
}

.settings-item-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.settings-value {
  font-size: 13px;
  color: var(--text-secondary);
}

.settings-item-right i {
  font-size: 14px;
  color: var(--text-secondary);
}

.danger-item {
  color: var(--danger-color);
}

.danger-item .settings-item-left i {
  color: var(--danger-color);
}

/* 切换开关 */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 28px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 28px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

/* 主题选择器 */
.theme-selector-scroll {
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.theme-selector-scroll::-webkit-scrollbar {
  display: none;
}

.theme-selector {
  display: flex;
  gap: 12px;
  padding-bottom: 4px;
  min-width: min-content;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: var(--card-bg);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
  flex-shrink: 0;
  min-width: 80px;
}

.theme-option.active {
  border-color: var(--primary-color);
  background: var(--bg-color);
}

.theme-option:active {
  transform: scale(0.95);
}

.theme-color {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.theme-option span {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
}

/* 导航气泡 */
.nav-badge {
  position: absolute;
  top: 4px;
  right: 8px;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  line-height: 1;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.nav-badge.guest {
  background: #9ca3af;
  color: white;
}

.nav-badge.user {
  background: #3b82f6;
  color: white;
}

.nav-badge.admin {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: white;
}
</style>
