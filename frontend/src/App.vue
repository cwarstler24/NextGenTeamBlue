<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header>
      <div class="header-content">
        <div class="brand">
          <h1>Team Blue Asset Management</h1>
        </div>
        <nav>
          <RouterLink to="/">
            Home
          </RouterLink>
          <RouterLink to="/assets">
            Assets
          </RouterLink>
          <RouterLink to="/add-asset">
            Add Asset
          </RouterLink>
        </nav>
      </div>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: white;
  box-shadow: var(--shadow-md);
  padding: 1.5rem 2rem;
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.brand h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

nav {
  display: flex;
  gap: 0.5rem;
}

nav a {
  color: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

nav a:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

nav a.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  nav {
    width: 100%;
    flex-wrap: wrap;
  }

  .brand h1 {
    font-size: 1.25rem;
  }
}
</style>
