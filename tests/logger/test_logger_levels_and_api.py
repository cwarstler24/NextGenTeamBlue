import pytest
from src.logger import logger

pytestmark = pytest.mark.unit

def test_event_security_methods_exist():
    assert hasattr(logger, "event")
    assert hasattr(logger, "security")

def test_logger_emits_messages_with_levels(loguru_capture):
    logger.event("asset created", level="info")
    logger.security("policy violation", level="warning")

    msgs = [r.record["message"] for r in loguru_capture]
    lvls = [r.record["level"].name for r in loguru_capture]

    assert any("asset created" in m for m in msgs)
    assert any("policy violation" in m for m in msgs)
    # at least one WARNING from security
    assert "WARNING" in lvls or "ERROR" in lvls or "CRITICAL" in lvls
