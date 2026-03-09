import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isProd = mode === 'production'
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
      allowedHosts: [
        'localhost',
        '127.0.0.1',
        'bx.gr.prlrr.com',
        '.prlrr.com'
      ],
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    esbuild: {
      drop: isProd ? ['console', 'debugger'] : []
    },
    build: {
      target: 'esnext',
      minify: 'esbuild',
      sourcemap: false,
      cssCodeSplit: true,
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        output: {
          chunkFileNames: 'js/[name]-[hash].js',
          entryFileNames: 'js/[name]-[hash].js',
          assetFileNames: '[ext]/[name]-[hash].[ext]',
          manualChunks: {
            'vue-vendor': ['vue', 'vue-router', 'pinia'],
            'element-plus': ['element-plus'],
            'axios': ['axios']
          }
        }
      }
    },
    optimizeDeps: {
      include: ['vue', 'vue-router', 'pinia', 'axios', 'element-plus']
    }
  }
})
