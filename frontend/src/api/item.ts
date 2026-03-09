import http from './http'
import type { ApiResponse } from '../types/api'
import type { Item, OCRResult, ChatMessage } from '../types/models'

/**
 * 物品 API 接口
 */

// 获取所有物品
export function getAllItems(fridgeId: string = 'public') {
  return http.get<ApiResponse<Item[]>>('/item/total', {
    params: { fridge_id: fridgeId }
  })
}

// 获取单个物品
export function getItem(itemId: string) {
  return http.get<ApiResponse<Item>>(`/item/getone/${itemId}`)
}

// 添加物品
export function addItem(data: {
  name: string
  quantity: number
  expire_date: string
  place: string
  type: string
  fridge_id?: string
}) {
  return http.post<ApiResponse>('/item/insert', {
    itemName: data.name,
    itemNum: data.quantity,
    itemDate: data.expire_date,
    itemPlace: data.place,
    itemType: data.type,
    fridge_id: data.fridge_id || 'public'
  })
}

// 批量添加物品
export function batchAddItems(items: Array<{
  name: string
  quantity: number
  unit?: string
  expire_date: string
  place: string
  type: string
}>, fridgeId: string = 'public') {
  return http.post<ApiResponse<{
    added: number
    failed: number
    total: number
    items: Array<{ id: string; name: string; quantity: number }>
    failed_items?: Array<{ name: string; error: string }>
    validation_errors?: Array<{ index: number; errors: string[] }>
  }>>('/item/batch-insert', {
    items,
    fridge_id: fridgeId
  })
}

// 更新物品
export function updateItem(itemId: string, data: {
  name?: string
  quantity?: number
  expire_date?: string
  place?: string
  type?: string
}) {
  return http.put<ApiResponse>('/item/update', {
    itemId,
    itemName: data.name,
    itemNum: data.quantity,
    itemDate: data.expire_date,
    itemPlace: data.place,
    itemType: data.type
  })
}

// 删除物品
export function deleteItem(itemId: string) {
  return http.delete<ApiResponse>('/item/delete', {
    data: { itemId }
  })
}

// 搜索物品
export function searchItems(keyword: string, fridgeId: string = 'public') {
  return http.post<ApiResponse<Item[]>>('/item/search', {
    text: keyword,
    fridge_id: fridgeId
  })
}

// 获取过期物品
export function getExpiredItems(days: number = 0) {
  return http.get<ApiResponse<Item[]>>(`/item/statebad/${days}`)
}

// OCR 识别
export function ocrRecognize(imageData: string, useVision: boolean = false) {
  return http.post<ApiResponse<OCRResult>>('/item/ocr', {
    image: imageData,
    use_vision: useVision
  })
}

// AI 对话（流式输出）
export function aiChat(messages: ChatMessage[]) {
  // 注意：这是一个 SSE 流式接口，需要特殊处理
  // 返回的是 EventSource 或 fetch 的 ReadableStream
  return http.post('/item/ai-chat', {
    messages
  })
}

// 语音转文字
export function voiceToText(audioData: string) {
  return http.post<ApiResponse<{ text: string }>>('/item/voice-to-text', {
    audio: audioData
  })
}

// 获取对话历史
export function getChatHistory() {
  return http.get<ApiResponse<ChatMessage[]>>('/item/chat-history')
}

// 清空对话历史
export function clearChatHistory() {
  return http.post<ApiResponse>('/item/chat-history/clear')
}
