import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
from fastapi import FastAPI, Request, HTTPException
from src.logger import logger # Logger() instance
from src.validate import validate_request
from src.authenticate import authenticate_request

# --- add near the top ---
import time
from fastapi.responses import JSONResponse
from fastapi import status

def connect_with_connector():
        connector = Connector()
        # Replace with your project ID, region, and instance name
        instance_connection_name = f"teamblue-asset-ms:us-central1:teamblue-asset-ms" 
        db_user = "teamblue"  # If using basic authentication
        db_password = "Lnx4you!" # If using basic authentication
        db_name = "teamblue-asset-ms"

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

app = FastAPI(
    title="Team Blue Inventory Listener",
    description="Listens for GET, POST, PUT, DELETE requests, validates tokens, and authorizes by role.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Listener active on localhost"}

@app.api_route("/listener", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_request(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Step 1: Validate token and request body
    validation_result = await validate_request(request, token)
    decoded_payload = validation_result["decoded_payload"]

    # Step 2: Authorize the request
    authorization_result = await authorize_request(request, decoded_payload)

    # Step 3: Return results
    return {
        "method": request.method,
        "path": str(request.url),
        "user": f"{decoded_payload.get('first_name', '')} {decoded_payload.get('last_name', '')}".strip(),
        "role": authorization_result["role"],
        "validation_result": validation_result,
        "authorization_result": authorization_result
    }

@app.get("/health")
def health():
    logger.event("health check called")
    return {"status": "ok"}

# Optional sample route that uses the engine (tests will mock it):
@app.get("/employees/count")
def employees_count():
    engine = connect_with_connector()
    with engine.connect() as conn:
        rows = conn.execute(sqlalchemy.text("SELECT 1")).fetchall()
    logger.security("employees_count accessed", level="info")
    return {"count": len(rows)}

# Optional indirection for easier testing/mocking
def get_engine():
    return connect_with_connector()

def _probe_db(engine_factory=get_engine):
    """Try a very small query; return (ok: bool, payload: dict)."""
    started = time.monotonic()
    try:
        engine = engine_factory()
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        latency_ms = (time.monotonic() - started) * 1000.0
        return True, {"db": {"status": "up", "latency_ms": round(latency_ms, 2)}}
    except Exception as exc:  # broad on purpose for readiness
        latency_ms = (time.monotonic() - started) * 1000.0
        # Security log for operational failures
        logger.security(f"readiness db check FAILED: {exc}", level="warning")
        return False, {"db": {"status": "down", "latency_ms": round(latency_ms, 2)}}

@app.get("/health/ready")
def health_ready():
    ok, db = _probe_db()
    payload = {"status": "ok" if ok else "error", **db}
    code = status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE
    # Event log is fine here (informational)
    logger.event(f"readiness probe result={payload['status']}", level="info")
    return JSONResponse(payload, status_code=code)

if __name__ == "__main__":
    engine = connect_with_connector()
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM Employee"))
        for row in result:
            print(row)