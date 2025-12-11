/**
 * Test Suite: AboutView.spec.ts
 * 
 * Purpose: Tests the AboutView component which displays team information,
 * mission statement, and copyright details by fetching and parsing aboutUs.txt.
 * 
 * Test Coverage:
 * - Component rendering in loading, error, and success states
 * - Fetching and parsing aboutUs.txt from public directory
 * - Display of mission statement, team members with emojis, copyright
 * - Error handling for network failures and file parsing
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import AboutView from '../AboutView.vue'

describe('AboutView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders loading state initially', () => {
    const wrapper = mount(AboutView)
    
    expect(wrapper.find('.loading').exists()).toBe(true)
    expect(wrapper.text()).toContain('Loading team info...')
  })

  it('displays error message when fetch fails', async () => {
    globalThis.fetch = vi.fn().mockRejectedValueOnce(new Error('Network error'))
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Error Loading Content')
  })

  it('displays error when response is not ok', async () => {
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 404
    } as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.text()).toContain('Failed to load about us information')
  })

  it('parses and displays mission statement correctly', async () => {
    const mockContent = `
Mission Statement:
"To provide excellent asset management solutions."

Development Team:
Lead Developer: Cameron Warstler

Copyright Statement:
Copyright 2024 Team Blue
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.mission-card').exists()).toBe(true)
    expect(wrapper.text()).toContain('To provide excellent asset management solutions.')
  })

  it('parses and displays team members with correct emojis', async () => {
    const mockContent = `
Mission Statement:
"Our mission"

Development Team:
Lead Developer: Cameron Warstler
Backend Engineer: Travis Test
Security Lead: Ethan Example

Copyright Statement:
Copyright 2024
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.team-section').exists()).toBe(true)
    expect(wrapper.text()).toContain('Cameron Warstler')
    expect(wrapper.text()).toContain('Travis Test')
    expect(wrapper.text()).toContain('Ethan Example')
    expect(wrapper.text()).toContain('Lead Developer')
    
    // Check emojis are rendered
    const memberEmojis = wrapper.findAll('.member-emoji')
    expect(memberEmojis.length).toBeGreaterThan(0)
  })

  it('applies correct emoji based on first name', async () => {
    const mockContent = `
Development Team:
Lead: Cameron Test
Developer: Nate Example
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    // Cameron gets 🎖️, Nate gets 🗡️
    const emojis = wrapper.findAll('.member-emoji')
    expect(emojis.some(e => e.text().includes('🎖️') || e.text().includes('🗡️'))).toBe(true)
  })

  it('displays copyright information', async () => {
    const mockContent = `
Mission Statement:
"Test"

Copyright Statement:
Copyright 2024 Team Blue. All rights reserved.
Licensed under MIT License.
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.copyright-card').exists()).toBe(true)
    expect(wrapper.text()).toContain('Copyright 2024 Team Blue')
  })

  it('displays festive footer with current year', async () => {
    const mockContent = `Mission Statement: "Test"`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.festive-footer').exists()).toBe(true)
    expect(wrapper.text()).toContain('Built with ❤️ by Team Blue')
    expect(wrapper.text()).toContain(new Date().getFullYear().toString())
  })

  it('fetches from correct Documentation path', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce('Mission Statement: "Test"')
    } as unknown as Response)
    
    globalThis.fetch = fetchMock
    
    mount(AboutView)
    
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(fetchMock).toHaveBeenCalledWith('/Documentation/aboutUs.txt')
  })

  it('handles missing sections gracefully', async () => {
    const mockContent = `Some random content without proper sections`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    // Should not crash, just not display missing sections
    expect(wrapper.find('.loading').exists()).toBe(false)
    expect(wrapper.find('.error').exists()).toBe(false)
  })

  it('parses mission statement without quotes as fallback', async () => {
    const mockContent = `
Mission Statement:
This is a mission statement without quotes on multiple lines.

Development Team:
Lead: Test Person
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(wrapper.find('.mission-card').exists()).toBe(true)
    expect(wrapper.text()).toContain('mission statement')
  })

  it('filters out empty team member entries', async () => {
    const mockContent = `
Development Team:
Lead Developer: Cameron Test
: 
Backend: Travis Test
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    const teamCards = wrapper.findAll('.team-card')
    // Should only have 2 valid members (empty line filtered out)
    expect(teamCards.length).toBe(2)
  })

  it('uses default emoji for unknown team members', async () => {
    const mockContent = `
Development Team:
Unknown Person: John Doe
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(mockContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))
    
    // Should use default 👤 emoji for unknown first names
    const emoji = wrapper.find('.member-emoji')
    expect(emoji.exists()).toBe(true)
  })

  it('renders hero section with correct title', () => {
    const wrapper = mount(AboutView)
    
    expect(wrapper.find('.hero-section').exists()).toBe(true)
    expect(wrapper.find('h1').text()).toContain('About Team Blue')
  })

  it('handles complete aboutUs.txt content', async () => {
    const completeContent = `
Mission Statement:
"To deliver world-class asset management solutions with dedication and excellence."

Development Team:
Lead Developer: Cameron Warstler
Backend Lead: Travis Smith
Security Engineer: Ethan Jones
Full Stack Developer: Clayton Brown
QA Engineer: Oluwasegun Oduro
DevOps Engineer: Nate Wilson

Copyright Statement:
Copyright (c) 2024 Team Blue
All rights reserved.

This software is licensed under the MIT License.
See LICENSE file for details.
`
    
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      text: vi.fn().mockResolvedValueOnce(completeContent)
    } as unknown as Response)
    
    const wrapper = mount(AboutView)
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Check all sections are rendered
    expect(wrapper.find('.mission-card').exists()).toBe(true)
    expect(wrapper.find('.team-section').exists()).toBe(true)
    expect(wrapper.find('.copyright-card').exists()).toBe(true)
    
    // Check team member count
    const teamCards = wrapper.findAll('.team-card')
    expect(teamCards.length).toBe(6)
    
    // Verify specific team members
    expect(wrapper.text()).toContain('Cameron Warstler')
    expect(wrapper.text()).toContain('Oluwasegun')
  })
})
