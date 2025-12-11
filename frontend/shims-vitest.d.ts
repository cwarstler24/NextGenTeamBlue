declare module 'vitest/config' {
  import type { UserConfig } from 'vite'
  export function defineConfig(config: UserConfig): UserConfig
  export default function defineConfig(config: UserConfig): UserConfig
}
