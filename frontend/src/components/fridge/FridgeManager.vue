<template>
  <div class="fridge-manager">
    <!-- 我的冰箱 -->
    <div v-if="myFridges.length > 0" class="fridge-section">
      <div class="section-header">
        <div class="section-title">
          <i class="fas fa-snowflake"></i>
          <span>我的冰箱</span>
          <span class="count">({{ myFridges.length }})</span>
        </div>
      </div>

      <div class="fridge-list">
        <div
          v-for="fridge in myFridges"
          :key="fridge._id"
          class="fridge-item"
        >
          <div class="fridge-icon">
            <i class="fas fa-snowflake"></i>
          </div>
          
          <div class="fridge-info">
            <div class="fridge-name">{{ fridge.name }}</div>
            <div class="fridge-meta">
              <span class="item-count">
                <i class="fas fa-box"></i>
                {{ fridge.item_count || 0 }} 件物品
              </span>
            </div>
          </div>

          <div class="fridge-actions">
            <button
              class="action-btn history-btn"
              @click="showHistoryDialog(fridge)"
              title="历史记录"
            >
              <i class="fas fa-history"></i>
            </button>
            <button
              class="action-btn permission-btn"
              @click="showPermissionDialog(fridge)"
              title="权限设置"
            >
              <i class="fas fa-shield-alt"></i>
            </button>
            <button
              class="action-btn edit-btn"
              @click="showRenameDialog(fridge)"
              title="重命名"
            >
              <i class="fas fa-edit"></i>
            </button>
            <button
              class="action-btn delete-btn"
              @click="showDeleteDialog(fridge)"
              title="删除"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 共享冰箱 -->
    <div v-if="sharedFridges.length > 0" class="fridge-section">
      <div class="section-header">
        <div class="section-title">
          <i class="fas fa-users"></i>
          <span>共享冰箱</span>
          <span class="count">({{ sharedFridges.length }})</span>
        </div>
      </div>

      <div class="fridge-list">
        <div
          v-for="fridge in sharedFridges"
          :key="fridge._id"
          class="fridge-item shared"
        >
          <div class="fridge-icon shared">
            <i class="fas fa-users"></i>
          </div>
          
          <div class="fridge-info">
            <div class="fridge-name">{{ fridge.name }}</div>
            <div class="fridge-meta">
              <span class="owner">
                <i class="fas fa-user"></i>
                来自 {{ fridge.owner_username }}
              </span>
              <span class="item-count">
                <i class="fas fa-box"></i>
                {{ fridge.item_count || 0 }} 件物品
              </span>
            </div>
          </div>

          <div class="fridge-badge">
            <span class="shared-badge">共享</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="myFridges.length === 0 && sharedFridges.length === 0" class="empty-state">
      <i class="fas fa-snowflake empty-icon"></i>
      <p class="empty-text">暂无冰箱</p>
      <p class="empty-hint">点击下方按钮创建您的第一个冰箱</p>
    </div>

    <!-- 重命名对话框 -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名冰箱"
      width="90%"
      :style="{ maxWidth: '400px' }"
    >
      <el-form ref="renameFormRef" :model="renameForm" :rules="renameRules">
        <el-form-item label="冰箱名称" prop="name">
          <el-input
            v-model="renameForm.name"
            placeholder="请输入冰箱名称"
            maxlength="20"
            show-word-limit
            @keyup.enter="handleRename"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="renaming" @click="handleRename">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="删除冰箱"
      width="90%"
      :style="{ maxWidth: '400px' }"
    >
      <div class="delete-confirm">
        <i class="fas fa-exclamation-triangle warning-icon"></i>
        <p class="warning-text">
          确定要删除冰箱 <strong>{{ currentFridge?.name }}</strong> 吗？
        </p>
        <p class="warning-hint">
          删除后，该冰箱中的所有物品也将被删除，此操作不可恢复！
        </p>
      </div>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="deleting" @click="handleDelete">
          确定删除
        </el-button>
      </template>
    </el-dialog>

    <!-- 权限设置对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="冰箱权限设置"
      width="90%"
      :style="{ maxWidth: '500px' }"
    >
      <div class="permission-settings">
        <div class="permission-item">
          <div class="permission-info">
            <div class="permission-title">
              <i class="fas fa-users"></i>
              家庭共享
            </div>
            <div class="permission-desc">
              开启后，家庭成员可以看到这个冰箱
            </div>
          </div>
          <el-switch
            v-model="permissionForm.isFamilyShared"
            size="large"
          />
        </div>

        <div class="permission-item" :class="{ disabled: !permissionForm.isFamilyShared }">
          <div class="permission-info">
            <div class="permission-title">
              <i class="fas fa-edit"></i>
              家庭成员可编辑
            </div>
            <div class="permission-desc">
              开启后，家庭成员可以编辑冰箱中的物品
            </div>
          </div>
          <el-switch
            v-model="permissionForm.isEditableByFamily"
            size="large"
            :disabled="!permissionForm.isFamilyShared"
          />
        </div>

        <div class="permission-hint">
          <i class="fas fa-info-circle"></i>
          <span>提示：关闭家庭共享后，家庭成员将无法看到此冰箱</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="savingPermission" @click="handleSavePermission">
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 历史记录对话框 -->
    <el-dialog
      v-model="historyDialogVisible"
      :title="`${currentFridge?.name} - 历史记录`"
      width="600px"
      :close-on-click-modal="false"
    >
      <ItemHistory
        v-if="currentFridge && historyDialogVisible"
        :fridge-id="currentFridge._id"
        @restored="handleItemRestored"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useFridgeStore } from '@/stores/fridge'
import { useFamilyStore } from '@/stores/family'
import { useItemStore } from '@/stores/item'
import type { Fridge } from '@/types/models'
import ItemHistory from '@/components/item/ItemHistory.vue'

const fridgeStore = useFridgeStore()
const familyStore = useFamilyStore()
const itemStore = useItemStore()

// 表单引用
const renameFormRef = ref<FormInstance>()

// 重命名表单数据
const renameForm = reactive({
  name: ''
})

// 重命名表单验证规则
const renameRules: FormRules = {
  name: [
    { required: true, message: '请输入冰箱名称', trigger: 'blur' },
    { min: 1, max: 20, message: '名称长度在 1 到 20 个字符', trigger: 'blur' }
  ]
}

// 权限表单数据
const permissionForm = reactive({
  isFamilyShared: false,
  isEditableByFamily: false
})

// 状态
const renameDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const permissionDialogVisible = ref(false)
const historyDialogVisible = ref(false)
const renaming = ref(false)
const deleting = ref(false)
const savingPermission = ref(false)
const currentFridge = ref<Fridge | null>(null)

// 计算属性
const myFridges = computed(() => fridgeStore.myFridges)
const sharedFridges = computed(() => fridgeStore.sharedFridges)

// 显示重命名对话框
const showRenameDialog = (fridge: Fridge) => {
  currentFridge.value = fridge
  renameForm.name = fridge.name
  renameDialogVisible.value = true
}

// 显示删除确认对话框
const showDeleteDialog = (fridge: Fridge) => {
  currentFridge.value = fridge
  deleteDialogVisible.value = true
}

// 显示权限设置对话框
const showPermissionDialog = async (fridge: Fridge) => {
  currentFridge.value = fridge
  
  // 加载当前权限设置
  try {
    const response = await familyStore.getFridgePermission(fridge._id)
    if (response.success && response.data) {
      permissionForm.isFamilyShared = response.data.is_family_shared || false
      permissionForm.isEditableByFamily = response.data.is_editable_by_family || false
    } else {
      // 默认值
      permissionForm.isFamilyShared = false
      permissionForm.isEditableByFamily = false
    }
  } catch (_error) {
    // 使用默认值
    permissionForm.isFamilyShared = false
    permissionForm.isEditableByFamily = false
  }
  
  permissionDialogVisible.value = true
}

// 显示历史记录对话框
const showHistoryDialog = (fridge: Fridge) => {
  currentFridge.value = fridge
  historyDialogVisible.value = true
}

// 处理重命名
const handleRename = async () => {
  if (!renameFormRef.value || !currentFridge.value) return

  try {
    await renameFormRef.value.validate()
  } catch {
    return
  }

  renaming.value = true

  try {
    const response = await fridgeStore.renameFridge(
      currentFridge.value._id,
      renameForm.name
    )
    if (response.success) {
      ElMessage.success('重命名成功')
      renameDialogVisible.value = false
      // 重新加载冰箱列表
      await fridgeStore.loadFridges()
    } else {
      ElMessage.error(response.error || '重命名失败')
    }
  } catch (error: any) {
    console.error('[冰箱管理] 重命名失败', error)
    ElMessage.error('重命名失败，请稍后重试')
  } finally {
    renaming.value = false
  }
}

// 处理删除
const handleDelete = async () => {
  if (!currentFridge.value) return

  deleting.value = true

  try {
    const response = await fridgeStore.deleteFridge(currentFridge.value._id)
    if (response.success) {
      ElMessage.success('删除成功')
      deleteDialogVisible.value = false
      // 重新加载冰箱列表
      await fridgeStore.loadFridges()
      // 如果删除的是当前冰箱，重新加载物品列表
      if (currentFridge.value._id === fridgeStore.currentFridgeId) {
        await itemStore.loadItems()
      }
    } else {
      ElMessage.error(response.error || '删除失败')
    }
  } catch (error: any) {
    console.error('[冰箱管理] 删除失败', error)
    ElMessage.error('删除失败，请稍后重试')
  } finally {
    deleting.value = false
  }
}

// 保存权限设置
const handleSavePermission = async () => {
  if (!currentFridge.value) return

  savingPermission.value = true

  try {
    const response = await familyStore.setFridgePermission(
      currentFridge.value._id,
      permissionForm.isFamilyShared,
      permissionForm.isEditableByFamily
    )
    if (response.success) {
      ElMessage.success('权限设置已保存')
      permissionDialogVisible.value = false
      // 重新加载冰箱列表
      await fridgeStore.loadFridges()
    } else {
      ElMessage.error(response.error || '保存失败')
    }
  } catch (error: any) {
    console.error('[冰箱管理] 保存权限失败', error)
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    savingPermission.value = false
  }
}

// 处理物品恢复
const handleItemRestored = async () => {
  // 重新加载冰箱列表以更新物品数量
  await fridgeStore.loadFridges()
  // 重新加载物品列表
  await itemStore.loadItems()
  ElMessage.success('物品已恢复')
}
</script>

<style scoped>
.fridge-manager {
  padding: 0;
}

/* 冰箱分组 */
.fridge-section {
  margin-bottom: 32px;
}

.fridge-section:last-child {
  margin-bottom: 0;
}

.section-header {
  margin-bottom: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.section-title i {
  font-size: 18px;
  color: var(--primary-color);
}

.count {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 400;
}

/* 冰箱列表 */
.fridge-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fridge-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: var(--bg-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  transition: all 0.3s;
}

.fridge-item:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.fridge-item.shared {
  border-color: rgba(16, 185, 129, 0.3);
}

.fridge-item.shared:hover {
  border-color: #10b981;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
}

/* 冰箱图标 */
.fridge-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  flex-shrink: 0;
}

.fridge-icon.shared {
  background: linear-gradient(135deg, #10b981, #059669);
}

/* 冰箱信息 */
.fridge-info {
  flex: 1;
  min-width: 0;
}

.fridge-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fridge-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.fridge-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--text-secondary);
}

.fridge-meta i {
  font-size: 12px;
}

.owner {
  color: #10b981;
}

/* 冰箱操作按钮 */
.fridge-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.action-btn:active {
  transform: translateY(0);
}

.edit-btn:hover {
  background: var(--primary-color);
  color: white;
}

.delete-btn:hover {
  background: var(--danger-color);
  color: white;
}

.history-btn:hover {
  background: var(--info-color);
  color: white;
}

/* 共享标签 */
.fridge-badge {
  flex-shrink: 0;
}

.shared-badge {
  padding: 4px 12px;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  color: var(--border-color);
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: var(--text-secondary);
  opacity: 0.8;
}

/* 删除确认对话框 */
.delete-confirm {
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  font-size: 48px;
  color: var(--warning-color);
  margin-bottom: 16px;
}

.warning-text {
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 12px;
  line-height: 1.5;
}

.warning-text strong {
  color: var(--danger-color);
}

.warning-hint {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* 权限设置对话框 */
.permission-settings {
  padding: 10px 0;
}

.permission-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: var(--bg-color);
  border-radius: 12px;
  margin-bottom: 12px;
  transition: all 0.3s;
}

.permission-item:hover {
  background: var(--bg-secondary);
}

.permission-item.disabled {
  opacity: 0.5;
}

.permission-info {
  flex: 1;
}

.permission-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.permission-title i {
  color: var(--primary-color);
}

.permission-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.permission-hint {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 16px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  margin-top: 12px;
}

.permission-hint i {
  color: #3b82f6;
  margin-top: 2px;
  flex-shrink: 0;
}

.permission-hint span {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.permission-btn:hover {
  background: #3b82f6;
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .fridge-item {
    padding: 12px;
    gap: 12px;
  }

  .fridge-icon {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }

  .fridge-name {
    font-size: 15px;
  }

  .fridge-meta {
    gap: 12px;
  }

  .fridge-meta span {
    font-size: 12px;
  }

  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 13px;
  }

  .section-title {
    font-size: 15px;
  }

  .section-title i {
    font-size: 16px;
  }
}

/* 小屏幕优化 */
@media (max-height: 667px) {
  .fridge-section {
    margin-bottom: 24px;
  }

  .empty-state {
    padding: 40px 20px;
  }

  .empty-icon {
    font-size: 48px;
  }
}
</style>
