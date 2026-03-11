<template>
  <div class="fridge-permission-manager">
    <div class="permission-header">
      <div class="fridge-info">
        <div class="fridge-icon">
          <i class="fas fa-snowflake"></i>
        </div>
        <div class="fridge-details">
          <div class="fridge-name">{{ fridge.name }}</div>
          <div class="fridge-meta">{{ fridge.item_count || 0 }} 个物品</div>
        </div>
      </div>
    </div>

    <div class="permission-settings">
      <div class="setting-item">
        <div class="setting-info">
          <div class="setting-label">
            <i class="fas fa-users"></i>
            <span>家庭共享</span>
          </div>
          <div class="setting-desc">允许家庭成员查看此冰箱</div>
        </div>
        <label class="toggle-switch">
          <input 
            type="checkbox" 
            v-model="localPermission.is_family_shared"
            @change="handleShareChange"
          >
          <span class="toggle-slider"></span>
        </label>
      </div>

      <div 
        class="setting-item" 
        :class="{ disabled: !localPermission.is_family_shared }"
      >
        <div class="setting-info">
          <div class="setting-label">
            <i class="fas fa-edit"></i>
            <span>允许编辑</span>
          </div>
          <div class="setting-desc">家庭成员可以添加、编辑和删除物品</div>
        </div>
        <label class="toggle-switch">
          <input 
            type="checkbox" 
            v-model="localPermission.is_editable_by_family"
            :disabled="!localPermission.is_family_shared"
            @change="handleEditableChange"
          >
          <span class="toggle-slider"></span>
        </label>
      </div>
    </div>

    <div v-if="saving" class="saving-indicator">
      <i class="fas fa-spinner fa-spin"></i>
      <span>保存中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { setFridgePermission } from '../../api/family'
import { ElMessage } from 'element-plus'
import type { Fridge, FridgePermission } from '../../types/models'

interface Props {
  fridge: Fridge
}

const props = defineProps<Props>()
const emit = defineEmits<{
  updated: []
}>()

const localPermission = ref<FridgePermission>({
  fridge_id: props.fridge._id,
  is_family_shared: props.fridge.permission?.is_family_shared || false,
  is_editable_by_family: props.fridge.permission?.is_editable_by_family || false
})

const saving = ref(false)

// 监听 props 变化
watch(() => props.fridge.permission, (newPermission) => {
  if (newPermission) {
    localPermission.value = {
      fridge_id: props.fridge._id,
      is_family_shared: newPermission.is_family_shared || false,
      is_editable_by_family: newPermission.is_editable_by_family || false
    }
  }
}, { deep: true })

const handleShareChange = async () => {
  // 如果关闭共享，同时关闭编辑权限
  if (!localPermission.value.is_family_shared) {
    localPermission.value.is_editable_by_family = false
  }
  await savePermission()
}

const handleEditableChange = async () => {
  await savePermission()
}

const savePermission = async () => {
  saving.value = true
  try {
    await setFridgePermission(
      props.fridge._id,
      localPermission.value.is_family_shared,
      localPermission.value.is_editable_by_family
    )
    ElMessage.success('权限设置已保存')
    emit('updated')
  } catch (error: any) {
    ElMessage.error(error.message || '保存失败')
    // 恢复原值
    localPermission.value = {
      fridge_id: props.fridge._id,
      is_family_shared: props.fridge.permission?.is_family_shared || false,
      is_editable_by_family: props.fridge.permission?.is_editable_by_family || false
    }
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.fridge-permission-manager {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.permission-header {
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.fridge-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.fridge-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  flex-shrink: 0;
}

.fridge-details {
  flex: 1;
}

.fridge-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.fridge-meta {
  font-size: 13px;
  color: var(--text-secondary);
}

.permission-settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.setting-item.disabled {
  opacity: 0.5;
}

.setting-info {
  flex: 1;
  min-width: 0;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.setting-label i {
  color: var(--primary-color);
  font-size: 16px;
}

.setting-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 28px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 28px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.toggle-switch input:disabled + .toggle-slider {
  opacity: 0.5;
  cursor: not-allowed;
}

.saving-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: var(--bg-color);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.saving-indicator i {
  color: var(--primary-color);
}
</style>
