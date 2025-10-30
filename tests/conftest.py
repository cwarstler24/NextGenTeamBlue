# tests/conftest.py
import types
import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from src.main import app
import os, sys, pytest

# --- make src importable no matter where pytest runs ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)


# --- DB gating (off by default) ---
def pytest_addoption(parser):
    parser.addoption(
        "--with-db",
        action="store_true",
        default=False,
        help="Run tests marked with @pytest.mark.db (real database required).",
    )

def pytest_collection_modifyitems(config, items):
    if not config.getoption("--with-db"):
        skip_db = pytest.mark.skip(reason="skipped: enable with --with-db")
        for item in items:
            if "db" in item.keywords:
                item.add_marker(skip_db)

# --- logging to your wrapper: every test annotates logs ---
from src.logger import logger # <- your Logger() instance
from loguru import logger as _core # for capture when needed

@pytest.fixture(autouse=True)
def _log_test_start_end(request):
    nodeid = request.node.nodeid
    logger.event(f"TEST START :: {nodeid}", level="info")
    yield
    logger.event(f"TEST END   :: {nodeid}", level="info")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call":
        return
    nodeid = item.nodeid
    if rep.passed:
        logger.event(f"TEST PASS  :: {nodeid}", level="info")
    elif rep.failed:
        # keep message short to avoid noisy logs
        msg = str(rep.longrepr)[:500]
        logger.security(f"TEST FAIL  :: {nodeid} :: {msg}", level="error")
    elif rep.skipped:
        logger.event(f"TEST SKIP  :: {nodeid}", level="warning")

# Optional sink to assert on log content inside specific tests
@pytest.fixture
def loguru_capture():
    records = []
    sink_id = _core.add(lambda m: records.append(m), level="DEBUG")
    try:
        yield records
    finally:
        _core.remove(sink_id)

# A tiny in-memory sqlite engine used by integration tests
@pytest.fixture
def sqlite_engine():
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("SELECT 1"))  # warm up
    return engine


