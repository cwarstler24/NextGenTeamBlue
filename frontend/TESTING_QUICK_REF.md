# Vue Component Testing - Quick Reference

## Running Tests

```bash
# Run all tests once
npm test

# Run tests in watch mode (re-runs on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run a specific test file
npx vitest src/views/__tests__/HomeView.spec.ts

# Run tests matching a pattern
npx vitest --grep="token"
```

## Writing a Basic Test

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/views/MyComponent.vue'

describe('MyComponent.vue', () => {
  beforeEach(() => {
    // Setup before each test
    localStorage.clear()
  })

  it('renders correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.find('h1').text()).toBe('Expected Title')
  })
})
```

## Common Test Patterns

### Testing with Router
```typescript
import { mountWithRouter } from '@/__tests__/testUtils'

it('navigates on click', async () => {
  const mockRouter = { push: vi.fn() }
  const wrapper = mountWithRouter(MyComponent, {
    global: { mocks: { $router: mockRouter } }
  })
  
  await wrapper.find('.nav-button').trigger('click')
  expect(mockRouter.push).toHaveBeenCalledWith('/target')
})
```

### Testing Async Operations
```typescript
import { flushPromises } from '@/__tests__/testUtils'

it('loads data on mount', async () => {
  const wrapper = mount(MyComponent)
  await flushPromises()
  expect(wrapper.find('.data').text()).toContain('Loaded')
})
```

### Testing Form Input
```typescript
it('updates on input', async () => {
  const wrapper = mount(MyComponent)
  const input = wrapper.find('input')
  
  await input.setValue('new value')
  expect(wrapper.vm.inputData).toBe('new value')
})
```

### Testing Button Clicks
```typescript
it('calls method on click', async () => {
  const wrapper = mount(MyComponent)
  const button = wrapper.find('button')
  
  await button.trigger('click')
  expect(wrapper.find('.result').text()).toBe('Clicked')
})
```

### Mocking API Calls
```typescript
import axios from 'axios'
vi.mock('axios')

it('fetches data', async () => {
  axios.get.mockResolvedValue({ data: { name: 'Test' } })
  
  const wrapper = mount(MyComponent)
  await flushPromises()
  expect(wrapper.text()).toContain('Test')
})
```

### Using Mock Data
```typescript
import { createMockAsset } from '@/__tests__/testUtils'

it('displays asset', () => {
  const asset = createMockAsset({ resource_id: 'TEST-001' })
  const wrapper = mount(AssetCard, { props: { asset } })
  expect(wrapper.text()).toContain('TEST-001')
})
```

## Useful Assertions

```typescript
// Element existence
expect(wrapper.find('.my-class').exists()).toBe(true)

// Text content
expect(wrapper.text()).toContain('Expected Text')
expect(wrapper.find('h1').text()).toBe('Title')

// Classes
expect(wrapper.classes()).toContain('active')
expect(wrapper.find('div').classes('highlighted')).toBe(true)

// Attributes
expect(wrapper.attributes('href')).toBe('/path')
expect(wrapper.find('img').attributes('alt')).toBe('Description')

// Component state
expect(wrapper.vm.myData).toBe('value')

// Array/object matching
expect(wrapper.findAll('.item')).toHaveLength(3)
expect(mockFn).toHaveBeenCalledWith({ id: 1 })

// Mock function calls
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledTimes(2)
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
```

## Test Utilities Reference

### Mounting
- `mount(Component, options)` - Basic mount
- `mountWithRouter(Component, options)` - Mount with router mock

### Data Factories
- `createMockAsset(overrides)` - Create test asset
- `createMockEmployee(overrides)` - Create test employee
- `createMockAssetType(overrides)` - Create test asset type
- `createMockLocation(overrides)` - Create test location

### Helpers
- `flushPromises()` - Wait for promises to resolve
- `clearAllMocks()` - Clear all mocks and storage
- `waitFor(ms)` - Wait specified milliseconds

### Router Mock
- `createMockRouter(overrides)` - Create mock router

## Debugging Tests

### View Test Output
```bash
# Run with verbose output
npx vitest --reporter=verbose

# Run single test with debug output
npx vitest src/path/to/test.spec.ts --reporter=verbose
```

### Debug in Test
```typescript
it('debugs component', () => {
  const wrapper = mount(MyComponent)
  
  // Print HTML
  console.log(wrapper.html())
  
  // Print text
  console.log(wrapper.text())
  
  // Check component data
  console.log(wrapper.vm.$data)
})
```

### Common Issues

**"Cannot find module"**
→ Check import paths and `@` alias in `tsconfig.json`

**"Element not found"**
→ Use `await wrapper.vm.$nextTick()` or `flushPromises()`

**"Mock not working"**
→ Ensure `vi.mock()` is called before importing the module

**"Router injection not found"**
→ Use `mountWithRouter()` instead of `mount()`

## Coverage

```bash
# Generate coverage report
npm run test:coverage

# View HTML report
# Open coverage/index.html in browser

# Coverage thresholds (can be configured in vite.config.ts)
# - statements: 80%
# - branches: 80%
# - functions: 80%
# - lines: 80%
```

## Best Practices

✅ **DO:**
- Test user behavior, not implementation
- Use descriptive test names
- Clean up after each test
- Mock external dependencies
- Wait for async operations

❌ **DON'T:**
- Access private component methods
- Test implementation details
- Share state between tests
- Use real API calls
- Forget to await async operations

## Resources

- [Vitest Docs](https://vitest.dev/)
- [Vue Test Utils Docs](https://test-utils.vuejs.org/)
- [Vue Testing Guide](https://vuejs.org/guide/scaling-up/testing.html)
- Full Guide: `TESTING.md`
- Setup Summary: `COMPONENT_TESTING_SETUP.md`
