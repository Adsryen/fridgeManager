import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Family, FamilyMember } from '@/types/models'
import * as familyApi from '@/api/family'

/**
 * 家庭状态管理 Store
 * 管理家庭列表、成员和相关操作
 */
export const useFamilyStore = defineStore('family', () => {
  // 状态
  const families = ref<Family[]>([])
  const currentFamily = ref<Family | null>(null)
  const members = ref<FamilyMember[]>([])
  const loading = ref(false)
  
  // 计算属性
  
  /**
   * 家庭数量
   */
  const familyCount = computed(() => families.value.length)
  
  /**
   * 当前家庭成员数量
   */
  const memberCount = computed(() => members.value.length)
  
  /**
   * 当前用户是否是家庭创建者
   * @param userId 当前用户 ID
   */
  const isOwner = computed(() => (userId: string) => {
    return currentFamily.value?.owner_id === userId
  })
  
  /**
   * 用户拥有的家庭列表
   * @param userId 当前用户 ID
   */
  const ownedFamilies = computed(() => (userId: string) => {
    return families.value.filter(family => family.owner_id === userId)
  })
  
  /**
   * 用户加入的家庭列表（非创建者）
   * @param userId 当前用户 ID
   */
  const joinedFamilies = computed(() => (userId: string) => {
    return families.value.filter(family => family.owner_id !== userId)
  })
  
  // 操作方法
  
  /**
   * 加载家庭列表
   * 从后端获取用户所属的所有家庭
   */
  async function loadFamilies() {
    loading.value = true
    try {
      const response = await familyApi.getFamilyList()
      if (response.success && response.data) {
        families.value = response.data
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 创建家庭
   * @param name 家庭名称
   */
  async function createFamily(name: string) {
    const response = await familyApi.createFamily(name)
    if (response.success) {
      // 重新加载家庭列表
      await loadFamilies()
    }
    return response
  }
  
  /**
   * 加入家庭
   * @param familyCode 家庭邀请码
   */
  async function joinFamily(familyCode: string) {
    const response = await familyApi.joinFamily(familyCode)
    if (response.success) {
      // 重新加载家庭列表
      await loadFamilies()
    }
    return response
  }
  
  /**
   * 离开家庭
   * @param familyId 家庭 ID
   */
  async function leaveFamily(familyId: string) {
    const response = await familyApi.leaveFamily(familyId)
    if (response.success) {
      // 从本地列表中移除
      families.value = families.value.filter(family => family._id !== familyId)
      // 如果离开的是当前家庭，清空当前家庭
      if (currentFamily.value?._id === familyId) {
        currentFamily.value = null
        members.value = []
      }
    }
    return response
  }
  
  /**
   * 加载家庭成员
   * @param familyId 家庭 ID
   */
  async function loadMembers(familyId: string) {
    loading.value = true
    try {
      const response = await familyApi.getFamilyMembers(familyId)
      if (response.success && response.data) {
        members.value = response.data
        // 更新当前家庭
        const family = families.value.find(f => f._id === familyId)
        if (family) {
          currentFamily.value = family
        }
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 移除家庭成员
   * @param familyId 家庭 ID
   * @param userId 用户 ID
   */
  async function removeMember(familyId: string, userId: string) {
    const response = await familyApi.removeFamilyMember(familyId, userId)
    if (response.success) {
      // 从本地成员列表中移除
      members.value = members.value.filter(member => member.user_id !== userId)
      // 更新家庭成员数量
      const family = families.value.find(f => f._id === familyId)
      if (family) {
        family.member_count = Math.max(0, family.member_count - 1)
      }
    }
    return response
  }
  
  /**
   * 更新家庭信息
   * @param familyId 家庭 ID
   * @param name 新名称
   */
  async function updateFamily(familyId: string, name: string) {
    const response = await familyApi.updateFamily(familyId, name)
    if (response.success) {
      // 更新本地家庭列表中的名称
      const family = families.value.find(f => f._id === familyId)
      if (family) {
        family.name = name
      }
      // 如果是当前家庭，也更新当前家庭
      if (currentFamily.value?._id === familyId) {
        currentFamily.value.name = name
      }
    }
    return response
  }
  
  /**
   * 删除家庭
   * @param familyId 家庭 ID
   */
  async function deleteFamily(familyId: string) {
    const response = await familyApi.deleteFamily(familyId)
    if (response.success) {
      // 从本地列表中移除
      families.value = families.value.filter(family => family._id !== familyId)
      // 如果删除的是当前家庭，清空当前家庭
      if (currentFamily.value?._id === familyId) {
        currentFamily.value = null
        members.value = []
      }
    }
    return response
  }
  
  /**
   * 设置当前家庭
   * @param familyId 家庭 ID
   */
  function setCurrentFamily(familyId: string) {
    const family = families.value.find(f => f._id === familyId)
    if (family) {
      currentFamily.value = family
    }
  }
  
  /**
   * 获取家庭共享冰箱
   * @param familyId 家庭 ID
   */
  async function getFamilyFridges(familyId: string) {
    return await familyApi.getFamilyFridges(familyId)
  }
  
  /**
   * 设置冰箱共享权限
   * @param fridgeId 冰箱 ID
   * @param isFamilyShared 是否家庭共享
   * @param isEditableByFamily 家庭成员是否可编辑
   */
  async function setFridgePermission(
    fridgeId: string,
    isFamilyShared: boolean,
    isEditableByFamily: boolean
  ) {
    return await familyApi.setFridgePermission(fridgeId, isFamilyShared, isEditableByFamily)
  }
  
  /**
   * 获取冰箱权限
   * @param fridgeId 冰箱 ID
   */
  async function getFridgePermission(fridgeId: string) {
    return await familyApi.getFridgePermission(fridgeId)
  }
  
  /**
   * 清空状态
   * 用户登出时调用
   */
  function clearState() {
    families.value = []
    currentFamily.value = null
    members.value = []
    loading.value = false
  }
  
  return {
    // 状态
    families,
    currentFamily,
    members,
    loading,
    // 计算属性
    familyCount,
    memberCount,
    isOwner,
    ownedFamilies,
    joinedFamilies,
    // 操作方法
    loadFamilies,
    createFamily,
    joinFamily,
    leaveFamily,
    loadMembers,
    removeMember,
    updateFamily,
    deleteFamily,
    setCurrentFamily,
    getFamilyFridges,
    setFridgePermission,
    getFridgePermission,
    clearState
  }
})
