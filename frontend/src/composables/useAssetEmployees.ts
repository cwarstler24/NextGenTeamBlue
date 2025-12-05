import { ref } from 'vue';
import axios from 'axios';

const API_BASE = 'http://0.0.0.0:0000';

/**
 * Composable for managing asset employees
 * Handles fetching asset employees and provides utilities to look up type names
 */
export function useAssetEmployees() {
  const assetEmployees = ref<any[]>([]);
  const assetEmployeeMap = ref<{ [key: number]: string }>({});
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetch asset employees from the API
   */
  const fetchAssetEmployees = async () => {
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

      assetEmployees.value = response.data;

      // Build lookup map for type names
      const map: { [key: number]: string } = {};
      response.data.forEach((type: any) => {
        map[type.id] = type.asset_employee_name;
      });
      assetEmployeeMap.value = map;

      console.log('Asset Employees loaded:', assetEmployees.value);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Failed to fetch asset employees';
      console.error('Error fetching asset employees:', err);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Get the human-readable name for an asset type ID
   */
  const getAssetEmployeeName = (employeeId: number): string => {
    return assetEmployeeMap.value[employeeId] || `Employee ${employeeId}`;
  };

  return {
    assetEmployees,
    assetEmployeeMap,
    isLoading,
    error,
    fetchAssetEmployees,
    getAssetEmployeeName,
  };
}
