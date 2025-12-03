<template>
  <div>
    <h1>Add New Asset</h1>
    <form @submit.prevent="addAsset">
      <label for="type_id">Type ID:</label>
      <input type="number" v-model="assetType" required />
      <label for="location_id">Location ID:</label>
      <input type="number" v-model="assetLocation" />
      <label for="employee_id">Employee ID:</label>
      <input type="number" v-model="assetEmployeeID" />
      <label for="notes">Notes:</label>
      <input type="text" v-model="assetNotes" />
      <label for="is_decommissioned">Is Decommissioned (0 or 1):</label>
      <input type="number" v-model="assetIsDecommissioned" required min="0" max="1" />

      <button type="submit">Add Asset</button>
    </form>
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
        alert('No bearer token set. Go to Home and save one first.');
        return;
      }
      if (!token.toLowerCase().startsWith('bearer ')) {
        token = `Bearer ${token}`;
      }
      try {
        await axios.post(`${API_BASE}/resources/`, {
          type_id: assetType.value,
          location_id: assetLocation.value ? parseInt(assetLocation.value) : null,
          employee_id: assetEmployeeID.value ? parseInt(assetEmployeeID.value) : null,
          notes: assetNotes.value,
          is_decommissioned: assetIsDecommissioned.value === 1 ? 1 : 0,
        }, {
          headers: { Authorization: token },
        });
        // Reset form fields
        assetType.value = '';
        assetLocation.value = '';
        assetEmployeeID.value = '';
        assetNotes.value = '';
        assetIsDecommissioned.value = 0;

        alert('Asset added successfully!');
        router.push({ name: 'AssetList' });
      } catch (error) {
        console.error('Error adding asset:', error);
        alert(error?.response?.data?.detail || 'Failed to add asset');
      }
    };

    return { assetType, assetLocation, assetEmployeeID, assetNotes, assetIsDecommissioned, addAsset };
  },
};
</script>

<style scoped>
/* Add any specific styles for this view here */
</style>
