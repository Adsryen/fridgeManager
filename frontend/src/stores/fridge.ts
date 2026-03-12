import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Fridge } from '@/types/models'
import * as fridgeApi from '@/api/fridge'

/**
 * 冰箱状态管理 Store
 * 管理冰箱列表、当前冰箱和相关操作
 */
export const useFridgeStore = defineStore('fridge', () => {
  // 状态
  const currentFridgeId = ref<string>('public')
  const myFridges = ref<Fridge[]>([])
  const sharedFridges = ref<Fridge[]>([])
  const loading = ref(false)
  const fridgeItemCounts = ref<Record<string, number>>({}) // 存储各个冰箱的物品数量
  
  // 计算属性
  
  /**
   * 所有冰箱列表（我的 + 共享的）
   */
  const allFridges = computed(() => [...myFridges.value, ...sharedFridges.value])
  
  /**
   * 当前选中的冰箱
   */
  const currentFridge = computed(() => {
    if (currentFridgeId.value === 'public') {
      return {
        _id: 'public',
        name: '公共冰箱',
        user_id: '',
        item_count: 0,
        created_at: ''
      } as Fridge
    }
    return allFridges.value.find(f => f._id === currentFridgeId.value) || null
  })
  
  /**
   * 我的冰箱数量
   */
  const myFridgeCount = computed(() => myFridges.value.length)
  
  /**
   * 共享冰箱数量
   */
  const sharedFridgeCount = computed(() => sharedFridges.value.length)
  
  // 操作方法
  
  /**
   * 加载冰箱列表
   * 从后端获取用户的所有冰箱（我的 + 共享的）
   */
  async function loadFridges() {
    loading.value = true
    try {
      const response = await fridgeApi.getFridgeList()
      if (response.success) {
        myFridges.value = response.my_fridges || []
        sharedFridges.value = response.shared_fridges || []
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 切换当前冰箱
   * @param fridgeId 冰箱 ID
   */
  async function switchFridge(fridgeId: string) {
    const response = await fridgeApi.switchFridge(fridgeId)
    if (response.success) {
      currentFridgeId.value = fridgeId
      // 保存到本地存储
      localStorage.setItem('currentFridgeId', fridgeId)
    }
    return response
  }
  
  /**
   * 创建新冰箱
   * @param name 冰箱名称
   */
  async function createFridge(name: string) {
    const response = await fridgeApi.createFridge(name)
    if (response.success) {
      // 重新加载冰箱列表
      await loadFridges()
      // 如果创建成功且返回了冰箱信息，自动切换到新冰箱
      if (response.data?.fridge) {
        await switchFridge(response.data.fridge._id)
      }
    }
    return response
  }
  
  /**
   * 重命名冰箱
   * @param fridgeId 冰箱 ID
   * @param name 新名称
   */
  async function renameFridge(fridgeId: string, name: string) {
    const response = await fridgeApi.renameFridge(fridgeId, name)
    if (response.success) {
      // 更新本地冰箱列表中的名称
      const fridge = myFridges.value.find(f => f._id === fridgeId)
      if (fridge) {
        fridge.name = name
      }
    }
    return response
  }
  
  /**
   * 删除冰箱
   * @param fridgeId 冰箱 ID
   */
  async function deleteFridge(fridgeId: string) {
    const response = await fridgeApi.deleteFridge(fridgeId)
    if (response.success) {
      // 重新加载冰箱列表
      await loadFridges()
      // 如果删除的是当前冰箱，切换到公共冰箱
      if (currentFridgeId.value === fridgeId) {
        currentFridgeId.value = 'public'
        localStorage.setItem('currentFridgeId', 'public')
      }
    }
    return response
  }
  
  /**
   * 从本地存储初始化当前冰箱 ID
   * 应用启动时调用
   */
  function initFromStorage() {
    const storedFridgeId = localStorage.getItem('currentFridgeId')
    if (storedFridgeId) {
      currentFridgeId.value = storedFridgeId
    }
  }
  
  /**
   * 获取指定冰箱的物品数量
   * @param fridgeId 冰箱 ID
   */
  function getFridgeItemCount(fridgeId: string): number {
    if (fridgeId === 'public') {
      return fridgeItemCounts.value['public'] || 0
    }
    
    // 先从冰箱对象的 item_count 字段获取
    const fridge = allFridges.value.find(f => f._id === fridgeId)
    if (fridge && typeof fridge.item_count === 'number') {
      return fridge.item_count
    }
    
    // 如果没有，从缓存中获取
    return fridgeItemCounts.value[fridgeId] || 0
  }
  
  /**
   * 更新冰箱物品数量
   * @param fridgeId 冰箱 ID
   * @param count 物品数量
   */
  function updateFridgeItemCount(fridgeId: string, count: number) {
    fridgeItemCounts.value[fridgeId] = count
    
    // 同时更新冰箱对象中的 item_count
    if (fridgeId !== 'public') {
      const fridge = myFridges.value.find(f => f._id === fridgeId) || 
                   sharedFridges.value.find(f => f._id === fridgeId)
      if (fridge) {
        fridge.item_count = count
      }
    }
  }
  
  /**
   * 获取指定冰箱的详细信息
   * @param fridgeId 冰箱 ID
   */
  async function getFridgeDetails(fridgeId: string) {
    return await fridgeApi.getFridge(fridgeId)
  }
  
  /**
   * 清空状态
   * 用户登出时调用
   */
  function clearState() {
    currentFridgeId.value = 'public'
    myFridges.value = []
    sharedFridges.value = []
    loading.value = false
    fridgeItemCounts.value = {}
    localStorage.removeItem('currentFridgeId')
  }
  
  return {
    // 状态
    currentFridgeId,
    myFridges,
    sharedFridges,
    loading,
    fridgeItemCounts,
    // 计算属性
    allFridges,
    currentFridge,
    myFridgeCount,
    sharedFridgeCount,
    // 操作方法
    loadFridges,
    switchFridge,
    createFridge,
    renameFridge,
    deleteFridge,
    initFromStorage,
    getFridgeDetails,
    getFridgeItemCount,
    updateFridgeItemCount,
    clearState
  }
})
