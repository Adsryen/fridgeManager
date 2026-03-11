import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import './styles/index.css'
import App from './App.vue'
import router from './router'
import './router/guards'
import { useUserStore } from './stores/user'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 异步初始化用户状态
const userStore = useUserStore()
userStore.initFromStorage().then(() => {
  console.log('用户状态初始化完成')
}).catch((error) => {
  console.error('用户状态初始化失败:', error)
})

app.mount('#app')
