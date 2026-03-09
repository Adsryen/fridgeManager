import { ref, computed, onMounted } from 'vue'

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
    
    // 主题设置仅在前端存储，不同步到后端
    // 如果未来需要跨设备同步主题，可以通过用户设置接口实现
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
    isDark: computed(() => currentTheme.value === 'dark'),
    toggleTheme,
    setTheme,
    loadTheme
  }
}
