<script setup lang="ts">
import { ref, onMounted } from 'vue'

const token = ref('')

onMounted(() => {
  const saved = localStorage.getItem('bearerToken')
  if (saved) token.value = saved
})

function saveToken() {
  const raw = token.value.trim()
  const prefixed = raw.toLowerCase().startsWith('bearer ') ? raw : `Bearer ${raw}`
  localStorage.setItem('bearerToken', prefixed)
}
</script>

<template>
  <div class="home-view">
    <div class="hero">
      <h1>Welcome to Asset Management System</h1>
      <p>Manage your organization's assets efficiently and securely</p>
    </div>

    <section class="token-section">
      <div class="card">
        <div class="card-header">
          <h2>API Access Token</h2>
          <p>Enter a bearer token to enable calling protected endpoints.</p>
        </div>
        <div class="card-body">
          <div class="input-group">
            <input 
              v-model="token" 
              type="text" 
              placeholder="Bearer eyJ..." 
              class="token-input"
            />
            <button @click="saveToken" class="btn-primary">Save Token</button>
          </div>
          <small class="help-text">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            Token will be saved in browser localStorage as <code>bearerToken</code>.
          </small>
        </div>
      </div>
    </section>

    <section class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-cards">
        <RouterLink to="/assets" class="action-card">
          <h3>View Assets</h3>
          <p>Browse all assets in the system</p>
        </RouterLink>
        <RouterLink to="/add-asset" class="action-card">
          <h3>Add Asset</h3>
          <p>Register a new asset</p>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 900px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
}

.hero h1 {
  font-size: 2.5rem;
  color: var(--color-heading);
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.125rem;
  color: var(--color-text-muted);
}

.token-section {
  margin-bottom: 3rem;
}

.card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
}

.card-header h2 {
  font-size: 1.25rem;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
}

.card-header p {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.875rem;
}

.card-body {
  padding: 1.5rem;
}

.input-group {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.token-input {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.btn-primary {
  white-space: nowrap;
  min-width: 120px;
}

.help-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-muted);
  font-size: 0.8125rem;
}

.help-text svg {
  flex-shrink: 0;
}

.help-text code {
  background: var(--color-background-mute);
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
  font-size: 0.75rem;
  color: var(--color-primary);
}

.quick-actions {
  margin-top: 3rem;
}

.quick-actions h2 {
  font-size: 1.5rem;
  color: var(--color-heading);
  margin-bottom: 1.5rem;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: var(--color-background);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  text-align: center;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.action-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.action-card .icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  font-size: 1.125rem;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
}

.action-card p {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.875rem;
  }

  .input-group {
    flex-direction: column;
  }

  .btn-primary {
    width: 100%;
  }
}
</style>
