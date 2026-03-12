<template>
  <div class="global-add-container">
    <!-- 添加方式选择气泡菜单 -->
    <BubbleMenu v-model="showAddMethodSelector">
      <AddMethodSelector @select="handleAddMethodSelect" />
    </BubbleMenu>

    <!-- 物品表单抽屉 -->
    <Drawer v-model="showItemForm" title="添加物品">
      <ItemForm @success="handleItemSuccess" @cancel="showItemForm = false" />
    </Drawer>

    <!-- OCR上传抽屉 -->
    <Drawer v-model="showOCRUpload" title="文字识别">
      <OCRUpload @success="handleItemSuccess" @cancel="showOCRUpload = false" />
    </Drawer>

    <!-- AI 对话抽屉 -->
    <Drawer v-model="showChatDialog" title="AI 助手">
      <ChatDialog />
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useItemStore } from '../../stores/item'
import BubbleMenu from './BubbleMenu.vue'
import Drawer from './Drawer.vue'
import ItemForm from '../item/ItemForm.vue'
import ChatDialog from '../ai/ChatDialog.vue'
import OCRUpload from '../ai/OCRUpload.vue'
import AddMethodSelector from '../item/AddMethodSelector.vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const itemStore = useItemStore()

const showAddMethodSelector = ref(false)
const showItemForm = ref(false)
const showOCRUpload = ref(false)
const showChatDialog = ref(false)

// 暴露给父组件的方法
const openAddMenu = () => {
  showAddMethodSelector.value = true
}

const handleAddMethodSelect = (method: 'ocr' | 'manual' | 'ai') => {
  showAddMethodSelector.value = false
  
  // OCR 和 AI 需要登录
  if ((method === 'ocr' || method === 'ai') && !userStore.isLoggedIn) {
    ElMessage.warning('该功能需要登录后使用')
    router.push('/login')
    return
  }
  
  if (method === 'manual') {
    showItemForm.value = true
  } else if (method === 'ocr') {
    showOCRUpload.value = true
  } else if (method === 'ai') {
    showChatDialog.value = true
  }
}

const handleItemSuccess = () => {
  showItemForm.value = false
  showOCRUpload.value = false
  itemStore.loadItems()
}

// 暴露方法给父组件
defineExpose({
  openAddMenu
})
</script>

<style scoped>
.global-add-container {
  /* 这个组件主要用于管理弹窗，不需要特殊样式 */
}
</style>