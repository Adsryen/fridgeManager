<template>
  <div class="admin-header">
    <div class="admin-header-content">
      <div class="admin-header-left">
        <button class="admin-back-btn" @click="goBack" title="返回">
          <i class="fas fa-arrow-left"></i>
        </button>
        <div class="admin-header-info">
          <h1 class="admin-title">{{ title }}</h1>
          <p v-if="subtitle" class="admin-subtitle">{{ subtitle }}</p>
        </div>
      </div>
      <div class="admin-header-right">
        <button class="admin-theme-btn" @click="toggleDarkMode" :title="isDark ? '切换到浅色模式' : '切换到深色模式'">
          <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
        </button>
        <router-link to="/profile" class="admin-profile-btn" title="返回个人中心">
          <i class="fas fa-user"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useTheme } from '../../composables/useTheme'

interface Props {
  title: string
  subtitle?: string
  showBackButton?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showBackButton: true
})

const router = useRouter()
const { isDark, toggleTheme } = useTheme()

const goBack = () => {
  // 如果有历史记录，返回上一页
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    // 否则返回管理员仪表板
    router.push('/admin/dashboard')
  }
}

const toggleDarkMode = async () => {
  await toggleTheme()
}
</script>

<style scoped>
.admin-header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 16px 20px;
  margin-bottom: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.admin-header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

.admin-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.admin-back-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
}

.admin-back-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: translateX(-2px);
}

.admin-back-btn:active {
  transform: translateX(-2px) scale(0.95);
}

.admin-header-info {
  flex: 1;
}

.admin-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  line-height: 1.2;
}

.admin-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

.admin-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-theme-btn,
.admin-profile-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
  text-decoration: none;
}

.admin-theme-btn:hover {
  background: var(--secondary-color);
  color: white;
  border-color: var(--secondary-color);
  transform: rotate(15deg);
}

.admin-profile-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
  transform: scale(1.05);
}

.admin-theme-btn:active,
.admin-profile-btn:active {
  transform: scale(0.95);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-header {
    padding: 12px 16px;
    margin-bottom: 20px;
  }

  .admin-header-left {
    gap: 12px;
  }

  .admin-title {
    font-size: 20px;
  }

  .admin-subtitle {
    font-size: 13px;
  }

  .admin-back-btn,
  .admin-theme-btn,
  .admin-profile-btn {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }

  .admin-header-right {
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .admin-header {
    padding: 10px 12px;
  }

  .admin-title {
    font-size: 18px;
  }

  .admin-subtitle {
    display: none; /* 在很小的屏幕上隐藏副标题 */
  }
}
</style>