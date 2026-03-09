<template>
  <div class="family-page">
    <!-- 顶部导航栏 -->
    <div class="mobile-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="app-name">家庭管理</div>
        </div>
        <div class="header-right">
          <button class="icon-btn" @click="toggleDarkMode" title="切换深色模式">
            <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="mobile-content">
      <div class="family-content">
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button class="action-btn primary" @click="showCreateForm = true">
            <i class="fas fa-plus"></i>
            <span>创建家庭</span>
          </button>
          <button class="action-btn success" @click="showJoinForm = true">
            <i class="fas fa-sign-in-alt"></i>
            <span>加入家庭</span>
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="familyStore.loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 家庭列表 -->
        <div v-else-if="familyStore.families.length > 0" class="family-list">
          <div
            v-for="family in familyStore.families"
            :key="family._id"
            class="family-card"
          >
            <div class="family-card-header">
              <div class="family-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="family-info">
                <div class="family-name">{{ family.name }}</div>
                <div class="family-meta">
                  <span v-if="family.owner_id === userStore.user?._id" class="owner-badge">
                    <i class="fas fa-crown"></i> 所有者
                  </span>
                  <span class="member-count">
                    <i class="fas fa-user"></i> {{ family.member_count }} 人
                  </span>
                </div>
              </div>
            </div>
            <div class="family-card-body">
              <div class="family-code">
                <span class="label">家庭编号:</span>
                <span class="code">{{ family.family_code }}</span>
                <button class="copy-btn" @click="copyCode(family.family_code)" title="复制">
                  <i class="fas fa-copy"></i>
                </button>
              </div>
              <div class="family-actions">
                <button class="btn-secondary" @click="viewMembers(family)">
                  <i class="fas fa-users"></i> 查看成员
                </button>
                <button
                  v-if="family.owner_id === userStore.user?._id"
                  class="btn-danger"
                  @click="deleteFamily(family)"
                >
                  <i class="fas fa-trash"></i> 解散
                </button>
                <button v-else class="btn-danger" @click="leaveFamily(family)">
                  <i class="fas fa-sign-out-alt"></i> 退出
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-state">
          <i class="fas fa-users"></i>
          <h4>还没有家庭</h4>
          <p>创建一个家庭或加入现有家庭开始使用</p>
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <div class="mobile-bottom-nav">
      <button class="nav-item" @click="$router.push('/')">
        <i class="fas fa-home"></i>
        <span>首页</span>
      </button>
      <button class="nav-item" @click="$router.push('/fridge')">
        <i class="fas fa-snowflake"></i>
        <span>冰箱</span>
      </button>
      <button class="nav-item add-btn" @click="$router.push('/')">
        <div class="add-icon">
          <i class="fas fa-plus"></i>
        </div>
      </button>
      <button class="nav-item active">
        <i class="fas fa-users"></i>
        <span>家庭</span>
      </button>
      <button class="nav-item" @click="$router.push('/profile')">
        <i class="fas fa-user"></i>
        <span>我的</span>
        <span v-if="!userStore.isLoggedIn" class="nav-badge guest">游客</span>
        <span v-else-if="userStore.isAdmin" class="nav-badge admin">管理员</span>
        <span v-else class="nav-badge user">私人</span>
      </button>
    </div>

    <!-- 创建家庭抽屉 -->
    <Drawer v-model="showCreateForm" title="创建家庭">
      <div class="form-content">
        <div class="form-group">
          <label><i class="fas fa-users"></i> 家庭名称</label>
          <input
            v-model="createForm.name"
            type="text"
            class="mobile-input"
            placeholder="请输入家庭名称"
            maxlength="50"
          />
        </div>
        <div class="form-actions">
          <button class="btn-secondary" @click="showCreateForm = false">取消</button>
          <button class="btn-primary" :disabled="creating" @click="handleCreate">
            <i class="fas fa-check"></i>
            {{ creating ? '创建中...' : '创建' }}
          </button>
        </div>
      </div>
    </Drawer>

    <!-- 加入家庭抽屉 -->
    <Drawer v-model="showJoinForm" title="加入家庭">
      <div class="form-content">
        <div class="form-group">
          <label><i class="fas fa-key"></i> 家庭编号</label>
          <input
            v-model="joinForm.code"
            type="text"
            class="mobile-input"
            placeholder="请输入6位家庭编号"
            maxlength="6"
          />
        </div>
        <div class="form-actions">
          <button class="btn-secondary" @click="showJoinForm = false">取消</button>
          <button class="btn-primary" :disabled="joining" @click="handleJoin">
            <i class="fas fa-check"></i>
            {{ joining ? '加入中...' : '加入' }}
          </button>
        </div>
      </div>
    </Drawer>

    <!-- 成员列表抽屉 -->
    <Drawer v-model="showMemberList" title="家庭成员">
      <MemberList
        v-if="currentFamily"
        :family-id="currentFamily._id"
        :members="[]"
      />
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFamilyStore } from '../stores/family'
import { useUserStore } from '../stores/user'
import { useTheme } from '../composables/useTheme'
import Drawer from '../components/common/Drawer.vue'
import MemberList from '../components/family/MemberList.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Family } from '../types/models'

const familyStore = useFamilyStore()
const userStore = useUserStore()
const { isDark, toggleTheme } = useTheme()

const showCreateForm = ref(false)
const showJoinForm = ref(false)
const showMemberList = ref(false)
const creating = ref(false)
const joining = ref(false)
const currentFamily = ref<Family | null>(null)

const createForm = ref({
  name: ''
})

const joinForm = ref({
  code: ''
})

const toggleDarkMode = () => {
  toggleTheme()
}

const copyCode = async (code: string) => {
  try {
    await navigator.clipboard.writeText(code)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}

const viewMembers = (family: Family) => {
  currentFamily.value = family
  showMemberList.value = true
}

const handleCreate = async () => {
  if (!createForm.value.name) {
    ElMessage.error('请输入家庭名称')
    return
  }

  creating.value = true
  try {
    await familyStore.createFamily(createForm.value.name)
    ElMessage.success('创建成功')
    showCreateForm.value = false
    createForm.value.name = ''
    await familyStore.loadFamilies()
  } catch (error: any) {
    ElMessage.error(error.message || '创建失败')
  } finally {
    creating.value = false
  }
}

const handleJoin = async () => {
  if (!joinForm.value.code) {
    ElMessage.error('请输入家庭编号')
    return
  }

  if (joinForm.value.code.length !== 6) {
    ElMessage.error('家庭编号应为6位')
    return
  }

  joining.value = true
  try {
    await familyStore.joinFamily(joinForm.value.code)
    ElMessage.success('加入成功')
    showJoinForm.value = false
    joinForm.value.code = ''
    await familyStore.loadFamilies()
  } catch (error: any) {
    ElMessage.error(error.message || '加入失败')
  } finally {
    joining.value = false
  }
}

const deleteFamily = async (family: Family) => {
  try {
    await ElMessageBox.confirm(
      `确定要解散家庭"${family.name}"吗？解散后所有成员将被移除。`,
      '确认解散',
      {
        confirmButtonText: '解散',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await familyStore.deleteFamily(family._id)
    ElMessage.success('解散成功')
    await familyStore.loadFamilies()
  } catch {
    // 用户取消
  }
}

const leaveFamily = async (family: Family) => {
  try {
    await ElMessageBox.confirm(
      `确定要退出家庭"${family.name}"吗？`,
      '确认退出',
      {
        confirmButtonText: '退出',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await familyStore.leaveFamily(family._id)
    ElMessage.success('退出成功')
    await familyStore.loadFamilies()
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  familyStore.loadFamilies()
})
</script>

<style scoped>
.family-page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.family-content {
  padding: 20px;
  padding-bottom: 80px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.action-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
}

.action-btn.primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.action-btn.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

.action-btn:active {
  transform: scale(0.98);
}

.family-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.family-card {
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.family-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.family-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.family-info {
  flex: 1;
  min-width: 0;
}

.family-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.family-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  opacity: 0.9;
}

.owner-badge {
  display: flex;
  align-items: center;
  gap: 4px;
}

.member-count {
  display: flex;
  align-items: center;
  gap: 4px;
}

.family-card-body {
  padding: 16px;
}

.family-code {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: var(--bg-color);
  border-radius: 8px;
  margin-bottom: 12px;
}

.family-code .label {
  font-size: 13px;
  color: var(--text-secondary);
}

.family-code .code {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  font-family: monospace;
  color: var(--primary-color);
}

.copy-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: var(--primary-color);
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:active {
  transform: scale(0.9);
}

.family-actions {
  display: flex;
  gap: 8px;
}

.btn-secondary,
.btn-danger {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-secondary {
  background: var(--bg-color);
  color: var(--text-primary);
}

.btn-secondary:active {
  transform: scale(0.98);
  background: var(--border-color);
}

.btn-danger {
  background: var(--danger-color);
  color: white;
}

.btn-danger:active {
  transform: scale(0.98);
}

.form-content {
  padding: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-group label i {
  color: var(--primary-color);
}

.mobile-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card-bg);
  color: var(--text-primary);
  transition: all 0.3s;
}

.mobile-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
