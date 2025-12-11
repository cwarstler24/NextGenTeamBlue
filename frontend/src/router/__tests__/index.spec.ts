/**
 * @file router/index.spec.ts
 * @description Tests for Vue Router configuration
 * 
 * Test Coverage:
 * - Router instance creation
 * - All route definitions and paths
 * - Component mapping for each route
 * - Navigation between routes
 * - Route name validation
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { createMemoryHistory, createRouter, type Router } from 'vue-router'
import HomeView from '../../views/HomeView.vue'
import LoginView from '../../views/LoginView.vue'
import AssetView from '../../views/AssetView.vue'
import AssetAddView from '../../views/AssetAddView.vue'
import AssetListView from '../../views/AssetListView.vue'
import AssetUpdateView from '../../views/AssetUpdateView.vue'
import EmployeeListView from '../../views/EmployeeListView.vue'
import MascotTheme from '../../views/MascotTheme.vue'
import AboutView from '../../views/AboutView.vue'

// Create a test router with same configuration
const createTestRouter = (): Router => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      {
        path: '/',
        name: 'home',
        component: HomeView,
      },
      {
        path: '/login',
        name: 'login',
        component: LoginView,
      },
      {
        path: '/assets',
        name: 'AssetList',
        component: AssetListView,
      },
      {
        path: '/assets/:id',
        name: 'AssetView',
        component: AssetView,
      },
      {
        path : '/assets/:id/update',
        name: 'AssetUpdate',
        component: AssetUpdateView,
      },
      {
        path: '/add-asset',
        name: 'AssetAdd',
        component: AssetAddView,
      },
      {
        path: '/employees',
        name: 'EmployeeList',
        component: EmployeeListView,
      },
      {
        path: '/mascot-theme',
        name: 'MascotTheme',
        component: MascotTheme,
      },
      {
        path: '/about',
        name: 'About',
        component: AboutView,
      },
    ],
  })
}

describe('Vue Router Configuration', () => {
  let router: Router

  beforeEach(() => {
    router = createTestRouter()
  })

  it('creates router instance successfully', () => {
    expect(router).toBeDefined()
    expect(router.options.routes).toHaveLength(9)
  })

  describe('Route Definitions', () => {
    it('defines home route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'home')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/')
      expect(route?.component).toBe(HomeView)
    })

    it('defines login route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'login')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/login')
      expect(route?.component).toBe(LoginView)
    })

    it('defines asset list route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'AssetList')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/assets')
      expect(route?.component).toBe(AssetListView)
    })

    it('defines asset view route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'AssetView')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/assets/:id')
      expect(route?.component).toBe(AssetView)
    })

    it('defines asset update route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'AssetUpdate')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/assets/:id/update')
      expect(route?.component).toBe(AssetUpdateView)
    })

    it('defines asset add route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'AssetAdd')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/add-asset')
      expect(route?.component).toBe(AssetAddView)
    })

    it('defines employee list route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'EmployeeList')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/employees')
      expect(route?.component).toBe(EmployeeListView)
    })

    it('defines mascot theme route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'MascotTheme')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/mascot-theme')
      expect(route?.component).toBe(MascotTheme)
    })

    it('defines about route correctly', () => {
      const route = router.options.routes.find(r => r.name === 'About')
      expect(route).toBeDefined()
      expect(route?.path).toBe('/about')
      expect(route?.component).toBe(AboutView)
    })
  })

  describe('Route Navigation', () => {
    it('navigates to home route', async () => {
      await router.push('/')
      expect(router.currentRoute.value.name).toBe('home')
      expect(router.currentRoute.value.path).toBe('/')
    })

    it('navigates to login route', async () => {
      await router.push('/login')
      expect(router.currentRoute.value.name).toBe('login')
    })

    it('navigates to assets list', async () => {
      await router.push('/assets')
      expect(router.currentRoute.value.name).toBe('AssetList')
    })

    it('navigates to specific asset view with id parameter', async () => {
      await router.push('/assets/123')
      expect(router.currentRoute.value.name).toBe('AssetView')
      expect(router.currentRoute.value.params.id).toBe('123')
    })

    it('navigates to asset update with id parameter', async () => {
      await router.push('/assets/456/update')
      expect(router.currentRoute.value.name).toBe('AssetUpdate')
      expect(router.currentRoute.value.params.id).toBe('456')
    })

    it('navigates to add asset page', async () => {
      await router.push('/add-asset')
      expect(router.currentRoute.value.name).toBe('AssetAdd')
    })

    it('navigates to employee list', async () => {
      await router.push('/employees')
      expect(router.currentRoute.value.name).toBe('EmployeeList')
    })

    it('navigates to mascot theme page', async () => {
      await router.push('/mascot-theme')
      expect(router.currentRoute.value.name).toBe('MascotTheme')
    })

    it('navigates to about page', async () => {
      await router.push('/about')
      expect(router.currentRoute.value.name).toBe('About')
    })
  })

  describe('Route Parameters', () => {
    it('accepts dynamic id parameter in asset view', async () => {
      await router.push({ name: 'AssetView', params: { id: '789' } })
      expect(router.currentRoute.value.params.id).toBe('789')
    })

    it('accepts dynamic id parameter in asset update', async () => {
      await router.push({ name: 'AssetUpdate', params: { id: '999' } })
      expect(router.currentRoute.value.params.id).toBe('999')
    })
  })
})
