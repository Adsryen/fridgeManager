import http from './http'
import type { ApiResponse, FridgeListResponse } from '../types/api'
import type { Fridge } from '../types/models'

/**
 * 冰箱 API 接口
 */

// 获取冰箱列表
export function getFridgeList() {
  return http.get<FridgeListResponse>('/fridge/list')
}

// 获取单个冰箱信息
export function getFridge(fridgeId: string) {
  return http.get<ApiResponse<Fridge>>(`/fridge/${fridgeId}`)
}

// 创建冰箱
export function createFridge(name: string) {
  return http.post<ApiResponse<{ fridge: Fridge }>>('/fridge/create', {
    name
  })
}

// 切换当前冰箱
export function switchFridge(fridgeId: string) {
  return http.post<ApiResponse>('/fridge/switch', {
    fridge_id: fridgeId
  })
}

// 重命名冰箱
export function renameFridge(fridgeId: string, name: string) {
  return http.put<ApiResponse>(`/fridge/${fridgeId}/rename`, {
    name
  })
}

// 删除冰箱
export function deleteFridge(fridgeId: string) {
  return http.delete<ApiResponse>(`/fridge/${fridgeId}`)
}
