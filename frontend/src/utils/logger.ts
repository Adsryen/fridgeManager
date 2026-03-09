/**
 * 日志工具类
 * 在生产环境中禁用日志输出
 */

const isDev = import.meta.env.DEV

export const logger = {
  log: (...args: any[]) => {
    if (isDev) {
      console.log(...args)
    }
  },
  
  info: (...args: any[]) => {
    if (isDev) {
      console.info(...args)
    }
  },
  
  warn: (...args: any[]) => {
    if (isDev) {
      console.warn(...args)
    }
  },
  
  error: (...args: any[]) => {
    // 错误日志在生产环境也保留
    console.error(...args)
  },
  
  debug: (...args: any[]) => {
    if (isDev) {
      console.debug(...args)
    }
  }
}
