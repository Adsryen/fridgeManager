<template>
  <div class="family-card" @click="handleViewDetail">
    <div class="family-card-header">
      <div>
        <div class="family-name">{{ family.name }}</div>
        <div v-if="isOwner" class="family-code">
          <i class="fas fa-key"></i>
          <span>{{ family.family_code }}</span>
          <el-tooltip content="点击复制" placement="top">
            <i class="fas fa-copy copy-icon" @click.stop="copyCode"></i>
          </el-tooltip>
        </div>
      </div>
      <span :class="['role-badge', roleClass]">{{ roleText }}</span>
    </div>
    
    <div class="family-info">
      <div class="family-meta">
        <i class="fas fa-user"></i>
        创建者: {{ family.owner_username }}
      </div>
      <div class="family-meta">
        <i class="fas fa-users"></i>
        成员数量: {{ family.member_count }}
      </div>
      <div class="family-meta">
        <i class="fas fa-calendar"></i>
        创建时间: {{ formatDate(family.created_at) }}
      </div>
    </div>
    
    <div class="family-actions" @click.stop>
      <button class="card-btn primary" @click="handleViewDetail">
        <i class="fas fa-cog"></i>
        <span>管理</span>
      </button>
      <button
        v-if="!isOwner"
        class="card-btn danger"
        @click="handleLeave"
      >
        <i class="fas fa-sign-out-alt"></i>
        <span>离开</span>
      </button>
      <button
        v-else
        class="card-btn danger"
        @click="handleDelete"
      >
        <i class="fas fa-trash"></i>
        <span>删除</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { Family } from '@/types/models'

interface Props {
  family: Family
}

interface Emits {
  (e: 'view-detail', family: Family): void
  (e: 'leave', familyId: string): void
  (e: 'delete', familyId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const userStore = useUserStore()

// 判断当前用户是否是创建者
const isOwner = computed(() => {
  const userId = userStore.user?._id || userStore.user?.id
  return props.family.creator_id === userId
})

// 角色文本
const roleText = computed(() => {
  return isOwner.value ? '创建者' : '成员'
})

// 角色样式类
const roleClass = computed(() => {
  return isOwner.value ? 'creator' : 'member'
})

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 复制邀请码
const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(props.family.family_code)
    ElMessage.success('邀请码已复制到剪贴板')
  } catch (_error) {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 查看详情
const handleViewDetail = () => {
  emit('view-detail', props.family)
}

// 离开家庭
const handleLeave = () => {
  emit('leave', props.family._id)
}

// 删除家庭
const handleDelete = () => {
  emit('delete', props.family._id)
}
</script>

<style scoped>
.family-card {
  background: var(--card-bg);
  border-radius: 20px;
  padding: 24px;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
  cursor: pointer;
}

.family-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.1);
  border-color: var(--theme-color-2);
}

.family-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.family-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.family-code {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-color);
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: var(--theme-color-3);
  font-size: 16px;
}

.copy-icon {
  cursor: pointer;
  transition: all 0.3s;
  color: var(--text-secondary);
}

.copy-icon:hover {
  color: var(--theme-color-2);
  transform: scale(1.1);
}

.role-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.role-badge.creator {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.role-badge.member {
  background: linear-gradient(135deg, #6b7280, #4b5563);
}

.family-info {
  margin-bottom: 16px;
}

.family-meta {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.family-meta i {
  width: 16px;
  text-align: center;
}

.family-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.card-btn {
  flex: 1;
  padding: 10px 16px;
  border-radius: 12px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.card-btn.primary {
  background: var(--theme-color-2);
  color: white;
}

.card-btn.danger {
  background: #ef4444;
  color: white;
}

.card-btn:hover {
  transform: scale(1.05);
  opacity: 0.9;
}
</style>
