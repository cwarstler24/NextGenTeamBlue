/**
 * Unit Tests for HomeView Component
 * 
 * Tests the home view component which manages bearer token input and storage.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import HomeView from '@/views/HomeView.vue'
import { clearAllMocks, flushPromises } from '@/__tests__/testUtils'

describe('HomeView.vue', () => {
  beforeEach(() => {
    clearAllMocks()
  })

  afterEach(() => {
    localStorage.clear()
  })

  /**
   * @function renders the component correctly
   * @description Verifies that the HomeView component renders with expected structure and content
   */
  it('renders the component correctly', () => {
    const wrapper = mount(HomeView)

    expect(wrapper.find('.home-view').exists()).toBe(true)
    expect(wrapper.find('h1').text()).toBe('Welcome to Asset Management System')
    expect(wrapper.find('.token-section').exists()).toBe(true)
    expect(wrapper.find('.token-input').exists()).toBe(true)
    expect(wrapper.find('.btn-primary').text()).toBe('Save Token')
  })

  /**
   * @function loads existing token from localStorage on mount
   * @description Verifies that a saved token is loaded from localStorage when component mounts
   */
  it('loads existing token from localStorage on mount', async () => {
    const existingToken = 'Bearer test-token-123'
    localStorage.setItem('bearerToken', existingToken)

    const wrapper = mount(HomeView)
    await flushPromises()

    const input = wrapper.find<HTMLInputElement>('.token-input')
    expect(input.element.value).toBe(existingToken)
  })

  /**
   * @function saves token to localStorage when Save Token button is clicked
   * @description Verifies that token is properly saved to localStorage with Bearer prefix
   */
  it('saves token to localStorage when Save Token button is clicked', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')
    const button = wrapper.find('.btn-primary')

    await input.setValue('test-token-456')
    await button.trigger('click')

    expect(localStorage.getItem('bearerToken')).toBe('Bearer test-token-456')
  })

  /**
   * @function adds Bearer prefix if not present
   * @description Verifies that the Bearer prefix is automatically added to tokens without it
   */
  it('adds Bearer prefix if not present', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')
    const button = wrapper.find('.btn-primary')

    await input.setValue('raw-token-without-prefix')
    await button.trigger('click')

    expect(localStorage.getItem('bearerToken')).toBe('Bearer raw-token-without-prefix')
  })

  /**
   * @function does not duplicate Bearer prefix if already present
   * @description Verifies that existing Bearer prefix is preserved and not duplicated
   */
  it('does not duplicate Bearer prefix if already present', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')
    const button = wrapper.find('.btn-primary')

    await input.setValue('Bearer already-prefixed-token')
    await button.trigger('click')

    expect(localStorage.getItem('bearerToken')).toBe('Bearer already-prefixed-token')
  })

  /**
   * @function handles case-insensitive Bearer prefix check
   * @description Verifies that bearer prefix is recognized regardless of case
   */
  it('handles case-insensitive Bearer prefix check', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')
    const button = wrapper.find('.btn-primary')

    await input.setValue('bearer lowercase-bearer-token')
    await button.trigger('click')

    expect(localStorage.getItem('bearerToken')).toBe('bearer lowercase-bearer-token')
  })

  /**
   * @function trims whitespace from token input
   * @description Verifies that whitespace is properly trimmed from token input
   */
  it('trims whitespace from token input', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')
    const button = wrapper.find('.btn-primary')

    await input.setValue('  token-with-spaces  ')
    await button.trigger('click')

    expect(localStorage.getItem('bearerToken')).toBe('Bearer token-with-spaces')
  })

  /**
   * @function updates input field when typing
   * @description Verifies that v-model binding works correctly for input field
   */
  it('updates input field when typing', async () => {
    const wrapper = mount(HomeView)
    const input = wrapper.find<HTMLInputElement>('.token-input')

    await input.setValue('typing-test-token')

    expect(input.element.value).toBe('typing-test-token')
  })

  /**
   * @function renders help text about localStorage
   * @description Verifies that informative help text is displayed to users
   */
  it('renders help text about localStorage', () => {
    const wrapper = mount(HomeView)
    const helpText = wrapper.find('.help-text')

    expect(helpText.exists()).toBe(true)
    expect(helpText.text()).toContain('bearerToken')
    expect(helpText.text()).toContain('localStorage')
  })

})
