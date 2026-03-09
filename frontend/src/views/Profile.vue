<template>
  <div class="profile-page">
    <!-- 顶部导航栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <button class="icon-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i>
        </button>
        <div class="app-name">个人资料</div>
        <div style="width: 32px"></div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="profile-content">
      <!-- 用户信息卡片 -->
      <div class="user-card">
        <div class="user-avatar-large">
          <i class="fas fa-user"></i>
        </div>
        <div class="user-info">
          <div class="user-name">{{ user?.username }}</div>
          <div class="user-email">{{ user?.email }}</div>
          <div class="user-meta">
            <span v-if="user?.is_admin" class="badge-admin">
              <i class="fas fa-crown"></i> 管理员
            </span>
            <span class="user-join-date">
              注册于 {{ formatDate(user?.created_at) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 编辑个人资料 -->
      <div class="section">
        <div class="section-title">
          <i class="fas fa-user-edit"></i>
          <span>编辑资料</span>
        </div>
        <el-form ref="profileFormRef" :model="profileForm" :rules="profileRules" label-position="top">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="profileForm.username" disabled>
              <template #prefix>
                <i class="fas fa-user"></i>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="profileForm.email" type="email">
              <template #prefix>
                <i class="fas fa-envelope"></i>
              </template>
            </el-input>
          </el-form-item>
          <el-button type="primary" @click="handleUpdateProfile" :loading="profileLoading" size="large" style="width: 100%">
            保存修改
          </el-button>
        </el-form>
      </div>

      <!-- 修改密码 -->
      <div class="section">
        <div class="section-title">
          <i class="fas fa-lock"></i>
          <span>修改密码</span>
        </div>
        <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top">
          <el-form-item label="当前密码" prop="oldPassword">
            <el-input v-model="passwordForm.oldPassword" type="password" show-password>
              <template #prefix>
                <i class="fas fa-key"></i>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" type="password" show-password>
              <template #prefix>
                <i class="fas fa-lock"></i>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" type="password" show-password>
              <template #prefix>
                <i class="fas fa-lock"></i>
              </template>
            </el-input>
          </el-form-item>
          <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading" size="large" style="width: 100%">
            修改密码
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import * as authApi from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

// 计算属性
const user = computed(() => userStore.user)

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

// 个人资料表单
const profileForm = reactive({
  username: '',
  email: ''
})

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 加载状态
const profileLoading = ref(false)
const passwordLoading = ref(false)

// 表单验证规则
const profileRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const passwordRules: FormRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 格式化日期
const formatDate = (dateStr?: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 更新个人资料
const handleUpdateProfile = async () => {
  if (!profileFormRef.value) return

  try {
    await profileFormRef.value.validate()
  } catch {
    return
  }

  profileLoading.value = true

  try {
    const response = await authApi.updateProfile({
      email: profileForm.email
    })

    if (response.success) {
      ElMessage.success('个人资料更新成功')
      // 重新获取用户信息
      await userStore.fetchProfile()
    } else {
      ElMessage.error(response.error || '更新失败')
    }
  } catch (error: any) {
    console.error('[个人资料] 更新失败', error)
    ElMessage.error(error.message || '网络错误，请稍后重试')
  } finally {
    profileLoading.value = false
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
  } catch {
    return
  }

  passwordLoading.value = true

  try {
    const response = await authApi.changePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword
    )

    if (response.success) {
      ElMessage.success('密码修改成功')
      // 清空表单
      passwordFormRef.value?.resetFields()
    } else {
      ElMessage.error(response.error || '修改失败')
    }
  } catch (error: any) {
    console.error('[个人资料] 修改密码失败', error)
    ElMessage.error(error.message || '网络错误，请稍后重试')
  } finally {
    passwordLoading.value = false
  }
}

// 初始化
onMounted(async () => {
  const currentUser = user.value
  if (currentUser) {
    profileForm.username = currentUser.username
    profileForm.email = currentUser.email
  } else {
    // 如果没有用户信息，尝试获取
    try {
      await userStore.fetchProfile()
      const fetchedUser = userStore.user
      if (fetchedUser) {
        profileForm.username = fetchedUser.username
        profileForm.email = fetchedUser.email
      }
    } catch (error) {
      console.error('[个人资料] 获取用户信息失败', error)
      ElMessage.error('获取用户信息失败')
      router.push('/login')
    }
  }
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: var(--bg-color);
}

/* 顶部导航栏 */
.mobile-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 48px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  height: 100%;
}

.icon-btn {
  background: rgba(0, 0, 0, 0.2);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: white;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-btn:active {
  transform: scale(0.95);
  background: rgba(0, 0, 0, 0.3);
}

.app-name {
  font-size: 16px;
  font-weight: 600;
}

/* 主内容区 */
.profile-content {
  padding-top: 48px;
  padding-bottom: 24px;
}

/* 用户信息卡片 */
.user-card {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: white;
}

.user-avatar-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.user-info {
  text-align: center;
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.user-email {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 12px;
}

.user-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.badge-admin {
  padding: 4px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  font-size: 12px;
  font-weight: 600;
}

.user-join-date {
  font-size: 12px;
  opacity: 0.8;
}

/* 区块 */
.section {
  background: var(--card-bg);
  margin: 16px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--border-color);
}

.section-title i {
  color: var(--primary-color);
}

/* 表单样式 */
:deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  padding: 12px 16px;
}

:deep(.el-input__prefix) {
  color: var(--text-secondary);
  font-size: 16px;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 600;
}

/* 响应式布局 */
@media (min-width: 769px) {
  .profile-page {
    max-width: 768px;
    margin: 0 auto;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }
}
</style>
