"""
Database Connector Module

This module provides functions to initialize and manage a connection pool to a MySQL database
hosted on Google Cloud SQL using SQLAlchemy and the Cloud SQL Python Connector.

Features:
- Loads database configuration from a config.ini file.
- Initializes a SQLAlchemy connection pool with Google Cloud SQL Connector.
- Provides utility functions to execute SQL queries and clean up resources.

Configuration:
The config.ini file must contain a [mysql] section with the following keys:
    instance_connection_name
    db_user
    db_password
    db_name

Example usage:
    from database_connector import get_db_connection, execute_query, close_db_connection

    # Get a connection pool
    pool = get_db_connection()

    # Execute a query
    results = execute_query("SELECT * FROM users WHERE id = :user_id", {"user_id": 1})

    # Clean up resources
    close_db_connection()
"""

import sys
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
    sys.exit(1)

# --- Global variables for database connection ---
CONNECTOR = None  # Instance of google.cloud.sql.connector.Connector
POOL = None       # Instance of sqlalchemy.engine.Engine (connection pool)

def get_db_connection():
    """
    Initializes and returns a SQLAlchemy connection pool for the MySQL database.

    This function should be called once at application startup. It uses the Google Cloud SQL
    Connector to establish secure connections to the database instance.

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy connection pool engine, or None 
        if initialization fails.
    """
    global CONNECTOR, POOL

    # Only initialize if the pool doesn't exist
    if POOL:
        return POOL

    print(f"Initializing connection pool for {INSTANCE_CONNECTION_NAME}...")

    # Initialize the Cloud SQL connector
    CONNECTOR = Connector()

    try:
        # Function to create a new database connection
        def create_connection() -> sqlalchemy.engine.base.Connection:
            """
            Creates a new database connection using the Cloud SQL Connector.

            Returns:
                Connection object to the MySQL database.
            """
            conn = CONNECTOR.connect(
                INSTANCE_CONNECTION_NAME,
                "pymysql",
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME,
                ip_type=IPTypes.PUBLIC  # Use IPTypes.PRIVATE for private IP
            )
            return conn

        # Create a SQLAlchemy connection pool
        POOL = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=create_connection,
            pool_size=5,
            max_overflow=2,
            pool_timeout=15,
            pool_recycle=1800,
        )

        print("Connection pool initialized successfully.")
        return POOL

    except (sqlalchemy.exc.SQLAlchemyError, ValueError, ConnectionError) as e:
        print(f"Error initializing database connection: {e}")
        # Clean up the connector if initialization failed
        if CONNECTOR:
            CONNECTOR.close()
        return None

def execute_query(query: str, params: dict = None):
    """
    Executes a SQL query using a connection from the pool.

    Args:
        query (str): The SQL query string to execute (e.g., "SELECT * FROM users 
                                                            WHERE id = :user_id").
        params (dict, optional): Parameters to bind to the query (e.g., {"user_id": 1}).

    Returns:
        list[dict]: For SELECT queries, a list of result rows as dictionaries.
        dict: For INSERT/UPDATE/DELETE, a dict with status and rows_affected.
        None: If an error occurs.
    """
    global POOL

    # Initialize the pool if it hasn't been already
    if not POOL:
        POOL = get_db_connection()
        if not POOL:
            print("Failed to get database pool. Cannot execute query.")
            return None

    try:
        # Use the .connect() method on the engine to get a connection from the pool
        with POOL.connect() as db_conn:
            # Prepare the query as a text object for SQLAlchemy
            text_query = sqlalchemy.text(query)

            # Execute the query
            result = db_conn.execute(text_query, params or {})

            # For SELECT statements, fetch all results
            if result.returns_rows:
                rows = result.fetchall()
                print(f"Query executed successfully. Fetched {len(rows)} rows.")
                return [row._asdict() for row in rows]

            # For INSERT, UPDATE, DELETE, commit the transaction
            db_conn.commit()
            print(f"Query executed successfully. Rows affected: {result.rowcount}")
            return {"status": "success", "rows_affected": result.rowcount}

    except sqlalchemy.exc.OperationalError as e:
        print(f"Database connection error: {e}")
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"SQLAlchemy error occurred while executing the query: {e}")
        try:
            db_conn.rollback()
        except sqlalchemy.exc.SQLAlchemyError:
            pass  # Ignore rollback error specific to SQLAlchemy
    except (TypeError, ValueError, KeyError) as e:
        print(f"Parameter or data error while executing the query: {e}")
    return None

def close_db_connection():
    """
    Cleans up the connector and disposes of the connection pool.

    Call this function when your application is shutting down to release resources.
    """
    global CONNECTOR, POOL

    if POOL:
        POOL.dispose()
        POOL = None
        print("Database connection pool disposed.")

    if CONNECTOR:
        CONNECTOR.close()
        CONNECTOR = None
        print("Cloud SQL connector closed.")
