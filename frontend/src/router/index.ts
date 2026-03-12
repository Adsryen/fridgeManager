import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// 路由懒加载配置
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "auth" */ '../views/Login.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "auth" */ '../views/Register.vue'),
    meta: { requiresAuth: false, title: '注册' }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue'),
    meta: { requiresAuth: false, title: '首页' }
  },
  {
    path: '/fridge',
    name: 'Fridge',
    component: () => import(/* webpackChunkName: "fridge" */ '../views/Fridge.vue'),
    meta: { requiresAuth: false, title: '冰箱管理' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import(/* webpackChunkName: "user" */ '../views/Profile.vue'),
    meta: { requiresAuth: false, title: '个人资料' }
  },
  {
    path: '/family',
    name: 'Family',
    component: () => import(/* webpackChunkName: "family" */ '../views/Family.vue'),
    meta: { requiresAuth: false, title: '家庭管理' }
  },
  {
    path: '/admin',
    name: 'Admin',
    redirect: '/admin/dashboard',
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import(/* webpackChunkName: "admin" */ '../views/admin/Dashboard.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, title: '管理员仪表板' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import(/* webpackChunkName: "admin" */ '../views/admin/Users.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, title: '用户管理' }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import(/* webpackChunkName: "admin" */ '../views/admin/Settings.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, title: '系统设置' }
      },
      {
        path: 'ai-settings',
        name: 'AdminAISettings',
        component: () => import(/* webpackChunkName: "admin" */ '../views/admin/AISettings.vue'),
        meta: { requiresAuth: true, requiresAdmin: true, title: 'AI设置' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "error" */ '../views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // 路由滚动行为
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
