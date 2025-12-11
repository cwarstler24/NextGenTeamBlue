/**
 * @file api.spec.ts
 * @description Tests for API configuration utility
 * 
 * Test Coverage:
 * - Development environment detection (localhost with dev port)
 * - Docker/Production environment detection (localhost without dev port)
 * - nginx proxied environment (non-localhost)
 * - Port edge cases (80, 443, custom ports)
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

describe('API Configuration', () => {
  const originalLocation = window.location

  beforeEach(() => {
    // Delete the module from cache to force re-evaluation
    vi.resetModules()
  })

  afterEach(() => {
    // Restore original location
    Object.defineProperty(window, 'location', {
      writable: true,
      value: originalLocation
    })
  })

  it('returns direct backend URL for localhost with dev port', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'localhost',
        port: '5173',
        protocol: 'http:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('http://127.0.0.1:8000')
  })

  it('returns direct backend URL for 127.0.0.1 with dev port', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: '127.0.0.1',
        port: '3000',
        protocol: 'http:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('http://127.0.0.1:8000')
  })

  it('returns empty string for localhost without port', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'localhost',
        port: '',
        protocol: 'http:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('')
  })

  it('returns empty string for localhost with port 80', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'localhost',
        port: '80',
        protocol: 'http:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('')
  })

  it('returns empty string for localhost with port 443', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'localhost',
        port: '443',
        protocol: 'https:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('')
  })

  it('returns empty string for production domain', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'teamblue.example.com',
        port: '',
        protocol: 'https:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('')
  })

  it('returns empty string for Docker environment (nginx proxied)', async () => {
    Object.defineProperty(window, 'location', {
      writable: true,
      value: {
        hostname: 'app',
        port: '80',
        protocol: 'http:',
      }
    })

    const { API_BASE } = await import('../api')
    expect(API_BASE).toBe('')
  })
})
