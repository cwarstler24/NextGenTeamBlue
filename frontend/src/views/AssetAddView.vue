<template>
  <div class="asset-add-view">
    <div class="page-header">
      <button @click="goBack" class="btn-back">
        ← Back to List
      </button>
    </div>

    <div class="form-container">
      <div class="form-header">
        <h1>Add New Asset</h1>
        <p>Fill in the details to register a new asset in the system</p>
      </div>

      <form @submit.prevent="addAsset" class="asset-form">
        <div class="form-grid">
          <div class="form-group">
            <label for="type_id">
              Type ID
              <span class="required">*</span>
            </label>
            <select required v-model="selected" v-model.number="assetType" id="type_id">
              <option disabled value="">Please select one</option>
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
            </select>
            <small class="help-text">The category or type identifier for this asset</small>
          </div>

          <div class="form-group">
            <label for="location_id">Location ID</label>
            <select required v-model="selected" v-model.number="assetLocation" id="location_id">
              <option disabled value="">Please select one</option>
              <option></option>
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
            </select>
            <small class="help-text">Where this asset is physically located</small>
          </div>

          <div class="form-group">
            <label for="employee_id">Employee ID</label>
            <input 
              id="employee_id"
              type="number" 
              v-model.number="assetEmployeeID"
              placeholder="Enter employee ID (optional)"
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
          <button type="submit" class="btn-primary">
            Add Asset
          </button>
          <button type="button" @click="goBack" class="btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export default {
  setup() {
    const assetType = ref('');
    const assetLocation = ref('');
    const assetEmployeeID = ref('');
    const assetNotes = ref('');
    const assetIsDecommissioned = ref(0);
    const router = useRouter();

    const addAsset = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        alert('⚠️ No bearer token set. Go to Home and save one first.');
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      try {
        await axios.post(`${API_BASE}/resources/`, {
          type_id: assetType.value,
          location_id: assetLocation.value || null,
          employee_id: assetEmployeeID.value || null,
          notes: assetNotes.value || null,
          is_decommissioned: assetIsDecommissioned.value,
        }, {
          headers: { Authorization: token },
        });
        
        alert('✅ Asset added successfully!');
        router.push({ name: 'AssetList' });
      } catch (error) {
        console.error('Error adding asset:', error);
        alert('❌ ' + (error?.response?.data?.detail || 'Failed to add asset'));
      }
    };

    const goBack = () => {
      router.push({ name: 'AssetList' });
    };

    return { 
      assetType, 
      assetLocation, 
      assetEmployeeID, 
      assetNotes, 
      assetIsDecommissioned, 
      addAsset,
      goBack 
    };
  },
};
</script>

<style scoped>
.asset-add-view {
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

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.btn-primary {
  flex: 1;
  background: var(--color-success);
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
}

.btn-primary:hover {
  background: #059669;
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
