<template>
  <div class="item-filter">
    <!-- 搜索框 -->
    <div class="search-box">
      <i class="fas fa-search search-icon"></i>
      <input
        v-model="searchInput"
        type="text"
        class="search-input"
        placeholder="搜索物品名称..."
      />
      <button v-if="searchInput" class="clear-btn" @click="clearSearch">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- 过滤器 -->
    <div class="filter-chips">
      <!-- 存放位置过滤 -->
      <div class="filter-group">
        <button
          class="filter-chip"
          :class="{ active: !filterPlace }"
          @click="setPlace(null)"
        >
          <span>全部</span>
        </button>
        <button
          class="filter-chip"
          :class="{ active: filterPlace === 'cold' }"
          @click="setPlace('cold')"
        >
          <i class="fas fa-snowflake"></i>
          <span>冷藏</span>
        </button>
        <button
          class="filter-chip"
          :class="{ active: filterPlace === 'frozen' }"
          @click="setPlace('frozen')"
        >
          <i class="fas fa-icicles"></i>
          <span>冷冻</span>
        </button>
        <button
          class="filter-chip"
          :class="{ active: filterPlace === 'normal' }"
          @click="setPlace('normal')"
        >
          <i class="fas fa-temperature-high"></i>
          <span>常温</span>
        </button>
      </div>

      <!-- 类型过滤 -->
      <div class="filter-group">
        <button
          class="filter-chip type-chip"
          :class="{ active: !filterType }"
          @click="setType(null)"
        >
          <span>全部类型</span>
        </button>
        <button
          v-for="type in itemTypes"
          :key="type.value"
          class="filter-chip type-chip"
          :class="{ active: filterType === type.value }"
          @click="setType(type.value)"
        >
          <i :class="type.icon"></i>
          <span>{{ type.label }}</span>
        </button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="filter-stats">
      <span class="stat-item">
        共 <strong>{{ itemCount }}</strong> 件物品
      </span>
      <span v-if="expiredCount > 0" class="stat-item expired">
        <i class="fas fa-exclamation-circle"></i>
        {{ expiredCount }} 件已过期
      </span>
      <span v-if="expiringCount > 0" class="stat-item expiring">
        <i class="fas fa-clock"></i>
        {{ expiringCount }} 件即将过期
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useItemStore } from '@/stores/item'
import { useDebounce } from '@/composables/useDebounce'

const itemStore = useItemStore()

// 搜索输入
const searchInput = ref('')

// 使用防抖 Hook
const debouncedSearch = useDebounce(searchInput, 300)

// 监听防抖后的搜索值
watch(debouncedSearch, (newValue) => {
  itemStore.setSearchKeyword(newValue.trim())
})

// 物品类型列表
const itemTypes = [
  { label: '蔬菜', value: '蔬菜', icon: 'fas fa-carrot' },
  { label: '水果', value: '水果', icon: 'fas fa-apple-alt' },
  { label: '肉类', value: '肉类', icon: 'fas fa-drumstick-bite' },
  { label: '海鲜', value: '海鲜', icon: 'fas fa-fish' },
  { label: '饮料', value: '饮料', icon: 'fas fa-glass-whiskey' },
  { label: '调味品', value: '调味品', icon: 'fas fa-pepper-hot' },
  { label: '面包糕点', value: '面包糕点', icon: 'fas fa-bread-slice' },
  { label: '乳制品', value: '乳制品', icon: 'fas fa-cheese' },
  { label: '速食', value: '速食', icon: 'fas fa-pizza-slice' },
  { label: '其他', value: '其他', icon: 'fas fa-box' }
]

// 计算属性
const filterPlace = computed(() => itemStore.filterPlace)
const filterType = computed(() => itemStore.filterType)
const itemCount = computed(() => itemStore.filteredItems.length)
const expiredCount = computed(() => itemStore.expiredItems.length)
const expiringCount = computed(() => itemStore.expiringItems.length)

// 清除搜索
const clearSearch = () => {
  searchInput.value = ''
}

// 设置存放位置过滤
const setPlace = (place: string | null) => {
  itemStore.setFilterPlace(place)
}

// 设置类型过滤
const setType = (type: string | null) => {
  itemStore.setFilterType(type)
}
</script>

<style scoped>
.item-filter {
  padding: 16px;
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
}

/* 搜索框 */
.search-box {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.search-icon {
  position: absolute;
  left: 16px;
  color: var(--text-secondary);
  font-size: 16px;
  pointer-events: none;
}

.search-input {
  flex: 1;
  padding: 12px 48px 12px 44px;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  font-size: 15px;
  background: var(--bg-color);
  color: var(--text-primary);
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: var(--card-bg);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.clear-btn {
  position: absolute;
  right: 12px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--text-secondary);
  border: none;
  color: white;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.clear-btn:active {
  transform: scale(0.9);
  background: var(--text-primary);
}

/* 过滤器 */
.filter-chips {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.filter-group {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.filter-group::-webkit-scrollbar {
  display: none;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  border: 2px solid var(--border-color);
  background: var(--bg-color);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.filter-chip i {
  font-size: 14px;
}

.filter-chip:active {
  transform: scale(0.95);
}

.filter-chip.active {
  border-color: var(--primary-color);
  background: var(--primary-color);
  color: white;
}

.filter-chip.type-chip {
  min-width: auto;
}

/* 统计信息 */
.filter-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  color: var(--text-secondary);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-item strong {
  color: var(--primary-color);
  font-weight: 600;
}

.stat-item.expired {
  color: var(--danger-color);
}

.stat-item.expiring {
  color: var(--warning-color);
}

.stat-item i {
  font-size: 12px;
}
</style>
