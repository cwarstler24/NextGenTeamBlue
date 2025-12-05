import { ref } from 'vue';
import axios from 'axios';

const API_BASE = 'http://0.0.0.0:0000';

/**
 * Composable for managing asset locations
 * Handles fetching asset locations and provides utilities to look up type names
 */
export function useAssetLocations() {
  const assetLocations = ref<any[]>([]);
  const assetLocationMap = ref<{ [key: number]: string }>({});
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetch asset locations from the API
   */
  const fetchAssetLocations = async () => {
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
      const response = await axios.get(`${API_BASE}//`, {
        headers: { Authorization: token },
      });

      assetLocations.value = response.data;

      // Build lookup map for type names
      const map: { [key: number]: string } = {};
      response.data.forEach((type: any) => {
        map[type.id] = type.asset_location_name;
      });
      assetLocationMap.value = map;

      console.log('Asset Locations loaded:', assetLocations.value);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Failed to fetch asset locations';
      console.error('Error fetching asset locations:', err);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Get the human-readable name for an asset type ID
   */
  const getAssetLocationName = (locationId: number): string => {
    return assetLocationMap.value[locationId] || `Location ${locationId}`;
  };

  return {
    assetLocations,
    assetLocationMap,
    isLoading,
    error,
    fetchAssetLocations,
    getAssetLocationName,
  };
}
