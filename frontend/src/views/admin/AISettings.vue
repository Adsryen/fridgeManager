<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <header class="admin-header">
      <a @click="goBack" class="admin-header-back">
        <i class="fas fa-arrow-left"></i>
      </a>
      <div class="admin-header-title">AI设置</div>
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
        <!-- AI功能开关 -->
        <div class="settings-card">
          <div class="card-header">
            <div class="header-icon">
              <i class="fas fa-power-off"></i>
            </div>
            <div class="header-content">
              <div class="header-title">AI功能控制</div>
              <div class="header-subtitle">管理系统AI功能的启用状态</div>
            </div>
          </div>
          <div class="card-body">
            <div class="toggle-setting">
              <div class="toggle-info">
                <div class="toggle-label">启用AI功能</div>
                <div class="toggle-description">开启后用户可以使用OCR识别和AI对话功能</div>
              </div>
              <div class="toggle-control">
                <label class="modern-switch">
                  <input 
                    type="checkbox" 
                    v-model="settings.enable_ai_features"
                    @change="handleToggleAI"
                  >
                  <span class="switch-slider">
                    <span class="switch-button"></span>
                  </span>
                </label>
              </div>
            </div>
          </div>
        </div>
        <!-- API配置 -->
        <div class="settings-card">
          <div class="card-header">
            <div class="header-icon">
              <i class="fas fa-server"></i>
            </div>
            <div class="header-content">
              <div class="header-title">API配置</div>
              <div class="header-subtitle">配置OpenAI兼容的API服务</div>
            </div>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleSave" class="ai-form">
              <div class="input-group">
                <label class="input-label">
                  <i class="fas fa-link"></i>
                  <span>API地址</span>
                </label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    class="modern-input" 
                    v-model="settings.openai_api_base"
                    placeholder="https://api.openai.com/v1"
                  >
                </div>
                <div class="input-hint">
                  支持OpenAI官方API、one-api等兼容OpenAI协议的中转服务
                </div>
              </div>
              
              <div class="input-group">
                <label class="input-label">
                  <i class="fas fa-key"></i>
                  <span>API密钥</span>
                </label>
                <div class="input-wrapper">
                  <input 
                    type="password" 
                    class="modern-input" 
                    v-model="settings.openai_api_key"
                    placeholder="sk-..."
                  >
                  <button 
                    type="button" 
                    class="input-action"
                    @click="togglePasswordVisibility"
                  >
                    <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                  </button>
                </div>
                <div class="input-hint">
                  API访问密钥，用于身份验证
                </div>
              </div>
              
              <div class="input-group">
                <label class="input-label">
                  <i class="fas fa-robot"></i>
                  <span>对话模型</span>
                </label>
                <div class="model-selector">
                  <div class="model-input-wrapper">
                    <input 
                      type="text" 
                      class="modern-input model-input" 
                      v-model="settings.openai_chat_model"
                      placeholder="gpt-3.5-turbo" 
                      readonly
                    >
                    <button 
                      type="button" 
                      class="model-select-btn" 
                      @click="showModelSelector('chat')"
                    >
                      <i class="fas fa-chevron-down"></i>
                    </button>
                  </div>
                </div>
                <div class="input-hint">
                  用于AI对话功能的模型
                </div>
              </div>
              
              <div class="input-group">
                <label class="input-label">
                  <i class="fas fa-eye"></i>
                  <span>视觉模型</span>
                </label>
                <div class="model-selector">
                  <div class="model-input-wrapper">
                    <input 
                      type="text" 
                      class="modern-input model-input" 
                      v-model="settings.openai_vision_model"
                      placeholder="gpt-4-vision-preview" 
                      readonly
                    >
                    <button 
                      type="button" 
                      class="model-select-btn" 
                      @click="showModelSelector('vision')"
                    >
                      <i class="fas fa-chevron-down"></i>
                    </button>
                  </div>
                </div>
                <div class="input-hint">
                  用于OCR图片识别功能的模型
                </div>
              </div>
              
              <div class="input-group">
                <label class="input-label">
                  <i class="fas fa-microphone"></i>
                  <span>语音模型</span>
                </label>
                <div class="model-selector">
                  <div class="model-input-wrapper">
                    <input 
                      type="text" 
                      class="modern-input model-input" 
                      v-model="settings.openai_audio_model"
                      placeholder="whisper-1" 
                      readonly
                    >
                    <button 
                      type="button" 
                      class="model-select-btn" 
                      @click="showModelSelector('audio')"
                    >
                      <i class="fas fa-chevron-down"></i>
                    </button>
                  </div>
                </div>
                <div class="input-hint">
                  用于语音识别功能的模型
                </div>
              </div>
              
              <div class="action-buttons">
                <button 
                  type="button" 
                  class="action-btn test-btn" 
                  @click="testConnection"
                  :disabled="testingConnection"
                >
                  <i class="fas fa-plug"></i>
                  <span>{{ testingConnection ? '测试中...' : '测试连接' }}</span>
                </button>
                
                <button 
                  type="submit" 
                  class="action-btn save-btn" 
                  :disabled="saving"
                >
                  <i class="fas fa-save"></i>
                  <span>{{ saving ? '保存中...' : '保存配置' }}</span>
                </button>
              </div>
              
              <div v-if="testResult" :class="['test-result-card', testResult.type]">
                <div class="result-icon">
                  <i :class="testResult.type === 'success' ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                </div>
                <div class="result-content">
                  <div class="result-title">
                    {{ testResult.type === 'success' ? '连接成功' : '连接失败' }}
                  </div>
                  <div class="result-message">{{ testResult.message }}</div>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- 使用说明 -->
        <div class="card">
          <div class="card-header">
            <i class="fas fa-info-circle"></i> 使用说明
          </div>
          <div class="card-body usage-info">
            <p><strong>支持的API：</strong></p>
            <ul>
              <li>OpenAI官方API</li>
              <li>Azure OpenAI</li>
              <li>one-api中转服务</li>
              <li>其他兼容OpenAI协议的API</li>
            </ul>
            
            <p><strong>配置步骤：</strong></p>
            <ol>
              <li>填写API地址（包含/v1后缀）</li>
              <li>填写API密钥</li>
              <li>点击"测试连接"验证配置</li>
              <li>点击"获取模型列表"查看可用模型</li>
              <li>选择默认使用的模型</li>
              <li>保存配置并启用AI功能</li>
            </ol>
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
      <router-link to="/admin/ai-settings" class="admin-nav-item active">
        <i class="fas fa-brain"></i>
        <span>AI</span>
      </router-link>
      <router-link to="/admin/settings" class="admin-nav-item">
        <i class="fas fa-cog"></i>
        <span>设置</span>
      </router-link>
    </nav>

    <!-- 模型选择弹窗 -->
    <div v-if="showModelModal" class="modal-overlay" @click="closeModelSelector">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>
            <i class="fas fa-robot"></i> 
            <span>{{ modalTitle }}</span>
          </h3>
          <button @click="closeModelSelector" class="modal-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-fetch-section">
          <button 
            type="button" 
            class="btn btn-primary btn-block" 
            @click="fetchModelsForSelector"
            :disabled="loadingModels"
          >
            <i class="fas fa-sync-alt"></i> 获取模型列表
          </button>
        </div>
        <div class="modal-model-list">
          <div v-if="loadingModels" class="loading-models">
            <i class="fas fa-spinner fa-spin"></i>
            <p>正在获取模型列表...</p>
          </div>
          <div v-else-if="availableModels.length === 0" class="empty-models">
            <i class="fas fa-info-circle"></i>
            <p>点击上方按钮获取模型列表</p>
          </div>
          <div v-else class="model-grid">
            <div
              v-for="model in availableModels"
              :key="model"
              :class="['model-item-card', { selected: model === getCurrentModelValue() }]"
              @click="selectModelForType(model)"
            >
              <div class="model-content">
                <div class="model-name">{{ model }}</div>
              </div>
              <i v-if="model === getCurrentModelValue()" class="fas fa-check-circle"></i>
              <i v-else class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
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
const testingConnection = ref(false)
const loadingModels = ref(false)
const showModelModal = ref(false)
const showPassword = ref(false)
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

const availableModels = ref<string[]>([])
const currentModelType = ref<'chat' | 'vision' | 'audio' | null>(null)
const testResult = ref<{ type: 'success' | 'error', message: string } | null>(null)

// 模态框标题
const modalTitle = ref('')

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

// 切换密码显示
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
  const input = document.querySelector('input[type="password"]') as HTMLInputElement
  if (input) {
    input.type = showPassword.value ? 'text' : 'password'
  }
}

// 加载系统设置
async function loadSettings() {
  loading.value = true
  try {
    const response = await adminApi.getSettings()
    if (response.success && response.data) {
      settings.value = { ...response.data }
    }
  } catch (_error) {
    showAlert('加载系统设置失败', 'danger')
  } finally {
    loading.value = false
  }
}
// 处理AI功能开关
async function handleToggleAI() {
  try {
    const response = await adminApi.saveSettings({
      ...settings.value,
      enable_ai_features: settings.value.enable_ai_features
    })
    if (response.success) {
      showAlert(settings.value.enable_ai_features ? 'AI功能已启用' : 'AI功能已禁用')
    }
  } catch (_error) {
    showAlert('更新失败', 'danger')
    // 恢复原状态
    settings.value.enable_ai_features = !settings.value.enable_ai_features
  }
}

// 保存设置
async function handleSave() {
  saving.value = true
  try {
    const response = await adminApi.saveSettings(settings.value)
    if (response.success) {
      showAlert('设置保存成功')
    }
  } catch (_error) {
    showAlert('保存设置失败', 'danger')
  } finally {
    saving.value = false
  }
}

// 测试 AI 连接
async function testConnection() {
  if (!settings.value.openai_api_base || !settings.value.openai_api_key) {
    showAlert('请先填写 API 地址和密钥', 'warning')
    return
  }

  testingConnection.value = true
  testResult.value = null
  
  try {
    const response = await adminApi.testAIConnection(
      settings.value.openai_api_base,
      settings.value.openai_api_key
    )
    if (response.success) {
      testResult.value = { type: 'success', message: '连接成功！API可以正常使用' }
      showAlert('AI 连接测试成功')
    }
  } catch (error: any) {
    testResult.value = { type: 'error', message: `连接失败: ${error.message}` }
    showAlert('AI 连接测试失败，请检查配置', 'danger')
  } finally {
    testingConnection.value = false
  }
}
// 显示模型选择器
function showModelSelector(type: 'chat' | 'vision' | 'audio') {
  currentModelType.value = type
  const titles = {
    'chat': '选择对话模型',
    'vision': '选择视觉模型',
    'audio': '选择语音模型'
  }
  modalTitle.value = titles[type]
  showModelModal.value = true
}

// 关闭模型选择器
function closeModelSelector() {
  showModelModal.value = false
  currentModelType.value = null
  availableModels.value = []
}

// 获取模型列表（在弹窗中）
async function fetchModelsForSelector() {
  if (!settings.value.openai_api_base || !settings.value.openai_api_key) {
    showAlert('请先填写并保存API地址和密钥', 'warning')
    return
  }

  loadingModels.value = true
  
  try {
    const response = await adminApi.listAIModels(
      settings.value.openai_api_base,
      settings.value.openai_api_key
    )
    if (response.success && response.data?.models) {
      availableModels.value = response.data.models
      showAlert(`获取到 ${response.data.models.length} 个模型`)
    } else {
      availableModels.value = []
      showAlert('未找到可用模型', 'warning')
    }
  } catch (error: any) {
    availableModels.value = []
    showAlert(`获取模型列表失败: ${error.message}`, 'danger')
  } finally {
    loadingModels.value = false
  }
}

// 获取当前模型值
function getCurrentModelValue() {
  if (currentModelType.value === 'chat') {
    return settings.value.openai_chat_model
  } else if (currentModelType.value === 'vision') {
    return settings.value.openai_vision_model
  } else if (currentModelType.value === 'audio') {
    return settings.value.openai_audio_model
  }
  return ''
}

// 为指定类型选择模型
function selectModelForType(modelName: string) {
  if (currentModelType.value === 'chat') {
    settings.value.openai_chat_model = modelName
    showAlert(`已选择对话模型: ${modelName}`)
  } else if (currentModelType.value === 'vision') {
    settings.value.openai_vision_model = modelName
    showAlert(`已选择视觉模型: ${modelName}`)
  } else if (currentModelType.value === 'audio') {
    settings.value.openai_audio_model = modelName
    showAlert(`已选择语音模型: ${modelName}`)
  }
  closeModelSelector()
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
/* 设置卡片 */
.settings-card {
  background: var(--card-background);
  border-radius: 16px;
  border: 2px solid var(--divider-color);
  margin-bottom: 16px;
  overflow: hidden;
  transition: all 0.3s;
}

.settings-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.card-header {
  padding: 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.header-content {
  flex: 1;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.header-subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.card-body {
  padding: 20px;
}

/* 开关设置 */
.toggle-setting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.toggle-info {
  flex: 1;
}

.toggle-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.toggle-description {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.toggle-control {
  flex-shrink: 0;
}

/* 现代化开关 */
.modern-switch {
  position: relative;
  display: inline-block;
  width: 56px;
  height: 32px;
}

.modern-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--divider-color);
  transition: .4s;
  border-radius: 32px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.switch-button {
  position: absolute;
  content: "";
  height: 24px;
  width: 24px;
  left: 4px;
  bottom: 4px;
  background: white;
  transition: .4s;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

input:checked + .switch-slider {
  background: var(--primary-color);
}

input:checked + .switch-slider .switch-button {
  transform: translateX(24px);
}

/* 表单样式 */
.ai-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.input-label i {
  width: 16px;
  text-align: center;
  color: var(--primary-color);
}

.input-wrapper {
  position: relative;
}

.modern-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border: 2px solid var(--divider-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-background);
  color: var(--text-primary);
  transition: all 0.3s;
}

.modern-input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-action {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
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

.input-action:hover {
  background: var(--primary-color);
  color: white;
}

.input-hint {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

/* 模型选择器 */
.model-selector {
  position: relative;
}

.model-input-wrapper {
  position: relative;
}

.model-input {
  padding-right: 48px !important;
  cursor: pointer;
}

.model-select-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.model-select-btn:hover {
  background: var(--primary-dark);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  height: 48px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.test-btn {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
}

.test-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(33, 150, 243, 0.3);
}

.save-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* 测试结果卡片 */
.test-result-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  margin-top: 16px;
}

.test-result-card.success {
  background: rgba(76, 175, 80, 0.1);
  border: 2px solid #4CAF50;
}

.test-result-card.error {
  background: rgba(244, 67, 54, 0.1);
  border: 2px solid #F44336;
}

.result-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.test-result-card.success .result-icon {
  background: #4CAF50;
  color: white;
}

.test-result-card.error .result-icon {
  background: #F44336;
  color: white;
}

.result-content {
  flex: 1;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.test-result-card.success .result-title {
  color: #2E7D32;
}

.test-result-card.error .result-title {
  color: #C62828;
}

.result-message {
  font-size: 14px;
  color: var(--text-secondary);
}
/* 表单组 */
.form-group {
  margin-bottom: 12px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 12px;
  color: var(--text-primary);
}

.form-control {
  width: 100%;
  min-height: 38px;
  padding: 10px 12px;
  border: 1px solid var(--divider-color);
  border-radius: 8px;
  font-size: 13px;
  background: var(--card-background);
  color: var(--text-primary);
}

.form-control:focus {
  border-color: var(--primary-color);
  outline: none;
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
  background: var(--gradient-primary);
  color: white;
}

.btn-secondary {
  background: var(--divider-color);
  color: var(--text-primary);
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  border: 3px solid var(--divider-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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