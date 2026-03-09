import { ref, onMounted } from 'vue'
import { updateProfile } from '@/api/auth'

export type Theme = 'light' | 'dark'

const THEME_STORAGE_KEY = 'theme-preference'

// 全局主题状态
const currentTheme = ref<Theme>('light')

export function useTheme() {
  /**
   * 切换主题
   */
  const toggleTheme = async () => {
    const newTheme: Theme = currentTheme.value === 'light' ? 'dark' : 'light'
    await setTheme(newTheme)
  }

  /**
   * 设置主题
   */
  const setTheme = async (theme: Theme) => {
    currentTheme.value = theme
    
    // 更新 HTML 根元素的 data-theme 属性
    document.documentElement.setAttribute('data-theme', theme)
    
    // 保存到 localStorage
    localStorage.setItem(THEME_STORAGE_KEY, theme)
    
    // 同步主题设置到后端用户配置（如果用户已登录）
    try {
      const token = localStorage.getItem('token')
      if (token) {
        await updateProfile({ theme_preference: theme } as any)
      }
    } catch (error) {
      console.error('[useTheme] 同步主题到后端失败', error)
      // 不影响前端主题切换，静默失败
    }
  }

  /**
   * 从 localStorage 加载主题偏好
   */
  const loadTheme = () => {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) as Theme | null
    
    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      // 不使用 await，因为这是初始化加载
      setTheme(savedTheme)
    } else {
      // 默认使用浅色主题
      setTheme('light')
    }
  }

  /**
   * 初始化主题
   */
  onMounted(() => {
    loadTheme()
  })

  return {
    currentTheme,
    toggleTheme,
    setTheme,
    loadTheme
  }
}
