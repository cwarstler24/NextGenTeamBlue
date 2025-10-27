import pytest
import src.main as m

pytestmark = pytest.mark.integration

def test_health_ready_db_down(client, monkeypatch, loguru_capture):
    class Boom(Exception):
        pass

    # make engine factory blow up
    monkeypatch.setattr(m, "get_engine", lambda: (_ for _ in ()).throw(Boom("no db")))

    r = client.get("/health/ready")
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "error"
    assert body["db"]["status"] == "down"

    # ensure a security log was written for the failure
    sec_msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("readiness db check FAILED" in msg for msg in sec_msgs)
