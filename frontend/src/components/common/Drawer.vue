<template>
  <div class="drawer-overlay" :class="{ active: modelValue }" @click="handleOverlayClick">
    <div class="drawer-content" :class="{ 'full-height': fullHeight }" @click.stop>
      <div class="drawer-header">
        <h5>{{ title }}</h5>
        <button class="close-btn" @click="handleClose">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="drawer-body">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  title?: string
  fullHeight?: boolean
  closeOnClickOutside?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  fullHeight: false,
  closeOnClickOutside: true
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'close': []
}>()

const handleClose = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleOverlayClick = () => {
  if (props.closeOnClickOutside) {
    handleClose()
  }
}
</script>

<style scoped>
.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>
