/**
 * Test Suite: EmployeeListView.spec.ts
 * 
 * Purpose: Tests the EmployeeListView component which displays a searchable
 * list of all employees in the system. Provides search functionality to filter
 * employees by name with debouncing.
 * 
 * Test Coverage:
 * - Component rendering with employee table
 * - Fetching employee data from API on mount
 * - Search functionality with debounced input
 * - Display states: loading, empty, error, data
 * - Result count display
 * - Token validation and authorization headers
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import EmployeeListView from '../EmployeeListView.vue'
import axios from 'axios'

vi.mock('axios')

const mockEmployees = [
  { employee_id: 101, first_name: 'John', last_name: 'Doe' },
  { employee_id: 102, first_name: 'Jane', last_name: 'Smith' },
  { employee_id: 103, first_name: 'Bob', last_name: 'Johnson' }
]

describe('EmployeeListView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.useFakeTimers()
    localStorage.setItem('bearerToken', 'Bearer test-token')
    
    vi.mocked(axios.get).mockResolvedValue({ data: mockEmployees })
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
    vi.useRealTimers()
  })

  it('renders page header with title', () => {
    const wrapper = mount(EmployeeListView)
    
    expect(wrapper.find('h1').text()).toBe('Employee Directory')
    expect(wrapper.text()).toContain('Browse all employees in the system')
  })

  it('renders search input', () => {
    const wrapper = mount(EmployeeListView)
    
    expect(wrapper.find('.search-input').exists()).toBe(true)
    expect(wrapper.find('.search-input').attributes('placeholder')).toBe('Search by name...')
  })

  it('displays loading state initially', async () => {
    vi.mocked(axios.get).mockImplementation(() => new Promise(() => {}))
    
    const wrapper = mount(EmployeeListView)
    
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.loading-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('Loading employees...')
  })

  it('fetches employees on mount', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/resources/employees/'),
      expect.objectContaining({
        headers: { Authorization: 'Bearer test-token' },
        params: { limit: 1000 }
      })
    )
  })

  it('displays employee data in table', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.employee-table').exists()).toBe(true)
    expect(wrapper.text()).toContain('John')
    expect(wrapper.text()).toContain('Doe')
    expect(wrapper.text()).toContain('Jane')
    expect(wrapper.text()).toContain('Smith')
    expect(wrapper.text()).toContain('Bob')
    expect(wrapper.text()).toContain('Johnson')
  })

  it('displays employee IDs in table', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.text()).toContain('101')
    expect(wrapper.text()).toContain('102')
    expect(wrapper.text()).toContain('103')
  })

  it('displays full names in table', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.text()).toContain('John Doe')
    expect(wrapper.text()).toContain('Jane Smith')
    expect(wrapper.text()).toContain('Bob Johnson')
  })

  it('displays correct result count', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.text()).toContain('Showing 3 employees')
  })

  it('displays singular result count for one employee', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [mockEmployees[0]] })
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.text()).toContain('Showing 1 employee')
    expect(wrapper.text()).not.toMatch(/Showing \d+ employees/)
  })

  it('displays error message when fetch fails', async () => {
    vi.mocked(axios.get).mockRejectedValueOnce({
      response: { data: { detail: 'Fetch error' } }
    })
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Fetch error')
  })

  it('displays error when no bearer token exists', async () => {
    localStorage.removeItem('bearerToken')
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('No bearer token set')
  })

  it('displays empty state when no employees found', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('No Employees Found')
  })

  it('performs search with debouncing', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    vi.clearAllMocks()
    
    const searchInput = wrapper.find('.search-input')
    await searchInput.setValue('John')
    await searchInput.trigger('input')
    
    // Should not call immediately
    expect(axios.get).not.toHaveBeenCalled()
    
    // Advance timers past debounce delay
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({
          q: 'John'
        })
      })
    )
  })

  it('cancels previous search when typing quickly', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    vi.clearAllMocks()
    
    const searchInput = wrapper.find('.search-input')
    
    // Type multiple times quickly
    await searchInput.setValue('J')
    await searchInput.trigger('input')
    vi.advanceTimersByTime(100)
    
    await searchInput.setValue('Jo')
    await searchInput.trigger('input')
    vi.advanceTimersByTime(100)
    
    await searchInput.setValue('John')
    await searchInput.trigger('input')
    
    // Advance to debounce delay
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    // Should only call once with final value
    expect(axios.get).toHaveBeenCalledTimes(1)
    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({
          q: 'John'
        })
      })
    )
  })

  it('displays search query in result count', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    const searchInput = wrapper.find('.search-input')
    await searchInput.setValue('John')
    await searchInput.trigger('input')
    
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    expect(wrapper.text()).toContain('matching "John"')
  })

  it('shows message to adjust search when no results with query', async () => {
    vi.mocked(axios.get).mockResolvedValueOnce({ data: [] })
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    const searchInput = wrapper.find('.search-input')
    await searchInput.setValue('NonexistentName')
    await searchInput.trigger('input')
    
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('Try adjusting your search query')
  })

  it('adds Bearer prefix to token if missing', async () => {
    localStorage.setItem('bearerToken', 'plain-token')
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: { Authorization: 'Bearer plain-token' }
      })
    )
  })

  it('renders table headers correctly', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    const headers = wrapper.findAll('th')
    expect(headers[0]!.text()).toBe('ID')
    expect(headers[1]!.text()).toBe('First Name')
    expect(headers[2]!.text()).toBe('Last Name')
    expect(headers[3]!.text()).toBe('Full Name')
  })

  it('handles large employee lists', async () => {
    const manyEmployees = Array.from({ length: 100 }, (_, i) => ({
      employee_id: i,
      first_name: `Employee${i}`,
      last_name: 'Test'
    }))
    
    vi.mocked(axios.get).mockResolvedValueOnce({ data: manyEmployees })
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.text()).toContain('Showing 100 employees')
    const rows = wrapper.findAll('.employee-row')
    expect(rows.length).toBe(100)
  })

  it('clears employees on token error', async () => {
    localStorage.removeItem('bearerToken')
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.employee-table').exists()).toBe(false)
  })

  it('trims whitespace from search query', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    vi.clearAllMocks()
    
    const searchInput = wrapper.find('.search-input')
    await searchInput.setValue('  John  ')
    await searchInput.trigger('input')
    
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({
          q: 'John'
        })
      })
    )
  })

  it('does not include search param when query is empty', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    vi.clearAllMocks()
    
    const searchInput = wrapper.find('.search-input')
    await searchInput.setValue('')
    await searchInput.trigger('input')
    
    vi.advanceTimersByTime(300)
    await flushPromises()
    
    const callParams = vi.mocked(axios.get).mock.calls[0]![1]?.params
    expect(callParams).not.toHaveProperty('q')
  })

  it('fetches with limit of 1000', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(axios.get).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({
          limit: 1000
        })
      })
    )
  })

  it('displays generic error message when detail is missing', async () => {
    vi.mocked(axios.get).mockRejectedValueOnce(new Error('Network error'))
    
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Failed to fetch employees')
  })

  it('applies correct CSS classes to table elements', async () => {
    const wrapper = mount(EmployeeListView)
    
    await flushPromises()
    
    expect(wrapper.find('.employee-list-view').exists()).toBe(true)
    expect(wrapper.find('.employee-table-container').exists()).toBe(true)
    expect(wrapper.find('.employee-table').exists()).toBe(true)
    expect(wrapper.find('.employee-row').exists()).toBe(true)
    expect(wrapper.find('.employee-id').exists()).toBe(true)
    expect(wrapper.find('.full-name').exists()).toBe(true)
  })
})
