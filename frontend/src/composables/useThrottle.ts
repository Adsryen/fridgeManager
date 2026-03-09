import { ref, watch, type Ref } from 'vue'

/**
 * 节流 Hook
 * @param value 需要节流的值
 * @param delay 延迟时间（毫秒）
 * @returns 节流后的值
 */
export function useThrottle<T>(value: Ref<T>, delay: number = 300): Ref<T> {
  const throttledValue = ref(value.value) as Ref<T>
  let lastTime = 0

  watch(value, (newValue) => {
    const now = Date.now()
    if (now - lastTime >= delay) {
      throttledValue.value = newValue
      lastTime = now
    }
  })

  return throttledValue
}

/**
 * 节流函数
 * @param fn 需要节流的函数
 * @param delay 延迟时间（毫秒）
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number = 300
): (...args: Parameters<T>) => void {
  let lastTime = 0

  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      fn.apply(this, args)
      lastTime = now
    }
  }
}
