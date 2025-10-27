import configparser
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

# Initialize the config parser
config = configparser.ConfigParser()
config.read('./config.ini')

# --- Load configuration ---
try:
    settings = config['mysql']
    INSTANCE_CONNECTION_NAME = settings['instance_connection_name']
    DB_USER = settings['db_user']
    DB_PASS = settings['db_password']
    DB_NAME = settings['db_name']
except KeyError:
    print("Error: 'config.ini' is missing or incomplete. Please check the file.")
    exit(1)

# --- Global variables for database connection ---
connector = None
pool = None

def get_db_connection():
    """
    Initializes and returns a database connection pool.
    This function is designed to be called once to set up the connection.
    """
    global connector, pool
    
    # Only initialize if the pool doesn't exist
    if pool:
        return pool

    print(f"Initializing connection pool for {INSTANCE_CONNECTION_NAME}...")

    # Initialize the Cloud SQL connector
    connector = Connector()

    try:
        # Function to create a new database connection
        def create_connection() -> sqlalchemy.engine.base.Connection:
            conn = connector.connect(
                INSTANCE_CONNECTION_NAME,
                "pymysql",
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
                ip_type=IPTypes.PUBLIC  # Use IPTypes.PRIVATE for private IP
            )
            return conn

        # Create a SQLAlchemy connection pool
        # This pool will manage connections for us, reusing them efficiently.
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=create_connection,
            pool_size=5,        # Number of connections to keep open in the pool
            max_overflow=2,     # Max connections to allow beyond pool_size
            pool_timeout=30,    # Seconds to wait before giving up on getting a connection
            pool_recycle=1800,  # Seconds to recycle connections (e.g., 30 min)
        )
        
        print("Connection pool initialized successfully.")
        return pool

    except Exception as e:
        print(f"Error initializing database connection: {e}")
        # Clean up the connector if initialization failed
        if connector:
            connector.close()
        return None

def execute_query(query: str, params: dict = None):
    """
    Executes a SQL query using a connection from the pool.
    
    :param query: The SQL query string to execute (e.g., "SELECT * FROM users WHERE id = :user_id")
    :param params: A dictionary of parameters to bind to the query (e.g., {"user_id": 1})
    :return: A list of result rows, or None if an error occurs.
    """
    global pool
    
    # Initialize the pool if it hasn't been already
    if not pool:
        pool = get_db_connection()
        if not pool:
            print("Failed to get database pool. Cannot execute query.")
            return None

    try:
        # Use the .connect() method on the engine to get a connection from the pool
        with pool.connect() as db_conn:
            # Prepare the query as a text object for SQLAlchemy
            text_query = sqlalchemy.text(query)
            
            # Execute the query
            result = db_conn.execute(text_query, params or {})
            
            # For SELECT statements, fetch all results
            if result.returns_rows:
                rows = result.fetchall()
                # 'fetchall()' returns a list of Row objects. We convert them to
                # standard dictionaries for easier use in main.py.
                # A Row object can be accessed by index (row[0]) or key (row['column_name'])
                # We'll convert to dicts using _asdict()
                print(f"Query executed successfully. Fetched {len(rows)} rows.")
                return [row._asdict() for row in rows]
            
            # For INSERT, UPDATE, DELETE, commit the transaction
            else:
                db_conn.commit()
                print(f"Query executed successfully. Rows affected: {result.rowcount}")
                return {"status": "success", "rows_affected": result.rowcount}

    except sqlalchemy.exc.OperationalError as e:
        print(f"Database connection error: {e}")
        # In a real app, you might want to retry or handle this
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        # Rollback in case of error during a transaction
        try:
            db_conn.rollback()
        except:
            pass # Ignore rollback error
            
    return None

def close_db_connection():
    """
    Cleans up the connector and disposes of the connection pool.
    Call this when your application is shutting down.
    """
    global connector, pool
    
    if pool:
        pool.dispose()
        pool = None
        print("Database connection pool disposed.")
        
    if connector:
        connector.close()
        connector = None
        print("Cloud SQL connector closed.")
