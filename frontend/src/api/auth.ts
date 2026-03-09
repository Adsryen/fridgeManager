import http from './http'
import type { ApiResponse, LoginResponse } from '../types/api'
import type { User } from '../types/models'

/**
 * 认证 API 接口
 */

// 用户注册
export function register(username: string, email: string, password: string) {
  return http.post<ApiResponse>('/auth/register', {
    username,
    email,
    password
  })
}

// 用户登录
export function login(username: string, password: string) {
  return http.post<LoginResponse>('/auth/login', {
    username,
    password
  })
}

// 用户登出
export function logout() {
  return http.post<ApiResponse>('/auth/logout')
}

// 获取用户信息
export function getProfile() {
  return http.get<ApiResponse<User>>('/auth/profile')
}

// 更新用户信息
export function updateProfile(data: { email?: string; username?: string; theme?: string }) {
  return http.put<ApiResponse>('/auth/profile', data)
}

// 修改密码
export function changePassword(oldPassword: string, newPassword: string) {
  return http.post<ApiResponse>('/auth/change-password', {
    old_password: oldPassword,
    new_password: newPassword
  })
}

// 检查用户名是否可用
export function checkUsername(username: string) {
  return http.post<ApiResponse<{ available: boolean; message: string }>>('/auth/check-username', {
    username
  })
}

// 检查邮箱是否可用
export function checkEmail(email: string) {
  return http.post<ApiResponse<{ available: boolean; message: string }>>('/auth/check-email', {
    email
  })
}

// 忘记密码
export function forgotPassword(email: string) {
  return http.post<ApiResponse>('/auth/forgot-password', {
    email
  })
}

// 重置密码
export function resetPassword(token: string, password: string) {
  return http.post<ApiResponse>('/auth/reset-password', {
    token,
    password
  })
}
