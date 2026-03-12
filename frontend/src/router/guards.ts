import router from './index'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

/**
 * 全局前置守卫
 * 检查路由的认证和权限要求
 */
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      ElMessage.warning('请先登录')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin) {
    if (!userStore.isAdmin) {
      ElMessage.error('权限不足')
      next('/')
      return
    }
  }
  
  // 如果已登录用户访问登录/注册页，重定向到首页
  if ((to.path === '/login' || to.path === '/register') && userStore.isLoggedIn) {
    next('/')
    return
  }
  
  next()
})

/**
 * 全局后置钩子
 * 设置页面标题
 */
router.afterEach((to) => {
  // 设置页面标题
  const title = to.meta.title as string
  document.title = title ? `${title} - 冰箱里面还有啥` : '冰箱里面还有啥'
})
