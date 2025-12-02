<template>
  <div>
    <h1>Add New Asset</h1>
    <form @submit.prevent="addAsset">
      <label for="name">Asset Name:</label>
      <input type="text" v-model="assetName" required />
      <label for="description">Description:</label>
      <textarea v-model="assetDescription" required></textarea>
      <button type="submit">Add Asset</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const assetName = ref('');
    const assetDescription = ref('');

    const addAsset = async () => {
      try {
        await axios.post('/api/assets', {
          name: assetName.value,
          description: assetDescription.value,
        });
        // Reset form fields
        assetName.value = '';
        assetDescription.value = '';
      } catch (error) {
        console.error('Error adding asset:', error);
      }
    };

    return { assetName, assetDescription, addAsset };
  },
};
</script>

<style scoped>
/* Add any specific styles for this view here */
</style>
