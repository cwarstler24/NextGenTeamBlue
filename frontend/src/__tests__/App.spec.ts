/**
 * Unit Tests for App Component
 * 
 * Tests the main App component including navigation, music player, and layout.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '@/App.vue'
import { mountWithRouter, clearAllMocks } from '@/__tests__/testUtils'

describe('App.vue', () => {
  beforeEach(() => {
    clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  /**
   * @function renders the component correctly
   * @description Verifies that the App component renders with expected structure
   */
  it('renders the component correctly', () => {
    const wrapper = mountWithRouter(App)

    expect(wrapper.find('#app').exists()).toBe(true)
    expect(wrapper.find('header').exists()).toBe(true)
    expect(wrapper.find('main').exists()).toBe(true)
    expect(wrapper.find('footer').exists()).toBe(true)
  })

  /**
   * @function displays the brand name correctly
   * @description Verifies that the Team Blue branding is displayed
   */
  it('displays the brand name correctly', () => {
    const wrapper = mountWithRouter(App)

    expect(wrapper.text()).toContain('Team Blue')
    expect(wrapper.text()).toContain('Asset Management')
  })

  /**
   * @function renders all navigation links
   * @description Verifies that all expected navigation links are present
   */
  it('renders all navigation links', () => {
    const wrapper = mountWithRouter(App)

    const nav = wrapper.find('nav')
    expect(nav.exists()).toBe(true)
    
    const links = nav.findAll('a')
    expect(links.length).toBeGreaterThan(0)
    
    // Check for specific navigation items
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('Login')
    expect(wrapper.text()).toContain('Assets')
    expect(wrapper.text()).toContain('Add Asset')
    expect(wrapper.text()).toContain('Employees')
    expect(wrapper.text()).toContain('About Us')
  })

  /**
   * @function renders mascot logo
   * @description Verifies that the mascot logo is rendered in the header
   */
  it('renders mascot logo', () => {
    const wrapper = mountWithRouter(App)

    const logo = wrapper.find('.mascot-logo img')
    expect(logo.exists()).toBe(true)
    expect(logo.attributes('alt')).toBe('Team Blue Mascot')
  })

  /**
   * @function renders RouterView component
   * @description Verifies that RouterView is present for rendering child routes
   */
  it('renders RouterView component', () => {
    const wrapper = mountWithRouter(App)

    // RouterView is stubbed in tests, check for the stub instead
    const routerView = wrapper.find('.router-view')
    expect(routerView.exists()).toBe(true)
  })

  /**
   * @function renders footer with mascot
   * @description Verifies that the footer is rendered with mascot image
   */
  it('renders footer with mascot', () => {
    const wrapper = mountWithRouter(App)

    const footer = wrapper.find('.app-footer')
    expect(footer.exists()).toBe(true)
    
    const footerMascot = footer.find('.footer-mascot img')
    expect(footerMascot.exists()).toBe(true)
    expect(footerMascot.attributes('alt')).toBe('Santa Swab')
  })

  /**
   * @function renders music toggle button
   * @description Verifies that the music toggle button is present
   */
  it('renders music toggle button', () => {
    const wrapper = mountWithRouter(App)

    const musicButton = wrapper.find('.music-toggle')
    expect(musicButton.exists()).toBe(true)
  })

  /**
   * @function toggles music state when button is clicked
   * @description Verifies that clicking the music button toggles the playing state
   */
  it('toggles music state when button is clicked', async () => {
    const wrapper = mountWithRouter(App)

    const musicButton = wrapper.find('.music-toggle')
    const audioElement = wrapper.find('audio').element as HTMLAudioElement
    
    // Mock audio element methods
    audioElement.play = vi.fn().mockResolvedValue(undefined)
    audioElement.pause = vi.fn()

    // Initial state should be not playing
    expect(musicButton.classes()).not.toContain('playing')
    expect(wrapper.text()).toContain('🔇')

    // Click to play
    await musicButton.trigger('click')
    await wrapper.vm.$nextTick()

    expect(audioElement.play).toHaveBeenCalled()
  })

  /**
   * @function renders snowflakes decorations
   * @description Verifies that decorative snowflakes are rendered
   */
  it('renders snowflakes decorations', () => {
    const wrapper = mountWithRouter(App)

    const snowflakes = wrapper.find('.snowflakes')
    expect(snowflakes.exists()).toBe(true)
    
    const snowflakeElements = snowflakes.findAll('.snowflake')
    expect(snowflakeElements.length).toBeGreaterThan(0)
  })

  /**
   * @function renders sleigh cursor follower
   * @description Verifies that the sleigh cursor follower element is rendered
   */
  it('renders sleigh cursor follower', () => {
    const wrapper = mountWithRouter(App)

    const sleighCursor = wrapper.find('.sleigh-cursor')
    expect(sleighCursor.exists()).toBe(true)
    
    const sleighImage = sleighCursor.find('img')
    expect(sleighImage.exists()).toBe(true)
    expect(sleighImage.attributes('alt')).toContain('Sleigh')
  })

  /**
   * @function updates sleigh position on mouse move
   * @description Verifies that mouse movement updates the sleigh cursor position
   */
  it('updates sleigh position on mouse move', async () => {
    const wrapper = mountWithRouter(App)

    const sleighCursor = wrapper.find('.sleigh-cursor')
    const initialStyle = sleighCursor.attributes('style')

    // Simulate mouse move event
    const mouseMoveEvent = new MouseEvent('mousemove', {
      clientX: 100,
      clientY: 200,
    })
    window.dispatchEvent(mouseMoveEvent)

    await wrapper.vm.$nextTick()

    const updatedStyle = sleighCursor.attributes('style')
    expect(updatedStyle).not.toBe(initialStyle)
    expect(updatedStyle).toContain('left:')
    expect(updatedStyle).toContain('top:')
  })

  /**
   * @function renders audio element
   * @description Verifies that the audio element is present for music playback
   */
  it('renders audio element', () => {
    const wrapper = mountWithRouter(App)

    const audio = wrapper.find('audio')
    expect(audio.exists()).toBe(true)
    expect(audio.attributes('loop')).toBeDefined()
    
    const source = audio.find('source')
    expect(source.exists()).toBe(true)
    expect(source.attributes('type')).toBe('audio/mpeg')
  })

  /**
   * @function renders mascot background
   * @description Verifies that decorative background elements are rendered
   */
  it('renders mascot background', () => {
    const wrapper = mountWithRouter(App)

    const mascotBackground = wrapper.find('.mascot-background')
    expect(mascotBackground.exists()).toBe(true)
  })

  /**
   * @function renders mascot watermark
   * @description Verifies that the mascot watermark is rendered in main content
   */
  it('renders mascot watermark', () => {
    const wrapper = mountWithRouter(App)

    const mascotWatermark = wrapper.find('.mascot-watermark')
    expect(mascotWatermark.exists()).toBe(true)
  })

  /**
   * @function cleans up event listeners on unmount
   * @description Verifies that mousemove event listener is removed when component unmounts
   */
  it('cleans up event listeners on unmount', () => {
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener')
    const wrapper = mountWithRouter(App)

    wrapper.unmount()

    expect(removeEventListenerSpy).toHaveBeenCalledWith('mousemove', expect.any(Function))
  })

  /**
   * @function has proper semantic HTML structure
   * @description Verifies that the component uses proper semantic HTML elements
   */
  it('has proper semantic HTML structure', () => {
    const wrapper = mountWithRouter(App)

    expect(wrapper.find('header').exists()).toBe(true)
    expect(wrapper.find('nav').exists()).toBe(true)
    expect(wrapper.find('main').exists()).toBe(true)
    expect(wrapper.find('footer').exists()).toBe(true)
  })
})
