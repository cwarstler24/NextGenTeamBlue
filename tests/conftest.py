# tests/conftest.py
import types
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="function")
def client():
    return TestClient(app)

# Capture loguru records from your logger wrapper
from loguru import logger as core_loguru

@pytest.fixture
def loguru_capture():
    records = []
    sink_id = core_loguru.add(lambda m: records.append(m), level="DEBUG")
    try:
        yield records
    finally:
        core_loguru.remove(sink_id)

# A tiny in-memory sqlite engine used by integration tests
@pytest.fixture
def sqlite_engine():
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))  # warm up
    return engine
