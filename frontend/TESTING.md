# Vue Component Testing Guide

This document explains the Vue.js component testing setup for the Team Blue Asset Management System frontend.

## Overview

The project uses:
- **Vitest** - Fast unit test framework powered by Vite
- **@vue/test-utils** - Official Vue.js testing utilities
- **jsdom** - Simulated browser environment for tests

## Test Structure

```
frontend/src/
├── __tests__/               # Global test utilities
│   ├── setup.ts            # Test environment setup
│   ├── testUtils.ts        # Helper functions and mock factories
│   └── App.spec.ts         # App component tests
├── views/
│   └── __tests__/          # View component tests
│       ├── HomeView.spec.ts
│       └── AssetListView.spec.ts
└── composables/
    └── __tests__/          # Composable tests
        ├── useAssetTypes.spec.ts
        ├── useAssetEmployees.spec.ts
        └── useAssetLocations.spec.ts
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm run test:watch
```

### Run tests with coverage report
```bash
npm run test:coverage
```

### Run specific test file
```bash
npx vitest src/views/__tests__/HomeView.spec.ts
```

## Writing Tests

### Basic Component Test Example

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/views/MyComponent.vue'

describe('MyComponent.vue', () => {
  it('renders correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.find('h1').text()).toBe('Expected Title')
  })
})
```

### Testing with Router

Use the `mountWithRouter` utility for components that use vue-router:

```typescript
import { mountWithRouter } from '@/__tests__/testUtils'

it('navigates on button click', async () => {
  const wrapper = mountWithRouter(MyComponent)
  
  await wrapper.find('.navigate-btn').trigger('click')
  
  expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/target-route')
})
```

### Using Mock Data Factories

Test utilities provide factory functions for creating mock data:

```typescript
import { createMockAsset, createMockEmployee } from '@/__tests__/testUtils'

it('displays asset details', () => {
  const asset = createMockAsset({ 
    id: 1, 
    resource_id: 'TEST-001' 
  })
  
  const wrapper = mount(AssetCard, {
    props: { asset }
  })
  
  expect(wrapper.text()).toContain('TEST-001')
})
```

## Test Utilities Reference

### Helper Functions

- `mountWithRouter(component, options)` - Mount component with mock router
- `createMockRouter(overrides)` - Create a mock Vue Router instance
- `createMockAsset(overrides)` - Generate mock asset data
- `createMockEmployee(overrides)` - Generate mock employee data
- `createMockAssetType(overrides)` - Generate mock asset type data
- `createMockLocation(overrides)` - Generate mock location data
- `flushPromises()` - Wait for all pending promises to resolve
- `waitFor(ms)` - Wait for specified milliseconds
- `clearAllMocks()` - Clear all mocks and storage

### Mocked APIs

The test environment automatically mocks:
- `localStorage` - Browser local storage
- `sessionStorage` - Browser session storage
- `window.matchMedia` - Media query matching

## Test Coverage

View coverage reports after running `npm run test:coverage`:
- Console output shows summary
- `coverage/index.html` contains detailed HTML report

### Coverage Excludes

The following are excluded from coverage:
- `node_modules/`
- Test files (`*.spec.ts`, `*.test.ts`)
- Test utilities (`src/__tests__/`)
- Configuration files (`vite.config.ts`, `eslint.config.js`)

## Best Practices

### 1. Test User Behavior, Not Implementation

❌ Bad:
```typescript
it('calls fetchData method', () => {
  wrapper.vm.fetchData()
  expect(wrapper.vm.data).toBeDefined()
})
```

✅ Good:
```typescript
it('displays data when component mounts', async () => {
  const wrapper = mount(MyComponent)
  await flushPromises()
  expect(wrapper.find('.data-display').exists()).toBe(true)
})
```

### 2. Use Descriptive Test Names

Test names should clearly describe what is being tested:

```typescript
it('displays error message when API request fails', async () => {
  // test implementation
})
```

### 3. Arrange-Act-Assert Pattern

Structure tests clearly:

```typescript
it('filters assets by employee ID', async () => {
  // Arrange - Setup test data
  const mockAssets = [
    createMockAsset({ employee_id: 1 }),
    createMockAsset({ employee_id: 2 }),
  ]
  
  // Act - Perform the action
  const wrapper = mountWithRouter(AssetListView)
  await wrapper.find('#employeeFilter').setValue('1')
  await wrapper.find('.search-btn').trigger('click')
  
  // Assert - Verify the result
  expect(wrapper.findAll('.asset-card')).toHaveLength(1)
})
```

### 4. Clean Up After Tests

```typescript
beforeEach(() => {
  clearAllMocks()
})

afterEach(() => {
  localStorage.clear()
})
```

### 5. Mock External Dependencies

Always mock axios, API calls, and composables:

```typescript
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

vi.mock('@/composables/useAssetTypes', () => ({
  useAssetTypes: () => ({
    getAssetTypeName: vi.fn((id) => `Type ${id}`),
    fetchAssetTypes: vi.fn(),
  }),
}))
```

## Troubleshooting

### Tests fail with "Cannot find module"

Make sure TypeScript paths are configured correctly in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Component doesn't update after async operation

Use `await flushPromises()` to wait for async operations:

```typescript
await wrapper.find('button').trigger('click')
await flushPromises()
expect(wrapper.text()).toContain('Updated')
```

### Mock not being applied

Ensure mocks are defined before importing the module:

```typescript
// ✅ Correct order
vi.mock('axios')
import MyComponent from '@/components/MyComponent.vue'

// ❌ Wrong order
import MyComponent from '@/components/MyComponent.vue'
vi.mock('axios') // Too late!
```

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils Documentation](https://test-utils.vuejs.org/)
- [Vue.js Testing Guide](https://vuejs.org/guide/scaling-up/testing.html)
