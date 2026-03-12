<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useTheme } from './composables/useTheme'
import GlobalAddButton from './components/common/GlobalAddButton.vue'
import { ref, provide } from 'vue'

// 初始化主题
const { loadTheme } = useTheme()
loadTheme()

// 全局添加按钮引用
const globalAddButtonRef = ref()

// 提供全局添加方法
const openGlobalAddMenu = () => {
  if (globalAddButtonRef.value) {
    globalAddButtonRef.value.openAddMenu()
  }
}

// 向子组件提供全局添加方法
provide('openGlobalAddMenu', openGlobalAddMenu)
</script>

<template>
  <div id="app">
    <RouterView />
    <!-- 全局添加按钮组件 -->
    <GlobalAddButton ref="globalAddButtonRef" />
  </div>
</template>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
