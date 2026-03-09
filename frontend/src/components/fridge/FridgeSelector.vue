<template>
  <div class="fridge-selector">
    <!-- 当前冰箱 -->
    <div class="current-fridge">
      <div class="fridge-icon">
        <i class="fas fa-snowflake"></i>
      </div>
      <div class="fridge-info">
        <div class="fridge-name">{{ currentFridge?.name || '公共冰箱' }}</div>
        <div class="fridge-count">{{ currentFridge?.item_count || 0 }} 件物品</div>
      </div>
    </div>

    <!-- 我的冰箱 -->
    <div v-if="myFridges.length > 0" class="fridge-section">
      <div class="section-title">
        <i class="fas fa-snowflake"></i>
        <span>我的冰箱</span>
      </div>
      <div class="fridge-list">
        <button
          v-for="fridge in myFridges"
          :key="fridge._id"
          class="fridge-item"
          :class="{ active: fridge._id === currentFridgeId }"
          @click="handleSwitch(fridge._id)"
        >
          <div class="fridge-item-icon">
            <i class="fas fa-snowflake"></i>
          </div>
          <div class="fridge-item-info">
            <div class="fridge-item-name">{{ fridge.name }}</div>
            <div class="fridge-item-count">{{ fridge.item_count || 0 }} 件物品</div>
          </div>
          <i v-if="fridge._id === currentFridgeId" class="fas fa-check-circle check-icon"></i>
        </button>
      </div>
    </div>

    <!-- 共享冰箱 -->
    <div v-if="sharedFridges.length > 0" class="fridge-section">
      <div class="section-title">
        <i class="fas fa-users"></i>
        <span>共享冰箱</span>
      </div>
      <div class="fridge-list">
        <button
          v-for="fridge in sharedFridges"
          :key="fridge._id"
          class="fridge-item"
          :class="{ active: fridge._id === currentFridgeId }"
          @click="handleSwitch(fridge._id)"
        >
          <div class="fridge-item-icon shared">
            <i class="fas fa-users"></i>
          </div>
          <div class="fridge-item-info">
            <div class="fridge-item-name">{{ fridge.name }}</div>
            <div class="fridge-item-owner">来自 {{ fridge.owner_username }}</div>
            <div class="fridge-item-count">{{ fridge.item_count || 0 }} 件物品</div>
          </div>
          <i v-if="fridge._id === currentFridgeId" class="fas fa-check-circle check-icon"></i>
        </button>
      </div>
    </div>

    <!-- 创建新冰箱 -->
    <div class="create-fridge-section">
      <button class="create-fridge-btn" @click="showCreateDialog">
        <i class="fas fa-plus-circle"></i>
        <span>创建新冰箱</span>
      </button>
    </div>

    <!-- 创建冰箱对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建新冰箱"
      width="90%"
      :style="{ maxWidth: '400px' }"
    >
      <el-form ref="createFormRef" :model="createForm" :rules="createRules">
        <el-form-item label="冰箱名称" prop="name">
          <el-input
            v-model="createForm.name"
            placeholder="请输入冰箱名称"
            maxlength="20"
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useFridgeStore } from '@/stores/fridge'
import { useItemStore } from '@/stores/item'

const emit = defineEmits<{
  close: []
}>()

const fridgeStore = useFridgeStore()
const itemStore = useItemStore()

// 表单引用
const createFormRef = ref<FormInstance>()

// 创建表单数据
const createForm = reactive({
  name: ''
})

// 创建表单验证规则
const createRules: FormRules = {
  name: [
    { required: true, message: '请输入冰箱名称', trigger: 'blur' },
    { min: 1, max: 20, message: '名称长度在 1 到 20 个字符', trigger: 'blur' }
  ]
}

// 状态
const createDialogVisible = ref(false)
const creating = ref(false)

// 计算属性
const currentFridgeId = computed(() => fridgeStore.currentFridgeId)
const currentFridge = computed(() => fridgeStore.currentFridge)
const myFridges = computed(() => fridgeStore.myFridges)
const sharedFridges = computed(() => fridgeStore.sharedFridges)

// 显示创建对话框
const showCreateDialog = () => {
  createDialogVisible.value = true
  createForm.name = ''
}

// 处理切换冰箱
const handleSwitch = async (fridgeId: string) => {
  if (fridgeId === currentFridgeId.value) {
    emit('close')
    return
  }

  try {
    const response = await fridgeStore.switchFridge(fridgeId)
    if (response.success) {
      ElMessage.success('切换成功')
      // 重新加载物品列表
      await itemStore.loadItems()
      emit('close')
    } else {
      ElMessage.error(response.error || '切换失败')
    }
  } catch (error: any) {
    console.error('[冰箱选择器] 切换失败', error)
    ElMessage.error('切换失败，请稍后重试')
  }
}

// 处理创建冰箱
const handleCreate = async () => {
  if (!createFormRef.value) return

  try {
    await createFormRef.value.validate()
  } catch {
    return
  }

  creating.value = true

  try {
    const response = await fridgeStore.createFridge(createForm.name)
    if (response.success) {
      ElMessage.success('创建成功')
      createDialogVisible.value = false
      createForm.name = ''
      // 重新加载物品列表
      await itemStore.loadItems()
    } else {
      ElMessage.error(response.error || '创建失败')
    }
  } catch (error: any) {
    console.error('[冰箱选择器] 创建失败', error)
    ElMessage.error('创建失败，请稍后重试')
  } finally {
    creating.value = false
  }
}
</script>

<style scoped>
.fridge-selector {
  padding: 0;
}

/* 当前冰箱 */
.current-fridge {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 16px;
  color: white;
  margin-bottom: 20px;
}

.fridge-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.fridge-info {
  flex: 1;
}

.fridge-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 4px;
}

.fridge-count {
  font-size: 14px;
  opacity: 0.9;
}

/* 冰箱分组 */
.fridge-section {
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 12px;
  padding: 0 4px;
}

.fridge-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.fridge-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
}

.fridge-item:active {
  transform: scale(0.98);
}

.fridge-item.active {
  border-color: var(--primary-color);
  background: rgba(102, 126, 234, 0.1);
}

.fridge-item-icon {
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

.fridge-item-icon.shared {
  background: linear-gradient(135deg, #10b981, #059669);
}

.fridge-item-info {
  flex: 1;
  min-width: 0;
}

.fridge-item-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fridge-item-owner {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.fridge-item-count {
  font-size: 13px;
  color: var(--text-secondary);
}

.check-icon {
  font-size: 20px;
  color: var(--primary-color);
  flex-shrink: 0;
}

/* 创建新冰箱 */
.create-fridge-section {
  margin-top: 20px;
}

.create-fridge-btn {
  width: 100%;
  padding: 16px;
  background: var(--bg-color);
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.create-fridge-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: rgba(102, 126, 234, 0.05);
}

.create-fridge-btn:active {
  transform: scale(0.98);
}

.create-fridge-btn i {
  font-size: 18px;
}
</style>
