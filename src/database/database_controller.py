"""
Sample Docstring
"""

import datetime
from src.database import database_connector
from src.logger import logger

def add_resource_type(user_position: str, resource) -> int:
    """
    Adds a resource to the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to add
    Returns:
        int: the status code
    """
    logger.event("add_resource_type called", level="trace")

    # Only Managers can add resource types
    if user_position == "Manager":
        logger.event("User is Manager", level="trace")
        asset_type_name = resource.get("asset_type_name")

        update_query = """
        INSERT INTO AssetTypes (asset_type_name)
        VALUES (:asset_type_name); 
        """

        params = {
            "asset_type_name": asset_type_name
        }

        logger.event(f"Running query {update_query} with params: {params}"
                     , level="trace")
        result = database_connector.execute_query(update_query, params)

        if result is not None:
            logger.event(f"Successfully added resource type {asset_type_name}",
                         level="info")
            return 200
        logger.event(f"Failed to add resource type {asset_type_name}",
                     level="error")
        return 400
    logger.event("User is not Manager", level="info")
    return 401

def add_resource_asset(user_position: str, resource) -> int:
    """
    Adds an asset resource to the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to add
    Returns:
        int: the status code
    """
    logger.event("add_resource_asset called", level="trace")

    # Only Managers can add assets
    if user_position != "Manager":
        logger.event(f"Postion of Manager required but {user_position} provided",
                     level="error")
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

    update_result = update_resource_id(resource.get("type_id"), new_asset_id)
    logger.event(f"Update result: {update_result}", level="trace")

    if update_result is False:
        logger.event("Error updating resource ID", level="error")
        return 400
    else:
        logger.event("Successfully updated resource ID", level="info")
        return 200

def delete_resource(user_position: str, resource: int) -> int:
    """
    Deletes the resource from the database.
    Args:
        user_position (str): the user's position
        resource (int): the resource to delete
    Returns:
        int: the status code
    """
    logger.event("delete_resource called", level="trace")

    if user_position != "Manager":
        logger.event(f"Postion of Manager required but {user_position} provided",
                     level="error")
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


def update_resource(user_position: str, resource) -> int:
    """
    Updates the resource in the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to update
    Returns:
        int: the status code
    """
    logger.event("update_resource called", level="trace")

    if user_position != "Manager":
        logger.event(f"Postion of Manager required but {user_position} provided",
                     level="error")
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

def get_resources() -> tuple[int, list]:
    """
    Gets the resources from the database.
    Args:
        None
    Returns:
        int: the status code
        list: the resources
    """
    logger.event("get_resources called", level="trace")

    select_query = "SELECT * FROM Asset;"
    logger.event(f"Running query {select_query}", level="trace")
    results = database_connector.execute_query(select_query)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resources", level="info")
        return 200, results
    logger.event("Failed to retrieve resources", level="error")
    return 400, []

def get_resource_types() -> tuple[int, list]:
    """
    Gets the resource types from the database.
    Args:
        None
    Returns:
        int: the status code
        list: the resource types
    """
    logger.event("get_resource_types called", level="trace")

    select_query = "SELECT * FROM AssetTypes;"
    logger.event(f"Running query {select_query}", level="trace")
    results = database_connector.execute_query(select_query)

    if results is not None:
        logger.event(f"Successfully retrieved {len(results)} resource types", level="info")
        return 200, results

    logger.event(f"Failed to retrieve resource types", level="error")
    return 400, []

def get_resource_by_id(resource_id: int) -> tuple[int, dict]:
    """
    Gets the resource by ID from the database.
    Args:
        resource_id (int): the resource ID
    Returns:
        int: the status code
        dict: the resource
    """
    logger.event("get_resource_by_id called", level="trace")

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

def get_resource_by_employee_id(employee_id: int) -> tuple[int, list]:
    """
    Gets the resources by employee ID from the database.
    Args:
        employee_id (int): the employee ID
    Returns:
        int: the status code
        list: the resources
    """
    logger.event("get_resource_by_employee called", level="trace")

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

def get_resource_by_location_id(location_id: int) -> tuple[int, list]:
    """
    Gets the resources by location ID from the database.
    Args:
        location_id (int): the location ID
    Returns:
        int: the status code
        list: the resources
    """
    logger.event("get_resource_by_location_id called", level="trace")

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

def update_resource_id(type_id: int, new_asset_id: int) -> bool:
    logger.event("update_resource_id called", level="trace")

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
        return 400
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
        logger.event(f"Successfully updated resource ID {new_asset_id}",
                        level="info")
        return True
    else:
        logger.event(f"Failed to update resource ID {new_asset_id}",
                        level="error")
    return False
