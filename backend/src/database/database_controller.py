"""
Database Controller Module

This module provides high-level functions for managing asset resources and resource types in 
the database. It enforces user permissions (e.g., only Managers can add, update, or delete assets),
handles logging, and interacts with the database via the database_connector module.

Features:
- Add, update, and delete asset resources and resource types.
- Retrieve assets by various criteria (ID, employee, location).
- Enforces role-based access control for sensitive operations.
- Logs all operations for traceability.

Example usage:
    status = add_resource_type("Manager", {"asset_type_name": "Laptop"})
    status, assets = get_resources()
    status = delete_resource("Manager", 123)
"""

import datetime
from src.database import database_connector
from src.logger import logger
import src.database.authorize as auth


def add_resource_type(
        resource,
        user_position: auth.Role = auth.Role.OTHER
        ) -> int:
    """
    Adds a new resource type to the database.

    Only users with the "Manager" position are allowed to add resource types.

    Args:
        resource (dict): Dictionary containing resource type details (expects "asset_type_name").
        user_position (Role): The user's position (must be "Manager").

    Returns:
        int: 200 if successful, 400 if failed, 401 if unauthorized.
    """
    logger.event("add_resource_type called", level="trace")

    # Only Managers can add resource types
    if not auth.can_write(user_position):
        logger.event("Returning error 401: user does not have write access",
                     level="trace")
        return 401

    logger.event("User has write access", level="trace")
    asset_type_name = resource.get("asset_type_name")

    update_query = """
    INSERT INTO AssetTypes (asset_type_name)
    VALUES (:asset_type_name);
    """

    params = {
        "asset_type_name": asset_type_name
    }

    logger.event(f"Running query {update_query} with params: {params}", level="trace")
    result = database_connector.execute_query(update_query, params)

    if result is not None:
        logger.event(f"Successfully added resource type {asset_type_name}", level="info")
        return 200
    logger.event(f"Failed to add resource type {asset_type_name}", level="error")
    return 400


def add_resource_asset(
        resource,
        user_position: auth.Role = auth.Role.OTHER
        ) -> int:
    """
    Adds a new asset resource to the database.

    Only users with the "Manager" position are allowed to add assets.

    Args:
        user_position (str): The user's position (must be "Manager").
        resource (dict): Dictionary containing asset details.

    Returns:
        int: 200 if successful, 400 if failed, 401 if unauthorized.
    """
    logger.event("add_resource_asset called", level="trace")

    # Only Managers can add assets
    if not auth.can_write(user_position):
        logger.event(f"Position of Manager required but {user_position} provided", level="error")
        return 401

    insert_query = """
    INSERT INTO Asset (type_id, location_id, employee_id, notes, is_decommissioned)
    VALUES (:type_id, :location_id, :employee_id, :notes, :is_decommissioned);
    """

    params = {
        "type_id": resource.get("type_id"),
        "location_id": resource.get("location_id"),
        "employee_id": resource.get("employee_id"),
        "notes": resource.get("notes"),
        "is_decommissioned": resource.get("is_decommissioned")
    }

    logger.event(f"Running query {insert_query} with params: {params}", level="trace")
    result = database_connector.execute_query(insert_query, params)
    logger.event(f"result: {result}", level="warning")
    if result is None:
        logger.event("Item not added to Database", level="error")
        return 400

    logger.event("Item added to Database", level="info")

    new_asset_id_row = database_connector.execute_query("SELECT LAST_INSERT_ID() as new_id;")
    logger.event(f"New asset ID row: {new_asset_id_row}", level="trace")

    if not new_asset_id_row:
        logger.event("Error getting new asset ID", level="error")
        return 400

    new_asset_id = new_asset_id_row[0]['new_id']
    logger.event(f"New asset ID: {new_asset_id}", level="trace")

    update_result = update_resource_id(resource.get("type_id"), new_asset_id, user_position)
    logger.event(f"Update result: {update_result}", level="trace")

    if update_result is False:
        logger.event("Error updating resource ID", level="error")
        return 400
    logger.event("Successfully updated resource ID", level="info")
    return 200


def delete_resource(
        resource: int,
        user_position: auth.Role = auth.Role.OTHER
        ) -> int:
    """
    Marks an asset resource as decommissioned in the database.

    Only users with the "Manager" position are allowed to delete resources.

    Args:
        resource (int): The asset ID to decommission.
        user_position (Role): The user's role.

    Returns:
        int: 200 if successful, 400 if failed, 401 if unauthorized.
    """
    logger.event("delete_resource called", level="trace")

    if not auth.can_write(user_position):
        logger.event(f"Position of Manager required but {user_position} provided", level="error")
        return 401

    update_query = """
        UPDATE Asset
        SET is_decommissioned = 1,
            decommission_date = NOW()
        WHERE id = :asset_id;
        """

    params = {
        "asset_id": resource
    }

    logger.event(f"Running query {update_query} with params: {params}", level="trace")
    result = database_connector.execute_query(update_query, params)

    if result is not None:
        logger.event(f"Successfully deleted resource {resource}", level="info")
        return 200
    logger.event(f"Failed to delete resource {resource}", level="error")
    return 400


def update_resource(
        resource,
        user_position: auth.Role = auth.Role.OTHER
        ) -> int:
    """
    Updates an existing asset resource in the database.

    Only users with the "Manager" position are allowed to update assets.

    Args:
        resource (dict): Dictionary containing updated asset details.
        user_position (Role): The user's role.

    Returns:
        int: 200 if successful, 400 if failed, 401 if unauthorized.
    """
    logger.event("update_resource called", level="trace")

    if not auth.can_write(user_position):
        logger.event(f"Position of Manager required but {user_position} provided", level="error")
        return 401

    update_query = """
    UPDATE Asset
    SET type_id = :type_id,
        location_id = :location_id,
        employee_id = :employee_id,
        notes = :notes,
        is_decommissioned = :is_decommissioned
    WHERE id = :asset_id;
    """

    params = {
        "type_id": resource.get("type_id"),
        "location_id": resource.get("location_id"),
        "employee_id": resource.get("employee_id"),
        "notes": resource.get("notes"),
        "is_decommissioned": resource.get("is_decommissioned"),
        "asset_id": resource.get("asset_id")
    }

    logger.event(f"Running query {update_query} with params: {params}", level="trace")
    result = database_connector.execute_query(update_query, params)

    if result is not None:
        logger.event(f"Successfully updated resource {resource}", level="info")
        return 200
    logger.event(f"Failed to update resource {resource}", level="error")
    return 400


def get_resources(user_position=auth.Role.OTHER) -> tuple[int, list]:
    """
    Retrieves all asset resources from the database.
    Args:
        user_position (Role): The user's role.
    Returns:
        tuple: (status code, list of asset resources)
            - status code: 200 if successful, 400 if failed
            - list: List of asset resource dictionaries
    """
    logger.event("get_resources called", level="trace")

    logger.event(f"user_position: {user_position}", level="trace")
    if not auth.can_read(user_position):
        logger.event("Returning error 401: {user_position} does not have read access",
                     level="trace")
        return 401, []

    select_query = "SELECT * FROM Asset;"
    logger.event(f"Running query {select_query}", level="trace")
    results = database_connector.execute_query(select_query)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resources", level="info")
        return 200, results
    logger.event("Failed to retrieve resources", level="error")
    return 400, []


def get_resource_types(
        user_position: auth.Role = auth.Role.OTHER
        ) -> tuple[int, list]:
    """
    Retrieves all resource types from the database.
    Args:
        user_position (Role): The user's role.

    Returns:
        tuple: (status code, list of resource types)
            - status code: 200 if successful, 400 if failed
            - list: List of resource type dictionaries
    """
    logger.event("get_resource_types called", level="trace")

    if not auth.can_read(user_position):
        logger.event("Returning error 401: user does not have read access", level="trace")
        return 401

    select_query = "SELECT * FROM AssetTypes;"
    logger.event(f"Running query {select_query}", level="trace")
    results = database_connector.execute_query(select_query)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resource types", level="info")
        return 200, results

    logger.event("Failed to retrieve resource types", level="error")
    return 400, []


def get_resource_by_id(
        resource_id: int,
        user_position: auth.Role = auth.Role.OTHER
        ) -> tuple[int, dict]:
    """
    Retrieves a single asset resource by its ID.

    Args:
        resource_id (int): The asset ID to retrieve.
        user_position (Role): The user's role.

    Returns:
        tuple: (status code, resource dictionary)
            - status code: 200 if successful, 400 if failed
            - dict: Asset resource dictionary (empty if not found)
    """
    logger.event("get_resource_by_id called", level="trace")

    if not auth.can_read(user_position):
        logger.event("Returning error 401: user does not have read access", level="trace")
        return 401

    select_query = "SELECT * FROM Asset WHERE id = :asset_id;"
    params = {
        "asset_id": resource_id
    }
    logger.event(f"Running query {select_query} with params: {params}", level="trace")
    results = database_connector.execute_query(select_query, params)

    if results is not None and len(results) > 0:
        logger.event(f"Successfully retrieved {len(results)} resources", level="info")
        return 200, results[0]

    logger.event(f"Failed to retrieve resource by ID {resource_id}", level="error")
    return 400, {}


def get_resource_by_employee_id(
        employee_id: int,
        user_position: auth.Role = auth.Role.OTHER
        ) -> tuple[int, list]:
    """
    Retrieves all asset resources assigned to a specific employee.

    Args:
        employee_id (int): The employee's ID.
        user_position (Role): The user's role.

    Returns:
        tuple: (status code, list of resources)
            - status code: 200 if successful, 400 if failed
            - list: List of asset resource dictionaries
    """
    logger.event("get_resource_by_employee called", level="trace")

    logger.event(f"user_position: {user_position}", level="trace")
    if not auth.can_read(user_position):
        logger.event("Returning error 401: user does not have read access", level="trace")
        return 401

    select_query = "SELECT * FROM Asset WHERE employee_id = :employee_id;"
    params = {
        "employee_id": employee_id
    }

    logger.event(f"Running query {select_query} with params: {params}", level="trace")
    results = database_connector.execute_query(select_query, params)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resources", level="info")
        return 200, results
    logger.event(f"Failed to retrieve resources by employee ID {employee_id}", level="error")
    return 400, []


def get_resource_by_location_id(
        location_id: int,
        user_position: auth.Role = auth.Role.OTHER
        ) -> tuple[int, list]:
    """
    Retrieves all asset resources at a specific location.

    Args:
        location_id (int): The location's ID.
        user_position (Role): The user's role.

    Returns:
        tuple: (status code, list of resources)
            - status code: 200 if successful, 400 if failed
            - list: List of asset resource dictionaries
    """
    logger.event("get_resource_by_location_id called", level="trace")

    if not auth.can_read(user_position):
        logger.event("Returning error 401: user does not have read access", level="trace")
        return 401

    select_query = "SELECT * FROM Asset WHERE location_id = :location_id;"
    params = {
        "location_id": location_id
    }
    logger.event(f"Running query {select_query} with params: {params}", level="trace")
    results = database_connector.execute_query(select_query, params)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resources", level="info")
        return 200, results

    logger.event(f"Failed to retrieve resources by location ID {location_id}", level="error")
    return 400, []


def update_resource_id(
        type_id: int,
        new_asset_id: int,
        user_position: auth.Role = auth.Role.OTHER
        ) -> bool:
    """
    Updates the resource_id field for a given asset.

    The resource_id is generated based on the asset type, current year, and asset ID.

    Args:
        type_id (int): The asset type ID.
        new_asset_id (int): The new asset's ID.
        user_position (Role): The user's role.

    Returns:
        bool: True if successful, False otherwise.
    """
    logger.event("update_resource_id called", level="trace")

    if not auth.can_write(user_position):
        logger.event("Returning error 401: user does not have write access", level="trace")
        return 401

    type_query = """
    SELECT asset_type_name
    FROM AssetTypes
    WHERE id = :type_id;
    """
    params = {
        "type_id": type_id
    }
    logger.event(f"Running query {type_query} with params: {params}", level="trace")
    type_result = database_connector.execute_query(type_query, params)
    if not type_result:
        logger.event("Error getting asset type name", level="error")
        return False
    asset_type_name = type_result[0]['asset_type_name']
    current_year = datetime.datetime.now().year
    padded_id = str(new_asset_id).zfill(3)
    # Construct the final resource_id string
    resource_id_value = f"{asset_type_name}-{current_year}-{padded_id}"
    update_resource_id_query = """
    UPDATE Asset
    SET resource_id = :resource_id
    WHERE id = :asset_id;
    """
    update_params = {
        "resource_id": resource_id_value,
        "asset_id": new_asset_id
    }
    result = database_connector.execute_query(update_resource_id_query, update_params)
    if result is not None:
        logger.event(f"Successfully updated resource ID {new_asset_id}", level="info")
        return True
    logger.event(f"Failed to update resource ID {new_asset_id}", level="error")
    return False

def get_employees_basic(user_role: str, q: str | None = None, limit: int = 250):
    """
    Return basic employee info (id, first_name, last_name).
    """
    try:
        query = """
            SELECT id, first_name, last_name
            FROM Employee
        """
        params = {}

        if q:
            query += " WHERE LOWER(first_name) LIKE :q OR LOWER(last_name) LIKE :q"
            params["q"] = f"%{q.lower()}%"

        query += " ORDER BY last_name, first_name LIMIT :limit"
        params["limit"] = limit

        rows = database_connector.execute_query(query, params)
        return (200, rows)
    except Exception as e:
        # logger.event(f"DB error: {e}", level="error")
        return (400, {"error": "DB failure"})

