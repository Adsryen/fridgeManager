<template>
  <div class="fridge-page">
    <!-- 顶部导航栏 -->
    <div class="mobile-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <i class="fas fa-snowflake"></i>
          </div>
          <div class="app-name">冰箱管理</div>
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
      <div class="fridge-manager-content">
        <!-- 我的冰箱 -->
        <div v-if="fridgeStore.myFridges.length > 0" class="fridge-section">
          <div class="section-header">
            <div class="section-title">
              <i class="fas fa-snowflake"></i>
              <span>我的冰箱</span>
              <span class="count">({{ fridgeStore.myFridges.length }})</span>
            </div>
          </div>

          <div class="fridge-list">
            <div
              v-for="fridge in fridgeStore.myFridges"
              :key="fridge._id"
              class="fridge-item"
            >
              <div class="fridge-icon">
                <i class="fas fa-snowflake"></i>
              </div>
              <div class="fridge-info">
                <div class="fridge-name">{{ fridge.name }}</div>
                <div class="fridge-meta">{{ fridge.item_count || 0 }} 个物品</div>
              </div>
              <div class="fridge-actions">
                <button class="icon-btn" @click="renameFridge(fridge)" title="重命名">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="icon-btn danger" @click="deleteFridge(fridge)" title="删除">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 共享冰箱 -->
        <div v-if="fridgeStore.sharedFridges.length > 0" class="fridge-section">
          <div class="section-header">
            <div class="section-title">
              <i class="fas fa-users"></i>
              <span>共享冰箱</span>
              <span class="count">({{ fridgeStore.sharedFridges.length }})</span>
            </div>
          </div>

          <div class="fridge-list">
            <div
              v-for="fridge in fridgeStore.sharedFridges"
              :key="fridge._id"
              class="fridge-item"
            >
              <div class="fridge-icon shared">
                <i class="fas fa-users"></i>
              </div>
              <div class="fridge-info">
                <div class="fridge-name">{{ fridge.name }}</div>
                <div class="fridge-meta">
                  所有者: {{ fridge.owner_username }} · {{ fridge.item_count || 0 }} 个物品
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="fridgeStore.myFridges.length === 0 && fridgeStore.sharedFridges.length === 0" class="empty-state">
          <i class="fas fa-snowflake"></i>
          <h4>还没有冰箱</h4>
          <p>点击下方按钮创建你的第一个冰箱</p>
        </div>

        <!-- 添加冰箱按钮 -->
        <div class="add-fridge-section">
          <button class="btn-primary full-width" @click="showCreateForm = true">
            <i class="fas fa-plus"></i>
            创建新冰箱
          </button>
        </div>
      </div>
    </div>

    <!-- 底部导航栏 -->
    <div class="mobile-bottom-nav">
      <button class="nav-item" @click="$router.push('/')">
        <i class="fas fa-home"></i>
        <span>首页</span>
      </button>
      <button class="nav-item active">
        <i class="fas fa-snowflake"></i>
        <span>冰箱</span>
      </button>
      <button class="nav-item add-btn" @click="$router.push('/')">
        <div class="add-icon">
          <i class="fas fa-plus"></i>
        </div>
      </button>
      <button class="nav-item" @click="$router.push('/family')">
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

    <!-- 创建冰箱抽屉 -->
    <Drawer v-model="showCreateForm" title="创建冰箱">
      <FridgeForm @success="handleCreateSuccess" @cancel="showCreateForm = false" />
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFridgeStore } from '../stores/fridge'
import { useUserStore } from '../stores/user'
import { useTheme } from '../composables/useTheme'
import Drawer from '../components/common/Drawer.vue'
import FridgeForm from '../components/fridge/FridgeForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Fridge } from '../types/models'

const fridgeStore = useFridgeStore()
const userStore = useUserStore()
const { isDark, toggleTheme } = useTheme()
const showCreateForm = ref(false)

const toggleDarkMode = () => {
  toggleTheme()
}

const renameFridge = async (fridge: Fridge) => {
  try {
    const { value: newName } = await ElMessageBox.prompt('请输入新名称', '重命名冰箱', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: fridge.name,
      inputPattern: /.+/,
      inputErrorMessage: '名称不能为空'
    })

    if (newName) {
      await fridgeStore.renameFridge(fridge._id, newName)
      ElMessage.success('重命名成功')
    }
  } catch {
    // 用户取消
  }
}

const deleteFridge = async (fridge: Fridge) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除冰箱"${fridge.name}"吗？删除后冰箱内的所有物品也会被删除。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await fridgeStore.deleteFridge(fridge._id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const handleCreateSuccess = () => {
  showCreateForm.value = false
  fridgeStore.loadFridges()
}

onMounted(() => {
  fridgeStore.loadFridges()
})
</script>

<style scoped>
.fridge-page {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.fridge-manager-content {
  padding: 20px;
  padding-bottom: 80px;
}

.fridge-section {
  margin-bottom: 32px;
}

.section-header {
  margin-bottom: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.section-title i {
  color: var(--primary-color);
}

.count {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 400;
}

.fridge-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fridge-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.fridge-item:active {
  transform: scale(0.98);
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

.fridge-icon.shared {
  background: linear-gradient(135deg, #10b981, #059669);
}

.fridge-info {
  flex: 1;
  min-width: 0;
}

.fridge-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.fridge-meta {
  font-size: 13px;
  color: var(--text-secondary);
}

.fridge-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: var(--bg-secondary);
  transform: scale(1.05);
}

.icon-btn.danger {
  color: var(--danger-color);
}

.icon-btn.danger:hover {
  background: var(--danger-color);
  color: white;
}

.add-fridge-section {
  margin-top: 24px;
}

.btn-primary {
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

.btn-primary.full-width {
  width: 100%;
}

.btn-primary:active {
  transform: scale(0.98);
}
</style>
