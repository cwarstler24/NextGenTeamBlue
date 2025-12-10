
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// IMPORTANT: mock axios and API_BASE import used inside the composable
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
  },
}))

// Mock the API_BASE constant so tests don't depend on the real config
vi.mock('@/config/api', () => ({
  API_BASE: 'https://api.test',
}))

// Import AFTER mocks so the composable uses the mocked modules
import { useAssetTypes } from '@/composables/useAssetTypes'

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock, writable: true })

describe('useAssetTypes', () => {
  const mockedAxiosGet = (axios as { get: ReturnType<typeof vi.fn> }).get

  beforeEach(() => {
    // Clean localStorage and reset mocks between tests
    localStorage.removeItem('bearerToken')
    vi.clearAllMocks()
    // Silence console noise from the composable (optional)
    vi.spyOn(console, 'log').mockImplementation(() => {})
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  /**
   * @function initial state is correct
   * @description Verifies that all reactive state values are initialized with expected default values.
   */
  it('initial state is correct', () => {
    const {
      assetTypes,
      assetTypeMap,
      isLoading,
      error,
    } = useAssetTypes()

    expect(assetTypes.value).toEqual([])
    expect(assetTypeMap.value).toEqual({})
    expect(isLoading.value).toBe(false)
    expect(error.value).toBeNull()
  })

  /**
   * @function returns error when no bearer token set and does not call API
   * @description Verifies that fetchAssetTypes returns an error when no bearer token is present in localStorage.
   */
  it('returns error when no bearer token set and does not call API', async () => {
    const { fetchAssetTypes, error, isLoading } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('No bearer token set')
    expect(isLoading.value).toBe(false)
    expect(mockedAxiosGet).not.toHaveBeenCalled()
  })

  /**
   * @function adds "Bearer " prefix when token does not start with bearer
   * @description Verifies that the Authorization header is properly prefixed with "Bearer " when the token lacks it.
   */
  it('adds "Bearer " prefix when token does not start with bearer', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockResolvedValueOnce({
      data: [
        { id: 1, asset_type_name: 'Laptop' },
        { id: 2, asset_type_name: 'Monitor' },
      ],
    })

    const { fetchAssetTypes } = useAssetTypes()
    await fetchAssetTypes()

    expect(mockedAxiosGet).toHaveBeenCalledTimes(1)
    const [url, options] = mockedAxiosGet.mock.calls[0]
    expect(url).toBe('https://api.test/resources/types/')
    expect(options).toMatchObject({
      headers: { Authorization: 'Bearer abc123' },
    })
  })

  /**
   * @function does NOT add prefix when token already starts with "bearer "
   * @description Verifies that tokens already containing "bearer " are not modified when passed to the API.
   */
  it('does NOT add prefix when token already starts with "bearer "', async () => {
    // Any case is accepted by your check; it uses toLowerCase for startsWith
    localStorage.setItem('bearerToken', 'bearer xyz')

    mockedAxiosGet.mockResolvedValueOnce({ data: [] })

    const { fetchAssetTypes } = useAssetTypes()
    await fetchAssetTypes()

    const [, options] = mockedAxiosGet.mock.calls[0]
    // Header uses the token verbatim, which will be 'bearer xyz'
    expect(options).toMatchObject({
      headers: { Authorization: 'bearer xyz' },
    })
  })

  /**
   * @function successful fetch populates assetTypes and assetTypeMap
   * @description Verifies that a successful API call correctly populates the reactive state and lookup map.
   */
  it('successful fetch populates assetTypes and assetTypeMap', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const payload = [
      { id: 10, asset_type_name: 'Desktop Computer' },
      { id: 20, asset_type_name: 'Printer' },
    ]

    mockedAxiosGet.mockResolvedValueOnce({ data: payload })

    const {
      fetchAssetTypes,
      assetTypes,
      assetTypeMap,
      isLoading,
      error,
      getAssetTypeName,
    } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBeNull()
    expect(isLoading.value).toBe(false)
    expect(assetTypes.value).toEqual(payload)
    expect(assetTypeMap.value).toEqual({
      10: 'Desktop Computer',
      20: 'Printer',
    })
    expect(getAssetTypeName(10)).toBe('Desktop Computer')
    expect(getAssetTypeName(999)).toBe('Type 999')
  })

  /**
   * @function sets meaningful error message on failed fetch (with detail)
   * @description Verifies that API errors with detail messages are properly captured and exposed.
   */
  it('sets meaningful error message on failed fetch (with detail)', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockRejectedValueOnce({
      response: { data: { detail: 'Boom' } },
    })

    const { fetchAssetTypes, error, isLoading } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('Boom')
    expect(isLoading.value).toBe(false)
  })

  /**
   * @function sets generic error message on failed fetch (no detail)
   * @description Verifies that a generic error message is displayed when the API error lacks detail information.
   */
  it('sets generic error message on failed fetch (no detail)', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockRejectedValueOnce(new Error('Network down'))

    const { fetchAssetTypes, error, isLoading } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('Failed to fetch asset types')
    expect(isLoading.value).toBe(false)
  })

  /**
   * @function isLoading toggles correctly during request
   * @description Verifies that the isLoading flag is properly set during the fetch lifecycle.
   */
  it('isLoading toggles correctly during request', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    // Create a controllable promise so we can assert mid-flight state
    let resolveFn: (v?: unknown) => void
    const pending = new Promise((resolve) => (resolveFn = resolve))
    mockedAxiosGet.mockImplementationOnce(() => pending as Promise<any>)

    const { fetchAssetTypes, isLoading } = useAssetTypes()

    const p = fetchAssetTypes()
    expect(isLoading.value).toBe(true) // immediately after call

    // Finish the request
    resolveFn!({ data: [] })
    await p

    expect(isLoading.value).toBe(false)
  })

  /**
   * @function getAssetTypeName returns default value for unknown type IDs
   * @description Verifies that getAssetTypeName returns a fallback value when the type ID is not in the map.
   */
  it('getAssetTypeName returns default value for unknown type IDs', async () => {
    const { getAssetTypeName } = useAssetTypes()

    // Before fetching, map is empty
    expect(getAssetTypeName(123)).toBe('Type 123')
    expect(getAssetTypeName(0)).toBe('Type 0')
    expect(getAssetTypeName(-1)).toBe('Type -1')
  })

  /**
   * @function handles empty response array
   * @description Verifies that an empty response from the API is handled correctly without errors.
   */
  it('handles empty response array', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockResolvedValueOnce({ data: [] })

    const {
      fetchAssetTypes,
      assetTypes,
      assetTypeMap,
      error,
    } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBeNull()
    expect(assetTypes.value).toEqual([])
    expect(assetTypeMap.value).toEqual({})
  })

  /**
   * @function handles response with duplicate IDs
   * @description Verifies that when multiple types have the same ID, the last one wins in the map.
   */
  it('handles response with duplicate IDs', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const payload = [
      { id: 5, asset_type_name: 'First Name' },
      { id: 5, asset_type_name: 'Second Name' },
      { id: 10, asset_type_name: 'Different Type' },
    ]

    mockedAxiosGet.mockResolvedValueOnce({ data: payload })

    const {
      fetchAssetTypes,
      assetTypeMap,
      getAssetTypeName,
    } = useAssetTypes()

    await fetchAssetTypes()

    // The second entry should overwrite the first
    expect(assetTypeMap.value[5]).toBe('Second Name')
    expect(getAssetTypeName(5)).toBe('Second Name')
    expect(getAssetTypeName(10)).toBe('Different Type')
  })

  /**
   * @function handles malformed response data
   * @description Verifies behavior when API returns objects without expected properties.
   */
  it('handles malformed response data', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const payload = [
      { id: 1, asset_type_name: 'Valid Type' },
      { id: 2 }, // Missing asset_type_name
      { asset_type_name: 'Missing ID' }, // Missing id
    ]

    mockedAxiosGet.mockResolvedValueOnce({ data: payload })

    const {
      fetchAssetTypes,
      assetTypes,
      assetTypeMap,
      getAssetTypeName,
    } = useAssetTypes()

    await fetchAssetTypes()

    expect(assetTypes.value).toEqual(payload)
    expect(assetTypeMap.value[1]).toBe('Valid Type')
    expect(assetTypeMap.value[2]).toBeUndefined()
    expect(getAssetTypeName(2)).toBe('Type 2')
  })

  /**
   * @function clears previous error on subsequent fetch
   * @description Verifies that error state is reset when a new fetch is initiated.
   */
  it('clears previous error on subsequent fetch', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const { fetchAssetTypes, error } = useAssetTypes()

    // First call fails
    mockedAxiosGet.mockRejectedValueOnce(new Error('First error'))
    await fetchAssetTypes()
    expect(error.value).toBe('Failed to fetch asset types')

    // Second call succeeds
    mockedAxiosGet.mockResolvedValueOnce({ data: [{ id: 1, asset_type_name: 'Type A' }] })
    await fetchAssetTypes()
    expect(error.value).toBeNull()
  })

  /**
   * @function handles network timeout errors
   * @description Verifies that network timeout errors are handled gracefully.
   */
  it('handles network timeout errors', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const timeoutError = {
      code: 'ECONNABORTED',
      message: 'timeout of 5000ms exceeded',
    }

    mockedAxiosGet.mockRejectedValueOnce(timeoutError)

    const { fetchAssetTypes, error } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('Failed to fetch asset types')
  })

  /**
   * @function handles 401 unauthorized errors
   * @description Verifies that 401 errors with specific detail messages are properly exposed.
   */
  it('handles 401 unauthorized errors', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockRejectedValueOnce({
      response: {
        status: 401,
        data: { detail: 'Invalid authentication credentials' },
      },
    })

    const { fetchAssetTypes, error } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('Invalid authentication credentials')
  })

  /**
   * @function handles 403 forbidden errors
   * @description Verifies that 403 errors are properly handled and exposed.
   */
  it('handles 403 forbidden errors', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockRejectedValueOnce({
      response: {
        status: 403,
        data: { detail: 'You do not have permission to access this resource' },
      },
    })

    const { fetchAssetTypes, error } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('You do not have permission to access this resource')
  })

  /**
   * @function handles 500 server errors
   * @description Verifies that 500 errors are handled gracefully with proper error messages.
   */
  it('handles 500 server errors', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    mockedAxiosGet.mockRejectedValueOnce({
      response: {
        status: 500,
        data: { detail: 'Internal server error' },
      },
    })

    const { fetchAssetTypes, error } = useAssetTypes()

    await fetchAssetTypes()

    expect(error.value).toBe('Internal server error')
  })

  /**
   * @function multiple successive fetches update state correctly
   * @description Verifies that calling fetchAssetTypes multiple times properly updates state each time.
   */
  it('multiple successive fetches update state correctly', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const { fetchAssetTypes, assetTypes, assetTypeMap } = useAssetTypes()

    // First fetch
    mockedAxiosGet.mockResolvedValueOnce({
      data: [{ id: 1, asset_type_name: 'Type A' }],
    })
    await fetchAssetTypes()
    expect(assetTypes.value).toEqual([{ id: 1, asset_type_name: 'Type A' }])
    expect(assetTypeMap.value).toEqual({ 1: 'Type A' })

    // Second fetch with different data
    mockedAxiosGet.mockResolvedValueOnce({
      data: [
        { id: 2, asset_type_name: 'Type B' },
        { id: 3, asset_type_name: 'Type C' },
      ],
    })
    await fetchAssetTypes()
    expect(assetTypes.value).toEqual([
      { id: 2, asset_type_name: 'Type B' },
      { id: 3, asset_type_name: 'Type C' },
    ])
    expect(assetTypeMap.value).toEqual({ 2: 'Type B', 3: 'Type C' })
  })

  /**
   * @function Bearer prefix is case-insensitive
   * @description Verifies that "Bearer", "bearer", and mixed case variants are all recognized.
   */
  it('Bearer prefix is case-insensitive', async () => {
    mockedAxiosGet.mockResolvedValue({ data: [] })

    // Test with different cases
    const testCases = ['Bearer token123', 'bearer token456', 'BEARER token789', 'BeArEr tokenABC']

    for (const token of testCases) {
      localStorage.setItem('bearerToken', token)
      const { fetchAssetTypes } = useAssetTypes()
      await fetchAssetTypes()

      const [, options] = mockedAxiosGet.mock.calls[mockedAxiosGet.mock.calls.length - 1]
      expect(options.headers.Authorization).toBe(token)
    }
  })
})
