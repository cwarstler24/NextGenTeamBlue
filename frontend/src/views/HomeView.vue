<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TheWelcome from '../components/TheWelcome.vue'

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
  <main>
    <section class="token-gate">
      <h2>API Access Token</h2>
      <p>Enter a bearer token to enable calling protected endpoints.</p>
      <div class="row">
        <input v-model="token" type="text" placeholder="Bearer eyJ..." />
        <button @click="saveToken">Save</button>
      </div>
      <small>Saved in browser localStorage as <code>bearerToken</code>.</small>
    </section>

    <TheWelcome />
  </main>
</template>

<style scoped>
.token-gate {
  border: 1px solid var(--color-border);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.row { display: flex; gap: 0.5rem; }
input { flex: 1; padding: 0.5rem; }
button { padding: 0.5rem 1rem; }
</style>
