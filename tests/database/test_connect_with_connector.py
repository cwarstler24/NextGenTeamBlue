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
        calls["creator_result"] = creator()  # call the creator once
        return SimpleNamespace(kind="engine")

    # IMPORTANT: patch where the symbols are USED now
    import src.DatabaseController.engine as dbm

    monkeypatch.setattr(dbm, "Connector", lambda: FakeConnector())
    monkeypatch.setattr(dbm.sqlalchemy, "create_engine", fake_create_engine)

    engine = dbm.connect_with_connector()

    assert engine.kind == "engine"
    assert calls["url"] == "mysql+pymysql://"
    instance, driver, user, pwd, db, ip_type = calls["args"]
    assert driver == "pymysql"
    assert user and pwd and db
