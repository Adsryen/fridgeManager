<template>
  <Teleport to="body">
    <Transition name="bubble-fade">
      <div v-if="modelValue" class="bubble-menu-overlay" @click="handleClose">
        <Transition name="bubble-scale">
          <div v-if="modelValue" class="bubble-menu-content" @click.stop>
            <div class="bubble-arrow"></div>
            <slot></slot>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const handleClose = () => {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.bubble-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 9998;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 70px;
}

.bubble-menu-content {
  position: relative;
  background: var(--card-bg);
  border-radius: 20px;
  padding: 20px;
  max-width: 90%;
  width: 340px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  margin-bottom: 10px;
}

.bubble-arrow {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid var(--card-bg);
}

/* 淡入淡出动画 */
.bubble-fade-enter-active,
.bubble-fade-leave-active {
  transition: opacity 0.25s ease;
}

.bubble-fade-enter-from,
.bubble-fade-leave-to {
  opacity: 0;
}

/* 缩放动画 */
.bubble-scale-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.bubble-scale-leave-active {
  transition: all 0.2s ease;
}

.bubble-scale-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.bubble-scale-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(10px);
}
</style>
