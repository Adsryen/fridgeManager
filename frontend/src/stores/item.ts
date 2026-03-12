import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Item } from '@/types/models'
import * as itemApi from '@/api/item'
import { useFridgeStore } from './fridge'

/**
 * 物品状态管理 Store
 * 管理物品列表、搜索过滤和相关操作
 */
export const useItemStore = defineStore('item', () => {
  // 状态
  const items = ref<Item[]>([])
  const searchKeyword = ref('')
  const filterPlace = ref<string | null>(null)
  const filterType = ref<string | null>(null)
  const loading = ref(false)
  
  // 计算属性
  
  /**
   * 过滤后的物品列表
   * 根据搜索关键词、存放位置和类型进行过滤
   */
  const filteredItems = computed(() => {
    let result = items.value
    
    // 按关键词搜索
    if (searchKeyword.value) {
      const keyword = searchKeyword.value.toLowerCase()
      result = result.filter(item => 
        item.name.toLowerCase().includes(keyword)
      )
    }
    
    // 按存放位置过滤
    if (filterPlace.value) {
      result = result.filter(item => item.place === filterPlace.value)
    }
    
    // 按类型过滤
    if (filterType.value) {
      result = result.filter(item => item.type === filterType.value)
    }
    
    return result
  })
  
  /**
   * 已过期物品
   * 过期日期早于当前日期的物品
   */
  const expiredItems = computed(() => {
    const now = new Date()
    now.setHours(0, 0, 0, 0) // 重置到当天开始
    return items.value.filter(item => {
      const expireDate = new Date(item.expire_date)
      expireDate.setHours(0, 0, 0, 0)
      return expireDate < now
    })
  })
  
  /**
   * 即将过期物品（3天内）
   * 过期日期在当前日期之后但在3天内的物品
   */
  const expiringItems = computed(() => {
    const now = new Date()
    now.setHours(0, 0, 0, 0)
    const threeDaysLater = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
    
    return items.value.filter(item => {
      const expireDate = new Date(item.expire_date)
      expireDate.setHours(0, 0, 0, 0)
      return expireDate >= now && expireDate <= threeDaysLater
    })
  })
  
  /**
   * 正常物品
   * 过期日期在3天之后的物品
   */
  const normalItems = computed(() => {
    const now = new Date()
    now.setHours(0, 0, 0, 0)
    const threeDaysLater = new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
    
    return items.value.filter(item => {
      const expireDate = new Date(item.expire_date)
      expireDate.setHours(0, 0, 0, 0)
      return expireDate > threeDaysLater
    })
  })
  
  /**
   * 物品总数
   */
  const itemCount = computed(() => items.value.length)
  
  /**
   * 按存放位置分组的物品数量
   */
  const itemsByPlace = computed(() => {
    const result: Record<string, number> = {
      cold: 0,
      frozen: 0,
      normal: 0
    }
    items.value.forEach(item => {
      const place = item.place as keyof typeof result
      if (place in result) {
        result[place] = (result[place] || 0) + 1
      }
    })
    return result
  })
  
  /**
   * 按类型分组的物品数量
   */
  const itemsByType = computed(() => {
    const result: Record<string, number> = {}
    items.value.forEach(item => {
      result[item.type] = (result[item.type] || 0) + 1
    })
    return result
  })
  
  // 操作方法
  
  /**
   * 标准化物品数据
   * 将后端返回的大写字段名转换为小写
   */
  function normalizeItem(item: any): Item {
    return {
      _id: item._id,
      user_id: item.user_id,
      fridge_id: item.fridge_id,
      name: item.name || item.Name,
      num: item.num || item.Num,
      unit: item.unit,
      expire_date: item.expire_date || item.ExpireDate,
      place: (item.place || item.Place) as any,
      type: item.type || item.Type,
      created_at: item.created_at,
      updated_at: item.updated_at
    }
  }

  /**
   * 加载物品列表
   * 从后端获取当前冰箱的所有物品
   */
  async function loadItems() {
    loading.value = true
    try {
      const fridgeStore = useFridgeStore()
      console.log('[ItemStore] 加载物品，当前冰箱ID:', fridgeStore.currentFridgeId)
      const response = await itemApi.getAllItems(fridgeStore.currentFridgeId)
      console.log('[ItemStore] 物品加载结果:', response)
      if (response.success && response.data) {
        // 标准化数据
        items.value = response.data.map(normalizeItem)
        console.log('[ItemStore] 物品数量:', items.value.length)
        console.log('[ItemStore] 第一个物品:', items.value[0])
        
        // 更新冰箱的物品数量
        fridgeStore.updateFridgeItemCount(fridgeStore.currentFridgeId, items.value.length)
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 添加物品
   * @param itemData 物品数据
   */
  async function addItem(itemData: {
    name: string
    quantity: number
    expire_date: string
    place: string
    type: string
  }) {
    const fridgeStore = useFridgeStore()
    const response = await itemApi.addItem({
      ...itemData,
      fridge_id: fridgeStore.currentFridgeId
    })
    if (response.success) {
      // 重新加载物品列表
      await loadItems()
    }
    return response
  }
  
  /**
   * 批量添加物品
   * @param itemsData 物品数据数组
   */
  async function batchAddItems(itemsData: Array<{
    name: string
    quantity: number
    unit?: string
    expire_date: string
    place: string
    type: string
  }>) {
    const fridgeStore = useFridgeStore()
    const response = await itemApi.batchAddItems(itemsData, fridgeStore.currentFridgeId)
    if (response.success) {
      // 重新加载物品列表
      await loadItems()
    }
    return response
  }
  
  /**
   * 更新物品
   * @param itemId 物品 ID
   * @param itemData 要更新的物品数据
   */
  async function updateItem(itemId: string, itemData: {
    name?: string
    quantity?: number
    expire_date?: string
    place?: string
    type?: string
  }) {
    const response = await itemApi.updateItem(itemId, itemData)
    if (response.success) {
      // 重新加载物品列表以确保数据一致
      await loadItems()
    }
    return response
  }
  
  /**
   * 删除物品
   * @param itemId 物品 ID
   */
  async function deleteItem(itemId: string) {
    const response = await itemApi.deleteItem(itemId)
    if (response.success) {
      // 从本地列表中移除
      items.value = items.value.filter(item => item._id !== itemId)
    }
    return response
  }
  
  /**
   * 搜索物品
   * @param keyword 搜索关键词
   */
  async function searchItems(keyword: string) {
    loading.value = true
    try {
      const fridgeStore = useFridgeStore()
      const response = await itemApi.searchItems(keyword, fridgeStore.currentFridgeId)
      if (response.success && response.data) {
        items.value = response.data
      }
      return response
    } finally {
      loading.value = false
    }
  }
  
  /**
   * 获取单个物品详情
   * @param itemId 物品 ID
   */
  async function getItemDetails(itemId: string) {
    return await itemApi.getItem(itemId)
  }
  
  /**
   * 设置搜索关键词
   * @param keyword 关键词
   */
  function setSearchKeyword(keyword: string) {
    searchKeyword.value = keyword
  }
  
  /**
   * 设置存放位置过滤
   * @param place 存放位置
   */
  function setFilterPlace(place: string | null) {
    filterPlace.value = place
  }
  
  /**
   * 设置类型过滤
   * @param type 物品类型
   */
  function setFilterType(type: string | null) {
    filterType.value = type
  }
  
  /**
   * 清除所有过滤条件
   */
  function clearFilters() {
    searchKeyword.value = ''
    filterPlace.value = null
    filterType.value = null
  }
  
  /**
   * 清空状态
   * 用户登出或切换冰箱时调用
   */
  function clearState() {
    items.value = []
    searchKeyword.value = ''
    filterPlace.value = null
    filterType.value = null
    loading.value = false
  }
  
  return {
    // 状态
    items,
    searchKeyword,
    filterPlace,
    filterType,
    loading,
    // 计算属性
    filteredItems,
    expiredItems,
    expiringItems,
    normalItems,
    itemCount,
    itemsByPlace,
    itemsByType,
    // 操作方法
    loadItems,
    addItem,
    batchAddItems,
    updateItem,
    deleteItem,
    searchItems,
    getItemDetails,
    setSearchKeyword,
    setFilterPlace,
    setFilterType,
    clearFilters,
    clearState
  }
})
