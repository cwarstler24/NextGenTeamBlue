<template>
  <div class="asset-view">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        ← Back to List
      </button>
    </div>

    <div v-if="errorMsg" class="error">
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <div v-if="asset" class="asset-details">
      <div class="details-header">
        <div>
          <h1>{{ asset.resource_id || `Asset #${asset.id}` }}</h1>
          <span 
            class="badge" 
            :class="asset.is_decommissioned ? 'badge-danger' : 'badge-success'"
          >
            {{ asset.is_decommissioned ? 'Decommissioned' : 'Active' }}
          </span>
        </div>
      </div>

      <div class="details-grid">
        <div class="detail-card">
          <h3>Basic Information</h3>
          <div class="detail-rows">
            <div class="detail-row">
              <span class="label">Asset ID:</span>
              <span class="value">{{ asset.id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Resource ID:</span>
              <span class="value">{{ asset.resource_id || 'Not set' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Type ID:</span>
              <span class="value">{{ asset.type_id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Date Added:</span>
              <span class="value">{{ formatDate(asset.date_added) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-card">
          <h3>Assignment Details</h3>
          <div class="detail-rows">
            <div class="detail-row">
              <span class="label">Location ID:</span>
              <span class="value">{{ asset.location_id || 'Not assigned' }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Employee ID:</span>
              <span class="value">{{ asset.employee_id || 'Not assigned' }}</span>
            </div>
          </div>
        </div>

        <div v-if="asset.is_decommissioned" class="detail-card decommission-card">
          <h3>Decommission Information</h3>
          <div class="detail-rows">
            <div class="detail-row">
              <span class="label">Status:</span>
              <span class="value danger">Decommissioned</span>
            </div>
            <div v-if="asset.decommission_date" class="detail-row">
              <span class="label">Decommission Date:</span>
              <span class="value">{{ formatDate(asset.decommission_date) }}</span>
            </div>
          </div>
        </div>

        <div v-if="asset.notes" class="detail-card notes-card">
          <h3>Notes</h3>
          <p class="notes-content">{{ asset.notes }}</p>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="goBack" class="btn-secondary">
          ← Back to List
        </button>
        <button 
          v-if="!asset.is_decommissioned"
          @click="decommissionAsset" 
          class="btn-danger"
          :disabled="isDecommissioning"
        >
          {{ isDecommissioning ? 'Decommissioning...' : 'Decommission Asset' }}
        </button>
      </div>
    </div>

    <div v-else-if="!errorMsg" class="loading-state">
      <div class="spinner"></div>
      <p>Loading asset details...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export default {
  setup() {
    const asset = ref(null);
    const errorMsg = ref('');
    const route = useRoute();
    const router = useRouter();
    const isDecommissioning = ref(false);

    const fetchAsset = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        errorMsg.value = 'No bearer token set. Go to Home and save one first.';
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      try {
        const response = await axios.get(`${API_BASE}/resources/${route.params.id}`, {
          headers: { Authorization: token },
        });
        asset.value = response.data;
        
        // Convert binary is_decommissioned to proper boolean
        // MySQL binary field returns buffer/bytes: \x00 = false, \x01 = true
        if (asset.value.is_decommissioned !== null && asset.value.is_decommissioned !== undefined) {
          // Check if it's a buffer/array or number
          if (typeof asset.value.is_decommissioned === 'object') {
            asset.value.is_decommissioned = asset.value.is_decommissioned[0] === 1;
          } else if (typeof asset.value.is_decommissioned === 'number') {
            asset.value.is_decommissioned = asset.value.is_decommissioned === 1;
          } else if (typeof asset.value.is_decommissioned === 'string') {
            asset.value.is_decommissioned = asset.value.is_decommissioned === '1' || 
                                             asset.value.is_decommissioned.charCodeAt(0) === 1;
          }
        }
        
        console.log('Asset details:', response.data);
        console.log('is_decommissioned (normalized):', asset.value.is_decommissioned);
      } catch (error) {
        console.error('Error fetching asset:', error);
        errorMsg.value = error?.response?.data?.detail || 'Failed to fetch asset details';
      }
    };

    const goBack = () => {
      router.push({ name: 'AssetList' });
    };

    const decommissionAsset = async () => {
      const confirmed = window.confirm(
        `Are you sure you want to decommission "${asset.value.resource_id || `Asset #${asset.value.id}`}"?\n\nThis action will mark the asset as decommissioned.`
      );

      if (!confirmed) {
        return;
      }

      isDecommissioning.value = true;

      let token = localStorage.getItem('bearerToken');
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }

      try {
        const response = await axios.put(
          `${API_BASE}/resources/${asset.value.id}`,
          {
            ...asset.value,
            is_decommissioned: 1,
          },
          {
            headers: { Authorization: token },
          }
        );

        console.log('Decommission response:', response);

        // Refresh the asset to show updated status
        await fetchAsset();
        
        alert('Asset decommissioned successfully!');
      } catch (error) {
        console.error('Error decommissioning asset:', error);
        errorMsg.value = error?.response?.data?.detail || 'Failed to decommission asset';
        alert((error?.response?.data?.detail || 'Failed to decommission asset'));
      } finally {
        isDecommissioning.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    onMounted(fetchAsset);

    return { asset, errorMsg, goBack, decommissionAsset, isDecommissioning, formatDate };
  },
};
</script>

<style scoped>
.asset-view {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 1.5rem;
}

.btn-back {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-border);
  box-shadow: none;
  padding: 0.5rem 1rem;
}

.btn-back:hover {
  background: var(--color-background-soft);
  border-color: var(--color-primary);
}

.btn-secondary {
  background: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-background-mute);
}

.btn-danger {
  background: var(--color-danger);
  color: white;
  border: none;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.asset-details {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.details-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid var(--color-border);
}

.details-header > div {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.details-header h1 {
  font-size: 2rem;
  color: var(--color-heading);
  margin: 0;
  font-weight: 700;
}

.badge {
  padding: 0.375rem 0.875rem;
  border-radius: 16px;
  font-size: 0.8125rem;
  font-weight: 600;
}

.badge-success {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.badge-danger {
  background: rgba(239, 68, 68, 0.15);
  color: var(--color-danger);
}

.details-grid {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.detail-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.decommission-card {
  border-color: var(--color-danger);
  background: rgba(239, 68, 68, 0.02);
}

.notes-card {
  grid-column: 1 / -1;
}

.detail-card h3 {
  font-size: 1.125rem;
  color: var(--color-heading);
  margin: 0 0 1rem 0;
  font-weight: 600;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--color-border);
}

.detail-rows {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.detail-row .label {
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 0.875rem;
}

.detail-row .value {
  color: var(--color-text);
  font-weight: 500;
  text-align: right;
}

.detail-row .value.danger {
  color: var(--color-danger);
  font-weight: 600;
}

.notes-content {
  color: var(--color-text);
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: var(--color-text-muted);
}

@media (min-width: 768px) {
  .details-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .details-header h1 {
    font-size: 1.5rem;
  }

  .detail-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .detail-row .value {
    text-align: left;
  }
}
</style>