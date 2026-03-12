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
                @keyup.enter="focusPassword"
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
                @keyup.enter="handleSubmit"
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
  router.push('/profile')
}

// 聚焦到密码输入框
const focusPassword = () => {
  const passwordInput = document.getElementById('password') as HTMLInputElement
  if (passwordInput) {
    passwordInput.focus()
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
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--bg-color);
  position: relative;
  overflow: hidden;
}

.login-page::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--theme-color-1) 0%, transparent 70%);
  opacity: 0.15;
  border-radius: 50%;
  pointer-events: none;
}

.login-page::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, var(--theme-color-2) 0%, transparent 70%);
  opacity: 0.12;
  border-radius: 50%;
  pointer-events: none;
}

/* 返回按钮 */
.back-btn-wrapper {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1000;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
}

.back-btn:active {
  transform: scale(0.95);
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* 主内容区 */
.login-content {
  flex: 1;
  padding: 80px 20px 40px;
  display: flex;
  flex-direction: column;
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

/* Logo区域 */
.login-logo-section {
  text-align: center;
  padding: 0 0 32px;
  margin-bottom: 8px;
  flex-shrink: 0;
}

.login-logo-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 12px var(--theme-color-1));
  opacity: 0.95;
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
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.login-logo-subtitle {
  font-size: 15px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* 表单区域 */
.login-form-section {
  background: var(--card-bg);
  border-radius: 24px;
  padding: 32px 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__content) {
  line-height: normal;
}

.login-form-label {
  display: none;
}

.login-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.login-input-icon {
  position: absolute;
  left: 18px;
  color: var(--text-secondary);
  font-size: 18px;
  z-index: 1;
}

.login-input {
  width: 100%;
  padding: 16px 50px 16px 52px;
  border: 2px solid var(--border-color);
  border-radius: 14px;
  font-size: 15px;
  background: var(--bg-color);
  color: var(--text-primary);
  transition: all 0.3s ease;
  font-weight: 400;
}

.login-input::placeholder {
  color: var(--text-secondary);
  opacity: 0.6;
}

.login-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: var(--card-bg);
  box-shadow: 0 0 0 4px var(--theme-color-1);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--primary-color) 15%, transparent);
  transform: translateY(-1px);
}

.toggle-password-btn {
  position: absolute;
  right: 14px;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 18px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 1;
  border-radius: 8px;
}

.toggle-password-btn:hover {
  background: color-mix(in srgb, var(--primary-color) 10%, transparent);
}

.toggle-password-btn:active {
  color: var(--primary-color);
  transform: scale(0.95);
  background: color-mix(in srgb, var(--primary-color) 15%, transparent);
}

/* 记住我 */
.login-remember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  padding: 0 4px;
}

.remember-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-remember input[type='checkbox'] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary-color);
  border-radius: 4px;
}

.login-remember label {
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
  font-weight: 500;
}

.forgot-password-link {
  font-size: 14px;
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.3s;
  font-weight: 600;
}

.forgot-password-link:active {
  opacity: 0.7;
  color: var(--secondary-color);
}

/* 按钮容器 */
.login-buttons-container {
  margin-top: 0;
}

/* 登录按钮 */
.login-submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, var(--header-bg-start) 0%, var(--header-bg-end) 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 6px 20px color-mix(in srgb, var(--primary-color) 35%, transparent);
  letter-spacing: 0.3px;
}

.login-submit-btn:hover {
  box-shadow: 0 8px 24px color-mix(in srgb, var(--primary-color) 45%, transparent);
  transform: translateY(-2px);
  filter: brightness(1.05);
}

.login-submit-btn:active {
  transform: scale(0.98) translateY(0);
  box-shadow: 0 4px 12px color-mix(in srgb, var(--primary-color) 30%, transparent);
  filter: brightness(0.95);
}

.login-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 分隔线 */
.login-divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
}

.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--border-color), transparent);
}

.login-divider span {
  padding: 0 16px;
  color: var(--text-secondary);
  opacity: 0.8;
}

/* 注册按钮 */
.login-register-btn {
  width: 100%;
  padding: 16px;
  background: var(--bg-color);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-decoration: none;
  letter-spacing: 0.3px;
}

.login-register-btn:hover {
  background: var(--card-bg);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  color: var(--primary-color);
}

.login-register-btn:active {
  transform: scale(0.98) translateY(0);
  background: var(--bg-color);
  border-color: var(--secondary-color);
  color: var(--secondary-color);
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
  line-height: 1.6;
}

/* 响应式优化 */
@media (max-width: 480px) {
  .login-content {
    padding: 70px 16px 32px;
  }

  .login-form-section {
    padding: 28px 20px;
    border-radius: 20px;
  }

  .login-logo-title {
    font-size: 24px;
  }

  .login-logo-icon {
    width: 80px;
    height: 80px;
  }

  .login-logo-section {
    padding: 0 0 24px;
  }
}

@media (max-height: 600px) {
  .login-content {
    padding: 70px 20px 32px;
  }

  .login-logo-section {
    padding: 0 0 20px;
  }

  .login-logo-icon {
    width: 70px;
    height: 70px;
    margin-bottom: 12px;
  }

  .login-logo-title {
    font-size: 22px;
  }

  .login-form-section {
    padding: 24px 20px;
  }
}

@media (min-height: 800px) {
  .login-content {
    padding: 100px 20px 40px;
  }

  .login-logo-section {
    padding: 20px 0 48px;
  }
}
</style>
