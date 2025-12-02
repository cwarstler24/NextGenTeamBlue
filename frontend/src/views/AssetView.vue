<template>
  <div>
    <h1>Asset Details</h1>
    <div v-if="asset">
      <h2>{{ asset.name }}</h2>
      <p>{{ asset.description }}</p>
      <button @click="goBack">Back to List</button>
    </div>
    <div v-else>
      <p>Loading asset details...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const asset = ref(null);
    const route = useRoute();
    const router = useRouter();

    const fetchAsset = async () => {
      try {
        const response = await axios.get(`/api/assets/${route.params.id}`); // Adjust the endpoint as necessary
        asset.value = response.data;
      } catch (error) {
        console.error('Error fetching asset:', error);
      }
    };

    const goBack = () => {
      router.push({ name: 'AssetList' });
    };

    onMounted(fetchAsset);

    return { asset, goBack };
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>