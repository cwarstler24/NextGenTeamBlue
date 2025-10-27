import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy

def connect_with_connector():
        connector = Connector()
        # Replace with your project ID, region, and instance name
        instance_connection_name = f"teamblue-asset-ms:us-central1:teamblue-asset-ms" 
        db_user = "teamblue"  # If using basic authentication
        db_password = "Lnx4you!" # If using basic authentication
        db_name = "teamblue-asset-ms"

        # Use IAM database authentication (recommended)
        engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=lambda: connector.connect(
                instance_connection_name,
                "pymysql",
                user=db_user, # Omit if using IAM database authentication
                password=db_password, # Omit if using IAM database authentication
                db=db_name,
                ip_type=IPTypes.PUBLIC, # Or IPTypes.PRIVATE if using private IP
            ),
        )
        return engine

if __name__ == "__main__":
    engine = connect_with_connector()
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM Employee"))
        for row in result:
            print(row)
