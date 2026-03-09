import { ref, type Ref } from 'vue'
import { useErrorHandler } from './useErrorHandler'

/**
 * 异步操作 Hook
 * 提供统一的异步操作状态管理
 */
export function useAsync<T>() {
  const data = ref<T | null>(null) as Ref<T | null>
  const loading = ref(false)
  const error = ref<Error | null>(null)
  const { handleError } = useErrorHandler()

  /**
   * 执行异步操作
   * @param asyncFn 异步函数
   * @param showError 是否显示错误消息
   */
  const execute = async (
    asyncFn: () => Promise<T>,
    showError: boolean = true
  ): Promise<T | null> => {
    loading.value = true
    error.value = null

    try {
      const result = await asyncFn()
      data.value = result
      return result
    } catch (err) {
      error.value = err as Error
      if (showError) {
        handleError(err)
      }
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 重置状态
   */
  const reset = () => {
    data.value = null
    loading.value = false
    error.value = null
  }

  return {
    data,
    loading,
    error,
    execute,
    reset
  }
}
