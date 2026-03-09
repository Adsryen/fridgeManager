<template>
  <div class="family-page">
    <!-- 页面头部 -->
    <div class="family-header">
      <div class="family-header-content">
        <div class="family-title">
          <i class="fas fa-users"></i>
          <h1>家庭管理</h1>
        </div>
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i>
        </button>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="family-container">
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="action-btn primary" @click="showCreateDialog">
          <i class="fas fa-plus"></i>
          <span>创建家庭</span>
        </button>
        <button class="action-btn success" @click="showJoinDialog">
          <i class="fas fa-sign-in-alt"></i>
          <span>加入家庭</span>
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="familyStore.loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>

      <!-- 家庭列表 -->
      <div v-else-if="familyStore.families.length > 0" class="family-grid">
        <FamilyCard
          v-for="family in familyStore.families"
          :key="family._id"
          :family="family"
          @view-detail="handleViewDetail"
          @leave="handleLeave"
          @delete="handleDelete"
        />
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <i class="fas fa-users"></i>
        <p>您还没有加入任何家庭</p>
        <p class="empty-hint">创建一个家庭或加入现有家庭开始使用</p>
      </div>
    </div>

    <!-- 创建家庭对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建家庭"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="80px"
      >
        <el-form-item label="家庭名称" prop="name">
          <el-input
            v-model="createForm.name"
            placeholder="请输入家庭名称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreate">
          创建
        </el-button>
      </template>
    </el-dialog>

    <!-- 加入家庭对话框 -->
    <el-dialog
      v-model="joinDialogVisible"
      title="加入家庭"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="joinFormRef"
        :model="joinForm"
        :rules="joinRules"
        label-width="80px"
      >
        <el-form-item label="家庭编号" prop="code">
          <el-input
            v-model="joinForm.code"
            placeholder="请输入6位家庭编号"
            maxlength="6"
            @input="joinForm.code = joinForm.code.toUpperCase()"
          />
          <template #extra>
            <span class="form-hint">请向家庭创建者索取家庭编号</span>
          </template>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="joinDialogVisible = false">取消</el-button>
        <el-button type="success" :loading="joining" @click="handleJoin">
          加入
        </el-button>
      </template>
    </el-dialog>

    <!-- 家庭详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="currentFamily?.name"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-tabs v-model="activeTab">
        <el-tab-pane label="成员" name="members">
          <MemberList
            v-if="currentFamily"
            :family-id="currentFamily._id"
            :members="familyStore.members"
            :loading="familyStore.loading"
            @remove="handleRemoveMember"
          />
        </el-tab-pane>
        <el-tab-pane label="共享冰箱" name="fridges">
          <div v-if="activeTab === 'fridges'">
            <SharedFridgeList
              v-if="currentFamily"
              :family-id="currentFamily._id"
            />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useFamilyStore } from '@/stores/family'
import FamilyCard from '@/components/family/FamilyCard.vue'
import MemberList from '@/components/family/MemberList.vue'
import SharedFridgeList from '@/components/family/SharedFridgeList.vue'
import type { Family } from '@/types/models'

const router = useRouter()
const familyStore = useFamilyStore()

// 对话框状态
const createDialogVisible = ref(false)
const joinDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const activeTab = ref('members')

// 表单引用
const createFormRef = ref<FormInstance>()
const joinFormRef = ref<FormInstance>()

// 表单数据
const createForm = ref({
  name: ''
})

const joinForm = ref({
  code: ''
})

// 表单验证规则
const createRules: FormRules = {
  name: [
    { required: true, message: '请输入家庭名称', trigger: 'blur' },
    { min: 1, max: 50, message: '家庭名称长度在 1 到 50 个字符', trigger: 'blur' }
  ]
}

const joinRules: FormRules = {
  code: [
    { required: true, message: '请输入家庭编号', trigger: 'blur' },
    { len: 6, message: '家庭编号应为6位', trigger: 'blur' }
  ]
}

// 加载状态
const creating = ref(false)
const joining = ref(false)

// 当前家庭
const currentFamily = ref<Family | null>(null)

// 返回首页
const goBack = () => {
  router.push('/')
}

// 显示创建对话框
const showCreateDialog = () => {
  createForm.value.name = ''
  createDialogVisible.value = true
}

// 显示加入对话框
const showJoinDialog = () => {
  joinForm.value.code = ''
  joinDialogVisible.value = true
}

// 创建家庭
const handleCreate = async () => {
  if (!createFormRef.value) return

  await createFormRef.value.validate(async (valid) => {
    if (!valid) return

    creating.value = true
    try {
      const response = await familyStore.createFamily(createForm.value.name)
      if (response.success && response.data) {
        ElMessage.success(`家庭创建成功！家庭编号: ${response.data.family_code}`)
        createDialogVisible.value = false
        createForm.value.name = ''
      } else {
        ElMessage.error(response.error || '创建失败')
      }
    } catch (_error) {
      ElMessage.error('创建家庭失败')
    } finally {
      creating.value = false
    }
  })
}

// 加入家庭
const handleJoin = async () => {
  if (!joinFormRef.value) return

  await joinFormRef.value.validate(async (valid) => {
    if (!valid) return

    joining.value = true
    try {
      const response = await familyStore.joinFamily(joinForm.value.code)
      if (response.success) {
        ElMessage.success('成功加入家庭！')
        joinDialogVisible.value = false
        joinForm.value.code = ''
      } else {
        ElMessage.error(response.error || '加入失败')
      }
    } catch (_error) {
      ElMessage.error('加入家庭失败')
    } finally {
      joining.value = false
    }
  })
}

// 查看家庭详情
const handleViewDetail = async (family: Family) => {
  currentFamily.value = family
  activeTab.value = 'members'
  detailDialogVisible.value = true
  
  // 加载成员列表
  await familyStore.loadMembers(family._id)
}

// 离开家庭
const handleLeave = async (familyId: string) => {
  try {
    await ElMessageBox.confirm(
      '确定要离开这个家庭吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await familyStore.leaveFamily(familyId)
    if (response.success) {
      ElMessage.success('已离开家庭')
    } else {
      ElMessage.error(response.error || '操作失败')
    }
  } catch (_error) {
    // 用户取消操作
  }
}

// 删除家庭
const handleDelete = async (familyId: string) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个家庭吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error'
      }
    )

    const response = await familyStore.deleteFamily(familyId)
    if (response.success) {
      ElMessage.success('家庭已删除')
    } else {
      ElMessage.error(response.error || '删除失败')
    }
  } catch (_error) {
    // 用户取消操作
  }
}

// 移除成员
const handleRemoveMember = async (userId: string) => {
  if (!currentFamily.value) return

  try {
    await ElMessageBox.confirm(
      '确定要移除该成员吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await familyStore.removeMember(currentFamily.value._id, userId)
    if (response.success) {
      ElMessage.success('成员已移除')
    } else {
      ElMessage.error(response.error || '操作失败')
    }
  } catch (_error) {
    // 用户取消操作
  }
}

// 页面加载时获取家庭列表
onMounted(async () => {
  await familyStore.loadFamilies()
})
</script>

<style scoped>
/* 家庭管理页面样式 */
.family-page {
  min-height: 100vh;
  background: var(--bg-color);
  padding-bottom: 80px;
}

.family-header {
  background: var(--card-bg);
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.family-header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.family-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.family-title i {
  font-size: 24px;
  color: var(--theme-color-2);
}

.family-title h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--bg-color);
  border: none;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn:hover {
  transform: scale(1.05);
  background: var(--hover-bg);
}

.family-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 150px;
  padding: 16px 24px;
  border-radius: 16px;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.action-btn.primary {
  background: linear-gradient(135deg, var(--theme-color-2), var(--theme-color-3));
  color: white;
}

.action-btn.success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.action-btn:active {
  transform: translateY(0);
}

.loading-state {
  padding: 40px 20px;
}

.family-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

.empty-hint {
  margin-top: 8px;
  font-size: 14px;
}

.form-hint {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 768px) {
  .family-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>
