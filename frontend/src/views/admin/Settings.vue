<template>
  <div class="admin-settings">
    <div class="settings-header">
      <h1>系统设置</h1>
      <p class="subtitle">配置系统参数和 AI 功能</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>

    <div v-else class="settings-content">
      <el-form
        :model="settings"
        label-width="180px"
        label-position="left"
      >
        <!-- 基础设置 -->
        <div class="settings-section">
          <h2>基础设置</h2>
          
          <el-form-item label="会话超时时间（小时）">
            <el-input-number
              v-model="settings.session_timeout"
              :min="1"
              :max="168"
              :step="1"
            />
            <span class="form-hint">用户登录会话的有效时长</span>
          </el-form-item>

          <el-form-item label="每用户最大物品数">
            <el-input-number
              v-model="settings.max_items_per_user"
              :min="10"
              :max="10000"
              :step="10"
            />
            <span class="form-hint">单个用户可创建的最大物品数量</span>
          </el-form-item>

          <el-form-item label="默认过期提醒天数">
            <el-input-number
              v-model="settings.default_expiry_warning_days"
              :min="1"
              :max="30"
              :step="1"
            />
            <span class="form-hint">物品即将过期的提前提醒天数</span>
          </el-form-item>
        </div>

        <!-- AI 功能设置 -->
        <div class="settings-section">
          <h2>AI 功能设置</h2>

          <el-form-item label="启用 AI 功能">
            <el-switch v-model="settings.enable_ai_features" />
            <span class="form-hint">开启后可使用 OCR、对话助手等 AI 功能</span>
          </el-form-item>

          <template v-if="settings.enable_ai_features">
            <el-form-item label="OpenAI API 地址">
              <el-input
                v-model="settings.openai_api_base"
                placeholder="https://api.openai.com/v1"
              />
              <span class="form-hint">OpenAI 兼容的 API 基础地址</span>
            </el-form-item>

            <el-form-item label="OpenAI API 密钥">
              <el-input
                v-model="settings.openai_api_key"
                type="password"
                placeholder="sk-..."
                show-password
              />
              <span class="form-hint">用于调用 OpenAI API 的密钥</span>
            </el-form-item>

            <el-form-item label="对话模型">
              <div class="model-input-group">
                <el-input
                  v-model="settings.openai_chat_model"
                  placeholder="gpt-3.5-turbo"
                />
                <el-button
                  type="primary"
                  :loading="loadingModels"
                  @click="handleListModels"
                >
                  获取模型列表
                </el-button>
              </div>
              <span class="form-hint">用于 AI 对话的模型名称</span>
            </el-form-item>

            <el-form-item label="视觉模型">
              <el-input
                v-model="settings.openai_vision_model"
                placeholder="gpt-4-vision-preview"
              />
              <span class="form-hint">用于图像识别的模型名称</span>
            </el-form-item>

            <el-form-item label="语音模型">
              <el-input
                v-model="settings.openai_audio_model"
                placeholder="whisper-1"
              />
              <span class="form-hint">用于语音识别的模型名称</span>
            </el-form-item>

            <el-form-item label="测试连接">
              <el-button
                type="success"
                :loading="testingConnection"
                @click="handleTestConnection"
              >
                <i class="fas fa-plug"></i>
                测试 AI 连接
              </el-button>
              <span class="form-hint">验证 API 配置是否正确</span>
            </el-form-item>
          </template>
        </div>

        <!-- 操作按钮 -->
        <el-form-item>
          <el-button type="primary" size="large" :loading="saving" @click="handleSave">
            <i class="fas fa-save"></i>
            保存设置
          </el-button>
          <el-button size="large" @click="handleReset">
            <i class="fas fa-undo"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 模型列表对话框 -->
    <el-dialog
      v-model="modelsDialogVisible"
      title="可用模型列表"
      width="500px"
    >
      <el-table :data="availableModels" stripe max-height="400">
        <el-table-column prop="id" label="模型名称" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" @click="selectModel(row.id)">
              选择
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElSkeleton, ElForm, ElFormItem, ElInputNumber, ElSwitch, ElInput, ElButton, ElDialog, ElTable, ElTableColumn } from 'element-plus'
import * as adminApi from '@/api/admin'
import type { SystemSettings } from '@/types/models'

// 状态
const loading = ref(false)
const saving = ref(false)
const testingConnection = ref(false)
const loadingModels = ref(false)
const modelsDialogVisible = ref(false)

const settings = ref<SystemSettings>({
  session_timeout: 24,
  max_items_per_user: 1000,
  default_expiry_warning_days: 3,
  enable_ai_features: false,
  openai_api_base: '',
  openai_api_key: '',
  openai_chat_model: '',
  openai_vision_model: '',
  openai_audio_model: ''
})

const originalSettings = ref<SystemSettings | null>(null)
const availableModels = ref<Array<{ id: string }>>([])

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
    ElMessage.error('加载系统设置失败')
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
      ElMessage.success('设置保存成功')
      originalSettings.value = { ...settings.value }
    }
  } catch (_error) {
    ElMessage.error('保存设置失败')
  } finally {
    saving.value = false
  }
}

// 重置设置
function handleReset() {
  if (originalSettings.value) {
    settings.value = { ...originalSettings.value }
    ElMessage.info('已重置为上次保存的设置')
  }
}

// 测试 AI 连接
async function handleTestConnection() {
  if (!settings.value.openai_api_base || !settings.value.openai_api_key) {
    ElMessage.warning('请先填写 API 地址和密钥')
    return
  }

  testingConnection.value = true
  try {
    const response = await adminApi.testAIConnection(
      settings.value.openai_api_base,
      settings.value.openai_api_key
    )
    if (response.success) {
      ElMessage.success('AI 连接测试成功')
    }
  } catch (_error) {
    ElMessage.error('AI 连接测试失败，请检查配置')
  } finally {
    testingConnection.value = false
  }
}

// 获取模型列表
async function handleListModels() {
  if (!settings.value.openai_api_base || !settings.value.openai_api_key) {
    ElMessage.warning('请先填写 API 地址和密钥')
    return
  }

  loadingModels.value = true
  try {
    const response = await adminApi.listAIModels(
      settings.value.openai_api_base,
      settings.value.openai_api_key
    )
    if (response.success && response.data?.models) {
      availableModels.value = response.data.models.map((id: string) => ({ id }))
      modelsDialogVisible.value = true
    }
  } catch (_error) {
    ElMessage.error('获取模型列表失败')
  } finally {
    loadingModels.value = false
  }
}

// 选择模型
function selectModel(modelId: string) {
  settings.value.openai_chat_model = modelId
  modelsDialogVisible.value = false
  ElMessage.success(`已选择模型: ${modelId}`)
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.admin-settings {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.settings-header {
  margin-bottom: 30px;
}

.settings-header h1 {
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

.settings-content {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.settings-section {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid var(--border-color);
}

.settings-section:last-of-type {
  border-bottom: none;
}

.settings-section h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 24px 0;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.model-input-group {
  display: flex;
  gap: 12px;
  width: 100%;
}

.model-input-group .el-input {
  flex: 1;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

:deep(.el-input__inner),
:deep(.el-input-number__decrease),
:deep(.el-input-number__increase) {
  background: var(--bg-color);
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-switch.is-checked .el-switch__core) {
  background-color: var(--primary-color);
}

:deep(.el-button) {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .admin-settings {
    padding: 16px;
  }

  .settings-content {
    padding: 20px;
  }

  :deep(.el-form) {
    --el-form-label-font-size: 14px;
  }

  :deep(.el-form-item) {
    flex-direction: column;
  }

  :deep(.el-form-item__label) {
    text-align: left;
    margin-bottom: 8px;
  }

  .model-input-group {
    flex-direction: column;
  }
}
</style>
