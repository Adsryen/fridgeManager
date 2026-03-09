<template>
  <div class="register-page">
    <!-- 返回按钮 -->
    <div class="back-btn-wrapper">
      <button class="back-btn" @click="goBack">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>

    <!-- 主内容区 -->
    <div class="register-content">
      <!-- Logo区域 -->
      <div class="register-logo-section">
        <div class="register-logo-icon">
          <img src="/images/ice-box.png" alt="冰箱图标">
        </div>
        <h1 class="register-logo-title">冰箱里面还有啥</h1>
        <p class="register-logo-subtitle">创建新账号</p>
      </div>

      <!-- 表单区域 -->
      <div class="register-form-section">
        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" @submit.prevent="handleSubmit">
          <!-- 用户名 -->
          <el-form-item prop="username">
            <label class="register-form-label" for="username">
              <i class="fas fa-user"></i>
              <span>用户名</span>
              <span class="required-mark">*</span>
            </label>
            <div class="register-input-wrapper">
              <i class="fas fa-user register-input-icon"></i>
              <input
                v-model="registerForm.username"
                type="text"
                class="register-input"
                :class="{ valid: usernameValid, invalid: usernameInvalid }"
                id="username"
                placeholder="3-20个字符"
                autocomplete="username"
                @blur="validateUsername"
              />
            </div>
            <div v-if="usernameFeedback" class="field-feedback" :class="{ valid: usernameValid, invalid: usernameInvalid }">
              {{ usernameFeedback }}
            </div>
          </el-form-item>

          <!-- 邮箱 -->
          <el-form-item prop="email">
            <label class="register-form-label" for="email">
              <i class="fas fa-envelope"></i>
              <span>邮箱</span>
              <span class="required-mark">*</span>
            </label>
            <div class="register-input-wrapper">
              <i class="fas fa-envelope register-input-icon"></i>
              <input
                v-model="registerForm.email"
                type="email"
                class="register-input"
                :class="{ valid: emailValid, invalid: emailInvalid }"
                id="email"
                placeholder="your@email.com"
                autocomplete="email"
                @blur="validateEmail"
              />
            </div>
            <div v-if="emailFeedback" class="field-feedback" :class="{ valid: emailValid, invalid: emailInvalid }">
              {{ emailFeedback }}
            </div>
          </el-form-item>

          <!-- 密码 -->
          <el-form-item prop="password">
            <label class="register-form-label" for="password">
              <i class="fas fa-lock"></i>
              <span>密码</span>
              <span class="required-mark">*</span>
            </label>
            <div class="register-input-wrapper">
              <i class="fas fa-lock register-input-icon"></i>
              <input
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="register-input"
                id="password"
                placeholder="至少6个字符"
                autocomplete="new-password"
                @input="checkPasswordStrength"
                @focus="showPasswordRequirements = true"
              />
              <button type="button" class="toggle-password-btn" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <!-- 密码强度指示器 -->
            <div class="password-strength-bar">
              <div class="password-strength-fill" :class="passwordStrengthClass"></div>
            </div>
            <!-- 密码要求列表 -->
            <ul v-if="showPasswordRequirements && registerForm.password" class="password-requirements show">
              <li :class="{ valid: passwordChecks.length, invalid: !passwordChecks.length }">
                <i :class="passwordChecks.length ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                至少6个字符
              </li>
              <li :class="{ valid: passwordChecks.letter, invalid: !passwordChecks.letter }">
                <i :class="passwordChecks.letter ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                包含字母
              </li>
              <li :class="{ valid: passwordChecks.number, invalid: !passwordChecks.number }">
                <i :class="passwordChecks.number ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
                包含数字
              </li>
            </ul>
          </el-form-item>

          <!-- 确认密码 -->
          <el-form-item prop="confirmPassword">
            <label class="register-form-label" for="confirmPassword">
              <i class="fas fa-lock"></i>
              <span>确认密码</span>
              <span class="required-mark">*</span>
            </label>
            <div class="register-input-wrapper">
              <i class="fas fa-lock register-input-icon"></i>
              <input
                v-model="registerForm.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="register-input"
                :class="{ valid: confirmPasswordValid, invalid: confirmPasswordInvalid }"
                id="confirmPassword"
                placeholder="再次输入密码"
                autocomplete="new-password"
                @input="validateConfirmPassword"
              />
              <button type="button" class="toggle-password-btn" @click="showConfirmPassword = !showConfirmPassword">
                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <div v-if="confirmPasswordFeedback" class="field-feedback" :class="{ valid: confirmPasswordValid, invalid: confirmPasswordInvalid }">
              {{ confirmPasswordFeedback }}
            </div>
          </el-form-item>

          <button type="submit" class="register-submit-btn" :disabled="loading" @click="handleSubmit">
            <div v-if="loading" class="spinner"></div>
            <i v-else class="fas fa-user-plus"></i>
            <span>{{ loading ? '注册中...' : '注册' }}</span>
          </button>
        </el-form>

        <div class="register-login-link">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import * as authApi from '@/api/auth'

const router = useRouter()

// 表单引用
const registerFormRef = ref<FormInstance>()

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 自定义验证器
const validateUsernameRule = (_rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入用户名'))
  } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$/.test(value)) {
    callback(new Error('用户名必须是3-20个字符，只能包含字母、数字、下划线或中文'))
  } else {
    callback()
  }
}

const validateEmailRule = (_rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入邮箱'))
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('邮箱格式不正确'))
  } else {
    callback()
  }
}

const validatePasswordRule = (_rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码至少需要6个字符'))
  } else if (!/[a-zA-Z]/.test(value)) {
    callback(new Error('密码必须包含字母'))
  } else if (!/[0-9]/.test(value)) {
    callback(new Error('密码必须包含数字'))
  } else {
    callback()
  }
}

const validateConfirmPasswordRule = (_rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 注册表单验证规则
const registerRules: FormRules = {
  username: [
    { required: true, validator: validateUsernameRule, trigger: 'blur' }
  ],
  email: [
    { required: true, validator: validateEmailRule, trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePasswordRule, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPasswordRule, trigger: 'blur' }
  ]
}

// 状态
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const showPasswordRequirements = ref(false)

// 用户名验证状态
const usernameValid = ref(false)
const usernameInvalid = ref(false)
const usernameFeedback = ref('')

// 邮箱验证状态
const emailValid = ref(false)
const emailInvalid = ref(false)
const emailFeedback = ref('')

// 确认密码验证状态
const confirmPasswordValid = ref(false)
const confirmPasswordInvalid = ref(false)
const confirmPasswordFeedback = ref('')

// 密码强度检查
const passwordChecks = reactive({
  length: false,
  letter: false,
  number: false
})

// 密码强度等级
const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return 0

  let strength = 0
  if (password.length >= 6) strength++
  if (/[a-zA-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (password.length >= 10) strength++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++

  return strength
})

// 密码强度样式类
const passwordStrengthClass = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 2) return 'weak'
  if (strength <= 4) return 'medium'
  return 'strong'
})

// 返回上一页
const goBack = () => {
  router.push('/login')
}

// 验证用户名
const validateUsername = () => {
  const username = registerForm.username.trim()
  if (!username) {
    usernameValid.value = false
    usernameInvalid.value = false
    usernameFeedback.value = ''
    return
  }

  const pattern = /^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$/
  if (!pattern.test(username)) {
    usernameValid.value = false
    usernameInvalid.value = true
    usernameFeedback.value = '用户名必须是3-20个字符，只能包含字母、数字、下划线或中文'
  } else {
    usernameValid.value = true
    usernameInvalid.value = false
    usernameFeedback.value = '用户名格式正确'
  }
}

// 验证邮箱
const validateEmail = () => {
  const email = registerForm.email.trim()
  if (!email) {
    emailValid.value = false
    emailInvalid.value = false
    emailFeedback.value = ''
    return
  }

  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!pattern.test(email)) {
    emailValid.value = false
    emailInvalid.value = true
    emailFeedback.value = '邮箱格式不正确'
  } else {
    emailValid.value = true
    emailInvalid.value = false
    emailFeedback.value = '邮箱格式正确'
  }
}

// 检查密码强度
const checkPasswordStrength = () => {
  const password = registerForm.password

  passwordChecks.length = password.length >= 6
  passwordChecks.letter = /[a-zA-Z]/.test(password)
  passwordChecks.number = /[0-9]/.test(password)
}

// 验证确认密码
const validateConfirmPassword = () => {
  const confirmPassword = registerForm.confirmPassword
  if (!confirmPassword) {
    confirmPasswordValid.value = false
    confirmPasswordInvalid.value = false
    confirmPasswordFeedback.value = ''
    return
  }

  if (confirmPassword !== registerForm.password) {
    confirmPasswordValid.value = false
    confirmPasswordInvalid.value = true
    confirmPasswordFeedback.value = '两次输入的密码不一致'
  } else {
    confirmPasswordValid.value = true
    confirmPasswordInvalid.value = false
    confirmPasswordFeedback.value = '密码一致'
  }
}

// 处理注册提交
const handleSubmit = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
  } catch {
    return
  }

  const { username, email, password, confirmPassword } = registerForm

  // 基本验证
  if (!username.trim() || !email.trim() || !password || !confirmPassword) {
    ElMessage.warning('请填写所有必填字段')
    return
  }

  if (password !== confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  loading.value = true

  try {
    const response = await authApi.register(username.trim(), email.trim(), password)

    if (response.success) {
      ElMessage.success('注册成功！正在跳转...')
      setTimeout(() => {
        router.push('/login')
      }, 800)
    } else {
      ElMessage.error(response.error || '注册失败，请稍后重试')
    }
  } catch (error: any) {
    console.error('[注册] 注册失败', error)
    ElMessage.error(error.message || '网络连接失败，请检查网络或稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 注册页面专用样式 */
.register-page {
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
.register-content {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

/* Logo区域 */
.register-logo-section {
  text-align: center;
  padding: 32px 0 24px;
}

.register-logo-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 12px;
  animation: float 3s ease-in-out infinite;
}

.register-logo-icon img {
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

.register-logo-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.register-logo-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 表单区域 */
.register-form-section {
  flex: 1;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__content) {
  line-height: normal;
}

.register-form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.required-mark {
  color: var(--danger-color);
}

.register-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.register-input-icon {
  position: absolute;
  left: 16px;
  color: var(--text-secondary);
  font-size: 18px;
}

.register-input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-bg);
  color: var(--text-primary);
  transition: all 0.3s;
}

.register-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.register-input.valid {
  border-color: var(--success-color);
}

.register-input.invalid {
  border-color: var(--danger-color);
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

/* 密码强度指示器 */
.password-strength-bar {
  height: 4px;
  background: var(--border-color);
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.password-strength-fill {
  height: 100%;
  width: 0;
  transition: all 0.3s;
  border-radius: 2px;
}

.password-strength-fill.weak {
  width: 33%;
  background: var(--danger-color);
}

.password-strength-fill.medium {
  width: 66%;
  background: var(--warning-color);
}

.password-strength-fill.strong {
  width: 100%;
  background: var(--success-color);
}

/* 密码要求列表 */
.password-requirements {
  margin-top: 8px;
  padding: 12px;
  list-style: none;
  background: var(--card-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  display: none;
  animation: slideDown 0.3s ease-out;
}

.password-requirements.show {
  display: block;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.password-requirements li {
  font-size: 13px;
  color: var(--text-secondary);
  padding: 6px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.password-requirements li i {
  font-size: 14px;
  width: 16px;
  text-align: center;
}

.password-requirements li.valid {
  color: #10b981 !important;
}

.password-requirements li.valid i {
  color: #10b981 !important;
}

.password-requirements li.invalid {
  color: #ef4444 !important;
}

.password-requirements li.invalid i {
  color: #ef4444 !important;
}

/* 提示信息 */
.field-feedback {
  font-size: 12px;
  margin-top: 6px;
  display: block;
}

.field-feedback.valid {
  color: var(--success-color);
}

.field-feedback.invalid {
  color: var(--danger-color);
}

/* 注册按钮 */
.register-submit-btn {
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
  margin-top: 24px;
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

.register-submit-btn:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.register-submit-btn:active {
  transform: scale(0.98) translateY(0);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  animation: none;
}

.register-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  animation: none;
}

/* 登录链接 */
.register-login-link {
  text-align: center;
  margin-top: 20px;
  padding: 16px;
  font-size: 14px;
  color: var(--text-secondary);
}

.register-login-link a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.register-login-link a:active {
  opacity: 0.7;
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
</style>
