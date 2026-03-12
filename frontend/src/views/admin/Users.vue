<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <header class="admin-header">
      <a @click="goBack" class="admin-header-back">
        <i class="fas fa-arrow-left"></i>
      </a>
      <div class="admin-header-title">用户管理</div>
      <div class="admin-header-action"></div>
    </header>

    <!-- 主内容区 -->
    <div class="admin-content">
      <!-- 提示框 -->
      <div v-if="alertMessage" :class="['alert', `alert-${alertType}`]">
        <i class="fas fa-check-circle"></i>
        <span>{{ alertMessage }}</span>
      </div>

      <!-- 加载动画 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <template v-else>
        <!-- 搜索框 -->
        <div class="search-section">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              type="text" 
              class="search-input" 
              placeholder="搜索用户名或邮箱..."
              v-model="searchQuery"
              @input="handleSearch"
            >
            <button 
              v-if="searchQuery" 
              class="search-clear"
              @click="clearSearch"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>

        <!-- 筛选标签 -->
        <div class="filter-tabs">
          <button 
            :class="['filter-tab', { active: currentFilter === 'all' }]"
            @click="setFilter('all')"
          >
            全部 ({{ users.length }})
          </button>
          <button 
            :class="['filter-tab', { active: currentFilter === 'active' }]"
            @click="setFilter('active')"
          >
            活跃 ({{ activeUsers }})
          </button>
          <button 
            :class="['filter-tab', { active: currentFilter === 'admin' }]"
            @click="setFilter('admin')"
          >
            管理员 ({{ adminUsers }})
          </button>
          <button 
            :class="['filter-tab', { active: currentFilter === 'inactive' }]"
            @click="setFilter('inactive')"
          >
            禁用 ({{ inactiveUsers }})
          </button>
        </div>

        <!-- 用户列表 -->
        <div class="user-list">
          <div
            v-for="user in displayUsers"
            :key="user._id"
            class="user-card"
            @click="showUserDetails(user)"
          >
            <div class="user-card-header">
              <div class="user-avatar" :class="{ offline: !user.is_active }">
                <i class="fas fa-user"></i>
                <div v-if="user.is_active" class="status-dot"></div>
              </div>
              <div class="user-basic-info">
                <div class="user-name">
                  {{ user.username }}
                  <i v-if="user.is_admin" class="fas fa-crown admin-crown"></i>
                </div>
                <div class="user-email">{{ user.email }}</div>
              </div>
              <div class="user-actions">
                <button 
                  class="action-btn"
                  @click.stop="showUserActions(user)"
                >
                  <i class="fas fa-ellipsis-v"></i>
                </button>
              </div>
            </div>
            
            <div class="user-card-body">
              <div class="user-badges">
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  <i :class="user.is_active ? 'fas fa-check-circle' : 'fas fa-ban'"></i>
                  {{ user.is_active ? '激活' : '禁用' }}
                </span>
                <span :class="['role-badge', user.is_admin ? 'admin' : 'user']">
                  <i :class="user.is_admin ? 'fas fa-shield-alt' : 'fas fa-user'"></i>
                  {{ user.is_admin ? '管理员' : '普通用户' }}
                </span>
              </div>
              
              <div class="user-meta-info">
                <div class="meta-item">
                  <i class="fas fa-calendar-alt"></i>
                  <span>加入时间: {{ formatDate(user.created_at) }}</span>
                </div>
                <div class="meta-item">
                  <i class="fas fa-clock"></i>
                  <span>最后活跃: {{ formatLastActive(user.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="displayUsers.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="empty-title">
            <span v-if="searchQuery">未找到匹配的用户</span>
            <span v-else-if="currentFilter !== 'all'">该分类下暂无用户</span>
            <span v-else>暂无用户数据</span>
          </div>
          <div class="empty-description">
            <span v-if="searchQuery">尝试使用其他关键词搜索</span>
            <span v-else-if="currentFilter !== 'all'">切换到其他分类查看</span>
            <span v-else>系统中还没有注册用户</span>
          </div>
        </div>
      </template>
    </div>

    <!-- 底部导航栏 -->
    <nav class="admin-nav">
      <router-link to="/admin/dashboard" class="admin-nav-item">
        <i class="fas fa-tachometer-alt"></i>
        <span>仪表盘</span>
      </router-link>
      <router-link to="/admin/users" class="admin-nav-item active">
        <i class="fas fa-users"></i>
        <span>用户管理</span>
      </router-link>
      <router-link to="/admin/ai-settings" class="admin-nav-item">
        <i class="fas fa-brain"></i>
        <span>AI</span>
      </router-link>
      <router-link to="/admin/settings" class="admin-nav-item">
        <i class="fas fa-cog"></i>
        <span>设置</span>
      </router-link>
    </nav>

    <!-- 用户操作弹窗 -->
    <div v-if="showActionModal" class="modal-overlay" @click="closeActionModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>用户操作</h3>
          <button @click="closeActionModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="action-list">
            <button 
              class="action-item"
              @click="handleToggleStatus(currentUser)"
            >
              <i :class="currentUser?.is_active ? 'fas fa-ban' : 'fas fa-check'"></i>
              <span>{{ currentUser?.is_active ? '禁用用户' : '激活用户' }}</span>
            </button>
            <button 
              class="action-item"
              @click="handleToggleAdmin(currentUser)"
            >
              <i :class="currentUser?.is_admin ? 'fas fa-user-minus' : 'fas fa-user-shield'"></i>
              <span>{{ currentUser?.is_admin ? '取消管理员' : '设为管理员' }}</span>
            </button>
            <button 
              class="action-item"
              @click="handleResetPassword(currentUser)"
            >
              <i class="fas fa-key"></i>
              <span>重置密码</span>
            </button>
            <button 
              class="action-item danger"
              @click="handleDeleteUser(currentUser)"
            >
              <i class="fas fa-trash"></i>
              <span>删除用户</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 重置密码弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>重置密码</h3>
          <button @click="closePasswordModal" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">用户名</label>
            <input type="text" class="form-control" :value="currentUser?.username" disabled />
          </div>
          <div class="form-group">
            <label class="form-label">新密码</label>
            <input 
              type="password" 
              class="form-control" 
              v-model="newPassword"
              placeholder="请输入新密码"
            />
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="closePasswordModal">取消</button>
            <button class="btn btn-primary" @click="confirmResetPassword">确认</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as adminApi from '@/api/admin'
import type { User } from '@/types/models'

const router = useRouter()

// 状态
const loading = ref(false)
const users = ref<User[]>([])
const searchQuery = ref('')
const currentFilter = ref<'all' | 'active' | 'admin' | 'inactive'>('all')
const showActionModal = ref(false)
const showPasswordModal = ref(false)
const currentUser = ref<User | null>(null)
const newPassword = ref('')
const alertMessage = ref('')
const alertType = ref<'success' | 'danger' | 'warning' | 'info'>('success')

// 计算属性
const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) || 
    user.email.toLowerCase().includes(query)
  )
})

const displayUsers = computed(() => {
  let result = filteredUsers.value
  
  switch (currentFilter.value) {
    case 'active':
      result = result.filter(user => user.is_active)
      break
    case 'admin':
      result = result.filter(user => user.is_admin)
      break
    case 'inactive':
      result = result.filter(user => !user.is_active)
      break
  }
  
  return result
})

const activeUsers = computed(() => {
  return users.value.filter(user => user.is_active).length
})

const adminUsers = computed(() => {
  return users.value.filter(user => user.is_admin).length
})

const inactiveUsers = computed(() => {
  return users.value.filter(user => !user.is_active).length
})

// 返回上一页
function goBack() {
  router.push('/profile')
}

// 显示提示信息
function showAlert(message: string, type: 'success' | 'danger' | 'warning' | 'info' = 'success') {
  alertMessage.value = message
  alertType.value = type
  setTimeout(() => {
    alertMessage.value = ''
  }, 3000)
}

// 搜索处理
function handleSearch() {
  // 搜索功能通过计算属性自动处理
}

// 清除搜索
function clearSearch() {
  searchQuery.value = ''
}

// 设置筛选器
function setFilter(filter: 'all' | 'active' | 'admin' | 'inactive') {
  currentFilter.value = filter
}

// 显示用户详情
function showUserDetails(user: User) {
  // 可以添加用户详情查看功能
  console.log('查看用户详情:', user)
}

// 格式化最后活跃时间
function formatLastActive(createdAt: string) {
  const now = new Date()
  const createTime = new Date(createdAt)
  const diffMs = now.getTime() - createTime.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天注册'
  if (diffDays === 1) return '昨天注册'
  if (diffDays < 7) return `${diffDays}天前注册`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前注册`
  return `${Math.floor(diffDays / 30)}个月前注册`
}

// 格式化日期
function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载用户列表
async function loadUsers() {
  loading.value = true
  try {
    const response = await adminApi.getAllUsers()
    if (response.success && response.data) {
      users.value = response.data
    }
  } catch (_error) {
    showAlert('加载用户列表失败', 'danger')
  } finally {
    loading.value = false
  }
}

// 显示用户操作菜单
function showUserActions(user: User) {
  currentUser.value = user
  showActionModal.value = true
}

// 关闭操作菜单
function closeActionModal() {
  showActionModal.value = false
  currentUser.value = null
}

// 切换用户状态
async function handleToggleStatus(user: User | null) {
  if (!user) return
  
  try {
    const response = await adminApi.toggleUserStatus(user._id)
    if (response.success) {
      showAlert(`${user.is_active ? '禁用' : '激活'}成功`)
      await loadUsers()
      closeActionModal()
    }
  } catch (_error) {
    showAlert('操作失败', 'danger')
  }
}

// 切换管理员权限
async function handleToggleAdmin(user: User | null) {
  if (!user) return
  
  try {
    const response = await adminApi.toggleAdminStatus(user._id)
    if (response.success) {
      showAlert(`${user.is_admin ? '取消' : '设置'}管理员权限成功`)
      await loadUsers()
      closeActionModal()
    }
  } catch (_error) {
    showAlert('操作失败', 'danger')
  }
}

// 打开重置密码对话框
function handleResetPassword(user: User | null) {
  if (!user) return
  
  currentUser.value = user
  newPassword.value = ''
  showActionModal.value = false
  showPasswordModal.value = true
}

// 关闭重置密码对话框
function closePasswordModal() {
  showPasswordModal.value = false
  newPassword.value = ''
}

// 确认重置密码
async function confirmResetPassword() {
  if (!newPassword.value) {
    showAlert('请输入新密码', 'warning')
    return
  }

  if (newPassword.value.length < 6) {
    showAlert('密码长度至少为 6 位', 'warning')
    return
  }

  if (!currentUser.value) return

  try {
    const response = await adminApi.resetUserPassword(
      currentUser.value._id,
      newPassword.value
    )
    if (response.success) {
      showAlert('密码重置成功')
      closePasswordModal()
    }
  } catch (_error) {
    showAlert('密码重置失败', 'danger')
  }
}

// 删除用户
async function handleDeleteUser(user: User | null) {
  if (!user) return
  
  if (!confirm(`确定要删除用户 ${user.username} 吗？此操作不可恢复！`)) {
    return
  }

  try {
    const response = await adminApi.deleteUser(user._id)
    if (response.success) {
      showAlert('用户删除成功')
      await loadUsers()
      closeActionModal()
    }
  } catch (_error) {
    showAlert('删除失败', 'danger')
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
/* 管理后台移动端 - 用户管理页面样式 */

/* 容器 */
.admin-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--background-color);
}

/* 顶部导航栏 */
.admin-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 45px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 1000;
}

.admin-header-title {
  font-size: 15px;
  font-weight: 600;
}

.admin-header-back {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.admin-header-back:active {
  opacity: 0.7;
}

.admin-header-action {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
}

/* 主内容区 */
.admin-content {
  flex: 1;
  padding: calc(45px + 12px) 12px calc(60px + 12px);
  overflow-y: auto;
}

/* 底部导航栏 */
.admin-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
  z-index: 1000;
}

.admin-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 10px;
  padding: 6px;
  transition: all 0.3s;
  text-decoration: none;
}

.admin-nav-item i {
  font-size: 18px;
  margin-bottom: 3px;
}

.admin-nav-item.active {
  color: var(--primary-color);
}

.admin-nav-item:active {
  background-color: rgba(0,0,0,0.05);
}

/* 搜索区域 */
.search-section {
  margin-bottom: 16px;
}

.search-box {
  position: relative;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 44px 0 44px;
  border: 2px solid var(--divider-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-background);
  color: var(--text-primary);
  transition: all 0.3s;
}

.search-input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-size: 18px;
}

.search-clear {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border: none;
  background: var(--text-secondary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.search-clear:hover {
  background: var(--danger-color);
}

/* 筛选标签 */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.filter-tab {
  flex-shrink: 0;
  padding: 8px 16px;
  border: 2px solid var(--divider-color);
  border-radius: 20px;
  background: var(--card-background);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.filter-tab:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.filter-tab.active {
  border-color: var(--primary-color);
  background: var(--primary-color);
  color: white;
}

/* 用户列表 */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-card {
  background: var(--card-background);
  border-radius: 16px;
  border: 2px solid var(--divider-color);
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.user-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.user-card:active {
  transform: translateY(0);
}

.user-card-header {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 12px;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  position: relative;
  flex-shrink: 0;
}

.user-avatar.offline {
  background: var(--text-secondary);
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: #4CAF50;
  border: 2px solid white;
  border-radius: 50%;
}

.user-basic-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.admin-crown {
  color: #FFD700;
  font-size: 14px;
}

.user-email {
  font-size: 14px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-actions {
  flex-shrink: 0;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--background-color);
  color: var(--text-secondary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--primary-color);
  color: white;
}

.user-card-body {
  padding: 0 16px 16px;
}

.user-badges {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.status-badge, .role-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-badge.inactive {
  background: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

.role-badge.admin {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.role-badge.user {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.user-meta-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.meta-item i {
  width: 14px;
  text-align: center;
}

/* 空状态优化 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  line-height: 1.5;
}

.user-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.user-email {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.user-date {
  font-size: 10px;
  color: var(--text-secondary);
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background: var(--card-background);
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid var(--divider-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text-primary);
}

.modal-close {
  background: var(--background-color);
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-primary);
  padding: 4px 8px;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 16px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.modal-actions .btn {
  flex: 1;
}

/* 操作列表 */
.action-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--divider-color);
  border-radius: 8px;
  background: var(--card-background);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
}

.action-item:hover {
  background: var(--background-color);
  border-color: var(--primary-color);
}

.action-item.danger {
  color: var(--danger-color);
  border-color: var(--danger-color);
}

.action-item.danger:hover {
  background: rgba(244, 67, 54, 0.1);
}

.action-item i {
  font-size: 16px;
  width: 20px;
  text-align: center;
}
</style>
