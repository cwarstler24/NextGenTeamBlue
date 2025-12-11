import { ref } from 'vue';
import axios from 'axios';
import { API_BASE } from '../config/api';

/**
 * Composable for managing asset locations
 * Handles fetching asset locations and provides utilities to look up type names
 */
export function useAssetLocations() {
  const assetLocations = ref<any[]>([]);
  const assetLocationMap = ref<{ [key: number]: string }>({});
  // Map location ID to { city, country }
  const assetLocationCityCountryMap = ref<{ [key: number]: { city: string; country: string } }>({});
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
      const response = await axios.get(`${API_BASE}/resources/locations/`, {
        headers: { Authorization: token },
      });

      assetLocations.value = response.data;

      // Build lookup map for location names
      const nameMap: { [key: number]: string } = {};
      const cityCountryMap: { [key: number]: { city: string; country: string } } = {};
      response.data.forEach((location: any) => {
        nameMap[location.id] = location.asset_location_name;
        cityCountryMap[location.id] = {
          city: location.city,
          country: location.country,
        };
      });
      assetLocationMap.value = nameMap;
      assetLocationCityCountryMap.value = cityCountryMap;

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
  assetLocationCityCountryMap,
  isLoading,
  error,
  fetchAssetLocations,
  getAssetLocationName,
  };
}
