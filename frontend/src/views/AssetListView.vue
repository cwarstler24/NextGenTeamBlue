<template>
  <div>
    <h1>Asset List</h1>
    <button @click="goToAddAsset">Add Asset</button>
    <ul>
      <li v-for="asset in assets" :key="asset.id" @click="viewAsset(asset)">
        {{ asset.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const assets = ref([]);
    const router = useRouter();

    const fetchAssets = async () => {
      try {
        const response = await axios.get('/api/assets'); // Adjust the endpoint as necessary
        assets.value = response.data;
      } catch (error) {
        console.error('Error fetching assets:', error);
      }
    };

    const viewAsset = (asset) => {
      router.push({ name: 'AssetView', params: { id: asset.id } });
    };

    const goToAddAsset = () => {
      router.push({ name: 'AssetAdd' });
    };

    onMounted(fetchAssets);

    return { assets, viewAsset, goToAddAsset };
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>