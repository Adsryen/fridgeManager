<template>
  <div class="add-method-selector">
    <div class="add-method-grid">
      <!-- OCR识别 -->
      <div class="add-method-card" @click="handleSelect('ocr')">
        <span v-if="!isLoggedIn" class="login-badge">需登录</span>
        <div class="add-method-icon ocr">
          <i class="fas fa-camera"></i>
        </div>
        <div class="add-method-info">
          <div class="add-method-title">文字识别</div>
          <div class="add-method-desc">拍照识别</div>
        </div>
      </div>

      <!-- 手动添加 -->
      <div class="add-method-card" @click="handleSelect('manual')">
        <div class="add-method-icon manual">
          <i class="fas fa-edit"></i>
        </div>
        <div class="add-method-info">
          <div class="add-method-title">手动添加</div>
          <div class="add-method-desc">手动填写</div>
        </div>
      </div>

      <!-- AI对话 -->
      <div class="add-method-card full-width" @click="handleSelect('ai')">
        <span v-if="!isLoggedIn" class="login-badge">需登录</span>
        <div class="add-method-icon ai">
          <i class="fas fa-comments"></i>
        </div>
        <div class="add-method-info">
          <div class="add-method-title">AI对话</div>
          <div class="add-method-desc">与AI对话添加物品</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '../../stores/user'
import { computed } from 'vue'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)

const emit = defineEmits<{
  select: [method: 'ocr' | 'manual' | 'ai']
}>()

const handleSelect = (method: 'ocr' | 'manual' | 'ai') => {
  emit('select', method)
}
</script>

<style scoped>
.add-method-selector {
  padding: 0;
}

.add-method-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.add-method-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 10px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.add-method-card.full-width {
  grid-column: 1 / -1;
  flex-direction: row;
  justify-content: flex-start;
  padding: 12px 14px;
}

.add-method-card:active {
  transform: scale(0.96);
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.login-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  padding: 3px 7px;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: white;
  font-size: 10px;
  font-weight: 600;
  border-radius: 8px;
  z-index: 1;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.add-method-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  flex-shrink: 0;
}

.add-method-icon.ocr {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.add-method-icon.manual {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.add-method-icon.ai {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.add-method-info {
  flex: 1;
  text-align: center;
}

.add-method-card.full-width .add-method-info {
  text-align: left;
}

.add-method-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.add-method-desc {
  font-size: 11px;
  color: var(--text-secondary);
}
</style>
