<template>
  <div class="member-list">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 成员列表 -->
    <div v-else-if="members.length > 0" class="members-container">
      <div
        v-for="member in members"
        :key="member.user_id"
        class="member-item"
      >
        <div class="member-info">
          <div class="member-header">
            <i class="fas fa-user"></i>
            <h6>{{ member.username }}</h6>
            <span v-if="member.is_owner" class="owner-badge">
              <i class="fas fa-crown"></i>
              创建者
            </span>
          </div>
          <div class="member-details">
            <span class="member-email">
              <i class="fas fa-envelope"></i>
              {{ member.email }}
            </span>
            <span class="member-date">
              <i class="fas fa-calendar"></i>
              加入时间: {{ formatDate(member.joined_at) }}
            </span>
          </div>
        </div>
        
        <button
          v-if="!member.is_owner && canRemove"
          class="remove-btn"
          @click="handleRemove(member.user_id)"
        >
          <i class="fas fa-user-minus"></i>
          移除
        </button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <i class="fas fa-user-slash"></i>
      <p>暂无成员</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '../../stores/user'
import { useFamilyStore } from '../../stores/family'
import type { FamilyMember } from '../../types/models'

interface Props {
  familyId: string
  members: FamilyMember[]
  loading?: boolean
}

interface Emits {
  (e: 'remove', userId: string): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<Emits>()

const userStore = useUserStore()
const familyStore = useFamilyStore()

// 判断当前用户是否可以移除成员（只有创建者可以）
const canRemove = computed(() => {
  const family = familyStore.families.find(f => f._id === props.familyId)
  return family?.creator_id === userStore.user?._id
})

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  
  // 创建Date对象，如果是UTC时间字符串，会自动转换为本地时间
  const date = new Date(dateStr)
  
  // 检查日期是否有效
  if (isNaN(date.getTime())) {
    return dateStr // 如果无法解析，返回原字符串
  }
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hour}:${minute}`
}

// 移除成员
const handleRemove = (userId: string) => {
  emit('remove', userId)
}
</script>

<style scoped>
.member-list {
  min-height: 200px;
}

.loading-state {
  padding: 20px;
}

.members-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-item {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.member-item:hover {
  border-color: var(--theme-color-2);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.member-info {
  flex: 1;
}

.member-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.member-header i {
  color: var(--theme-color-2);
}

.member-header h6 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.owner-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.owner-badge i {
  color: white;
}

.member-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-email,
.member-date {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.member-email i,
.member-date i {
  width: 14px;
  text-align: center;
  font-size: 12px;
}

.remove-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: #ef4444;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.remove-btn:hover {
  background: #dc2626;
  transform: scale(1.05);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .member-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .remove-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
