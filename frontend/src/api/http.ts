import axios, { type AxiosInstance, AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router/index'

// 请求重试配置
const MAX_RETRY_COUNT = 3
const RETRY_DELAY = 1000

// 请求队列（用于防止重复请求）
const pendingRequests = new Map<string, AbortController>()

// 自定义 HTTP 客户端接口，返回类型直接是 T 而不是 AxiosResponse<T>
interface HttpClient {
  get<T = any>(url: string, config?: any): Promise<T>
  post<T = any>(url: string, data?: any, config?: any): Promise<T>
  put<T = any>(url: string, data?: any, config?: any): Promise<T>
  delete<T = any>(url: string, config?: any): Promise<T>
}

/**
 * 生成请求的唯一标识
 */
function generateRequestKey(config: InternalAxiosRequestConfig): string {
  const { method, url, params, data } = config
  return [method, url, JSON.stringify(params), JSON.stringify(data)].join('&')
}

/**
 * 添加请求到队列
 */
function addPendingRequest(config: InternalAxiosRequestConfig): void {
  const requestKey = generateRequestKey(config)
  
  // 如果已存在相同请求，取消之前的请求
  if (pendingRequests.has(requestKey)) {
    const controller = pendingRequests.get(requestKey)
    controller?.abort()
  }
  
  // 创建新的 AbortController
  const controller = new AbortController()
  config.signal = controller.signal
  pendingRequests.set(requestKey, controller)
}

/**
 * 从队列中移除请求
 */
function removePendingRequest(config: InternalAxiosRequestConfig): void {
  const requestKey = generateRequestKey(config)
  pendingRequests.delete(requestKey)
}

/**
 * 请求重试逻辑
 */
async function retryRequest(error: AxiosError, retryCount: number = 0): Promise<any> {
  const config = error.config as InternalAxiosRequestConfig & { __retryCount?: number }
  
  if (!config || retryCount >= MAX_RETRY_COUNT) {
    return Promise.reject(error)
  }
  
  config.__retryCount = retryCount + 1
  
  // 延迟后重试
  await new Promise(resolve => setTimeout(resolve, RETRY_DELAY * retryCount))
  
  return axiosInstance.request(config)
}

// 创建 Axios 实例
const axiosInstance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加 JWT Token 和防重复请求
axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加 JWT Token
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 防止重复请求（GET 请求）
    if (config.method?.toLowerCase() === 'get') {
      addPendingRequest(config)
    }
    
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一错误处理
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    // 移除已完成的请求
    removePendingRequest(response.config as InternalAxiosRequestConfig)
    
    // 直接返回 data，这样调用方就不需要再访问 response.data
    return response.data
  },
  async (error: AxiosError) => {
    const config = error.config as InternalAxiosRequestConfig
    
    // 移除失败的请求
    if (config) {
      removePendingRequest(config)
    }
    
    // 如果是取消的请求，不显示错误
    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }
    
    // 处理网络错误，尝试重试
    if (!error.response && error.code === 'ERR_NETWORK') {
      const retryCount = (config as any)?.__retryCount || 0
      if (retryCount < MAX_RETRY_COUNT) {
        return retryRequest(error, retryCount)
      }
    }
    
    if (error.response) {
      const status = error.response.status
      const data = error.response.data as { error?: string; message?: string }
      
      switch (status) {
        case 401:
          // Token 无效或过期，清除本地存储并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          ElMessage.error('登录已过期，请重新登录')
          router.push('/login')
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
        case 502:
        case 503:
        case 504:
          ElMessage.error('服务器错误，请稍后重试')
          break
        default:
          ElMessage.error(data?.error || data?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    // 开发环境下打印错误详情
    if (import.meta.env.DEV) {
      console.error('API Error:', error)
    }
    
    return Promise.reject(error)
  }
)

// 导出类型化的 HTTP 客户端
const http = axiosInstance as unknown as HttpClient

export default http
