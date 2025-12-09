<template>
  <div class="asset-list-view">
    <div class="page-header">
      <div>
        <h1>Asset Inventory</h1>
        <p class="subtitle">
          Browse and manage all system assets
        </p>
      </div>
      <button class="btn-add" @click="goToAddAsset">
        Add New Asset
      </button>
    </div>

    <div v-if="errorMsg" class="error">
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <div class="filter-section">
      <div class="filter-controls">
        <div class="filter-group">
          <label for="employeeIdFilter">Employee ID:</label>
          <input 
            id="employeeIdFilter"
            v-model.trim="filterEmployeeId" 
            type="text" 
            placeholder="Enter employee ID"
            class="filter-input"
            @keyup.enter="applyFilters"
          >
        </div>
        <div class="filter-group">
          <label for="typeIdFilter">Type ID:</label>
          <input 
            id="typeIdFilter"
            v-model.trim="filterTypeId" 
            type="text" 
            placeholder="Enter type ID"
            class="filter-input"
            @keyup.enter="applyFilters"
          >
        </div>
        <div class="filter-buttons">
          <button class="btn-filter" @click="applyFilters">
            Search
          </button>
          <button class="btn-clear" @click="clearFilters">
            Clear
          </button>
        </div>
      </div>
      <div v-if="activeFilters" class="active-filters">
        <span class="filter-tag">
          Filtered Results
          <span class="result-count">({{ filteredAssets.length }})</span>
        </span>
      </div>
    </div>

    <div v-if="displayedAssets.length === 0 && !errorMsg" class="empty-state">
      <h2>No Assets Found</h2>
      <p>Get started by adding your first asset to the system.</p>
      <button class="btn-primary" @click="goToAddAsset">
        Add First Asset
      </button>
    </div>

    <div v-else class="asset-grid">
      <div 
        v-for="asset in displayedAssets" 
        :key="asset.id" 
        class="asset-card"
        @click="viewAsset(asset)"
      >
        <div class="asset-header">
          <h3>{{ asset.resource_id || `Asset #${asset.id}` }}</h3>
          <span 
            class="badge" 
            :class="asset.is_decommissioned ? 'badge-danger' : 'badge-success'"
          >
            {{ asset.is_decommissioned ? 'Decommissioned' : 'Active' }}
          </span>
        </div>
        <div class="asset-body">
          <div v-if="asset.notes" class="asset-notes">
            {{ asset.notes }}
          </div>
          <div class="asset-meta">
            <div class="meta-item">
              <span class="meta-label">Type:</span>
              <span class="meta-value">{{ getAssetTypeName(asset.type_id) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Added:</span>
              <span class="meta-value">{{ formatDate(asset.date_added) }}</span>
            </div>
          </div>
        </div>
        <div class="asset-footer">
          <span class="view-link">View Details →</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAssetTypes } from '../composables/useAssetTypes';
import { useAssetEmployees } from '../composables/useAssetEmployees';
import { useAssetLocations } from '../composables/useAssetLocations';
import { API_BASE } from '../config/api';

export default {
  setup() {
    const assets = ref([]);
    const filteredAssets = ref([]);
    const router = useRouter();
    const errorMsg = ref('');
    const filterEmployeeId = ref('');
    const filterTypeId = ref('');
    const activeFilters = ref(false);
    const { getAssetTypeName, fetchAssetTypes } = useAssetTypes();
    const { getAssetLocationName, fetchAssetLocations } = useAssetLocations();
    const { getAssetEmployeeName, fetchAssetEmployees } = useAssetEmployees();

    const fetchAssets = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        errorMsg.value = 'No bearer token set. Go to Home and save one first.';
        assets.value = [];
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      
      // Fetch asset types first
      await fetchAssetTypes();
      
      try {
        const response = await axios.get(`${API_BASE}/resources/`, {
          headers: { Authorization: token },
        });
        assets.value = response.data;
        
        // Convert binary is_decommissioned to proper boolean for all assets
        assets.value.forEach(asset => {
          if (asset.is_decommissioned !== null && asset.is_decommissioned !== undefined) {
            if (typeof asset.is_decommissioned === 'object') {
              asset.is_decommissioned = asset.is_decommissioned[0] === 1;
            } else if (typeof asset.is_decommissioned === 'number') {
              asset.is_decommissioned = asset.is_decommissioned === 1;
            } else if (typeof asset.is_decommissioned === 'string') {
              asset.is_decommissioned = asset.is_decommissioned === '1' || 
                                        asset.is_decommissioned.charCodeAt(0) === 1;
            }
          }
        });
        
        console.log('Assets received from API:', response.data);
        errorMsg.value = '';
      } catch (error) {
        console.error('Error fetching assets:', error);
        errorMsg.value = error?.response?.data?.detail || 'Failed to fetch assets';
        assets.value = [];
      }
    };

    const viewAsset = (asset) => {
      router.push({ name: 'AssetView', params: { id: asset.id } });
    };

    const goToAddAsset = () => {
      router.push({ name: 'AssetAdd' });
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    };

    onMounted(fetchAssets);

    const applyFilters = () => {
      if (!filterEmployeeId.value && !filterTypeId.value) {
        activeFilters.value = false;
        filteredAssets.value = [];
        return;
      }

      filteredAssets.value = assets.value.filter(asset => {
        const matchesEmployee = !filterEmployeeId.value || 
          (asset.employee_id && asset.employee_id.toString().includes(filterEmployeeId.value));
        const matchesType = !filterTypeId.value || 
          (asset.type_id && asset.type_id.toString().includes(filterTypeId.value));
        
        return matchesEmployee && matchesType;
      });

      activeFilters.value = true;
    };

    const clearFilters = () => {
      filterEmployeeId.value = '';
      filterTypeId.value = '';
      filteredAssets.value = [];
      activeFilters.value = false;
    };

    const displayedAssets = computed(() => {
      return activeFilters.value ? filteredAssets.value : assets.value;
    });

    return { 
      assets, 
      displayedAssets,
      viewAsset, 
      goToAddAsset, 
      errorMsg, 
      formatDate,
      getAssetTypeName,
      filterEmployeeId,
      filterTypeId,
      applyFilters,
      clearFilters,
      activeFilters,
      filteredAssets
    };
  },
};
</script>

<style scoped>
.asset-list-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-header h1 {
  font-size: 2rem;
  color: var(--color-heading);
  margin: 0 0 0.25rem 0;
  font-weight: 700;
}

.subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.9375rem;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--color-success);
  padding: 0.75rem 1.5rem;
}

.btn-add:hover {
  background: #059669;
}

.btn-add .icon {
  font-size: 1rem;
}

.filter-section {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text);
}

.filter-input {
  padding: 0.625rem 0.875rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 0.9375rem;
  background: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s ease;
}

.filter-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-buttons {
  display: flex;
  gap: 0.75rem;
}

.btn-filter {
  background: var(--color-primary);
  color: white;
  padding: 0.625rem 1.5rem;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-filter:hover {
  background: var(--color-primary-hover);
}

.btn-clear {
  background: var(--color-background);
  color: var(--color-text);
  padding: 0.625rem 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-clear:hover {
  background: var(--color-border);
  border-color: var(--color-text-muted);
}

.active-filters {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--color-primary);
  color: white;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.8125rem;
  font-weight: 600;
}

.result-count {
  opacity: 0.9;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--color-background-soft);
  border-radius: var(--border-radius-lg);
  border: 2px dashed var(--color-border);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h2 {
  color: var(--color-heading);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--color-text-muted);
  margin-bottom: 1.5rem;
}

.asset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.asset-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.asset-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.asset-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 0.75rem;
}

.asset-header h3 {
  color: var(--color-heading);
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.badge {
  padding: 0.25rem 0.625rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--color-success);
}

.badge-danger {
  background: rgba(239, 68, 68, 0.1);
  color: var(--color-danger);
}

.asset-body {
  margin-bottom: 1rem;
}

.asset-notes {
  color: var(--color-text);
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  line-height: 1.5;
}

.asset-meta {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.meta-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.8125rem;
}

.meta-label {
  color: var(--color-text-muted);
  font-weight: 500;
}

.meta-value {
  color: var(--color-text);
}

.asset-footer {
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.view-link {
  color: var(--color-primary);
  font-size: 0.875rem;
  font-weight: 500;
}

.asset-card:hover .view-link {
  color: var(--color-primary-hover);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
  }

  .btn-add {
    width: 100%;
    justify-content: center;
  }

  .filter-controls {
    flex-direction: column;
  }

  .filter-group {
    min-width: unset;
  }

  .filter-buttons {
    width: 100%;
  }

  .btn-filter,
  .btn-clear {
    flex: 1;
  }

  .asset-grid {
    grid-template-columns: 1fr;
  }
}
</style>