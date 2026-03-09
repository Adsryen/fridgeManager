// API 响应类型定义

// 通用 API 响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
  details?: any
}

// 分页响应类型
export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  total: number
  page: number
  page_size: number
}

// 登录响应
export interface LoginResponse {
  success: boolean
  token: string
  user: {
    _id: string
    username: string
    email: string
    is_admin: boolean
  }
  error?: string
  message?: string
}

// 冰箱列表响应
export interface FridgeListResponse {
  success: boolean
  my_fridges: any[]
  shared_fridges: any[]
}

// 统计数据响应
export interface StatsResponse {
  success: boolean
  data: {
    total_users: number
    total_items: number
    total_fridges: number
    active_users: number
  }
}
