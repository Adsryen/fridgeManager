<template>
  <div class="loading-container" :class="{ 'loading-fullscreen': fullscreen }">
    <div class="loading-spinner">
      <div class="spinner"></div>
    </div>
    <div v-if="text" class="loading-text">{{ text }}</div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  text?: string
  fullscreen?: boolean
}

withDefaults(defineProps<Props>(), {
  text: '',
  fullscreen: false
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.loading-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  z-index: 9999;
}

[data-theme="dark"] .loading-fullscreen {
  background: rgba(0, 0, 0, 0.9);
}

.loading-spinner {
  margin-bottom: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 8px;
}
</style>
