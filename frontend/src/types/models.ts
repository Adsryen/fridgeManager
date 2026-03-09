// 数据模型类型定义

// 用户模型
export interface User {
  _id: string
  username: string
  email: string
  is_admin: boolean
  is_active: boolean
  created_at: string
  theme_preference?: 'light' | 'dark'
}

// 物品模型
export interface Item {
  _id: string
  user_id: string
  fridge_id: string
  name: string
  num: number
  unit?: string
  expire_date: string
  place: 'cold' | 'frozen' | 'normal' // 冷藏、冷冻、常温
  type: string // 蔬菜、水果、肉类、饮料、调味品、面包糕点、乳制品等
  created_at: string
  updated_at: string
}

// 冰箱模型
export interface Fridge {
  _id: string
  user_id: string
  name: string
  item_count: number
  created_at: string
  permission?: FridgePermission
  owner_username?: string // 共享冰箱显示所有者
}

// 冰箱权限模型
export interface FridgePermission {
  is_family_shared: boolean
  is_editable_by_family: boolean
}

// 家庭模型
export interface Family {
  _id: string
  name: string
  family_code: string
  owner_id: string
  owner_username: string
  member_count: number
  created_at: string
}

// 家庭成员模型
export interface FamilyMember {
  user_id: string
  username: string
  email: string
  joined_at: string
  is_owner: boolean
}

// AI 对话消息模型
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp?: string
}

// OCR 识别结果模型
export interface OCRResult {
  success: boolean
  method: 'ocr_only' | 'ocr_ai' | 'vision'
  text?: string
  items: Partial<Item>[]
}

// 系统设置模型
export interface SystemSettings {
  session_timeout: number
  max_items_per_user: number
  default_expiry_warning_days: number
  enable_ai_features: boolean
  openai_api_base: string
  openai_api_key: string
  openai_chat_model: string
  openai_vision_model: string
  openai_audio_model: string
}
