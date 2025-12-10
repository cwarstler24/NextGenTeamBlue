<template>
  <div class="employee-list-view">
    <div class="page-header">
      <div>
        <h1>Employee Directory</h1>
        <p class="subtitle">Browse all employees in the system</p>
      </div>
      <div class="search-container">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Search by name..."
          class="search-input"
          @input="handleSearch"
        />
      </div>
    </div>

    <div v-if="errorMsg" class="error">
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading employees...</p>
    </div>

    <div v-else-if="employees.length === 0 && !errorMsg" class="empty-state">
      <h2>No Employees Found</h2>
      <p v-if="searchQuery">Try adjusting your search query.</p>
      <p v-else>No employees are currently in the system.</p>
    </div>

    <div v-else class="employee-table-container">
      <table class="employee-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Full Name</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="employee in employees" 
            :key="employee.employee_id"
            class="employee-row"
          >
            <td class="employee-id">{{ employee.employee_id }}</td>
            <td>{{ employee.first_name }}</td>
            <td>{{ employee.last_name }}</td>
            <td class="full-name">{{ employee.first_name }} {{ employee.last_name }}</td>
          </tr>
        </tbody>
      </table>
      
      <div class="table-footer">
        <p class="result-count">
          Showing {{ employees.length }} employee{{ employees.length !== 1 ? 's' : '' }}
          <span v-if="searchQuery"> matching "{{ searchQuery }}"</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

interface Employee {
  employee_id: number
  first_name: string
  last_name: string
}

const employees = ref<Employee[]>([])
const searchQuery = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const fetchEmployees = async () => {
  let token = localStorage.getItem('bearerToken')
  if (!token) {
    errorMsg.value = 'No bearer token set. Go to Home and save one first.'
    employees.value = []
    return
  }
  if (!token.toLowerCase().startsWith('bearer ')) {
    token = `Bearer ${token}`
  }

  isLoading.value = true
  errorMsg.value = ''

  try {
    const params: { limit: number; q?: string } = { limit: 1000 }
    if (searchQuery.value.trim()) {
      params.q = searchQuery.value.trim()
    }

    const response = await axios.get(`${API_BASE}/resources/employees/`, {
      headers: { Authorization: token },
      params
    })
    employees.value = response.data
  } catch (error: any) {
    console.error('Error fetching employees:', error)
    errorMsg.value = error?.response?.data?.detail || 'Failed to fetch employees'
    employees.value = []
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  // Debounce search to avoid too many API calls
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = setTimeout(() => {
    fetchEmployees()
  }, 300)
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.employee-list-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #c41e3a;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.3);
}

.subtitle {
  color: #165b33;
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.search-container {
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-sm);
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem;
  border-radius: var(--border-radius-sm);
  margin-bottom: 1.5rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #165b33;
  font-size: 0.9375rem;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
}

.empty-state h2 {
  font-size: 1.5rem;
  color: #c41e3a;
  margin: 0 0 0.75rem 0;
}

.empty-state p {
  color: #4b5563;
  margin: 0;
  font-weight: 500;
}

.employee-table-container {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.employee-table {
  width: 100%;
  border-collapse: collapse;
}

.employee-table thead {
  background: var(--color-background-soft);
  border-bottom: 2px solid var(--color-border);
}

.employee-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.employee-table tbody tr {
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.15s ease;
}

.employee-table tbody tr:last-child {
  border-bottom: none;
}

.employee-table tbody tr:hover {
  background: var(--color-background-soft);
}

.employee-table td {
  padding: 1rem;
  color: #1f2937;
  font-weight: 500;
}

.employee-id {
  font-family: 'Courier New', monospace;
  color: #c41e3a;
  font-weight: 700;
}

.full-name {
  font-weight: 600;
  color: #165b33;
}

.table-footer {
  padding: 1rem;
  background: var(--color-background-soft);
  border-top: 1px solid var(--color-border);
}

.result-count {
  margin: 0;
  color: #4b5563;
  font-size: 0.875rem;
  font-weight: 600;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    min-width: auto;
  }

  .employee-table {
    font-size: 0.875rem;
  }

  .employee-table th,
  .employee-table td {
    padding: 0.75rem 0.5rem;
  }

  .employee-table th:nth-child(4),
  .employee-table td:nth-child(4) {
    display: none;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.5rem;
  }

  .employee-table th:nth-child(2),
  .employee-table td:nth-child(2) {
    display: none;
  }
}
</style>
