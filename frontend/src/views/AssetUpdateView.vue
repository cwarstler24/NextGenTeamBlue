<template>
  <div class="asset-update-view">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        ← Back to List
      </button>
    </div>

    <div v-if="errorMsg" class="error">
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <div class="form-container" v-if="asset">
      <div class="form-header">
        <h1>Update Asset</h1>
        <p>Modify the asset details and submit to save changes</p>
      </div>

      <form @submit.prevent="updateAsset" class="asset-form">
        <div class="form-grid">
          <div class="form-group">
            <label for="type_id">
              Type ID
              <span class="required">*</span>
            </label>
            <select required v-model.number="assetType" id="type_id">
              <option v-for="type in assetTypes" :key="type.id" :value="type.id">
                {{ type.id }}{{ type.type_name ? ` - ${type.type_name}` : '' }}
              </option>
            </select>
            <small class="help-text">The category or type identifier for this asset</small>
          </div>

          <div class="form-group">
            <label for="location_id">
              Location ID
              <span class="help-text-inline">(or Employee ID below)</span>
            </label>
            <select v-model.number="assetLocation" id="location_id">
              <option :value="null">Not assigned to location</option>
              <option :value="1">1</option>
              <option :value="2">2</option>
              <option :value="3">3</option>
              <option :value="4">4</option>
            </select>
            <small class="help-text">Where this asset is physically located</small>
          </div>

          <div class="form-group">
            <label for="employee_id">
              Employee ID
              <span class="help-text-inline">(or Location ID above)</span>
            </label>
            <input 
              id="employee_id"
              type="number" 
              v-model.number="assetEmployeeID"
              placeholder="Enter employee ID (or leave blank for location)"
            />
            <small class="help-text">Employee responsible for this asset</small>
          </div>

          <div class="form-group">
            <label for="is_decommissioned">
              Status
              <span class="required">*</span>
            </label>
            <select 
              id="is_decommissioned"
              v-model.number="assetIsDecommissioned" 
              required
            >
              <option :value="0">Active</option>
              <option :value="1">Decommissioned</option>
            </select>
            <small class="help-text">Current operational status</small>
          </div>
        </div>

        <div class="form-group full-width">
          <label for="notes">Notes</label>
          <textarea 
            id="notes"
            v-model="assetNotes"
            rows="4"
            placeholder="Add any additional notes or comments about this asset..."
          ></textarea>
          <small class="help-text">Optional description or special instructions</small>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="isUpdating">
            {{ isUpdating ? 'Updating...' : 'Update Asset' }}
          </button>
          <button type="button" @click="goBack" class="btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>

    <div v-else class="loading-state">
      <div class="spinner"></div>
      <p>Loading asset details...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export default {
  setup() {
    const asset = ref(null);
    const assetType = ref('');
    const assetLocation = ref(null);
    const assetEmployeeID = ref('');
    const assetNotes = ref('');
    const assetIsDecommissioned = ref(0);
    const assetTypes = ref([]);
    const errorMsg = ref('');
    const router = useRouter();
    const route = useRoute();
    const isUpdating = ref(false);

    const fetchAssetTypes = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        console.error('No bearer token set');
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      try {
        const response = await axios.get(`${API_BASE}/resources/types/`, {
          headers: { Authorization: token },
        });
        assetTypes.value = response.data;
        console.log('Asset types loaded:', assetTypes.value);
      } catch (error) {
        console.error('Error fetching asset types:', error);
      }
    };

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
        
        // Populate form fields with asset data
        assetType.value = asset.value.type_id;
        assetLocation.value = asset.value.location_id || null;
        assetEmployeeID.value = asset.value.employee_id || '';
        assetNotes.value = asset.value.notes || '';
        
        // Convert binary is_decommissioned to proper boolean/number
        if (asset.value.is_decommissioned !== null && asset.value.is_decommissioned !== undefined) {
          if (typeof asset.value.is_decommissioned === 'object') {
            assetIsDecommissioned.value = asset.value.is_decommissioned[0] === 1 ? 1 : 0;
          } else if (typeof asset.value.is_decommissioned === 'number') {
            assetIsDecommissioned.value = asset.value.is_decommissioned === 1 ? 1 : 0;
          } else if (typeof asset.value.is_decommissioned === 'string') {
            assetIsDecommissioned.value = (asset.value.is_decommissioned === '1' || 
                                             asset.value.is_decommissioned.charCodeAt(0) === 1) ? 1 : 0;
          }
        }
        
        console.log('Asset loaded for update:', asset.value);
      } catch (error) {
        console.error('Error fetching asset:', error);
        errorMsg.value = error?.response?.data?.detail || 'Failed to fetch asset details';
      }
    };

    const updateAsset = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        alert('⚠️ No bearer token set. Go to Home and save one first.');
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      
      isUpdating.value = true;
      
      try {
        // Build payload with updated values
        const payload = {
          type_id: assetType.value,
          is_decommissioned: assetIsDecommissioned.value,
        };
        
        // Add either location_id or employee_id (exactly one should be set)
        if (assetLocation.value) {
          payload.location_id = assetLocation.value;
        } else if (assetEmployeeID.value) {
          payload.employee_id = assetEmployeeID.value;
        } else {
          alert('Please assign the asset to either a location or an employee.');
          isUpdating.value = false;
          return;
        }
        
        // Add optional notes
        if (assetNotes.value) {
          payload.notes = assetNotes.value;
        }
        
        await axios.put(`${API_BASE}/resources/${route.params.id}`, payload, {
          headers: { Authorization: token },
        });
        
        alert('Asset updated successfully!');
        router.push({ name: 'AssetView', params: { id: route.params.id } });
      } catch (error) {
        console.error('Error updating asset:', error);
        alert((error?.response?.data?.detail || 'Failed to update asset'));
      } finally {
        isUpdating.value = false;
      }
    };

    const goBack = () => {
      router.push({ name: 'AssetView', params: { id: route.params.id } });
    };

    onMounted(() => {
      fetchAsset();
      fetchAssetTypes();
    });

    return {
      asset,
      assetType,
      assetLocation,
      assetEmployeeID,
      assetNotes,
      assetIsDecommissioned,
      assetTypes,
      errorMsg,
      updateAsset,
      goBack,
      isUpdating,
    };
  },
};
</script>

<style scoped>
.asset-update-view {
  max-width: 800px;
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

.form-container {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.form-header {
  padding: 2rem;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
}

.form-header h1 {
  font-size: 1.75rem;
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.form-header p {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.9375rem;
}

.asset-form {
  padding: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-heading);
  font-size: 0.875rem;
}

.required {
  color: var(--color-danger);
  font-weight: 700;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
  line-height: 1.5;
}

.help-text {
  margin-top: 0.375rem;
  color: var(--color-text-muted);
  font-size: 0.8125rem;
  line-height: 1.4;
}

.help-text-inline {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  font-weight: 400;
}

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.btn-primary {
  flex: 1;
  background: var(--color-primary);
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 0.875rem 1.5rem;
  box-shadow: none;
}

.btn-secondary:hover {
  background: var(--color-background-mute);
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

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
