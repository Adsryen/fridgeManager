<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>管理员仪表板</h1>
      <p class="subtitle">系统概览与统计</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <div v-else class="stats-container">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon users">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_users }}</div>
            <div class="stat-label">总用户数</div>
            <div class="stat-detail">活跃: {{ stats.active_users }}</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon items">
            <i class="fas fa-box"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_items }}</div>
            <div class="stat-label">总物品数</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon fridges">
            <i class="fas fa-snowflake"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_fridges }}</div>
            <div class="stat-label">总冰箱数</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon rate">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ activeRate }}%</div>
            <div class="stat-label">用户活跃率</div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions">
        <h2>快捷操作</h2>
        <div class="action-grid">
          <router-link to="/admin/users" class="action-card">
            <i class="fas fa-users-cog"></i>
            <span>用户管理</span>
          </router-link>
          <router-link to="/admin/settings" class="action-card">
            <i class="fas fa-cog"></i>
            <span>系统设置</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElSkeleton } from 'element-plus'
import * as adminApi from '@/api/admin'

// 状态
const loading = ref(false)
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

// 加载统计数据
async function loadStats() {
  loading.value = true
  try {
    const response = await adminApi.getStats()
    if (response.success && response.data) {
      stats.value = response.data
    }
  } catch (_error) {
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.loading-container {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.users {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon.items {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-icon.fridges {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-icon.rate {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.stat-detail {
  font-size: 12px;
  color: var(--text-secondary);
}

.quick-actions {
  margin-top: 40px;
}

.quick-actions h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 20px 0;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.action-card i {
  font-size: 32px;
}

.action-card span {
  font-size: 16px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-value {
    font-size: 28px;
  }
}
</style>
