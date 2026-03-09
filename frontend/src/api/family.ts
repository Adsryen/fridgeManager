import http from './http'
import type { ApiResponse } from '../types/api'
import type { Family, FamilyMember, Fridge, FridgePermission } from '../types/models'

/**
 * 家庭 API 接口
 */

// 创建家庭
export function createFamily(name: string) {
  return http.post<ApiResponse<{
    family_id: string
    family_code: string
  }>>('/family/create', {
    name
  })
}

// 加入家庭
export function joinFamily(familyCode: string) {
  return http.post<ApiResponse>('/family/join', {
    family_code: familyCode
  })
}

// 离开家庭
export function leaveFamily(familyId: string) {
  return http.post<ApiResponse>(`/family/leave/${familyId}`)
}

// 获取家庭列表
export function getFamilyList() {
  return http.get<ApiResponse<Family[]>>('/family/list')
}

// 获取家庭成员
export function getFamilyMembers(familyId: string) {
  return http.get<ApiResponse<FamilyMember[]>>(`/family/${familyId}/members`)
}

// 更新家庭信息
export function updateFamily(familyId: string, name: string) {
  return http.put<ApiResponse>(`/family/${familyId}`, {
    name
  })
}

// 删除家庭
export function deleteFamily(familyId: string) {
  return http.delete<ApiResponse>(`/family/${familyId}`)
}

// 移除家庭成员
export function removeFamilyMember(familyId: string, userId: string) {
  return http.delete<ApiResponse>(`/family/${familyId}/members/${userId}`)
}

// 获取家庭共享冰箱
export function getFamilyFridges(familyId: string) {
  return http.get<ApiResponse<Fridge[]>>(`/family/${familyId}/fridges`)
}

// 设置冰箱权限
export function setFridgePermission(
  fridgeId: string,
  isFamilyShared: boolean,
  isEditableByFamily: boolean
) {
  return http.post<ApiResponse>(`/family/fridge/${fridgeId}/permission`, {
    is_family_shared: isFamilyShared,
    is_editable_by_family: isEditableByFamily
  })
}

// 获取冰箱权限
export function getFridgePermission(fridgeId: string) {
  return http.get<ApiResponse<FridgePermission>>(`/family/fridge/${fridgeId}/permission`)
}
