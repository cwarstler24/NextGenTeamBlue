
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// IMPORTANT: mock axios and API_BASE import used inside the composable
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
  },
}))

// Mock the API_BASE constant so tests don’t depend on your real config
vi.mock('@/config/api', () => ({
  API_BASE: 'https://api.test',
}))

// Import AFTER mocks so the composable uses the mocked modules
import { useAssetEmployees } from '@/composables/useAssetEmployees'

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

describe('useAssetEmployees', () => {
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
      assetEmployees,
      assetEmployeeMap,
      isLoading,
      error,
    } = useAssetEmployees()

    expect(assetEmployees.value).toEqual([])
    expect(assetEmployeeMap.value).toEqual({})
    expect(isLoading.value).toBe(false)
    expect(error.value).toBeNull()
  })



  /**
   * @function returns error when no bearer token set and does not call API
   * @description Verifies that fetchAssetEmployees returns an error when no bearer token is present in localStorage.
   */
  it('returns error when no bearer token set and does not call API', async () => {
    const { fetchAssetEmployees, error, isLoading } = useAssetEmployees()

    await fetchAssetEmployees()

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
        { id: 1, asset_employee_name: 'Alice' },
        { id: 2, asset_employee_name: 'Bob' },
      ],
    })

    const { fetchAssetEmployees } = useAssetEmployees()
    await fetchAssetEmployees()

    expect(mockedAxiosGet).toHaveBeenCalledTimes(1)
    const [url, options] = mockedAxiosGet.mock.calls[0]
    expect(url).toBe('https://api.test//') // note the double slash in your composable
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

    const { fetchAssetEmployees } = useAssetEmployees()
    await fetchAssetEmployees()

    const [, options] = mockedAxiosGet.mock.calls[0]
    // Header uses the token verbatim, which will be 'bearer xyz'
    expect(options).toMatchObject({
      headers: { Authorization: 'bearer xyz' },
    })
  })



  /**
   * @function successful fetch populates assetEmployees and assetEmployeeMap
   * @description Verifies that a successful API call correctly populates the reactive state and lookup map.
   */
  it('successful fetch populates assetEmployees and assetEmployeeMap', async () => {
    localStorage.setItem('bearerToken', 'abc123')

    const payload = [
      { id: 10, asset_employee_name: 'Jane Doe' },
      { id: 20, asset_employee_name: 'John Smith' },
    ]

    mockedAxiosGet.mockResolvedValueOnce({ data: payload })

    const {
      fetchAssetEmployees,
      assetEmployees,
      assetEmployeeMap,
      isLoading,
      error,
      getAssetEmployeeName,
    } = useAssetEmployees()

    await fetchAssetEmployees()

    expect(error.value).toBeNull()
    expect(isLoading.value).toBe(false)
    expect(assetEmployees.value).toEqual(payload)
    expect(assetEmployeeMap.value).toEqual({
      10: 'Jane Doe',
      20: 'John Smith',
    })
    expect(getAssetEmployeeName(10)).toBe('Jane Doe')
    expect(getAssetEmployeeName(999)).toBe('Employee 999')
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

    const { fetchAssetEmployees, error, isLoading } = useAssetEmployees()

    await fetchAssetEmployees()

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

    const { fetchAssetEmployees, error, isLoading } = useAssetEmployees()

    await fetchAssetEmployees()

    expect(error.value).toBe('Failed to fetch asset employees')
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

    const { fetchAssetEmployees, isLoading } = useAssetEmployees()

    const p = fetchAssetEmployees()
    expect(isLoading.value).toBe(true) // immediately after call

    // Finish the request
    resolveFn!({ data: [] })
    await p

    expect(isLoading.value).toBe(false)
  })
})