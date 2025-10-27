# tests/unit/test_logger_api.py
import pytest
from logger import logger

pytestmark = pytest.mark.unit

def test_logger_methods_exist_and_accept_level(loguru_capture):
    logger.event("hello-event", level="info")
    logger.security("hello-sec", level="warning")
    # ensure messages hit loguru underneath (we look for substrings)
    joined = " ".join(r.record["message"] for r in loguru_capture)
    assert "hello-event" in joined
    assert "hello-sec" in joined
