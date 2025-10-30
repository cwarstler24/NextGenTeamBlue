from __future__ import annotations
import os
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes  # type: ignore

# Read secrets from env (fall back to your current constants if needed)
DB_INSTANCE = os.getenv("DB_INSTANCE", "teamblue-asset-ms:us-central1:teamblue-asset-ms")
DB_USER     = os.getenv("DB_USER", "teamblue")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Lnx4you!")
DB_NAME     = os.getenv("DB_NAME", "teamblue-asset-ms")
DB_IP_TYPE  = os.getenv("DB_IP_TYPE", "PUBLIC").upper()

def connect_with_connector():
    connector = Connector()
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=lambda: connector.connect(
            DB_INSTANCE,
            "pymysql",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            ip_type=getattr(IPTypes, DB_IP_TYPE, IPTypes.PUBLIC),
        ),
    )
    return engine

def get_engine():
    """Indirection so tests can monkeypatch/override easily."""
    return connect_with_connector()
