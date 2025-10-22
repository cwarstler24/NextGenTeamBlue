import configparser
import mysql.connector

def get_db_config(filename='config.ini', section='mysql'):
    """
    Reads database configuration from an INI file.
    """
    parser = configparser.ConfigParser()
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_config

if __name__ == "__main__":
    try:
        config = get_db_config()
        print("Database Configuration:", config)

        # Connect to MySQL using the retrieved configuration
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Example: Execute a query
        cursor.execute("SELECT * from Employee")
        db_version = cursor.fetchall()
        print(db_version)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")