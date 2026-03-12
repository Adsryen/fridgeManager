import http from './http'
import type { ApiResponse } from '../types/api'

/**
 * 物品历史记录 API 接口
 */

// 获取冰箱的物品历史记录
export function getFridgeHistory(fridgeId: string, limit?: number) {
  return http.get<ApiResponse<any[]>>(`/item-history/fridge/${fridgeId}`, {
    params: { limit }
  })
}

// 获取特定物品的历史记录
export function getItemHistory(itemId: string) {
  return http.get<ApiResponse<any[]>>(`/item-history/item/${itemId}`)
}

// 获取已删除的物品列表
export function getDeletedItems(fridgeId: string, limit?: number) {
  return http.get<ApiResponse<any[]>>(`/item-history/deleted/${fridgeId}`, {
    params: { limit }
  })
}

// 恢复已删除的物品
export function restoreItem(historyId: string) {
  return http.post<ApiResponse>(`/item-history/restore/${historyId}`)
}