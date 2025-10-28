import datetime
import db
from typing import Optional

def get_all_employees():
    """
    Fetches all users from the database and prints them.
    """
    print("\n--- Fetching all employees ---")
    
    select_query = "SELECT * FROM Employee LIMIT 50;"
    results = db.execute_query(select_query)
    
    if results is not None:
        if results:
            for row in results:
                print(row)
        else:
            print("  No users found in the database.")

def get_all_assets():
    """
    Fetches all assets from the database and prints them.
    """
    print("\n--- Fetching all assets ---")
    
    select_query = "SELECT * FROM Asset LIMIT 50;"
    results = db.execute_query(select_query)
    
    if results is not None:
        if results:
            for row in results:
                print(row)
        else:
            print("  No assets found in the database.")

def insert_new_asset(type_id: int, location_id: Optional[int], employee_id: Optional[int], notes: Optional[str], is_decommissioned: int):
    """
    Inserts a new asset into the database.
    
    :param type_id: The type ID of the asset.
    :param location_id: The location ID of the asset (optional).
    :param employee_id: The employee ID associated with the asset (optional).
    :param notes: Additional notes about the asset (optional).
    :param is_decommissioned: Flag indicating if the asset is decommissioned (0
    """
    print("\n--- Inserting new asset ---")
    
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
    insert_asset_initial = db.execute_query(insert_query, params) 
    
    # For MySQL/Google Cloud SQL, we use LAST_INSERT_ID()
    # Execute a query to get the ID right after the insert
    new_asset_id_row = db.execute_query("SELECT LAST_INSERT_ID() as new_id;")
    
    # Assuming the result is a list of rows, and we want the first column of the first row
    if not new_asset_id_row:
        print("ERROR: Failed to retrieve last inserted ID.")
        return None
        
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

    type_result = db.execute_query(type_query, params)
    
    if not type_result:
        print(f"ERROR: AssetType with ID {type_id} not found.")
        return None
        
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

    db.execute_query(update_resource_id_query, update_params)

    # Note: You should commit the transaction here if your db.execute_query 
    # doesn't handle transactions automatically.
    # db.commit() 

    print(f"Inserted new asset successfully. Assigned ID: {new_asset_id}, Resource ID: {resource_id_value}")
    
    return new_asset_id