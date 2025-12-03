<template>
  <div>
    <h1>Asset List</h1>
    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    <button @click="goToAddAsset">Add Asset</button>
    <p v-if="assets.length === 0 && !errorMsg">No assets found in database.</p>
    <ul>
      <li v-for="asset in assets" :key="asset.id" @click="viewAsset(asset)">
        <strong>{{ asset.resource_id || `Asset #${asset.id}` }}</strong>
        <span v-if="asset.notes"> - {{ asset.notes }}</span>
        <span class="meta"> (Type: {{ asset.type_id }}, Added: {{ asset.date_added }})</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export default {
  setup() {
    const assets = ref([]);
    const router = useRouter();
    const errorMsg = ref('');

    const fetchAssets = async () => {
      let token = localStorage.getItem('bearerToken');
      if (!token) {
        errorMsg.value = 'No bearer token set. Go to Home and save one first.';
        assets.value = [];
        return;
      }
      // Ensure proper Bearer prefix even if stored value was raw
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      try {
        const response = await axios.get(`${API_BASE}/resources/`, {
          headers: { Authorization: token },
        });
        assets.value = response.data;
        console.log('Assets received from API:', response.data);
        if (response.data.length > 0) {
          console.log('First asset structure:', response.data[0]);
        }
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

    onMounted(fetchAssets);

    return { assets, viewAsset, goToAddAsset, errorMsg };
  },
};
</script>

<style scoped>
/* Add your styles here */
.error { color: #c22; margin-bottom: 0.5rem; }
li {
  cursor: pointer;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  margin-bottom: 0.5rem;
  border-radius: 4px;
}
li:hover {
  background-color: var(--color-background-soft);
}
.meta {
  color: var(--color-text-muted, #888);
  font-size: 0.9em;
}
</style>