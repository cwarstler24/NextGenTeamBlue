import db  # Import our database module
import query.get_queries
            
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

    query.get_queries.insert_new_asset(type_id=1, location_id=1, employee_id=None, notes='Python Test', is_decommissioned=0)

    query.get_queries.get_all_assets()

    print("\nApplication finished.")
    
    # Clean up connections when the app is done
    db.close_db_connection()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication shutting down...")
        db.close_db_connection()
