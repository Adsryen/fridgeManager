<template>
  <div class="add-method-selector">
    <div class="add-method-grid">
      <!-- OCR识别 -->
      <div class="add-method-card" @click="handleSelect('ocr')">
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
const emit = defineEmits<{
  select: [method: 'ocr' | 'manual' | 'ai']
}>()

const handleSelect = (method: 'ocr' | 'manual' | 'ai') => {
  emit('select', method)
}
</script>

<style scoped>
.add-method-selector {
  padding: 24px;
}

.add-method-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.add-method-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px;
  background: var(--bg-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.add-method-card.full-width {
  grid-column: 1 / -1;
  flex-direction: row;
  justify-content: flex-start;
}

.add-method-card:active {
  transform: scale(0.98);
  border-color: var(--primary-color);
}

.add-method-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
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
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 3px;
}

.add-method-desc {
  font-size: 11px;
  color: var(--text-secondary);
}

.add-method-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 3px 8px;
  background: var(--danger-color);
  color: white;
  font-size: 9px;
  font-weight: 600;
  border-radius: 10px;
}
</style>
