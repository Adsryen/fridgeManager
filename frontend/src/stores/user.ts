import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/models'
import * as authApi from '@/api/auth'

/**
 * 用户状态管理 Store
 * 管理用户认证状态、用户信息和相关操作
 */
export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  
  // 操作方法
  
  /**
   * 用户登录
   * @param username 用户名
   * @param password 密码
   * @returns 登录响应
   */
  async function login(username: string, password: string) {
    const response = await authApi.login(username, password)
    if (response.success) {
      token.value = response.token
      user.value = response.user as User
      localStorage.setItem('token', response.token)
      localStorage.setItem('user', JSON.stringify(response.user))
    }
    return response
  }
  
  /**
   * 用户登出
   * 清除本地存储和状态
   */
  async function logout() {
    try {
      await authApi.logout()
    } catch (error) {
      // 即使后端请求失败，也要清除本地状态
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
  
  /**
   * 获取用户信息
   * 从后端获取最新的用户信息
   */
  async function fetchProfile() {
    const response = await authApi.getProfile()
    if (response.success && response.data) {
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    }
    return response
  }
  
  /**
   * 更新用户信息
   * @param data 要更新的用户数据
   */
  async function updateProfile(data: { email?: string; username?: string }) {
    const response = await authApi.updateProfile(data)
    if (response.success) {
      // 更新成功后重新获取用户信息
      await fetchProfile()
    }
    return response
  }
  
  /**
   * 修改密码
   * @param oldPassword 旧密码
   * @param newPassword 新密码
   */
  async function changePassword(oldPassword: string, newPassword: string) {
    return await authApi.changePassword(oldPassword, newPassword)
  }
  
  /**
   * 从本地存储初始化用户状态
   * 应用启动时调用
   */
  function initFromStorage() {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    
    if (storedUser && storedToken) {
      try {
        user.value = JSON.parse(storedUser)
        token.value = storedToken
      } catch (error) {
        console.error('Failed to parse stored user data:', error)
        // 如果解析失败，清除无效数据
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      }
    }
  }
  
  /**
   * 更新用户主题偏好
   * @param theme 主题类型
   */
  function updateTheme(theme: 'light' | 'dark') {
    if (user.value) {
      user.value.theme_preference = theme
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }
  
  return {
    // 状态
    user,
    token,
    // 计算属性
    isLoggedIn,
    isAdmin,
    // 操作方法
    login,
    logout,
    fetchProfile,
    updateProfile,
    changePassword,
    initFromStorage,
    updateTheme
  }
})
