# tests/database/test_database_connector_unit.py
from types import SimpleNamespace
import pytest
import sqlalchemy
import src.database.database_connector as dbm

pytestmark = pytest.mark.unit


# ---------- helpers (fakes) ----------
class FakeConnCtx:
    """
    Context-managed DB connection used by the Engine.connect().
    Mimics the minimal SQLAlchemy API surface we need.
    """

    def __init__(self, script):
        """
        script: list of dict instructions controlling behavior of successive executes.
        Each item may contain:
          - "returns_rows": bool
          - "rows": list[dict] (for SELECT)
          - "rowcount": int (for DML)
          - "raise": Exception to raise on execute
          - "on_commit_raise": Exception to raise on commit
        """
        self._script = list(script)
        self._executed = []
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._closed = True

    # SQLAlchemy 2.x Result emulation bits
    class _Result:
        def __init__(self, spec):
            self._spec = spec
            self.returns_rows = bool(spec.get("returns_rows", False))
            self.rowcount = spec.get("rowcount", 0)

        class _Row:
            def __init__(self, d):
                self._d = d
            def _asdict(self):
                return dict(self._d)

        def fetchall(self):
            return [self._Row(r) for r in self._spec.get("rows", [])]

    def execute(self, text_query, params):
        if not self._script:
            raise RuntimeError("FakeConnCtx script exhausted")
        spec = self._script.pop(0)
        self._executed.append((str(text_query), dict(params)))
        if "raise" in spec and spec["raise"]:
            raise spec["raise"]
        return self._Result(spec)

    def commit(self):
        # If instruction says commit should fail, raise
        if self._executed:
            last_spec = {}  # default no-op
        else:
            last_spec = {}
        # No special per-call commit behavior in this suite, but keep hook
        return

    def rollback(self):
        return


class FakeEngine:
    def __init__(self, ctx):
        self._ctx = ctx
        self.disposed = False

    def connect(self):
        return self._ctx

    def dispose(self):
        self.disposed = True


# ---------- tests ----------
def test_get_db_connection_idempotent(monkeypatch):
    calls = {}

    class FakeConnector:
        def connect(self, instance, driver, user, password, db, ip_type):
            calls["connect_args"] = (instance, driver, user, password, db, str(ip_type))
            return object()

    def fake_create_engine(url, creator, **kwargs):
        calls["url"] = url
        # verify creator returns a connection
        _ = creator()
        calls["pool_size"] = kwargs.get("pool_size")
        return SimpleNamespace(kind="engine-idem")

    # Patch ctor + create_engine + config constants (in case config.ini absent)
    monkeypatch.setattr(dbm, "Connector", lambda: FakeConnector())
    monkeypatch.setattr(dbm.sqlalchemy, "create_engine", fake_create_engine)
    monkeypatch.setattr(dbm, "INSTANCE_CONNECTION_NAME", "proj:region:inst")
    monkeypatch.setattr(dbm, "DB_USER", "u")
    monkeypatch.setattr(dbm, "DB_PASS", "p")
    monkeypatch.setattr(dbm, "DB_NAME", "d")

    # reset globals
    dbm.CONNECTOR = None
    dbm.POOL = None

    e1 = dbm.get_db_connection()
    e2 = dbm.get_db_connection()  # should reuse
    assert e1 is e2
    assert calls["url"] == "mysql+pymysql://"
    assert calls["pool_size"] == 5
    inst, drv, user, pwd, db, ipt = calls["connect_args"]
    assert drv == "pymysql" and user == "u" and pwd == "p" and db == "d"


def test_execute_query_select_returns_rows(monkeypatch):
    # engine that returns rows for the first (and only) execute
    ctx = FakeConnCtx([{"returns_rows": True, "rows": [{"id": 1}, {"id": 2}]}])
    engine = FakeEngine(ctx)

    monkeypatch.setattr(dbm, "POOL", engine)

    out = dbm.execute_query("SELECT * FROM T", {"x": 1})
    assert out == [{"id": 1}, {"id": 2}]


def test_execute_query_dml_returns_status(monkeypatch):
    ctx = FakeConnCtx([{"returns_rows": False, "rowcount": 3}])
    engine = FakeEngine(ctx)
    monkeypatch.setattr(dbm, "POOL", engine)

    out = dbm.execute_query("UPDATE T SET a=1", {"y": 2})
    assert out == {"status": "success", "rows_affected": 3}


def test_execute_query_initializes_pool_failure(monkeypatch):
    # If get_db_connection returns None, execute_query should return None
    monkeypatch.setattr(dbm, "POOL", None)
    monkeypatch.setattr(dbm, "get_db_connection", lambda: None)
    out = dbm.execute_query("SELECT 1")
    assert out is None


def test_execute_query_operational_error(monkeypatch):
    ctx = FakeConnCtx([{"raise": sqlalchemy.exc.OperationalError("stmt", {}, Exception("op"))}])
    engine = FakeEngine(ctx)
    monkeypatch.setattr(dbm, "POOL", engine)
    out = dbm.execute_query("SELECT 1")
    assert out is None


def test_execute_query_sqlalchemy_error_triggers_rollback(monkeypatch):
    class RollbackWatch(FakeConnCtx):
        def __init__(self, script):
            super().__init__(script)
            self.did_rollback = False
        def rollback(self):
            self.did_rollback = True

    ctx = RollbackWatch([{"raise": sqlalchemy.exc.SQLAlchemyError("boom")}])
    engine = FakeEngine(ctx)
    monkeypatch.setattr(dbm, "POOL", engine)

    out = dbm.execute_query("INSERT INTO X VALUES (1)")
    assert out is None
    assert ctx.did_rollback is True


def test_close_db_connection_disposes_and_closes(monkeypatch):
    # Attach fake globals & ensure cleanup flips flags and resets globals
    ctx = FakeConnCtx([])
    engine = FakeEngine(ctx)

    class ConnClose:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    conn_obj = ConnClose()

    dbm.POOL = engine
    dbm.CONNECTOR = conn_obj

    dbm.close_db_connection()
    assert engine.disposed is True
    assert conn_obj.closed is True
    assert dbm.POOL is None and dbm.CONNECTOR is None
