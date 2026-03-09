<template>
  <div class="admin-users">
    <div class="users-header">
      <h1>用户管理</h1>
      <p class="subtitle">管理所有系统用户</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else class="users-content">
      <!-- 用户列表 -->
      <el-table :data="users" stripe style="width: 100%">
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '激活' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_admin ? 'warning' : 'info'" size="small">
              {{ row.is_admin ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="300">
          <template #default="{ row }">
            <el-button
              size="small"
              :type="row.is_active ? 'warning' : 'success'"
              @click="handleToggleStatus(row)"
            >
              {{ row.is_active ? '禁用' : '激活' }}
            </el-button>
            <el-button
              size="small"
              :type="row.is_admin ? 'info' : 'warning'"
              @click="handleToggleAdmin(row)"
            >
              {{ row.is_admin ? '取消管理员' : '设为管理员' }}
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleResetPassword(row)"
            >
              重置密码
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDeleteUser(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPasswordDialogVisible"
      title="重置用户密码"
      width="400px"
    >
      <el-form :model="resetPasswordForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input :model-value="currentUser?.username" disabled />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input
            v-model="resetPasswordForm.password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetPasswordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmResetPassword">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox, ElTable, ElTableColumn, ElTag, ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElSkeleton } from 'element-plus'
import * as adminApi from '@/api/admin'
import type { User } from '@/types/models'

// 状态
const loading = ref(false)
const users = ref<User[]>([])
const resetPasswordDialogVisible = ref(false)
const currentUser = ref<User | null>(null)
const resetPasswordForm = ref({
  password: ''
})

// 格式化日期
function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载用户列表
async function loadUsers() {
  loading.value = true
  try {
    const response = await adminApi.getAllUsers()
    if (response.success && response.data) {
      users.value = response.data
    }
  } catch (_error) {
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 切换用户状态
async function handleToggleStatus(user: User) {
  try {
    await ElMessageBox.confirm(
      `确定要${user.is_active ? '禁用' : '激活'}用户 ${user.username} 吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await adminApi.toggleUserStatus(user._id)
    if (response.success) {
      ElMessage.success(`${user.is_active ? '禁用' : '激活'}成功`)
      await loadUsers()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

// 切换管理员权限
async function handleToggleAdmin(user: User) {
  try {
    await ElMessageBox.confirm(
      `确定要${user.is_admin ? '取消' : '设置'}用户 ${user.username} 的管理员权限吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await adminApi.toggleAdminStatus(user._id)
    if (response.success) {
      ElMessage.success(`${user.is_admin ? '取消' : '设置'}管理员权限成功`)
      await loadUsers()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

// 打开重置密码对话框
function handleResetPassword(user: User) {
  currentUser.value = user
  resetPasswordForm.value.password = ''
  resetPasswordDialogVisible.value = true
}

// 确认重置密码
async function confirmResetPassword() {
  if (!resetPasswordForm.value.password) {
    ElMessage.warning('请输入新密码')
    return
  }

  if (resetPasswordForm.value.password.length < 6) {
    ElMessage.warning('密码长度至少为 6 位')
    return
  }

  try {
    const response = await adminApi.resetUserPassword(
      currentUser.value!._id,
      resetPasswordForm.value.password
    )
    if (response.success) {
      ElMessage.success('密码重置成功')
      resetPasswordDialogVisible.value = false
    }
  } catch (_error) {
    ElMessage.error('密码重置失败')
  }
}

// 删除用户
async function handleDeleteUser(user: User) {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 ${user.username} 吗？此操作不可恢复！`,
      '危险操作',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )

    const response = await adminApi.deleteUser(user._id)
    if (response.success) {
      ElMessage.success('用户删除成功')
      await loadUsers()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.admin-users {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.users-header {
  margin-bottom: 30px;
}

.users-header h1 {
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

.users-content {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-table) {
  background: transparent;
  color: var(--text-primary);
}

:deep(.el-table th) {
  background: var(--bg-color);
  color: var(--text-primary);
}

:deep(.el-table tr) {
  background: transparent;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: var(--bg-color);
}

:deep(.el-table td),
:deep(.el-table th) {
  border-color: var(--border-color);
}

@media (max-width: 768px) {
  .admin-users {
    padding: 16px;
  }

  .users-content {
    padding: 12px;
    overflow-x: auto;
  }
}
</style>
