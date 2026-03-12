<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <header class="admin-header">
      <a @click="goBack" class="admin-header-back">
        <i class="fas fa-arrow-left"></i>
      </a>
      <div class="admin-header-title">系统设置</div>
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
        <!-- 基础设置 -->
        <div class="card">
          <div class="card-header">
            <i class="fas fa-cog"></i> 基础设置
          </div>
          <div class="card-body">
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">会话超时时间</div>
                <div class="setting-description">用户登录会话的有效时长（小时）</div>
              </div>
              <div class="setting-control">
                <input 
                  type="number" 
                  class="form-input" 
                  v-model="settings.session_timeout"
                  min="1" 
                  max="168"
                >
              </div>
            </div>
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">每用户最大物品数</div>
                <div class="setting-description">单个用户可创建的最大物品数量</div>
              </div>
              <div class="setting-control">
                <input 
                  type="number" 
                  class="form-input" 
                  v-model="settings.max_items_per_user"
                  min="10" 
                  max="10000"
                  step="10"
                >
              </div>
            </div>
            <div class="setting-item">
              <div class="setting-info">
                <div class="setting-label">默认过期提醒天数</div>
                <div class="setting-description">物品即将过期的提前提醒天数</div>
              </div>
              <div class="setting-control">
                <input 
                  type="number" 
                  class="form-input" 
                  v-model="settings.default_expiry_warning_days"
                  min="1" 
                  max="30"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- 保存按钮 -->
        <div class="card">
          <div class="card-body">
            <button 
              type="button" 
              class="btn btn-primary btn-block" 
              @click="handleSave"
              :disabled="saving"
            >
              <i class="fas fa-save"></i> 保存设置
            </button>
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
      <router-link to="/admin/users" class="admin-nav-item">
        <i class="fas fa-users"></i>
        <span>用户管理</span>
      </router-link>
      <router-link to="/admin/ai-settings" class="admin-nav-item">
        <i class="fas fa-brain"></i>
        <span>AI</span>
      </router-link>
      <router-link to="/admin/settings" class="admin-nav-item active">
        <i class="fas fa-cog"></i>
        <span>设置</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as adminApi from '@/api/admin'
import type { SystemSettings } from '@/types/models'

const router = useRouter()

// 状态
const loading = ref(false)
const saving = ref(false)
const alertMessage = ref('')
const alertType = ref<'success' | 'danger' | 'warning' | 'info'>('success')

const settings = ref<SystemSettings>({
  session_timeout: 24,
  max_items_per_user: 1000,
  default_expiry_warning_days: 3,
  enable_ai_features: false,
  openai_api_base: '',
  openai_api_key: '',
  openai_chat_model: 'gpt-3.5-turbo',
  openai_vision_model: 'gpt-4-vision-preview',
  openai_audio_model: 'whisper-1'
})

const originalSettings = ref<SystemSettings | null>(null)

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

// 加载系统设置
async function loadSettings() {
  loading.value = true
  try {
    const response = await adminApi.getSettings()
    if (response.success && response.data) {
      settings.value = { ...response.data }
      originalSettings.value = { ...response.data }
    }
  } catch (_error) {
    showAlert('加载系统设置失败', 'danger')
  } finally {
    loading.value = false
  }
}

// 保存设置
async function handleSave() {
  saving.value = true
  try {
    const response = await adminApi.saveSettings(settings.value)
    if (response.success) {
      showAlert('设置保存成功')
      originalSettings.value = { ...settings.value }
    }
  } catch (_error) {
    showAlert('保存设置失败', 'danger')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
/* 管理后台移动端 - AI设置页面样式 */

/* 容器 */
.admin-container {
  min-height: 100vh;
  padding-bottom: 60px;
  background: var(--background-color);
  overflow-y: auto;
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
  padding: calc(45px + 12px) 12px 12px;
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

/* 设置项样式 */
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--divider-color);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-label {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 13px;
  color: var(--text-primary);
}

.setting-description {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.setting-control {
  margin-left: 12px;
}

/* 开关样式 */
.form-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.form-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--divider-color);
  transition: .4s;
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(18px);
}

/* 模型输入组 */
.model-input-group {
  display: flex;
  gap: 8px;
}

.model-input-group .form-control {
  flex: 1;
  cursor: pointer;
}

.model-input-group .btn {
  padding: 0 16px;
  white-space: nowrap;
}

/* 表单提示 */
.form-hint {
  font-size: 11px;
  color: var(--text-secondary);
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

/* 表单输入框 */
.form-input {
  width: 64px;
  text-align: center;
  font-size: 13px;
  padding: 6px 8px;
  border: 1px solid var(--divider-color);
  border-radius: 6px;
  background: var(--card-background);
  color: var(--text-primary);
}

.form-input:focus {
  border-color: var(--primary-color);
  outline: none;
}

/* 测试结果 */
.test-result {
  margin-top: 12px;
  padding: 12px;
  border-radius: 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.test-result.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.test-result.error {
  background: #ffebee;
  color: #c62828;
}

/* 使用说明 */
.usage-info {
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.usage-info p {
  margin: 0 0 8px 0;
}

.usage-info strong {
  color: var(--text-primary);
}

.usage-info ul, .usage-info ol {
  margin: 0 0 12px 0;
  padding-left: 20px;
}

.usage-info li {
  margin-bottom: 4px;
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
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
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
  display: flex;
  align-items: center;
  gap: 8px;
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

.modal-fetch-section {
  padding: 16px;
  border-bottom: 1px solid var(--divider-color);
}

.modal-model-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.loading-models, .empty-models {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

.loading-models i, .empty-models i {
  font-size: 32px;
  margin-bottom: 12px;
}

.loading-models i {
  color: var(--primary-color);
}

.model-grid {
  display: grid;
  gap: 8px;
}

.model-item-card {
  padding: 12px;
  border: 2px solid var(--divider-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--card-background);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.model-item-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.model-item-card.selected {
  border-color: var(--primary-color);
  background: rgba(102, 126, 234, 0.1);
}

.model-content {
  flex: 1;
  overflow: hidden;
}

.model-name {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.model-item-card.selected .model-name {
  color: var(--primary-color);
}

.model-item-card i {
  font-size: 18px;
  color: var(--text-secondary);
}

.model-item-card.selected i {
  color: var(--primary-color);
}
</style>
