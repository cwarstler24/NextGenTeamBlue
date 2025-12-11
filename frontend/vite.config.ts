import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // Vitest configuration (typed via vitest/config)
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/__tests__/setup.ts'],
    coverage: { 
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      include: ['src/**/*.{js,ts,vue}'],
      exclude: [
        'node_modules/',
        'src/__tests__/',
        'src/**/__tests__/',
        '**/*.spec.ts',
        '**/*.test.ts',
        'vite.config.ts',
        'eslint.config.js',
        'src/main.ts',
      ],
      thresholds: {
        statements: 90,
      },
    },
  },
})
