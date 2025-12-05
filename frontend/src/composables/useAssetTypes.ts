import { ref } from 'vue';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

/**
 * Composable for managing asset types
 * Handles fetching asset types and provides utilities to look up type names
 */
export function useAssetTypes() {
  const assetTypes = ref<any[]>([]);
  const assetTypeMap = ref<{ [key: number]: string }>({});
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetch asset types from the API
   */
  const fetchAssetTypes = async () => {
    isLoading.value = true;
    error.value = null;

    let token = localStorage.getItem('bearerToken');
    if (!token) {
      error.value = 'No bearer token set';
      isLoading.value = false;
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

      // Build lookup map for type names
      const map: { [key: number]: string } = {};
      response.data.forEach((type: any) => {
        map[type.id] = type.asset_type_name;
      });
      assetTypeMap.value = map;

      console.log('Asset types loaded:', assetTypes.value);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Failed to fetch asset types';
      console.error('Error fetching asset types:', err);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Get the human-readable name for an asset type ID
   */
  const getAssetTypeName = (typeId: number): string => {
    return assetTypeMap.value[typeId] || `Type ${typeId}`;
  };

  return {
    assetTypes,
    assetTypeMap,
    isLoading,
    error,
    fetchAssetTypes,
    getAssetTypeName,
  };
}
