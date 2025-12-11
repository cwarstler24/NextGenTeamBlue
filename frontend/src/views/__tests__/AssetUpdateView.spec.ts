/**
 * Test Suite: AssetUpdateView.spec.ts
 * 
 * Purpose: Tests the AssetUpdateView component which provides a form to edit
 * existing assets. Loads current asset data, allows modifications, and saves
 * updates via PUT request to the API.
 * 
 * Test Coverage:
 * - Loading existing asset data based on route params
 * - Form pre-population with current asset values
 * - Form validation for required fields
 * - Asset update via PUT request to API
 * - Binary field conversion for is_decommissioned
 * - Success and error handling for updates
 * - Navigation actions (back to detail view, after successful update)
 * - Token validation and authorization headers
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import AssetUpdateView from '../AssetUpdateView.vue'
import axios from 'axios'

vi.mock('axios')

const mockRouter = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/assets/:id', name: 'AssetView', component: { template: '<div>View</div>' } },
    { path: '/assets/:id/update', name: 'AssetUpdate', component: AssetUpdateView }
  ]
})

const mockAsset = {
  id: 123,
  resource_id: 'LAPTOP-001',
  type_id: 1,
  location_id: 5,
  employee_id: null,
  date_added: '2024-01-15T10:30:00Z',
  is_decommissioned: 0,
  notes: 'Test notes'
}

const mockAssetTypes = [
  { id: 1, asset_type_name: 'Laptop' },
  { id: 2, asset_type_name: 'Monitor' }
]

const mockLocations = [
  { id: 5, asset_location_name: 'Building A' },
  { id: 6, asset_location_name: 'Building B' }
]

describe('AssetUpdateView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('bearerToken', 'Bearer test-token')
    mockRouter.push('/assets/123/update')
    
    // Default mock responses
    vi.mocked(axios.get).mockImplementation((url: string) => {
      if (url.includes('/resources/123')) {
        return Promise.resolve({ data: mockAsset })
      }
      if (url.includes('/asset_types')) {
        return Promise.resolve({ data: mockAssetTypes })
      }
      if (url.includes('/asset_locations')) {
        return Promise.resolve({ data: mockLocations })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('renders loading state initially', async () => {
    vi.mocked(axios.get).mockImplementation(() => new Promise(() => {}))
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.loading-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('Loading asset details...')
  })

  it('displays error when no bearer token exists', async () => {
    localStorage.removeItem('bearerToken')
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('No bearer token set')
  })

  it('fetches and pre-populates form with asset data', async () => {
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    expect(wrapper.find('h1').text()).toBe('Update Asset')
    expect(wrapper.find('.asset-form').exists()).toBe(true)
    
    const typeSelect = wrapper.find('#type_id')
    expect(typeSelect.element.value).toBe('1')
    
    const locationSelect = wrapper.find('#location_id')
    expect(locationSelect.element.value).toBe('5')
    
    const notesTextarea = wrapper.find('#notes')
    expect(notesTextarea.element.value).toBe('Test notes')
  })

  it('loads asset types and locations on mount', async () => {
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/resources/123'),
      expect.any(Object)
    )
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/asset_types'),
      expect.any(Object)
    )
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/asset_locations'),
      expect.any(Object)
    )
  })

  it('successfully updates asset with changed values', async () => {
    vi.mocked(axios.put).mockResolvedValueOnce({ data: { ...mockAsset, type_id: 2 } })
    window.alert = vi.fn()
    
    const pushSpy = vi.spyOn(mockRouter, 'push')
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    // Change type
    await wrapper.find('#type_id').setValue(2)
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(axios.put).toHaveBeenCalledWith(
      expect.stringContaining('/resources/123'),
      expect.objectContaining({
        type_id: 2,
        location_id: 5
      }),
      expect.any(Object)
    )
    
    expect(window.alert).toHaveBeenCalledWith('Asset updated successfully!')
    expect(pushSpy).toHaveBeenCalledWith({ name: 'AssetView', params: { id: '123' } })
  })

  it('includes notes in update payload when provided', async () => {
    vi.mocked(axios.put).mockResolvedValueOnce({ data: mockAsset })
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    await wrapper.find('#notes').setValue('Updated notes')
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(axios.put).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        notes: 'Updated notes'
      }),
      expect.any(Object)
    )
  })

  it('updates status to decommissioned', async () => {
    vi.mocked(axios.put).mockResolvedValueOnce({ data: mockAsset })
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    await wrapper.find('#is_decommissioned').setValue(1)
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(axios.put).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        is_decommissioned: 1
      }),
      expect.any(Object)
    )
  })

  it('switches from location to employee assignment', async () => {
    vi.mocked(axios.put).mockResolvedValueOnce({ data: mockAsset })
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    // Clear location and set employee
    await wrapper.find('#location_id').setValue('')
    await wrapper.find('#employee_id').setValue(42)
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(axios.put).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        employee_id: 42
      }),
      expect.any(Object)
    )
  })

  it('alerts when neither location nor employee is provided', async () => {
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    // Clear both location and employee
    await wrapper.find('#location_id').setValue('')
    await wrapper.find('#employee_id').setValue('')
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(window.alert).toHaveBeenCalledWith(
      'Please assign the asset to either a location or an employee.'
    )
    expect(axios.put).not.toHaveBeenCalled()
  })

  it('displays error alert when update fails', async () => {
    vi.mocked(axios.put).mockRejectedValueOnce({
      response: { data: { detail: 'Update failed' } }
    })
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    expect(window.alert).toHaveBeenCalledWith('Update failed')
  })

  it('navigates back to asset view when cancel clicked', async () => {
    const pushSpy = vi.spyOn(mockRouter, 'push')
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const cancelButton = wrapper.find('.btn-secondary')
    await cancelButton.trigger('click')
    
    expect(pushSpy).toHaveBeenCalledWith({ name: 'AssetView', params: { id: '123' } })
  })

  it('navigates back when top back button clicked', async () => {
    const pushSpy = vi.spyOn(mockRouter, 'push')
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const backButton = wrapper.find('.btn-back')
    await backButton.trigger('click')
    
    expect(pushSpy).toHaveBeenCalledWith({ name: 'AssetView', params: { id: '123' } })
  })

  it('converts binary is_decommissioned field correctly', async () => {
    vi.mocked(axios.get).mockImplementation((url: string) => {
      if (url.includes('/resources/123')) {
        return Promise.resolve({
          data: { ...mockAsset, is_decommissioned: [1] } // MySQL buffer format
        })
      }
      if (url.includes('/asset_types')) {
        return Promise.resolve({ data: mockAssetTypes })
      }
      if (url.includes('/asset_locations')) {
        return Promise.resolve({ data: mockLocations })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const statusSelect = wrapper.find('#is_decommissioned')
    expect(statusSelect.element.value).toBe('1')
  })

  it('adds Bearer prefix to token if missing', async () => {
    localStorage.setItem('bearerToken', 'plain-token')
    vi.mocked(axios.put).mockResolvedValueOnce({ data: mockAsset })
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    
    const axiosCall = vi.mocked(axios.put).mock.calls[0]
    expect(axiosCall![2]?.headers?.Authorization).toBe('Bearer plain-token')
  })

  it('disables submit button while updating', async () => {
    vi.mocked(axios.put).mockImplementation(() => new Promise(() => {})) // Never resolves
    window.alert = vi.fn()
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const submitButton = wrapper.find('.btn-primary')
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    await wrapper.vm.$nextTick()
    
    expect(submitButton.attributes('disabled')).toBeDefined()
    expect(submitButton.text()).toContain('Updating...')
  })

  it('displays error when asset fetch fails', async () => {
    vi.mocked(axios.get).mockImplementation((url: string) => {
      if (url.includes('/resources/123')) {
        return Promise.reject({
          response: { data: { detail: 'Asset not found' } }
        })
      }
      if (url.includes('/asset_types')) {
        return Promise.resolve({ data: mockAssetTypes })
      }
      if (url.includes('/asset_locations')) {
        return Promise.resolve({ data: mockLocations })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Asset not found')
  })

  it('handles asset with employee instead of location', async () => {
    vi.mocked(axios.get).mockImplementation((url: string) => {
      if (url.includes('/resources/123')) {
        return Promise.resolve({
          data: { ...mockAsset, location_id: null, employee_id: 42 }
        })
      }
      if (url.includes('/asset_types')) {
        return Promise.resolve({ data: mockAssetTypes })
      }
      if (url.includes('/asset_locations')) {
        return Promise.resolve({ data: mockLocations })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const locationSelect = wrapper.find('#location_id')
    expect(locationSelect.element.value).toBe('')
    
    const employeeInput = wrapper.find('#employee_id')
    expect(employeeInput.element.value).toBe('42')
  })

  it('handles asset without notes', async () => {
    vi.mocked(axios.get).mockImplementation((url: string) => {
      if (url.includes('/resources/123')) {
        return Promise.resolve({
          data: { ...mockAsset, notes: null }
        })
      }
      if (url.includes('/asset_types')) {
        return Promise.resolve({ data: mockAssetTypes })
      }
      if (url.includes('/asset_locations')) {
        return Promise.resolve({ data: mockLocations })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })
    
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const notesTextarea = wrapper.find('#notes')
    expect(notesTextarea.element.value).toBe('')
  })

  it('renders form description text', async () => {
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    expect(wrapper.text()).toContain('Modify the asset details and submit to save changes')
  })

  it('displays help text for form fields', async () => {
    const wrapper = mount(AssetUpdateView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await flushPromises()
    
    const helpTexts = wrapper.findAll('.help-text')
    expect(helpTexts.length).toBeGreaterThan(0)
  })
})
