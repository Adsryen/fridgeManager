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
        <div v-if="userStore.isLoggedIn" class="action-buttons">
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
                <div class="family-name" @click="editFamilyName(family)">
                  {{ family.name }}
                  <i v-if="family.creator_id === (userStore.user?._id || userStore.user?.id)" class="fas fa-edit edit-icon"></i>
                </div>
                <div class="family-meta">
                  <span v-if="family.creator_id === (userStore.user?._id || userStore.user?.id)" class="owner-badge">
                    <i class="fas fa-crown"></i> 所有者
                  </span>
                  <span class="member-count">
                    <i class="fas fa-user"></i> {{ family.member_count || 0 }} 人
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
              
              <!-- 家庭冰箱列表 -->
              <div class="family-fridges-section">
                <div class="section-title-small">
                  <i class="fas fa-snowflake"></i>
                  <span>家庭冰箱</span>
                  <button class="refresh-btn" @click="loadFamilyFridges(family._id)" title="刷新">
                    <i class="fas fa-sync-alt" :class="{ spinning: loadingFridges[family._id] }"></i>
                  </button>
                </div>
                
                <div v-if="loadingFridges[family._id]" class="loading-fridges">
                  <i class="fas fa-spinner fa-spin"></i>
                  <span>加载中...</span>
                </div>
                
                <div v-else-if="familyFridges[family._id] && familyFridges[family._id]!.length > 0" class="fridges-grid">
                  <div
                    v-for="fridge in familyFridges[family._id]"
                    :key="fridge._id"
                    class="fridge-mini-card"
                    @click="manageFridgePermission(fridge)"
                  >
                    <div class="fridge-mini-icon">
                      <i class="fas fa-snowflake"></i>
                    </div>
                    <div class="fridge-mini-info">
                      <div class="fridge-mini-name">{{ fridge.name }}</div>
                      <div class="fridge-mini-owner">{{ fridge.owner_username }}</div>
                    </div>
                    <div class="fridge-mini-status">
                      <span v-if="fridge.permission?.is_family_shared" class="status-badge shared">
                        <i class="fas fa-check-circle"></i>
                      </span>
                      <span v-if="fridge.permission?.is_editable_by_family" class="status-badge editable">
                        <i class="fas fa-edit"></i>
                      </span>
                      <span v-if="fridge.user_id === userStore.user?._id" class="status-badge owner">
                        <i class="fas fa-crown"></i>
                      </span>
                    </div>
                  </div>
                </div>
                
                <div v-else class="no-fridges">
                  <i class="fas fa-inbox"></i>
                  <span>暂无共享冰箱</span>
                </div>
              </div>
              
              <div class="family-actions">
                <button class="btn-secondary" @click="viewMembers(family)">
                  <i class="fas fa-users"></i> 查看成员
                </button>
                <button
                  v-if="family.creator_id === (userStore.user?._id || userStore.user?.id)"
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

        <!-- 游客提示 -->
        <div v-else-if="!userStore.isLoggedIn" class="empty-state guest-hint">
          <i class="fas fa-user-lock"></i>
          <h4>需要登录</h4>
          <p>登录后才能使用家庭管理功能</p>
          <div class="guest-actions">
            <router-link to="/login" class="btn-primary">
              <i class="fas fa-sign-in-alt"></i> 立即登录
            </router-link>
            <router-link to="/register" class="btn-secondary">
              <i class="fas fa-user-plus"></i> 注册账号
            </router-link>
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
      <button class="nav-item add-btn" @click="openGlobalAddMenu">
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
        :members="familyStore.members"
        :loading="familyStore.loading"
        @remove="handleRemoveMember"
      />
    </Drawer>

    <!-- 编辑家庭名称抽屉 -->
    <Drawer v-model="showEditForm" title="编辑家庭名称">
      <div class="form-content">
        <div class="form-group">
          <label><i class="fas fa-users"></i> 家庭名称</label>
          <input
            v-model="editForm.name"
            type="text"
            class="mobile-input"
            placeholder="请输入家庭名称"
            maxlength="50"
          />
        </div>
        <div class="form-actions">
          <button class="btn-secondary" @click="showEditForm = false">取消</button>
          <button class="btn-primary" :disabled="updating" @click="handleUpdate">
            <i class="fas fa-check"></i>
            {{ updating ? '更新中...' : '更新' }}
          </button>
        </div>
      </div>
    </Drawer>

    <!-- 冰箱权限管理抽屉 -->
    <Drawer v-model="showPermissionManager" title="冰箱权限设置">
      <FridgePermissionManager
        v-if="currentFridge"
        :fridge="currentFridge"
        @updated="handlePermissionUpdated"
      />
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import { useFamilyStore } from '../stores/family'
import { useUserStore } from '../stores/user'
import { useTheme } from '../composables/useTheme'
import Drawer from '../components/common/Drawer.vue'
import MemberList from '../components/family/MemberList.vue'
import FridgePermissionManager from '../components/fridge/FridgePermissionManager.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getFamilyFridges } from '../api/family'
import type { Family, Fridge } from '../types/models'

const familyStore = useFamilyStore()
const userStore = useUserStore()
const { isDark, toggleTheme } = useTheme()

// 注入全局添加方法
const openGlobalAddMenu = inject('openGlobalAddMenu') as () => void

const showCreateForm = ref(false)
const showJoinForm = ref(false)
const showMemberList = ref(false)
const showEditForm = ref(false)
const showPermissionManager = ref(false)
const creating = ref(false)
const joining = ref(false)
const updating = ref(false)
const currentFamily = ref<Family | null>(null)
const currentFridge = ref<Fridge | null>(null)

// 家庭冰箱数据
const familyFridges = ref<Record<string, Fridge[]>>({})
const loadingFridges = ref<Record<string, boolean>>({})

const createForm = ref({
  name: ''
})

const joinForm = ref({
  code: ''
})

const editForm = ref({
  name: ''
})

const toggleDarkMode = async () => {
  await toggleTheme()
}

const copyCode = async (code: string) => {
  try {
    await navigator.clipboard.writeText(code)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}

const viewMembers = async (family: Family) => {
  currentFamily.value = family
  // 加载家庭成员数据
  try {
    await familyStore.loadMembers(family._id)
  } catch (error: any) {
    console.error('加载家庭成员失败:', error)
    ElMessage.error('加载家庭成员失败')
  }
  showMemberList.value = true
}

const loadFamilyFridges = async (familyId: string) => {
  loadingFridges.value[familyId] = true
  try {
    const response = await getFamilyFridges(familyId)
    familyFridges.value[familyId] = response.data || []
  } catch (error: any) {
    console.error('加载家庭冰箱失败:', error)
    familyFridges.value[familyId] = []
  } finally {
    loadingFridges.value[familyId] = false
  }
}

const manageFridgePermission = (fridge: Fridge) => {
  // 获取用户ID，兼容 _id 和 id 字段
  const userId = userStore.user?._id || userStore.user?.id
  
  // 只有冰箱所有者可以管理权限
  if (fridge.user_id !== userId) {
    ElMessage.info('只有冰箱所有者可以管理权限')
    return
  }
  currentFridge.value = fridge
  showPermissionManager.value = true
}

const handlePermissionUpdated = async () => {
  // 重新加载当前家庭的冰箱列表
  if (currentFamily.value) {
    await loadFamilyFridges(currentFamily.value._id)
  }
  // 重新加载所有家庭的冰箱
  for (const family of familyStore.families) {
    await loadFamilyFridges(family._id)
  }
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
    // 加载新创建家庭的冰箱
    const newFamily = familyStore.families[familyStore.families.length - 1]
    if (newFamily) {
      await loadFamilyFridges(newFamily._id)
    }
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
    // 加载新加入家庭的冰箱
    const newFamily = familyStore.families[familyStore.families.length - 1]
    if (newFamily) {
      await loadFamilyFridges(newFamily._id)
    }
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

const editFamilyName = (family: Family) => {
  // 获取用户ID，兼容 _id 和 id 字段
  const userId = userStore.user?._id || userStore.user?.id
  
  // 只有创建者可以编辑
  if (family.creator_id !== userId) {
    ElMessage.info('只有家庭创建者可以修改名称')
    return
  }
  currentFamily.value = family
  editForm.value.name = family.name
  showEditForm.value = true
}

const handleUpdate = async () => {
  if (!currentFamily.value) return
  
  if (!editForm.value.name) {
    ElMessage.error('请输入家庭名称')
    return
  }

  updating.value = true
  try {
    await familyStore.updateFamily(currentFamily.value._id, editForm.value.name)
    ElMessage.success('更新成功')
    showEditForm.value = false
    await familyStore.loadFamilies()
  } catch (error: any) {
    ElMessage.error(error.message || '更新失败')
  } finally {
    updating.value = false
  }
}

const handleRemoveMember = async (userId: string) => {
  if (!currentFamily.value) return
  
  try {
    await ElMessageBox.confirm(
      '确定要移除该成员吗？',
      '确认移除',
      {
        confirmButtonText: '移除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await familyStore.removeMember(currentFamily.value._id, userId)
    ElMessage.success('成员已移除')
    // 重新加载家庭列表以更新成员数量
    await familyStore.loadFamilies()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '移除失败')
    }
  }
}

onMounted(async () => {
  console.log('[调试] Family.vue 组件挂载，开始加载家庭列表')
  await familyStore.loadFamilies()
  console.log('[调试] 家庭列表加载完成，数量:', familyStore.families.length)
  console.log('[调试] 家庭列表数据:', familyStore.families)
  // 加载所有家庭的冰箱
  for (const family of familyStore.families) {
    await loadFamilyFridges(family._id)
  }
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
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.family-name:hover {
  color: rgba(255, 255, 255, 0.8);
}

.edit-icon {
  font-size: 14px;
  opacity: 0.7;
  transition: all 0.2s;
}

.family-name:hover .edit-icon {
  opacity: 1;
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
  margin-top: 20px;
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

.guest-hint {
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.guest-hint i {
  font-size: 56px;
  color: var(--text-secondary);
  opacity: 0.25;
  margin-bottom: 16px;
}

.guest-hint h4 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  text-align: center;
}

.guest-hint p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 24px;
  text-align: center;
  line-height: 1.5;
}

.guest-actions {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 280px;
}

.guest-actions .btn-primary,
.guest-actions .btn-secondary {
  flex: 1;
  padding: 11px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.guest-actions .btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
}

.guest-actions .btn-secondary {
  background: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.guest-actions .btn-primary:active {
  transform: scale(0.97);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.guest-actions .btn-secondary:active {
  transform: scale(0.97);
  background: var(--bg-color);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.guest-actions .btn-primary i,
.guest-actions .btn-secondary i {
  font-size: 13px;
}

/* 家庭冰箱区域 */
.family-fridges-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.section-title-small {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.section-title-small i {
  color: var(--primary-color);
  font-size: 14px;
}

.refresh-btn {
  margin-left: auto;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:active {
  transform: scale(0.9);
}

.refresh-btn i.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-fridges {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  font-size: 13px;
  color: var(--text-secondary);
}

.loading-fridges i {
  color: var(--primary-color);
}

.fridges-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fridge-mini-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-color);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.fridge-mini-card:active {
  transform: scale(0.98);
  background: var(--card-bg);
}

.fridge-mini-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  flex-shrink: 0;
}

.fridge-mini-info {
  flex: 1;
  min-width: 0;
}

.fridge-mini-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fridge-mini-owner {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fridge-mini-status {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 10px;
}

.status-badge.shared {
  background: #10b981;
  color: white;
}

.status-badge.editable {
  background: #f59e0b;
  color: white;
}

.status-badge.owner {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: white;
}

.no-fridges {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px;
  color: var(--text-secondary);
  font-size: 13px;
}

.no-fridges i {
  font-size: 32px;
  opacity: 0.3;
}
</style>
