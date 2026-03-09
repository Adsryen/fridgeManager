<template>
  <div class="login-page">
    <!-- 返回按钮 -->
    <div class="back-btn-wrapper">
      <button class="back-btn" @click="goBack">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>

    <!-- 主内容区 -->
    <div class="login-content">
      <!-- Logo区域 -->
      <div class="login-logo-section">
        <div class="login-logo-icon">
          <img src="/images/ice-box.png" alt="冰箱图标">
        </div>
        <h1 class="login-logo-title">冰箱里面还有啥</h1>
        <p class="login-logo-subtitle">欢迎回来</p>
      </div>

      <!-- 表单区域 -->
      <div class="login-form-section">
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleSubmit">
          <el-form-item prop="username">
            <label class="login-form-label" for="username">
              <i class="fas fa-user"></i>
              <span>用户名</span>
            </label>
            <div class="login-input-wrapper">
              <i class="fas fa-user login-input-icon"></i>
              <input
                v-model="loginForm.username"
                type="text"
                class="login-input"
                id="username"
                placeholder="请输入用户名"
                autocomplete="username"
                autofocus
              />
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <label class="login-form-label" for="password">
              <i class="fas fa-lock"></i>
              <span>密码</span>
            </label>
            <div class="login-input-wrapper">
              <i class="fas fa-lock login-input-icon"></i>
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="login-input"
                id="password"
                placeholder="请输入密码"
                autocomplete="current-password"
              />
              <button type="button" class="toggle-password-btn" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </el-form-item>

          <div class="login-remember">
            <div class="remember-checkbox">
              <input v-model="rememberMe" type="checkbox" id="rememberMe" />
              <label for="rememberMe">记住我</label>
            </div>
            <a href="#" class="forgot-password-link" @click.prevent="showForgotPassword">忘记密码？</a>
          </div>
        </el-form>

        <div class="login-buttons-container">
          <button type="submit" class="login-submit-btn" :disabled="loading" @click="handleSubmit">
            <div v-if="loading" class="spinner"></div>
            <i v-else class="fas fa-sign-in-alt"></i>
            <span>{{ loading ? '登录中...' : '登录' }}</span>
          </button>

          <div class="login-divider">
            <span>或</span>
          </div>

          <router-link to="/register" class="login-register-btn">
            <i class="fas fa-user-plus"></i>
            <span>注册账号</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <el-dialog
      v-model="forgotPasswordVisible"
      title="忘记密码"
      width="90%"
      :style="{ maxWidth: '400px' }"
    >
      <p class="forgot-password-desc">
        请输入您注册时使用的邮箱地址，我们将向您发送密码重置链接。
      </p>
      <el-form ref="forgotFormRef" :model="forgotForm" :rules="forgotRules">
        <el-form-item label="邮箱地址" prop="email">
          <el-input
            v-model="forgotForm.email"
            type="email"
            placeholder="请输入您的邮箱"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="forgotPasswordVisible = false">取消</el-button>
        <el-button type="primary" :loading="forgotLoading" @click="handleForgotPassword">
          发送重置链接
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import * as authApi from '@/api/auth'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref<FormInstance>()
const forgotFormRef = ref<FormInstance>()

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 登录表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 忘记密码表单数据
const forgotForm = reactive({
  email: ''
})

// 忘记密码表单验证规则
const forgotRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

// 状态
const loading = ref(false)
const showPassword = ref(false)
const rememberMe = ref(false)
const forgotPasswordVisible = ref(false)
const forgotLoading = ref(false)

// 返回上一页
const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}

// 显示忘记密码弹窗
const showForgotPassword = () => {
  forgotPasswordVisible.value = true
}

// 处理登录提交
const handleSubmit = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
  } catch {
    return
  }

  const { username, password } = loginForm

  if (!username.trim() || !password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true

  try {
    const response = await userStore.login(username.trim(), password)

    if (response.success) {
      // 记住用户名
      if (rememberMe.value) {
        localStorage.setItem('rememberedUsername', username.trim())
      } else {
        localStorage.removeItem('rememberedUsername')
      }

      ElMessage.success('登录成功！')

      // 跳转到原访问页面或首页
      const redirect = route.query.redirect as string
      setTimeout(() => {
        router.push(redirect || '/')
      }, 800)
    } else {
      ElMessage.error(response.error || '登录失败，请检查用户名和密码')
      loginForm.password = ''
    }
  } catch (error: any) {
    console.error('[登录] 登录失败', error)
    ElMessage.error(error.message || '网络连接失败，请检查网络或稍后重试')
    loginForm.password = ''
  } finally {
    loading.value = false
  }
}

// 处理忘记密码
const handleForgotPassword = async () => {
  if (!forgotFormRef.value) return

  try {
    await forgotFormRef.value.validate()
  } catch {
    return
  }

  forgotLoading.value = true

  try {
    const response = await authApi.forgotPassword(forgotForm.email)

    if (response.success) {
      ElMessage.success('密码重置链接已发送到您的邮箱')
      forgotPasswordVisible.value = false
      forgotForm.email = ''
    } else {
      ElMessage.error(response.error || '发送失败，请稍后重试')
    }
  } catch (error: any) {
    console.error('[忘记密码] 发送失败', error)
    ElMessage.error('网络错误，请检查网络连接')
  } finally {
    forgotLoading.value = false
  }
}

// 初始化
onMounted(() => {
  // 从 localStorage 读取记住的用户名
  const rememberedUsername = localStorage.getItem('rememberedUsername')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    rememberMe.value = true
  }
})
</script>

<style scoped>
/* 登录页面专用样式 */
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--bg-color);
}

/* 返回按钮 */
.back-btn-wrapper {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

.back-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--card-bg);
  border: none;
  color: var(--text-primary);
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-btn:active {
  transform: scale(0.95);
  background: var(--hover-bg);
}

/* 主内容区 */
.login-content {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

/* Logo区域 */
.login-logo-section {
  text-align: center;
  padding: 40px 0 32px;
}

.login-logo-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  animation: float 3s ease-in-out infinite;
}

.login-logo-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.login-logo-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.login-logo-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 表单区域 */
.login-form-section {
  flex: 1;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__content) {
  line-height: normal;
}

.login-form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.login-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.login-input-icon {
  position: absolute;
  left: 16px;
  color: var(--text-secondary);
  font-size: 18px;
}

.login-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-bg);
  color: var(--text-primary);
  transition: all 0.3s;
}

.login-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.toggle-password-btn {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 18px;
  padding: 8px;
  cursor: pointer;
  transition: color 0.3s;
}

.toggle-password-btn:active {
  color: var(--primary-color);
}

/* 记住我 */
.login-remember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-remember input[type='checkbox'] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--primary-color);
}

.login-remember label {
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
}

.forgot-password-link {
  font-size: 14px;
  color: var(--primary-color);
  text-decoration: none;
  transition: opacity 0.3s;
}

.forgot-password-link:hover {
  opacity: 0.8;
}

/* 按钮容器 */
.login-buttons-container {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-top: 8px;
}

/* 登录按钮 */
.login-submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  animation: floatButton 3s ease-in-out infinite;
}

@keyframes floatButton {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.login-submit-btn:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.login-submit-btn:active {
  transform: scale(0.98) translateY(0);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  animation: none;
}

.login-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  animation: none;
}

/* 分隔线 */
.login-divider {
  display: flex;
  align-items: center;
  margin: 16px 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.login-divider span {
  padding: 0 12px;
}

/* 注册按钮 */
.login-register-btn {
  width: 100%;
  padding: 16px;
  background: var(--bg-color);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  animation: floatButton 3s ease-in-out infinite 0.5s;
}

.login-register-btn:hover {
  background: var(--hover-bg);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-register-btn:active {
  transform: scale(0.98) translateY(0);
  background: var(--hover-bg);
  border-color: var(--primary-color);
  animation: none;
}

/* 加载动画 */
.spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 忘记密码弹窗 */
.forgot-password-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.5;
}
</style>
