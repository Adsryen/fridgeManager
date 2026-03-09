<template>
  <div class="item-form">
    <el-form ref="formRef" :model="formData" :rules="formRules" label-position="top">
      <!-- 物品名称 -->
      <el-form-item label="物品名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入物品名称"
          clearable
        >
          <template #prefix>
            <i class="fas fa-tag"></i>
          </template>
        </el-input>
      </el-form-item>

      <!-- 数量和单位 -->
      <div class="form-row">
        <el-form-item label="数量" prop="quantity" class="form-col">
          <el-input-number
            v-model="formData.quantity"
            :min="1"
            :max="9999"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="单位" prop="unit" class="form-col">
          <el-select v-model="formData.unit" placeholder="选择单位">
            <el-option label="个" value="个" />
            <el-option label="袋" value="袋" />
            <el-option label="盒" value="盒" />
            <el-option label="瓶" value="瓶" />
            <el-option label="罐" value="罐" />
            <el-option label="包" value="包" />
            <el-option label="斤" value="斤" />
            <el-option label="克" value="克" />
            <el-option label="千克" value="千克" />
            <el-option label="升" value="升" />
            <el-option label="毫升" value="毫升" />
          </el-select>
        </el-form-item>
      </div>

      <!-- 过期日期 -->
      <el-form-item label="过期日期" prop="expire_date">
        <el-date-picker
          v-model="formData.expire_date"
          type="date"
          placeholder="选择过期日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        >
          <template #prefix>
            <i class="fas fa-calendar-alt"></i>
          </template>
        </el-date-picker>
      </el-form-item>

      <!-- 存放位置 -->
      <el-form-item label="存放位置" prop="place">
        <el-radio-group v-model="formData.place" class="place-radio-group">
          <el-radio-button value="cold">
            <i class="fas fa-snowflake"></i>
            <span>冷藏</span>
          </el-radio-button>
          <el-radio-button value="frozen">
            <i class="fas fa-icicles"></i>
            <span>冷冻</span>
          </el-radio-button>
          <el-radio-button value="normal">
            <i class="fas fa-temperature-high"></i>
            <span>常温</span>
          </el-radio-button>
        </el-radio-group>
      </el-form-item>

      <!-- 物品类型 -->
      <el-form-item label="物品类型" prop="type">
        <el-select v-model="formData.type" placeholder="选择物品类型">
          <el-option label="蔬菜" value="蔬菜">
            <i class="fas fa-carrot"></i>
            <span style="margin-left: 8px">蔬菜</span>
          </el-option>
          <el-option label="水果" value="水果">
            <i class="fas fa-apple-alt"></i>
            <span style="margin-left: 8px">水果</span>
          </el-option>
          <el-option label="肉类" value="肉类">
            <i class="fas fa-drumstick-bite"></i>
            <span style="margin-left: 8px">肉类</span>
          </el-option>
          <el-option label="海鲜" value="海鲜">
            <i class="fas fa-fish"></i>
            <span style="margin-left: 8px">海鲜</span>
          </el-option>
          <el-option label="饮料" value="饮料">
            <i class="fas fa-glass-whiskey"></i>
            <span style="margin-left: 8px">饮料</span>
          </el-option>
          <el-option label="调味品" value="调味品">
            <i class="fas fa-pepper-hot"></i>
            <span style="margin-left: 8px">调味品</span>
          </el-option>
          <el-option label="面包糕点" value="面包糕点">
            <i class="fas fa-bread-slice"></i>
            <span style="margin-left: 8px">面包糕点</span>
          </el-option>
          <el-option label="乳制品" value="乳制品">
            <i class="fas fa-cheese"></i>
            <span style="margin-left: 8px">乳制品</span>
          </el-option>
          <el-option label="速食" value="速食">
            <i class="fas fa-pizza-slice"></i>
            <span style="margin-left: 8px">速食</span>
          </el-option>
          <el-option label="其他" value="其他">
            <i class="fas fa-box"></i>
            <span style="margin-left: 8px">其他</span>
          </el-option>
        </el-select>
      </el-form-item>

      <!-- 按钮 -->
      <div class="form-actions">
        <el-button @click="handleCancel" size="large" style="flex: 1">
          取消
        </el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading" size="large" style="flex: 1">
          {{ mode === 'add' ? '添加' : '保存' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useItemStore } from '@/stores/item'
import type { Item } from '@/types/models'

interface Props {
  item?: Item
  mode?: 'add' | 'edit'
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'add'
})

const emit = defineEmits<{
  success: []
  cancel: []
}>()

const itemStore = useItemStore()

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive({
  name: '',
  quantity: 1,
  unit: '个',
  expire_date: '',
  place: 'cold',
  type: '其他'
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入物品名称', trigger: 'blur' },
    { min: 1, max: 50, message: '名称长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ],
  expire_date: [
    { required: true, message: '请选择过期日期', trigger: 'change' }
  ],
  place: [
    { required: true, message: '请选择存放位置', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择物品类型', trigger: 'change' }
  ]
}

// 状态
const loading = ref(false)

// 监听 item 变化，用于编辑模式
watch(() => props.item, (newItem) => {
  if (newItem && props.mode === 'edit') {
    formData.name = newItem.name
    formData.quantity = newItem.num
    formData.unit = newItem.unit || '个'
    formData.expire_date = newItem.expire_date
    formData.place = newItem.place
    formData.type = newItem.type
  }
}, { immediate: true })

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
    let response

    if (props.mode === 'add') {
      // 添加物品
      response = await itemStore.addItem({
        name: formData.name,
        quantity: formData.quantity,
        expire_date: formData.expire_date,
        place: formData.place,
        type: formData.type
      })
    } else {
      // 编辑物品
      if (!props.item) {
        ElMessage.error('物品信息不存在')
        return
      }
      response = await itemStore.updateItem(props.item._id, {
        name: formData.name,
        quantity: formData.quantity,
        expire_date: formData.expire_date,
        place: formData.place,
        type: formData.type
      })
    }

    if (response.success) {
      emit('success')
      // 重置表单
      if (props.mode === 'add') {
        formRef.value?.resetFields()
      }
    } else {
      ElMessage.error(response.error || '操作失败')
    }
  } catch (error: any) {
    console.error('[物品表单] 提交失败', error)
    ElMessage.error(error.message || '网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.item-form {
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

:deep(.el-select) {
  width: 100%;
}

:deep(.el-date-picker) {
  width: 100%;
}

/* 表单行 */
.form-row {
  display: flex;
  gap: 12px;
}

.form-col {
  flex: 1;
}

/* 存放位置单选按钮组 */
.place-radio-group {
  width: 100%;
  display: flex;
  gap: 8px;
}

:deep(.el-radio-button) {
  flex: 1;
}

:deep(.el-radio-button__inner) {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border-radius: 8px;
}

:deep(.el-radio-button__inner i) {
  font-size: 20px;
}

:deep(.el-radio-button__inner span) {
  font-size: 13px;
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
