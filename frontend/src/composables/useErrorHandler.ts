import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { AxiosError } from 'axios'

interface ErrorState {
  hasError: boolean
  message: string
  code?: string | number
}

/**
 * 错误处理 Hook
 * 提供统一的错误处理逻辑
 */
export function useErrorHandler() {
  const error = ref<ErrorState>({
    hasError: false,
    message: ''
  })

  /**
   * 处理错误
   * @param err 错误对象
   * @param showMessage 是否显示错误消息
   */
  const handleError = (err: unknown, showMessage: boolean = true) => {
    let message = '操作失败，请稍后重试'
    let code: string | number | undefined

    if (err instanceof Error) {
      message = err.message
    }

    // 处理 Axios 错误
    if (isAxiosError(err)) {
      const response = err.response
      if (response) {
        code = response.status
        const data = response.data as { error?: string; message?: string }
        message = data?.error || data?.message || message
      } else if (err.request) {
        message = '网络连接失败，请检查网络'
      }
    }

    error.value = {
      hasError: true,
      message,
      code
    }

    if (showMessage) {
      ElMessage.error(message)
    }

    // 记录错误到控制台（开发环境）
    if (import.meta.env.DEV) {
      console.error('Error:', err)
    }
  }

  /**
   * 清除错误状态
   */
  const clearError = () => {
    error.value = {
      hasError: false,
      message: ''
    }
  }

  /**
   * 类型守卫：判断是否为 Axios 错误
   */
  const isAxiosError = (error: unknown): error is AxiosError => {
    return (error as AxiosError).isAxiosError === true
  }

  return {
    error,
    handleError,
    clearError
  }
}
