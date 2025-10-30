

def get_all_employees():
    """
    Fetches all users from the database and prints them.
    """
    print("\n--- Fetching all employees ---")
    
    select_query = "SELECT * FROM Employee LIMIT 50;"
    results = database_connector.execute_query(select_query)
    
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
    results = database_connector.execute_query(select_query)
    
    if results is not None:
        if results:
            for row in results:
                print(row)
        else:
            print("  No assets found in the database.")



def decommission_asset(asset_id: int):
    """
    Marks an asset as decommissioned in the database.
    
    """
    print(f"\n--- Decommissioning asset ID: {asset_id} ---")
    
