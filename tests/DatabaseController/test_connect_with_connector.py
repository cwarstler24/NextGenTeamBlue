import pytest
from types import SimpleNamespace

pytestmark = pytest.mark.unit

def test_connect_with_connector_uses_creator(monkeypatch):
    calls = {}

    class FakeConnector:
        def connect(self, instance, driver, user, password, db, ip_type):
            calls["args"] = (instance, driver, user, password, db, str(ip_type))
            return object()

    def fake_create_engine(url, creator):
        calls["url"] = url
        calls["creator_result"] = creator()
        return SimpleNamespace(kind="engine")

    import src.main as m
    monkeypatch.setattr(m, "Connector", lambda: FakeConnector())
    monkeypatch.setattr(m.sqlalchemy, "create_engine", fake_create_engine)

    engine = m.connect_with_connector()
    assert engine.kind == "engine"
    assert calls["url"] == "mysql+pymysql://"
    _, drv, user, pwd, db, _ = calls["args"]
    assert drv == "pymysql" and user and pwd and db
