/**
 * Unit Tests for AssetListView Component
 * 
 * Tests the asset list view component which displays and filters assets.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AssetListView from '@/views/AssetListView.vue'
import { mountWithRouter, createMockAsset, clearAllMocks } from '@/__tests__/testUtils'
import axios from 'axios'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
  },
}))

// Mock the composables
vi.mock('@/composables/useAssetTypes', () => ({
  useAssetTypes: () => ({
    getAssetTypeName: vi.fn((id) => `Type ${id}`),
    fetchAssetTypes: vi.fn(),
  }),
}))

vi.mock('@/composables/useAssetEmployees', () => ({
  useAssetEmployees: () => ({
    getAssetEmployeeName: vi.fn((id) => `Employee ${id}`),
    fetchAssetEmployees: vi.fn(),
  }),
}))

vi.mock('@/composables/useAssetLocations', () => ({
  useAssetLocations: () => ({
    getAssetLocationName: vi.fn((id) => `Location ${id}`),
    fetchAssetLocations: vi.fn(),
  }),
}))

// Mock API_BASE
vi.mock('@/config/api', () => ({
  API_BASE: 'https://api.test',
}))

const mockedAxios = axios as { get: ReturnType<typeof vi.fn> }

describe('AssetListView.vue', () => {
  beforeEach(() => {
    clearAllMocks()
    vi.clearAllMocks()
    localStorage.setItem('bearerToken', 'Bearer test-token')
  })

  afterEach(() => {
    localStorage.clear()
  })

  /**
   * @function renders the component correctly
   * @description Verifies that the AssetListView component renders with expected structure
   */
  it('renders the component correctly', () => {
    mockedAxios.get.mockResolvedValue({ data: [] })
    const wrapper = mountWithRouter(AssetListView)

    expect(wrapper.find('.asset-list-view').exists()).toBe(true)
    expect(wrapper.find('.page-header').exists()).toBe(true)
    expect(wrapper.find('h1').text()).toBe('Asset Inventory')
  })

  /**
   * @function displays error when no bearer token is set
   * @description Verifies that an error message is shown when bearer token is missing
   */
  it('displays error when no bearer token is set', async () => {
    localStorage.removeItem('bearerToken')
    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('No bearer token')
  })

  /**
   * @function fetches and displays assets on mount
   * @description Verifies that assets are fetched and displayed when component mounts
   */
  it('fetches and displays assets on mount', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001' }),
      createMockAsset({ id: 2, resource_id: 'ASSET-002' }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    const assetCards = wrapper.findAll('.asset-card')
    expect(assetCards).toHaveLength(2)
    expect(wrapper.text()).toContain('ASSET-001')
    expect(wrapper.text()).toContain('ASSET-002')
  })

  /**
   * @function navigates to asset detail when card is clicked
   * @description Verifies that clicking an asset card navigates to the detail view
   */
  it('navigates to asset detail when card is clicked', async () => {
    const mockAssets = [createMockAsset({ id: 1, resource_id: 'ASSET-001' })]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const mockRouter = {
      push: vi.fn(),
    }

    const wrapper = mountWithRouter(AssetListView, {
      global: {
        mocks: {
          $router: mockRouter,
        },
      },
    })
    await flushPromises()

    const assetCard = wrapper.find('.asset-card')
    await assetCard.trigger('click')

    expect(mockRouter.push).toHaveBeenCalledWith({
      name: 'AssetView',
      params: { id: 1 },
    })
  })

  /**
   * @function navigates to add asset page when Add button is clicked
   * @description Verifies that clicking Add New Asset button navigates to add page
   */
  it('navigates to add asset page when Add button is clicked', async () => {
    mockedAxios.get.mockResolvedValue({ data: [] })
    
    const mockRouter = {
      push: vi.fn(),
    }

    const wrapper = mountWithRouter(AssetListView, {
      global: {
        mocks: {
          $router: mockRouter,
        },
      },
    })
    await flushPromises()

    const addButton = wrapper.find('.btn-add')
    await addButton.trigger('click')

    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'AssetAdd' })
  })

  /**
   * @function displays empty state when no assets exist
   * @description Verifies that empty state is shown when there are no assets
   */
  it('displays empty state when no assets exist', async () => {
    mockedAxios.get.mockResolvedValue({ data: [] })
    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('No Assets Found')
  })

  /**
   * @function filters assets by employee ID
   * @description Verifies that assets can be filtered by employee ID
   */
  it('filters assets by employee ID', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001', employee_id: 1 }),
      createMockAsset({ id: 2, resource_id: 'ASSET-002', employee_id: 2 }),
      createMockAsset({ id: 3, resource_id: 'ASSET-003', employee_id: 1 }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    const employeeFilter = wrapper.find('#employeeIdFilter')
    await employeeFilter.setValue('1')

    const searchButton = wrapper.find('.btn-filter')
    await searchButton.trigger('click')
    await flushPromises()

    const assetCards = wrapper.findAll('.asset-card')
    expect(assetCards).toHaveLength(2)
    expect(wrapper.text()).toContain('Filtered Results')
  })

  /**
   * @function filters assets by type ID
   * @description Verifies that assets can be filtered by type ID
   */
  it('filters assets by type ID', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001', type_id: 1 }),
      createMockAsset({ id: 2, resource_id: 'ASSET-002', type_id: 2 }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    const typeFilter = wrapper.find('#typeIdFilter')
    await typeFilter.setValue('2')

    const searchButton = wrapper.find('.btn-filter')
    await searchButton.trigger('click')
    await flushPromises()

    const assetCards = wrapper.findAll('.asset-card')
    expect(assetCards).toHaveLength(1)
  })

  /**
   * @function clears filters when Clear button is clicked
   * @description Verifies that filters are cleared and all assets are shown again
   */
  it('clears filters when Clear button is clicked', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001', employee_id: 1 }),
      createMockAsset({ id: 2, resource_id: 'ASSET-002', employee_id: 2 }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    // Apply filter
    const employeeFilter = wrapper.find('#employeeIdFilter')
    await employeeFilter.setValue('1')
    const searchButton = wrapper.find('.btn-filter')
    await searchButton.trigger('click')
    await flushPromises()

    // Clear filter
    const clearButton = wrapper.find('.btn-clear')
    await clearButton.trigger('click')
    await flushPromises()

    const assetCards = wrapper.findAll('.asset-card')
    expect(assetCards).toHaveLength(2)
    expect(employeeFilter.element.value).toBe('')
  })

  /**
   * @function handles API errors gracefully
   * @description Verifies that API errors are caught and displayed to the user
   */
  it('handles API errors gracefully', async () => {
    mockedAxios.get.mockRejectedValue({
      response: { data: { detail: 'API Error occurred' } },
    })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('API Error occurred')
  })

  /**
   * @function displays Active badge for active assets
   * @description Verifies that active assets show the correct badge
   */
  it('displays Active badge for active assets', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001', is_decommissioned: false }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    const badge = wrapper.find('.badge-success')
    expect(badge.exists()).toBe(true)
    expect(badge.text()).toBe('Active')
  })

  /**
   * @function displays Decommissioned badge for decommissioned assets
   * @description Verifies that decommissioned assets show the correct badge
   */
  it('displays Decommissioned badge for decommissioned assets', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, resource_id: 'ASSET-001', is_decommissioned: true }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    const badge = wrapper.find('.badge-danger')
    expect(badge.exists()).toBe(true)
    expect(badge.text()).toBe('Decommissioned')
  })

  /**
   * @function formats dates correctly
   * @description Verifies that dates are formatted in a readable format
   */
  it('formats dates correctly', async () => {
    const mockAssets = [
      createMockAsset({ id: 1, date_added: '2024-01-15' }),
    ]
    mockedAxios.get.mockResolvedValue({ data: mockAssets })

    const wrapper = mountWithRouter(AssetListView)
    await flushPromises()

    // Date formatting will vary by locale, but should contain the date
    expect(wrapper.text()).toContain('Jan')
  })
})
