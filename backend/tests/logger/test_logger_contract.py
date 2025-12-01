import pytest
from src.logger import logger

pytestmark = pytest.mark.unit

def test_event_and_security_emit(loguru_capture):
    logger.event("hello-event", level="info")
    logger.event("asset created", level="info")
    logger.security("policy violation", level="warning")
    msgs = [r.record["message"] for r in loguru_capture]
    assert any("hello-event" in m for m in msgs)
    assert any("asset created" in m for m in msgs)
    assert any("policy violation" in m for m in msgs)
