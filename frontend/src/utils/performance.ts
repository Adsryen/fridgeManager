/**
 * 性能监控工具
 */

/**
 * 测量函数执行时间
 */
export function measurePerformance<T extends (...args: any[]) => any>(
  fn: T,
  label?: string
): T {
  return ((...args: Parameters<T>) => {
    const start = performance.now()
    const result = fn(...args)
    
    if (result instanceof Promise) {
      return result.finally(() => {
        const end = performance.now()
        if (import.meta.env.DEV) {
          console.log(`[Performance] ${label || fn.name}: ${(end - start).toFixed(2)}ms`)
        }
      })
    }
    
    const end = performance.now()
    if (import.meta.env.DEV) {
      console.log(`[Performance] ${label || fn.name}: ${(end - start).toFixed(2)}ms`)
    }
    
    return result
  }) as T
}

/**
 * 图片懒加载
 */
export function lazyLoadImage(selector: string = 'img[data-src]') {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement
          const src = img.dataset.src
          if (src) {
            img.src = src
            img.removeAttribute('data-src')
            imageObserver.unobserve(img)
          }
        }
      })
    })
    
    document.querySelectorAll(selector).forEach((img) => {
      imageObserver.observe(img)
    })
  }
}

/**
 * 资源预加载
 */
export function preloadResource(url: string, type: 'script' | 'style' | 'image' = 'script') {
  const link = document.createElement('link')
  link.rel = 'preload'
  link.href = url
  
  switch (type) {
    case 'script':
      link.as = 'script'
      break
    case 'style':
      link.as = 'style'
      break
    case 'image':
      link.as = 'image'
      break
  }
  
  document.head.appendChild(link)
}
