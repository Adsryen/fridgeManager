<template>
  <div class="fridge-form">
    <el-form ref="formRef" :model="formData" :rules="formRules" label-position="top">
      <!-- 冰箱名称 -->
      <el-form-item label="冰箱名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入冰箱名称"
          maxlength="20"
          show-word-limit
          clearable
          @keyup.enter="handleSubmit"
        >
          <template #prefix>
            <i class="fas fa-snowflake"></i>
          </template>
        </el-input>
      </el-form-item>

      <!-- 按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel" size="large" style="flex: 1">
          取消
        </el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading" size="large" style="flex: 1">
          创建
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useFridgeStore } from '@/stores/fridge'

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const fridgeStore = useFridgeStore()

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive({
  name: ''
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入冰箱名称', trigger: 'blur' },
    { min: 1, max: 20, message: '名称长度在 1 到 20 个字符', trigger: 'blur' }
  ]
}

// 状态
const loading = ref(false)

// 处理取消
const handleCancel = () => {
  emit('cancel')
}

// 处理提交
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true

  try {
    const response = await fridgeStore.createFridge(formData.name)

    if (response.success) {
      ElMessage.success('创建成功')
      emit('success')
      // 重置表单
      formRef.value?.resetFields()
    } else {
      ElMessage.error(response.error || '创建失败')
    }
  } catch (error: any) {
    console.error('[冰箱表单] 创建失败', error)
    ElMessage.error(error.message || '网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fridge-form {
  padding: 0;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  padding: 12px 16px;
}

:deep(.el-input__prefix) {
  color: var(--text-secondary);
  font-size: 16px;
}

/* 按钮 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 600;
}
</style>
