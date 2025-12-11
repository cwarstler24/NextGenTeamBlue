/**
 * Test Suite: MascotTheme.spec.ts
 * 
 * Purpose: Tests the MascotTheme component which showcases the application's
 * mascot "Swab" in various themed scenarios (rescue hero, action hero, Santa's helper).
 * Includes interactive video modals and holiday theme color palette display.
 * 
 * Test Coverage:
 * - Component rendering with mascot cards and theme elements
 * - Video modal opening/closing for each mascot variant
 * - Color palette display
 * - Button showcase rendering
 * - Click event handling for interactive elements
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MascotTheme from '../MascotTheme.vue'

describe('MascotTheme', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders hero section with title', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.hero-section').exists()).toBe(true)
    expect(wrapper.find('h1').text()).toContain('Meet Swab!')
    expect(wrapper.text()).toContain('Delivering asset management joy this holiday season!')
  })

  it('renders all three mascot cards', () => {
    const wrapper = mount(MascotTheme)
    
    const mascotCards = wrapper.findAll('.mascot-card')
    expect(mascotCards.length).toBe(3)
  })

  it('displays rescue operations mascot card', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.text()).toContain('Rescue Operations')
    expect(wrapper.text()).toContain('Always ready to save the day and secure your assets!')
    expect(wrapper.text()).toContain('Hero Mode')
  })

  it('displays action ready mascot card', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.text()).toContain('Action Ready')
    expect(wrapper.text()).toContain('Armed with the best asset management tools!')
    expect(wrapper.text()).toContain('Combat Ready')
  })

  it('displays Santa helper mascot card', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.text()).toContain('Santa\'s Helper')
    expect(wrapper.text()).toContain('Making sure all kids get their presents!')
    expect(wrapper.text()).toContain('Jolly')
  })

  it('displays click hints on mascot cards', () => {
    const wrapper = mount(MascotTheme)
    
    const clickHints = wrapper.findAll('.click-hint')
    expect(clickHints.length).toBe(3)
    expect(wrapper.text()).toContain('Click to watch the rescue!')
    expect(wrapper.text()).toContain('Click to watch the action!')
    expect(wrapper.text()).toContain('Click to see the magic!')
  })

  it('renders mascot images', () => {
    const wrapper = mount(MascotTheme)
    
    const images = wrapper.findAll('img')
    expect(images.length).toBe(3)
    expect(images[0]!.attributes('src')).toBe('/mascot/mascot-hero.png')
    expect(images[0]!.attributes('alt')).toBe('Helicopter Rescue Hero')
    expect(images[1]!.attributes('src')).toBe('/mascot/mascot-action.png')
    expect(images[2]!.attributes('src')).toBe('/mascot/SantaSwab.png')
  })

  it('opens hero video modal when rescue card clicked', async () => {
    const wrapper = mount(MascotTheme)
    
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videoModals = wrapper.findAll('.video-modal')
    const heroModal = videoModals.find(modal => modal.text().includes('Swab The Savior'))
    expect(heroModal!.isVisible()).toBe(true)
  })

  it('opens action video modal when action card clicked', async () => {
    const wrapper = mount(MascotTheme)
    
    const actionCard = wrapper.findAll('.mascot-card')[1]
    await actionCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videoModals = wrapper.findAll('.video-modal')
    const actionModal = videoModals.find(modal => modal.text().includes('Swab The Leader'))
    expect(actionModal!.isVisible()).toBe(true)
  })

  it('opens Santa video modal when Santa card clicked', async () => {
    const wrapper = mount(MascotTheme)
    
    const santaCard = wrapper.findAll('.mascot-card')[2]
    await santaCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videoModals = wrapper.findAll('.video-modal')
    const santaModal = videoModals.find(modal => modal.text().includes('Swab The Giver'))
    expect(santaModal!.isVisible()).toBe(true)
  })

  it('closes hero video modal when clicking outside', async () => {
    const wrapper = mount(MascotTheme)
    
    // Open modal
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    // Click modal background
    const videoModals = wrapper.findAll('.video-modal')
    const heroModal = videoModals.find(modal => modal.text().includes('Swab The Savior'))
    await heroModal!.trigger('click')
    await wrapper.vm.$nextTick()
    
    expect(heroModal!.isVisible()).toBe(false)
  })

  it('closes video modal when close button clicked', async () => {
    const wrapper = mount(MascotTheme)
    
    // Open modal
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    // Click close button
    const closeButton = wrapper.find('.close-button')
    await closeButton.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videoModals = wrapper.findAll('.video-modal')
    const heroModal = videoModals.find(modal => modal.text().includes('Swab The Savior'))
    expect(heroModal!.isVisible()).toBe(false)
  })

  it('does not close modal when clicking video container', async () => {
    const wrapper = mount(MascotTheme)
    
    // Open modal
    const actionCard = wrapper.findAll('.mascot-card')[1]
    await actionCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    // Click video container (should not close due to @click.stop)
    const videoContainer = wrapper.find('.video-container')
    await videoContainer.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videoModals = wrapper.findAll('.video-modal')
    const actionModal = videoModals.find(modal => modal.text().includes('Swab The Leader'))
    expect(actionModal!.isVisible()).toBe(true)
  })

  it('renders video elements with correct sources', async () => {
    const wrapper = mount(MascotTheme)
    
    // Open each modal to check video sources
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const videos = wrapper.findAll('video')
    const sources = wrapper.findAll('source')
    
    expect(videos.length).toBeGreaterThan(0)
    expect(sources.some(s => s.attributes('src') === '/mascot/SwabTheSavior.mp4')).toBe(true)
  })

  it('sets video to autoplay', async () => {
    const wrapper = mount(MascotTheme)
    
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const video = wrapper.find('video')
    expect(video.attributes('autoplay')).toBeDefined()
  })

  it('enables video controls', async () => {
    const wrapper = mount(MascotTheme)
    
    const actionCard = wrapper.findAll('.mascot-card')[1]
    await actionCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    const video = wrapper.find('video')
    expect(video.attributes('controls')).toBeDefined()
  })

  it('renders Christmas theme colors section', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.theme-preview').exists()).toBe(true)
    expect(wrapper.text()).toContain('Christmas Theme Colors')
  })

  it('displays all four color swatches', () => {
    const wrapper = mount(MascotTheme)
    
    const swatches = wrapper.findAll('.color-swatch')
    expect(swatches.length).toBe(4)
    
    expect(wrapper.text()).toContain('Christmas Red')
    expect(wrapper.text()).toContain('Christmas Green')
    expect(wrapper.text()).toContain('Festive Gold')
    expect(wrapper.text()).toContain('Snow White')
  })

  it('renders button showcase section', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.button-showcase').exists()).toBe(true)
    expect(wrapper.text()).toContain('Holiday Buttons')
  })

  it('displays three button variants', () => {
    const wrapper = mount(MascotTheme)
    
    const buttons = wrapper.findAll('.button-showcase button')
    expect(buttons.length).toBe(3)
    
    expect(buttons[0]!.text()).toBe('Standard Button')
    expect(buttons[1]!.text()).toBe('Action Button')
    expect(buttons[2]!.text()).toBe('Disabled Button')
  })

  it('has disabled attribute on disabled button', () => {
    const wrapper = mount(MascotTheme)
    
    const buttons = wrapper.findAll('.button-showcase button')
    expect(buttons[2]!.attributes('disabled')).toBeDefined()
  })

  it('applies action-button class to action button', () => {
    const wrapper = mount(MascotTheme)
    
    const buttons = wrapper.findAll('.button-showcase button')
    expect(buttons[1]!.classes()).toContain('action-button')
  })

  it('applies correct CSS classes to color swatches', () => {
    const wrapper = mount(MascotTheme)
    
    const swatches = wrapper.findAll('.color-swatch')
    expect(swatches[0]!.classes()).toContain('red')
    expect(swatches[1]!.classes()).toContain('green')
    expect(swatches[2]!.classes()).toContain('gold')
    expect(swatches[3]!.classes()).toContain('snow')
  })

  it('applies cursor pointer to clickable cards', () => {
    const wrapper = mount(MascotTheme)
    
    const mascotCards = wrapper.findAll('.mascot-card')
    mascotCards.forEach(card => {
      expect(card.attributes('style')).toContain('cursor: pointer')
    })
  })

  it('applies staggered animation delays', () => {
    const wrapper = mount(MascotTheme)
    
    const mascotCards = wrapper.findAll('.mascot-card')
    expect(mascotCards[0]!.attributes('style')).toContain('animation-delay: 0.1s')
    expect(mascotCards[1]!.attributes('style')).toContain('animation-delay: 0.2s')
    expect(mascotCards[2]!.attributes('style')).toContain('animation-delay: 0.3s')
  })

  it('renders mascot showcase container', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.mascot-showcase').exists()).toBe(true)
  })

  it('renders mascot gallery', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.mascot-gallery').exists()).toBe(true)
  })

  it('initially hides all video modals', () => {
    const wrapper = mount(MascotTheme)
    
    const videoModals = wrapper.findAll('.video-modal')
    videoModals.forEach(modal => {
      expect(modal.isVisible()).toBe(false)
    })
  })

  it('displays correct video titles in modals', async () => {
    const wrapper = mount(MascotTheme)
    
    // Check hero modal title
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Swab The Savior')
    
    // Close and check action modal title
    const closeButton = wrapper.find('.close-button')
    await closeButton.trigger('click')
    
    const actionCard = wrapper.findAll('.mascot-card')[1]
    await actionCard!.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).toContain('Swab The Leader')
  })

  it('supports multiple modals without interference', async () => {
    const wrapper = mount(MascotTheme)
    
    // Open hero modal
    const rescueCard = wrapper.findAll('.mascot-card')[0]
    await rescueCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    let videoModals = wrapper.findAll('.video-modal')
    let heroModal = videoModals.find(modal => modal.text().includes('Swab The Savior'))
    let actionModal = videoModals.find(modal => modal.text().includes('Swab The Leader'))
    
    expect(heroModal!.isVisible()).toBe(true)
    expect(actionModal!.isVisible()).toBe(false)
    
    // Close hero, open action
    const closeButton = wrapper.find('.close-button')
    await closeButton.trigger('click')
    await wrapper.vm.$nextTick()
    
    const actionCard = wrapper.findAll('.mascot-card')[1]
    await actionCard!.trigger('click')
    await wrapper.vm.$nextTick()
    
    videoModals = wrapper.findAll('.video-modal')
    heroModal = videoModals.find(modal => modal.text().includes('Swab The Savior'))
    actionModal = videoModals.find(modal => modal.text().includes('Swab The Leader'))
    
    expect(heroModal!.isVisible()).toBe(false)
    expect(actionModal!.isVisible()).toBe(true)
  })

  it('displays badges on mascot cards', () => {
    const wrapper = mount(MascotTheme)
    
    const badges = wrapper.findAll('.badge')
    expect(badges.length).toBe(3)
  })

  it('applies animate-in class to sections', () => {
    const wrapper = mount(MascotTheme)
    
    expect(wrapper.find('.hero-section').classes()).toContain('animate-in')
    expect(wrapper.findAll('.mascot-card')[0]!.classes()).toContain('animate-in')
    expect(wrapper.find('.theme-preview').classes()).toContain('animate-in')
    expect(wrapper.find('.button-showcase').classes()).toContain('animate-in')
  })
})
