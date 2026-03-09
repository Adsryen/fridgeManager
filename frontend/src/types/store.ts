// Pinia Store 状态类型定义

import type { User, Fridge, Item, Family, FamilyMember } from './models'

// 用户 Store 状态
export interface UserState {
  user: User | null
  token: string | null
  isLoggedIn: boolean
  isAdmin: boolean
}

// 冰箱 Store 状态
export interface FridgeState {
  currentFridgeId: string
  myFridges: Fridge[]
  sharedFridges: Fridge[]
  loading: boolean
}

// 物品 Store 状态
export interface ItemState {
  items: Item[]
  filteredItems: Item[]
  searchKeyword: string
  filterPlace: string | null
  filterType: string | null
  loading: boolean
}

// 家庭 Store 状态
export interface FamilyState {
  families: Family[]
  currentFamily: Family | null
  members: FamilyMember[]
  loading: boolean
}
