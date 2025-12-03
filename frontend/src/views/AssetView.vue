<template>
  <div>
    <h1>Asset Details</h1>
    <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
    <div v-if="asset">
      <h2>{{ asset.resource_id || `Asset #${asset.id}` }}</h2>
      <div class="details">
        <p><strong>ID:</strong> {{ asset.id }}</p>
        <p><strong>Resource ID:</strong> {{ asset.resource_id || 'Not set' }}</p>
        <p><strong>Type ID:</strong> {{ asset.type_id }}</p>
        <p><strong>Date Added:</strong> {{ asset.date_added }}</p>
        <p v-if="asset.location_id"><strong>Location ID:</strong> {{ asset.location_id }}</p>
        <p v-if="asset.employee_id"><strong>Employee ID:</strong> {{ asset.employee_id }}</p>
        <p v-if="asset.notes"><strong>Notes:</strong> {{ asset.notes }}</p>
        <p><strong>Decommissioned:</strong> {{ asset.is_decommissioned ? 'Yes' : 'No' }}</p>
        <p v-if="asset.decommission_date"><strong>Decommission Date:</strong> {{ asset.decommission_date }}</p>
      </div>
      <button @click="goBack">Back to List</button>
    </div>
    <div v-else-if="!errorMsg">
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
        console.log('Asset details:', response.data);
      } catch (error) {
        console.error('Error fetching asset:', error);
        errorMsg.value = error?.response?.data?.detail || 'Failed to fetch asset details';
      }
    };

    const goBack = () => {
      router.push({ name: 'AssetList' });
    };

    onMounted(fetchAsset);

    return { asset, errorMsg, goBack };
  },
};
</script>

<style scoped>
.error {
  color: #c22;
  margin-bottom: 1rem;
}
.details {
  background: var(--color-background-soft);
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}
.details p {
  margin: 0.5rem 0;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>