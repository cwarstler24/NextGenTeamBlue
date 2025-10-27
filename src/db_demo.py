import db  # Import our database module
import time

def get_all_employees():
    """
    Fetches all users from the database and prints them.
    """
    print("\n--- Fetching all employees ---")
    
    select_query = "SELECT * FROM Employee;"
    results = db.execute_query(select_query)
    
    if results is not None:
        if results:
            for row in results:
                print(row)
        else:
            print("  No users found in the database.")
            
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
    get_all_employees()

    print("\nApplication finished.")
    
    # Clean up connections when the app is done
    db.close_db_connection()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication shutting down...")
        db.close_db_connection()
