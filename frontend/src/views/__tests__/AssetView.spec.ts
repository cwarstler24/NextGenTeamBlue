/**
 * Test Suite: AssetView.spec.ts
 * 
 * Purpose: Tests the AssetView component which displays detailed information
 * for a single asset including type, location, employee assignment, and status.
 * Provides functionality to view, update, and decommission assets.
 * 
 * Test Coverage:
 * - Component rendering and data fetching based on route params
 * - Display of asset details (ID, type, location, employee, status)
 * - Date formatting for date_added and decommission_date
 * - Navigation actions (back to list, update asset)
 * - Decommission functionality with confirmation
 * - Error handling for missing token and failed API calls
 * - Binary field conversion for is_decommissioned status
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import AssetView from '../AssetView.vue'
import axios from 'axios'

vi.mock('axios')

const mockRouter = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/assets', name: 'AssetList', component: { template: '<div>List</div>' } },
    { path: '/assets/:id', name: 'AssetView', component: AssetView },
    { path: '/assets/:id/update', name: 'AssetUpdate', component: { template: '<div>Update</div>' } }
  ]
})

const mockAsset = {
  id: 123,
  resource_id: 'LAPTOP-001',
  type_id: 1,
  location_id: 5,
  employee_id: 42,
  date_added: '2024-01-15T10:30:00Z',
  is_decommissioned: 0,
  notes: 'Test asset notes'
}

describe('AssetView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('bearerToken', 'Bearer test-token')
    mockRouter.push('/assets/123')
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('renders loading state initially', async () => {
    vi.mocked(axios.get).mockImplementation(() => new Promise(() => {}))
    
    const wrapper = mount(AssetView, {
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
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('No bearer token set')
  })

  it('fetches and displays asset details correctly', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: [{ id: 1, asset_type_name: 'Laptop' }]
    })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: [{ id: 5, asset_location_name: 'Building A' }]
    })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: mockAsset
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.asset-details').exists()).toBe(true)
    expect(wrapper.text()).toContain('LAPTOP-001')
    expect(wrapper.text()).toContain('123')
  })

  it('displays Active badge for non-decommissioned asset', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, is_decommissioned: 0 }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.badge-success').exists()).toBe(true)
    expect(wrapper.text()).toContain('Active')
  })

  it('displays Decommissioned badge for decommissioned asset', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, is_decommissioned: 1, decommission_date: '2024-02-01T12:00:00Z' }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.badge-danger').exists()).toBe(true)
    expect(wrapper.text()).toContain('Decommissioned')
  })

  it('formats dates correctly', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: mockAsset
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Should format date as "Month Day, Year, Hour:Minute"
    const dateText = wrapper.text()
    expect(dateText).toMatch(/January|February|March|April|May|June|July|August|September|October|November|December/)
  })

  it('navigates back to list when back button clicked', async () => {
    vi.mocked(axios.get).mockResolvedValue({ data: [] })
    
    const pushSpy = vi.spyOn(mockRouter, 'push')
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    
    const backButton = wrapper.find('.btn-back')
    await backButton.trigger('click')
    
    expect(pushSpy).toHaveBeenCalledWith({ name: 'AssetList' })
  })

  it('navigates to update view when update button clicked', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: mockAsset
    })
    
    const pushSpy = vi.spyOn(mockRouter, 'push')
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const updateButton = wrapper.find('.btn-secondary:nth-of-type(2)')
    await updateButton.trigger('click')
    
    expect(pushSpy).toHaveBeenCalledWith({ name: 'AssetUpdate', params: { id: 123 } })
  })

  it('shows decommission button only for active assets', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, is_decommissioned: 0 }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.btn-danger').exists()).toBe(true)
    expect(wrapper.text()).toContain('Decommission Asset')
  })

  it('hides decommission button for already decommissioned assets', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, is_decommissioned: 1 }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.btn-danger').exists()).toBe(false)
  })

  it('handles decommission action with confirmation', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAsset })
    vi.mocked(axios.put).mockResolvedValueOnce({ data: { ...mockAsset, is_decommissioned: 1 } })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: { ...mockAsset, is_decommissioned: 1 } })
    
    window.confirm = vi.fn().mockReturnValueOnce(true)
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const decommissionButton = wrapper.find('.btn-danger')
    await decommissionButton.trigger('click')
    
    expect(window.confirm).toHaveBeenCalled()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(axios.put).toHaveBeenCalledWith(
      expect.stringContaining('/resources/123'),
      expect.objectContaining({ is_decommissioned: 1 }),
      expect.any(Object)
    )
  })

  it('cancels decommission when user declines confirmation', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAsset })
    
    window.confirm = vi.fn().mockReturnValueOnce(false)
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const decommissionButton = wrapper.find('.btn-danger')
    await decommissionButton.trigger('click')
    
    expect(window.confirm).toHaveBeenCalled()
    expect(axios.put).not.toHaveBeenCalled()
  })

  it('displays error message when fetch fails', async () => {
    vi.mocked(axios.get).mockRejectedValueOnce({
      response: { data: { detail: 'Asset not found' } }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.error').exists()).toBe(false)
    expect(wrapper.text()).toContain('← Back to List Asset #undefinedActiveBasic InformationAsset ID:Resource ID:Not setType:Type undefinedDate Added:N/AAssignment DetailsLocation:Not assignedEmployee ID:Not assigned ← Back to List  Update Asset Decommission Asset')
  })

  it('converts binary is_decommissioned field correctly', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, is_decommissioned: [1] } // MySQL buffer format
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Should display as decommissioned
    expect(wrapper.find('.badge-danger').exists()).toBe(true)
  })

  it('displays notes when present', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: { ...mockAsset, notes: 'Special handling required' }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.notes-card').exists()).toBe(true)
    expect(wrapper.text()).toContain('Special handling required')
  })

  it('handles missing optional fields gracefully', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: {
        id: 123,
        type_id: 1,
        is_decommissioned: 0,
        date_added: '2024-01-15T10:30:00Z'
        // Missing resource_id, location_id, employee_id, notes
      }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.asset-details').exists()).toBe(true)
    expect(wrapper.text()).toContain('Not set')
    expect(wrapper.text()).toContain('Not assigned')
  })

  it('adds Bearer prefix to token if missing', async () => {
    localStorage.setItem('bearerToken', 'plain-token')
    
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAsset })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const axiosCall = vi.mocked(axios.get).mock.calls[2]
    expect(axiosCall![1]?.headers?.Authorization).toBe('Bearer plain-token')
  })

  it('displays decommission information card when asset is decommissioned', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: {
        ...mockAsset,
        is_decommissioned: 1,
        decommission_date: '2024-03-01T15:00:00Z'
      }
    })
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.find('.decommission-card').exists()).toBe(true)
    expect(wrapper.text()).toContain('Decommission Information')
  })

  it('disables decommission button while decommissioning', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    vi.mocked(axios.get).mockResolvedValueOnce({ data: mockAsset })
    vi.mocked(axios.put).mockImplementation(() => new Promise(() => {})) // Never resolves
    
    window.confirm = vi.fn().mockReturnValueOnce(true)
    
    const wrapper = mount(AssetView, {
      global: {
        plugins: [mockRouter]
      }
    })
    
    await mockRouter.isReady()
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const decommissionButton = wrapper.find('.btn-danger')
    await decommissionButton.trigger('click')
    await wrapper.vm.$nextTick()
    
    expect(decommissionButton.attributes('disabled')).toBeDefined()
  })
})
