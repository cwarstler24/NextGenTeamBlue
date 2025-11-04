# tests/conftest.py
import os
import sys
import pytest

# --- FastAPI test client ---
from starlette.testclient import TestClient
# --- auto-logging every test via your wrapper ---
from loguru import logger as _core
from src.main import app
from src.logger import logger  # safe now

# --- make src importable ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# --- PREP LOGGER: ensure env/log_key path exists BEFORE importing src.main ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_DIR = os.path.join(PROJECT_ROOT, "env")
LOG_KEY_PATH = os.path.join(ENV_DIR, "log_key")

os.makedirs(ENV_DIR, exist_ok=True)
# Write a dummy key only if absent; keep deterministic for CI
if not os.path.exists(LOG_KEY_PATH):
    with open(LOG_KEY_PATH, "wb") as f:
        f.write(b"dummy-test-key-32bytes____dummy-test-key")  # 40 bytes is fine; your logger just needs a file

# (Optional) if your logger reads an env var for key path, set it here:
# os.environ["LOG_KEY_PATH"] = LOG_KEY_PATH

# --- DB gating (keep) ---
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
        msg = str(rep.longrepr)[:500]
        logger.security(f"TEST FAIL  :: {nodeid} :: {msg}", level="error")
    elif rep.skipped:
        logger.event(f"TEST SKIP  :: {nodeid}", level="warning")

@pytest.fixture
def loguru_capture():
    records = []
    sink_id = _core.add(lambda m: records.append(m), level="DEBUG")
    try:
        yield records
    finally:
        _core.remove(sink_id)

@pytest.fixture
def client():
    """Starlette TestClient bound to our FastAPI app."""
    return TestClient(app)

@pytest.fixture
def anyio_backend():
    return "asyncio"

# --- finally import app (after logger prep) ---
from src.main import app
