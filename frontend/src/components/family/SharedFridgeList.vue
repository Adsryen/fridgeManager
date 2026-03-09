<template>
  <div class="shared-fridge-list">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 冰箱列表 -->
    <div v-else-if="fridges.length > 0" class="fridges-container">
      <div
        v-for="fridge in fridges"
        :key="fridge._id"
        class="fridge-item"
      >
        <div class="fridge-info">
          <div class="fridge-header">
            <i class="fas fa-snowflake"></i>
            <h6>{{ fridge.name }}</h6>
          </div>
          <div class="fridge-details">
            <span class="fridge-owner">
              <i class="fas fa-user"></i>
              所有者: {{ fridge.owner_username }}
            </span>
            <span v-if="fridge.item_count !== undefined" class="fridge-count">
              <i class="fas fa-box"></i>
              物品数量: {{ fridge.item_count }}
            </span>
          </div>
        </div>
        
        <span
          :class="['permission-badge', fridge.permission?.is_editable_by_family ? 'editable' : 'readonly']"
        >
          <i :class="['fas', fridge.permission?.is_editable_by_family ? 'fa-edit' : 'fa-eye']"></i>
          {{ fridge.permission?.is_editable_by_family ? '可编辑' : '只读' }}
        </span>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <i class="fas fa-snowflake"></i>
      <p>暂无共享冰箱</p>
      <p class="empty-hint">
        在主页的"管理冰箱"中，点击冰箱的权限设置按钮（盾牌图标），<br>
        开启"家庭共享"即可让家庭成员看到您的冰箱
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useFamilyStore } from '@/stores/family'
import type { Fridge } from '@/types/models'

interface Props {
  familyId: string
}

const props = defineProps<Props>()

const familyStore = useFamilyStore()

const fridges = ref<Fridge[]>([])
const loading = ref(false)

// 加载家庭共享冰箱
const loadFridges = async () => {
  loading.value = true
  try {
    const response = await familyStore.getFamilyFridges(props.familyId)
    if (response.success && response.data) {
      fridges.value = response.data
    } else {
      ElMessage.error(response.error || '加载失败')
    }
  } catch (_error) {
    ElMessage.error('加载冰箱列表失败')
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadFridges()
})
</script>

<style scoped>
.shared-fridge-list {
  min-height: 200px;
}

.loading-state {
  padding: 20px;
}

.fridges-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fridge-item {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.fridge-item:hover {
  border-color: var(--theme-color-2);
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.fridge-info {
  flex: 1;
}

.fridge-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.fridge-header i {
  color: var(--theme-color-2);
}

.fridge-header h6 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.fridge-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.fridge-owner,
.fridge-count {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.fridge-owner i,
.fridge-count i {
  width: 14px;
  text-align: center;
  font-size: 12px;
}

.permission-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: white;
  display: flex;
  align-items: center;
  gap: 6px;
}

.permission-badge.editable {
  background: linear-gradient(135deg, #10b981, #059669);
}

.permission-badge.readonly {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
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

.empty-hint {
  margin-top: 12px;
  font-size: 13px;
  line-height: 1.6;
}

/* 响应式 */
@media (max-width: 768px) {
  .fridge-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .permission-badge {
    width: 100%;
    justify-content: center;
  }
}
</style>
