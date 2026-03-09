<template>
  <div class="empty-state">
    <div class="empty-icon">
      <i :class="icon"></i>
    </div>
    <div class="empty-text">{{ text }}</div>
    <div v-if="$slots.action" class="empty-action">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  icon?: string
  text?: string
}

withDefaults(defineProps<Props>(), {
  icon: 'fas fa-inbox',
  text: '暂无数据'
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  color: var(--text-secondary);
  opacity: 0.5;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.empty-action {
  margin-top: 10px;
}
</style>
