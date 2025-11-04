from __future__ import annotations
import time
import sqlalchemy
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.logger import logger
# dependency you can monkeypatch in tests
from src.database.database_connector import get_db_connection  

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    logger.event("health check called", level="info")
    return {"status": "ok"}

def _probe_db(engine_factory=None):
    if engine_factory is None:
        engine_factory = get_db_connection
    started = time.monotonic()
    try:
        engine = engine_factory()
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        latency_ms = (time.monotonic() - started) * 1000.0
        return True, {"db": {"status": "up", "latency_ms": round(latency_ms, 2)}}
    except Exception as exc:
        latency_ms = (time.monotonic() - started) * 1000.0
        logger.security(f"readiness db check FAILED: {exc}", level="warning")
        return False, {"db": {"status": "down", "latency_ms": round(latency_ms, 2)}}

@router.get("/health/ready")
def health_ready():
    ok, db = _probe_db()
    payload = {"status": "ok" if ok else "error", **db}
    code = status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE
    logger.event(f"readiness probe result={payload['status']}", level="info")
    return JSONResponse(payload, status_code=code)
