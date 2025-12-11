/**
 * Unit Tests for LoginView Component
 * 
 * Tests the login view component which handles user authentication.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import LoginView from '@/views/LoginView.vue'
import { mountWithRouter, clearAllMocks } from '@/__tests__/testUtils'

// Mock the encryption module
vi.mock('@/router/encryption.js', () => ({
  encryptPassword: vi.fn((username, password) => ({
    username: `encrypted_${username}`,
    password: `encrypted_${password}`,
  })),
}))

// Mock fetch globally
globalThis.fetch = vi.fn()

describe('LoginView.vue', () => {
  beforeEach(() => {
    clearAllMocks()
    vi.clearAllMocks()
    globalThis.fetch = vi.fn()
  })

  afterEach(() => {
    localStorage.clear()
  })

  /**
   * @function renders the component correctly
   * @description Verifies that the LoginView component renders with expected structure
   */
  it('renders the component correctly', () => {
    const wrapper = mountWithRouter(LoginView)

    expect(wrapper.find('.login-view').exists()).toBe(true)
    expect(wrapper.find('h1').text()).toBe('Login')
    expect(wrapper.find('#username').exists()).toBe(true)
    expect(wrapper.find('#password').exists()).toBe(true)
    expect(wrapper.find('#api-url').exists()).toBe(true)
  })

  /**
   * @function shows error when submitting without username
   * @description Verifies that validation error is shown for empty username
   */
  it('shows error when submitting without username', async () => {
    const wrapper = mountWithRouter(LoginView)

    const passwordInput = wrapper.find('#password')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('Please enter both username and password')
  })

  /**
   * @function shows error when submitting without password
   * @description Verifies that validation error is shown for empty password
   */
  it('shows error when submitting without password', async () => {
    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    await usernameInput.setValue('testuser')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('Please enter both username and password')
  })

  /**
   * @function shows error when API URL is empty
   * @description Verifies that validation error is shown for empty API URL
   */
  it('shows error when API URL is empty', async () => {
    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')
    const apiUrlInput = wrapper.find('#api-url')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')
    await apiUrlInput.setValue('')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('Please enter the API URL')
  })

  /**
   * @function successfully logs in with valid credentials
   * @description Verifies that successful login saves token and redirects
   */
  it('successfully logs in with valid credentials', async () => {
    const mockToken = 'test-token-123'
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: mockToken }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(localStorage.getItem('bearerToken')).toBe(`Bearer ${mockToken}`)
    expect(wrapper.text()).toContain('Login successful')
  })

  /**
   * @function adds Bearer prefix to token if not present
   * @description Verifies that Bearer prefix is added to tokens without it
   */
  it('adds Bearer prefix to token if not present', async () => {
    const mockToken = 'raw-token-without-prefix'
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: mockToken }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(localStorage.getItem('bearerToken')).toBe(`Bearer ${mockToken}`)
  })

  /**
   * @function preserves Bearer prefix if already present in token
   * @description Verifies that existing Bearer prefix is not duplicated
   */
  it('preserves Bearer prefix if already present in token', async () => {
    const mockToken = 'Bearer already-prefixed-token'
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: mockToken }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(localStorage.getItem('bearerToken')).toBe(mockToken)
  })

  /**
   * @function handles different token field names
   * @description Verifies that various token field names from API are handled
   */
  it('handles different token field names', async () => {
    const mockToken = 'test-access-token'
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ access_token: mockToken }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(localStorage.getItem('bearerToken')).toBe(`Bearer ${mockToken}`)
  })

  /**
   * @function displays error message on login failure
   * @description Verifies that API errors are displayed to the user
   */
  it('displays error message on login failure', async () => {
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 401,
      json: async () => ({ message: 'Invalid credentials' }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('wrongpassword')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('Invalid credentials')
  })

  /**
   * @function displays error when no token is received
   * @description Verifies that missing token in response is handled
   */
  it('displays error when no token is received', async () => {
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true }), // No token field
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.text()).toContain('No token received from server')
  })

  /**
   * @function disables inputs while loading
   * @description Verifies that form inputs are disabled during login process
   */
  it('disables inputs while loading', async () => {
    // Create a promise we can control
    let resolveLogin: any
    const loginPromise = new Promise((resolve) => {
      resolveLogin = resolve
    })

    ;(globalThis.fetch as any).mockReturnValueOnce(loginPromise)

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find<HTMLInputElement>('#username')
    const passwordInput = wrapper.find<HTMLInputElement>('#password')
    const apiUrlInput = wrapper.find<HTMLInputElement>('#api-url')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await wrapper.vm.$nextTick()

    // Check that inputs are disabled
    expect(usernameInput.element.disabled).toBe(true)
    expect(passwordInput.element.disabled).toBe(true)
    expect(apiUrlInput.element.disabled).toBe(true)

    // Resolve the login
    resolveLogin({
      ok: true,
      json: async () => ({ token: 'test-token' }),
    })
    await flushPromises()
  })

  /**
   * @function displays loading state during login
   * @description Verifies that loading state is shown during authentication
   */
  it('displays loading state during login', async () => {
    let resolveLogin: any
    const loginPromise = new Promise((resolve) => {
      resolveLogin = resolve
    })

    ;(globalThis.fetch as any).mockReturnValueOnce(loginPromise)

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await wrapper.vm.$nextTick()

    const loginButton = wrapper.find('button[type="submit"]')
    if (loginButton.exists()) {
      expect(loginButton.text()).toContain('Logging in')
    }

    resolveLogin({
      ok: true,
      json: async () => ({ token: 'test-token' }),
    })
    await flushPromises()
  })

  /**
   * @function encrypts credentials before sending
   * @description Verifies that password encryption is called before API request
   */
  it('encrypts credentials before sending', async () => {
    const { encryptPassword } = await import('@/router/encryption.js')
    
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: 'test-token' }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(encryptPassword).toHaveBeenCalledWith('testuser', 'password123')
  })

  /**
   * @function allows customizing API URL
   * @description Verifies that users can change the API endpoint
   */
  it('allows customizing API URL', async () => {
    const customUrl = 'https://custom-api.example.com/login'
    
    ;(globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ token: 'test-token' }),
    })

    const wrapper = mountWithRouter(LoginView)

    const usernameInput = wrapper.find('#username')
    const passwordInput = wrapper.find('#password')
    const apiUrlInput = wrapper.find('#api-url')

    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')
    await apiUrlInput.setValue(customUrl)

    const form = wrapper.find('.login-form')
    await form.trigger('submit.prevent')
    await flushPromises()

    expect(globalThis.fetch).toHaveBeenCalledWith(
      customUrl,
      expect.objectContaining({
        method: 'POST',
      })
    )
  })
})

