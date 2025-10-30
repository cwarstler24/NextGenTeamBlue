import pytest
import requests

API_BASE_URL = "http://localhost:8000/api"  # Update with your actual dev server URL

# Sample tokens for testing
VALID_EMPLOYEE_TOKEN = "valid-employee-token"
VALID_MANAGER_TOKEN = "valid-manager-token"
INVALID_TOKEN = "invalid-token"

# Helper function to build headers
def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# -------------------------------
# 1. Query Resources by Location
# -------------------------------
def test_query_resources_by_location_valid_token():
    response = requests.get(
        f"{API_BASE_URL}/resources?location=NYC",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_query_resources_by_location_invalid_token():
    response = requests.get(
        f"{API_BASE_URL}/resources?location=NYC",
        headers=auth_header(INVALID_TOKEN)
    )
    assert response.status_code == 401

# -------------------------------
# 2. Add Resource
# -------------------------------
def test_add_resource_valid_manager():
    payload = {
        "name": "New Resource",
        "location": "NYC",
        "type": "equipment"
    }
    response = requests.post(
        f"{API_BASE_URL}/resources",
        json=payload,
        headers=auth_header(VALID_MANAGER_TOKEN)
    )
    assert response.status_code == 201

def test_add_resource_invalid_token():
    payload = {"name": "Invalid Resource"}
    response = requests.post(
        f"{API_BASE_URL}/resources",
        json=payload,
        headers=auth_header(INVALID_TOKEN)
    )
    assert response.status_code == 401

# -------------------------------
# 3. Delete Resource
# -------------------------------
def test_delete_resource_valid_manager():
    resource_id = 123  # Replace with a valid test ID
    response = requests.delete(
        f"{API_BASE_URL}/resources/{resource_id}",
        headers=auth_header(VALID_MANAGER_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 4. Update Resource
# -------------------------------
def test_update_resource_valid_manager():
    resource_id = 123
    payload = {"name": "Updated Resource"}
    response = requests.put(
        f"{API_BASE_URL}/resources/{resource_id}",
        json=payload,
        headers=auth_header(VALID_MANAGER_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 5. Query by Employee
# -------------------------------
def test_query_by_employee():
    response = requests.get(
        f"{API_BASE_URL}/resources?employee_id=456",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 6. Query by Resource ID
# -------------------------------
def test_query_by_resource_id():
    response = requests.get(
        f"{API_BASE_URL}/resources/123",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 7. Query by Date Assigned
# -------------------------------
def test_query_by_date_assigned():
    response = requests.get(
        f"{API_BASE_URL}/resources?date=2025-10-22",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 8. Query by Multiple Fields
# -------------------------------
def test_query_by_multiple_fields():
    response = requests.get(
        f"{API_BASE_URL}/resources?location=NYC&type=equipment",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 9. Modify Group of Resources
# -------------------------------
def test_modify_group_of_resources():
    payload = {
        "group_id": 789,
        "updates": {"status": "inactive"}
    }
    response = requests.put(
        f"{API_BASE_URL}/resources/group",
        json=payload,
        headers=auth_header(VALID_MANAGER_TOKEN)
    )
    assert response.status_code == 200

# -------------------------------
# 10. Invalid Request
# -------------------------------
def test_invalid_request():
    response = requests.get(
        f"{API_BASE_URL}/resources?location=",
        headers=auth_header(VALID_EMPLOYEE_TOKEN)
    )
    assert response.status_code == 400
