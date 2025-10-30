import datetime
import database.database_connector as database_connector
from typing import Optional

def AddResourceType(user_position: str, resource) -> int:
    """
    Adds a resource to the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to add
    Returns:
        int: the status code
    """
    #TODO: implement
    pass

def AddResourceAsset(user_position: str, resource) -> int:
    """
    Adds an asset resource to the database.
    Args:
        None
    Returns:
        int: the status code
    """

    # Only Managers can add assets
    if user_position == "Manager":        
        type_id = resource.get("type_id")
        location_id = resource.get("location_id")
        employee_id = resource.get("employee_id")
        notes = resource.get("notes")
        is_decommissioned = resource.get("is_decommissioned")
        
        insert_query = """
        INSERT INTO Asset (type_id, location_id, employee_id, notes, is_decommissioned)
        VALUES (:type_id, :location_id, :employee_id, :notes, :is_decommissioned);
        """
        
        params = {
            "type_id": type_id,
            "location_id": location_id,
            "employee_id": employee_id,
            "notes": notes,
            "is_decommissioned": is_decommissioned
        }

        # Execute the insert and typically get the new ID from the cursor object
        # NOTE: The implementation of `db.execute_query` is critical here.
        # It must support fetching the last inserted ID.
        insert_asset_initial = database_connector.execute_query(insert_query, params) 
        
        # For MySQL/Google Cloud SQL, we use LAST_INSERT_ID()
        # Execute a query to get the ID right after the insert
        new_asset_id_row = database_connector.execute_query("SELECT LAST_INSERT_ID() as new_id;")
        
        # Assuming the result is a list of rows, and we want the first column of the first row
        if not new_asset_id_row:
            return 400
            
        new_asset_id = new_asset_id_row[0]['new_id'] 

        # --- STEP 2: Fetch the Asset Type Name ---
        type_query = """
        SELECT asset_type_name
        FROM AssetTypes
        WHERE id = :type_id;
        """

        params = {
            "type_id": type_id
        }

        type_result = database_connector.execute_query(type_query, params)
        
        if not type_result:
            return 400
            
        # Get the asset_type_name (assuming it's the first column of the first row)
        asset_type_name = type_result[0]['asset_type_name']
        
        # --- STEP 3: Construct and Execute the UPDATE ---
        # We use Python to pre-calculate the date/year for simplicity and reliability.
        # We will assume 'date_added' in the database is the current year.
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

        # Note: You should commit the transaction here if your db.execute_query 
        # doesn't handle transactions automatically.
        # db.commit() 

        if result is not None:
            return 200
        else:
            return 400
    else: 
        return 401

def DeleteResource(user_position: str, resource: int) -> int:
    """
    Deletes the resource from the database.
    Args:
        user_position (str): the user's position
        resource (int): the resource to delete
    Returns:
        int: the status code
    """

    # Only Managers can delete assets
    if user_position == "Manager":
        update_query = """
        UPDATE Asset
        SET is_decommissioned = 1,
            decommission_date = NOW()
        WHERE id = :asset_id;
        """
    
        params = {
            "asset_id": resource
        }

        result = database_connector.execute_query(update_query, params)
        
        if result is not None:
            return 200
        else:
            return 400
        
    else: 
        return 401

def UpdateResource(user_position: str, resource) -> int:
    """
    Updates the resource in the database.
    Args:
        user_position (str): the user's position
        resource (dict): the resource to update
    Returns:
        int: the status code
    """

    #TODO: implement
    pass


def GetResources() -> tuple[int, list]:
    """
    Gets the resources from the database.
    Args:
        None

    Returns:
        int: the status code
        list: the resources
    """
    
    select_query = "SELECT * FROM Asset;"
    results = database_connector.execute_query(select_query)
    
    if results is not None:
        return 200, results
    else:
        return 400, []

def GetResourceTypes() -> tuple[int, list]:
    """
    Gets the resource types from the database.
    Args:
        None

    Returns:
        int: the status code
        list: the resource types
    """
    select_query = "SELECT * FROM AssetTypes;"
    results = database_connector.execute_query(select_query)
    
    if results is not None:
        return 200, results
    else:
        return 400, []
