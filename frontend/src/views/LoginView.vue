<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { encryptPassword } from '../router/encryption.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const apiUrl = ref('http://127.0.0.1:8000/api/auth/login') // Backend proxy endpoint
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function handleLogin() {
  if (!username.value || !password.value) {
    errorMessage.value = 'Please enter both username and password'
    return
  }

  if (!apiUrl.value) {
    errorMessage.value = 'Please enter the API URL'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    // Encrypt the password before sending
    const encrypted = encryptPassword(username.value, password.value)

    const response = await fetch(apiUrl.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: encrypted.username,
        password: encrypted.password,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Login failed' }))
      throw new Error(errorData.message || `Login failed with status ${response.status}`)
    }

    const data = await response.json()
    
    // Extract the token from the response
    // Adjust these field names based on your API's response structure
    let token = data.token || data.access_token || data.bearerToken || data.accessToken
    
    if (!token) {
      throw new Error('No token received from server')
    }

    // Ensure the token has the Bearer prefix
    const prefixed = token.toLowerCase().startsWith('bearer ') ? token : `Bearer ${token}`
    
    // Save token and username to localStorage
    localStorage.setItem('bearerToken', prefixed)
    localStorage.setItem('username', username.value)
    
    successMessage.value = 'Login successful! Redirecting...'
    
    // Redirect to home page after a short delay
    setTimeout(() => {
      router.push('/')
    }, 1000)
    
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'An error occurred during login'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>Login</h1>
          <p>Enter your credentials to access the Asset Management System</p>
        </div>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="api-url">API URL</label>
            <input 
              id="api-url"
              v-model="apiUrl" 
              type="text" 
              placeholder="http://127.0.0.1:8000/api/auth/login"
              class="form-input"
              :disabled="isLoading"
            >
            <small class="help-text">The endpoint to send login credentials to</small>
          </div>

          <div class="form-group">
            <label for="username">Username</label>
            <input 
              id="username"
              v-model="username" 
              type="text" 
              placeholder="Enter your username"
              class="form-input"
              :disabled="isLoading"
              autocomplete="username"
            >
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input 
              id="password"
              v-model="password" 
              type="password" 
              placeholder="Enter your password"
              class="form-input"
              :disabled="isLoading"
              autocomplete="current-password"
            >
          </div>

          <div v-if="errorMessage" class="alert alert-error">
            <svg
              xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" 
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="alert alert-success">
            <svg
              xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" 
              fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
            {{ successMessage }}
          </div>

          <button type="submit" class="btn-primary btn-full" :disabled="isLoading">
            <span v-if="!isLoading">Login</span>
            <span v-else class="loading">
              <span class="spinner" />
              Logging in...
            </span>
          </button>
        </form>

        <div class="login-footer">
          <p>
            <small>Token will be stored securely in your browser's localStorage</small>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.login-container {
  width: 100%;
  max-width: 480px;
}

.login-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.login-header {
  padding: 2rem 2rem 1.5rem;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
  text-align: center;
}

.login-header h1 {
  font-size: 1.75rem;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.login-header p {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.875rem;
}

.login-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-of-type {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-heading);
  font-weight: 500;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  font-size: 0.9375rem;
  transition: all 0.2s ease;
  background: var(--color-background);
  color: var(--color-text);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.help-text {
  display: block;
  margin-top: 0.375rem;
  color: var(--color-text-muted);
  font-size: 0.8125rem;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  border-radius: var(--border-radius-sm);
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

.alert svg {
  flex-shrink: 0;
}

.alert-error {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

.alert-success {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
}

.btn-full {
  width: 100%;
  justify-content: center;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.login-footer {
  padding: 1.5rem 2rem;
  background: var(--color-background-soft);
  border-top: 1px solid var(--color-border);
  text-align: center;
}

.login-footer p {
  margin: 0;
  color: var(--color-text-muted);
}

.login-footer small {
  font-size: 0.8125rem;
}

@media (max-width: 640px) {
  .login-view {
    padding: 1rem;
  }

  .login-form {
    padding: 1.5rem;
  }

  .login-header {
    padding: 1.5rem;
  }

  .login-header h1 {
    font-size: 1.5rem;
  }
}
</style>
