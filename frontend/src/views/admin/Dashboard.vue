<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <header class="admin-header">
      <a @click="goBack" class="admin-header-back">
        <i class="fas fa-arrow-left"></i>
      </a>
      <div class="admin-header-title">仪表盘</div>
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

      <!-- 统计卡片 -->
      <div v-else class="stats-grid">
        <div class="stat-card primary">
          <div class="stat-card-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-card-value">{{ stats.total_users }}</div>
          <div class="stat-card-label">用户总数</div>
        </div>

        <div class="stat-card success">
          <div class="stat-card-icon">
            <i class="fas fa-box"></i>
          </div>
          <div class="stat-card-value">{{ stats.total_items }}</div>
          <div class="stat-card-label">物品总数</div>
        </div>

        <div class="stat-card warning">
          <div class="stat-card-icon">
            <i class="fas fa-snowflake"></i>
          </div>
          <div class="stat-card-value">{{ stats.total_fridges }}</div>
          <div class="stat-card-label">冰箱总数</div>
        </div>

        <div class="stat-card info">
          <div class="stat-card-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-card-value">{{ activeRate }}%</div>
          <div class="stat-card-label">活跃用户</div>
        </div>
      </div>

      <!-- 系统状态 -->
      <div class="card">
        <div class="card-header">
          <i class="fas fa-server"></i> 系统状态
        </div>
        <div class="card-body">
          <div class="status-list">
            <div class="status-item">
              <div class="status-info">
                <div class="status-label">数据库连接</div>
                <div class="status-description">MySQL 数据库运行正常</div>
              </div>
              <div class="status-indicator success">
                <i class="fas fa-check-circle"></i>
              </div>
            </div>
            <div class="status-item">
              <div class="status-info">
                <div class="status-label">AI 服务</div>
                <div class="status-description">OpenAI API 连接正常</div>
              </div>
              <div class="status-indicator success">
                <i class="fas fa-check-circle"></i>
              </div>
            </div>
            <div class="status-item">
              <div class="status-info">
                <div class="status-label">文件存储</div>
                <div class="status-description">本地存储空间充足</div>
              </div>
              <div class="status-indicator success">
                <i class="fas fa-check-circle"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="card">
        <div class="card-header">
          <i class="fas fa-bolt"></i> 快捷操作
        </div>
        <div class="card-body">
          <div class="action-grid">
            <router-link to="/admin/users" class="action-btn primary">
              <div class="action-icon">
                <i class="fas fa-users-cog"></i>
              </div>
              <div class="action-content">
                <div class="action-title">用户管理</div>
                <div class="action-desc">管理系统用户</div>
              </div>
            </router-link>
            <router-link to="/admin/settings" class="action-btn info">
              <div class="action-icon">
                <i class="fas fa-cog"></i>
              </div>
              <div class="action-content">
                <div class="action-title">系统设置</div>
                <div class="action-desc">配置系统参数</div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <nav class="admin-nav">
      <router-link to="/admin/dashboard" class="admin-nav-item active">
        <i class="fas fa-tachometer-alt"></i>
        <span>仪表盘</span>
      </router-link>
      <router-link to="/admin/users" class="admin-nav-item">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as adminApi from '@/api/admin'

const router = useRouter()

// 状态
const loading = ref(false)
const alertMessage = ref('')
const alertType = ref('success')
const stats = ref({
  total_users: 0,
  total_items: 0,
  total_fridges: 0,
  active_users: 0
})

// 计算活跃率
const activeRate = computed(() => {
  if (stats.value.total_users === 0) return 0
  return Math.round((stats.value.active_users / stats.value.total_users) * 100)
})

// 返回上一页
const goBack = () => {
  router.push('/profile')
}

// 显示提示信息
const showAlert = (message: string, type: string = 'success') => {
  alertMessage.value = message
  alertType.value = type
  setTimeout(() => {
    alertMessage.value = ''
  }, 3000)
}

// 加载统计数据
async function loadStats() {
  loading.value = true
  try {
    const response = await adminApi.getStats()
    if (response.success && response.data) {
      stats.value = response.data
    }
  } catch (_error) {
    showAlert('加载统计数据失败', 'danger')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
/* 管理后台移动端 - 基础样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

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

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

/* 统计卡片 */
.stat-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-card.primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.stat-card.success {
  background: linear-gradient(135deg, #11998e, #38ef7d);
  color: white;
}

.stat-card.warning {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white;
}

.stat-card.info {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: white;
}

.stat-card-value {
  font-size: 29px;
  font-weight: 700;
  margin-bottom: 6px;
}

.stat-card-label {
  font-size: 13px;
  opacity: 0.9;
}

.stat-card-icon {
  font-size: 19px;
  margin-bottom: 6px;
}

/* 卡片 */
.card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);
  margin-bottom: 12px;
  overflow: hidden;
}

.card-header {
  padding: 12px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
}

.card-body {
  padding: 12px;
}

/* 操作网格 */
.action-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

/* 操作按钮 */
.action-btn {
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s;
  border: 1px solid var(--divider-color);
  background: var(--card-bg);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.action-btn.primary {
  border-color: var(--primary-color);
  background: rgba(102, 126, 234, 0.05);
}

.action-btn.info {
  border-color: #2196F3;
  background: rgba(33, 150, 243, 0.05);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 20px;
}

.action-btn.primary .action-icon {
  background: var(--primary-color);
  color: white;
}

.action-btn.info .action-icon {
  background: #2196F3;
  color: white;
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.action-desc {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 系统状态 */
.status-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--divider-color);
}

.status-item:last-child {
  border-bottom: none;
}

.status-info {
  flex: 1;
}

.status-label {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.status-description {
  font-size: 11px;
  color: var(--text-secondary);
}

.status-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.status-indicator.success {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

/* 按钮 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 38px;
  padding: 0 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.btn-info {
  background: #2196F3;
  color: white;
}

.btn-block {
  width: 100%;
}

.btn i {
  margin-right: 6px;
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

/* 提示框 */
.alert {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  font-size: 13px;
}

.alert i {
  margin-right: 8px;
}

.alert-success {
  background: #e8f5e9;
  color: #2e7d32;
}

.alert-danger {
  background: #ffebee;
  color: #c62828;
}

.alert-warning {
  background: #fff3e0;
  color: #ef6c00;
}

.alert-info {
  background: #e3f2fd;
  color: #1565c0;
}

/* 加载动画 */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>
