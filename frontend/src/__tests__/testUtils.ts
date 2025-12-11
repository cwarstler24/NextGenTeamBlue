/**
 * Test Utilities for Vue Component Testing
 * 
 * This file provides helper functions and utilities for testing Vue components.
 */

import { mount, VueWrapper, type MountingOptions } from '@vue/test-utils'
import type { Router } from 'vue-router'
import { createRouter, createMemoryHistory } from 'vue-router'
import { vi } from 'vitest'

/**
 * Creates a mock router for testing components that use vue-router
 */
export function createMockRouter(overrides = {}): Router {
  return {
    push: vi.fn(),
    replace: vi.fn(),
    go: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    beforeEach: vi.fn(),
    beforeResolve: vi.fn(),
    afterEach: vi.fn(),
    resolve: vi.fn(),
    getRoutes: vi.fn(() => []),
    hasRoute: vi.fn(),
    addRoute: vi.fn(),
    removeRoute: vi.fn(),
    install: vi.fn(),
    currentRoute: {
      value: {
        path: '/',
        name: 'home',
        params: {},
        query: {},
        hash: '',
        fullPath: '/',
        matched: [],
        meta: {},
        redirectedFrom: undefined,
      },
    },
    options: {
      history: {} as any,
      routes: [],
    },
    ...overrides,
  } as unknown as Router
}

/**
 * Mounts a Vue component with common test configuration
 * @param component - The Vue component to mount
 * @param options - Additional mounting options
 * @returns VueWrapper instance
 */
export function mountWithRouter<T>(
  component: T,
  options: MountingOptions<any> = {}
): VueWrapper {
  // Create a real router instance with spy methods
  const mockPush = vi.fn()
  const mockReplace = vi.fn()
  
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
      { path: '/assets', name: 'AssetList', component: { template: '<div>Assets</div>' } },
      { path: '/assets/:id', name: 'AssetView', component: { template: '<div>Asset</div>' } },
      { path: '/assets/add', name: 'AssetAdd', component: { template: '<div>Add</div>' } },
    ],
  })
  
  // Spy on router methods
  router.push = mockPush
  router.replace = mockReplace
  
  // If test provides custom mocks, use those
  const customRouter = options.global?.mocks?.$router
  if (customRouter?.push) {
    router.push = customRouter.push
  }
  if (customRouter?.replace) {
    router.replace = customRouter.replace
  }
  
  return mount(component as any, {
    ...options,
    global: {
      ...options.global,
      plugins: [
        router,
        ...(options.global?.plugins || []),
      ],
      mocks: {
        $router: router,
        $route: router.currentRoute.value,
        ...options.global?.mocks,
      },
      stubs: {
        RouterLink: {
          template: '<a @click="navigate"><slot /></a>',
          props: ['to'],
          methods: {
            navigate(e: Event) {
              e.preventDefault()
              // Can track navigation if needed
            },
          },
        },
        RouterView: {
          template: '<div class="router-view"><slot /></div>',
        },
        ...options.global?.stubs,
      },
    },
  })
}

/**
 * Mock asset data factory for testing
 */
export function createMockAsset(overrides = {}) {
  return {
    id: 1,
    resource_id: 'ASSET-001',
    is_decommissioned: false,
    date_commissioned: '2024-01-01',
    description: 'Test Asset',
    employee_id: 1,
    type_id: 1,
    location_id: 1,
    ...overrides,
  }
}

/**
 * Mock employee data factory for testing
 */
export function createMockEmployee(overrides = {}) {
  return {
    id: 1,
    first_name: 'John',
    last_name: 'Doe',
    email: 'john.doe@example.com',
    phone_number: '555-1234',
    job_title: 'Developer',
    ...overrides,
  }
}

/**
 * Mock asset type data factory for testing
 */
export function createMockAssetType(overrides = {}) {
  return {
    id: 1,
    type_name: 'Laptop',
    type_description: 'Portable computer',
    ...overrides,
  }
}

/**
 * Mock location data factory for testing
 */
export function createMockLocation(overrides = {}) {
  return {
    id: 1,
    location_name: 'Building A',
    location_description: 'Main office building',
    ...overrides,
  }
}

/**
 * Wait for the next tick and for Vue to update the DOM
 */
export async function flushPromises() {
  return new Promise((resolve) => {
    setTimeout(resolve, 0)
  })
}

/**
 * Simulates waiting for an async operation to complete
 */
export function waitFor(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Helper to get localStorage mock
 */
export function getLocalStorageMock() {
  return globalThis.localStorage
}

/**
 * Helper to clear all mocks
 */
export function clearAllMocks() {
  vi.clearAllMocks()
  if (typeof localStorage !== 'undefined' && localStorage.clear) {
    localStorage.clear()
  }
  if (typeof sessionStorage !== 'undefined' && sessionStorage.clear) {
    sessionStorage.clear()
  }
}
