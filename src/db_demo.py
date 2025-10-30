import database.database_connector as database_connector  # Import our database module
import src.database.database_controller            
def main():
    """
    Main function to run the application logic.
    """
    print("Application starting...")
    
    # 1. Test the connection by getting the current time
    # print("\n--- Testing connection ---")
    # time_result = db.execute_query("SELECT NOW() as current_time")
    # if time_result:
    #     print(f"Database current time: {time_result[0]['current_time']}")
    
    # # 2. Set up the database (create table, insert data)
    # setup_database()
    
    # 3. Fetch all users
    # fetch_users()
    
    # 4. Find a specific user
    # find_user_by_name("Alice")
    # find_user_by_name("Charlie") # Example of a user not in the DB

    # 5. Fetch all employees
    # query.get_queries.get_all_employees()

    # 6. Fetch all assets
    # query.get_queries.get_all_assets()

    resource = {
        "type_id": 4,
        "location_id": None,
        "employee_id": 79,
        "notes": 'Python Test',
        "is_decommissioned": 1
    }
    results = DatabaseController.database_controller.AddResourceAsset("Manager", resource)

    # query.get_queries.get_all_asset_types()

    # query.get_queries.decommission_asset(asset_id=36)
    results = DatabaseController.database_controller.GetResources()

    print(results)
    
    # Clean up connections when the app is done
    database_connector.close_db_connection()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication shutting down...")
        database_connector.close_db_connection()
