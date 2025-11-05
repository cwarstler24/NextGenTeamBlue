from types import SimpleNamespace
import pytest
import src.database.database_connector as dbm

pytestmark = pytest.mark.unit

def test_get_db_connection_uses_connector_and_creator(monkeypatch):
    # We patch inside the module under test (dbm) where symbols are USED.

    calls = {}

    class FakeConnector:
        def connect(self, instance, driver, user, password, db, ip_type):
            calls["connect_args"] = (instance, driver, user, password, db, str(ip_type))
            return object()

    def fake_create_engine(url, creator, **kwargs):
        calls["url"] = url
        # call the creator once to verify it's wired
        conn = creator()
        calls["creator_conn_type"] = type(conn).__name__
        # capture some pool kwargs for sanity
        calls["pool_size"] = kwargs.get("pool_size")
        return SimpleNamespace(kind="engine")

    # monkeypatch module globals that config may have set at import
    monkeypatch.setattr(dbm, "Connector", lambda: FakeConnector())
    monkeypatch.setattr(dbm.sqlalchemy, "create_engine", fake_create_engine)

    # also ensure config-derived constants are present (if config.ini is missing in CI)
    monkeypatch.setattr(dbm, "INSTANCE_CONNECTION_NAME", "proj:region:instance")
    monkeypatch.setattr(dbm, "DB_USER", "user")
    monkeypatch.setattr(dbm, "DB_PASS", "pass")
    monkeypatch.setattr(dbm, "DB_NAME", "db")

    engine = dbm.get_db_connection()
    assert engine.kind == "engine"
    assert calls["url"] == "mysql+pymysql://"
    inst, drv, user, pwd, db, ip_type = calls["connect_args"]
    assert drv == "pymysql" and user and pwd and db
    assert calls["pool_size"] == 5
