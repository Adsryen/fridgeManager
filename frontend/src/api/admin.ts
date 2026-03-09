import http from './http'
import type { ApiResponse, StatsResponse } from '../types/api'
import type { User, SystemSettings } from '../types/models'

/**
 * 管理员 API 接口
 */

// 获取统计数据
export function getStats() {
  return http.get<StatsResponse>('/admin/stats')
}

// 获取所有用户
export function getAllUsers() {
  return http.get<ApiResponse<User[]>>('/admin/users')
}

// 获取用户详情
export function getUserDetail(userId: string) {
  return http.get<ApiResponse<User>>(`/admin/user/${userId}`)
}

// 切换用户状态（激活/禁用）
export function toggleUserStatus(userId: string) {
  return http.post<ApiResponse>(`/admin/user/${userId}/toggle-status`)
}

// 切换管理员权限
export function toggleAdminStatus(userId: string) {
  return http.post<ApiResponse>(`/admin/user/${userId}/toggle-admin`)
}

// 重置用户密码
export function resetUserPassword(userId: string, password: string) {
  return http.post<ApiResponse>(`/admin/user/${userId}/reset-password`, {
    password
  })
}

// 删除用户
export function deleteUser(userId: string) {
  return http.post<ApiResponse>(`/admin/user/${userId}/delete`)
}

// 获取系统设置
export function getSettings() {
  return http.get<ApiResponse<SystemSettings>>('/admin/settings')
}

// 保存系统设置
export function saveSettings(settings: Partial<SystemSettings>) {
  return http.post<ApiResponse>('/admin/settings/save', {
    settings
  })
}

// 测试 AI 连接
export function testAIConnection(apiBase: string, apiKey: string) {
  return http.post<ApiResponse>('/admin/ai/test-connection', {
    api_base: apiBase,
    api_key: apiKey
  })
}

// 获取 AI 模型列表
export function listAIModels(apiBase: string, apiKey: string) {
  return http.post<ApiResponse<{ models: string[] }>>('/admin/ai/list-models', {
    api_base: apiBase,
    api_key: apiKey
  })
}

// 清理过期物品
export function cleanExpiredItems() {
  return http.post<ApiResponse<{ count: number }>>('/admin/maintenance/clean-expired')
}

// 备份数据库
export function backupDatabase() {
  return http.get('/admin/maintenance/backup', {
    responseType: 'blob'
  })
}
