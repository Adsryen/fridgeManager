<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <p>页面未找到</p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--el-bg-color);
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 120px;
  font-weight: bold;
  color: var(--el-color-primary);
  margin: 0;
}

.not-found-content p {
  font-size: 24px;
  color: var(--el-text-color-regular);
  margin: 20px 0 40px;
}
</style>
