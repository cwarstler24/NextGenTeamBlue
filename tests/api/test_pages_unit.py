from io import StringIO
import pytest
from fastapi.responses import JSONResponse

import src.api.pages as P  # module under test

pytestmark = pytest.mark.unit


# ---------- helpers ----------
def _fake_open_with(content: str):
    def _fake_open(_path, _mode="r", _encoding=None):
        return StringIO(content)
    return _fake_open


# ---------- /index/ ----------
def test_index_page_ok(client, monkeypatch, loguru_capture):
    # make path resolution deterministic + provide fake file contents
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/fake/index.html", raising=True)
    monkeypatch.setattr(P, "open", _fake_open_with("<h1>Hello</h1>"), raising=True)

    r = client.get("/index/")
    assert r.status_code == 200
    assert "<h1>Hello</h1>" in r.text

    # sanity check some logs were written
    messages = [rec.record["message"] for rec in loguru_capture]
    assert any("GET /index" in m for m in messages)
    assert any("Returning index page" in m for m in messages)


def test_index_page_missing_404(client, monkeypatch, loguru_capture):
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/missing/index.html", raising=True)
    def _boom(*_a, **_k):  # open() raises FileNotFoundError
        raise FileNotFoundError("nope")
    monkeypatch.setattr(P, "open", _boom, raising=True)

    r = client.get("/index/")
    assert r.status_code == 404
    assert r.json()["detail"] == "File not found"

    messages = [rec.record["message"] for rec in loguru_capture]
    assert any("File not found" in m for m in messages)


def test_index_page_other_error_500(client, monkeypatch, loguru_capture):
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/error/index.html", raising=True)
    def _boom(*_a, **_k):
        raise RuntimeError("boom")
    monkeypatch.setattr(P, "open", _boom, raising=True)

    r = client.get("/index/")
    assert r.status_code == 500
    assert r.json()["detail"] == "Error getting request"

    messages = [rec.record["message"] for rec in loguru_capture]
    assert any("Error getting request" in m for m in messages)


# ---------- /index_test/ ----------
def test_index_test_page_ok(client, monkeypatch, loguru_capture):
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/fake/index_test.html", raising=True)
    monkeypatch.setattr(P, "open", _fake_open_with("<p>ok test</p>"), raising=True)

    r = client.get("/index_test/")
    assert r.status_code == 200
    assert "<p>ok test</p>" in r.text

    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("GET /index_test" in m for m in msgs)
    assert any("Returning index test page" in m for m in msgs)


def test_index_test_page_missing_404(client, monkeypatch):
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/missing/index_test.html", raising=True)
    def _boom(*_a, **_k):  # open() raises FileNotFoundError
        raise FileNotFoundError("nope")
    monkeypatch.setattr(P, "open", _boom, raising=True)

    r = client.get("/index_test/")
    assert r.status_code == 404
    assert r.json()["detail"] == "File not found"


def test_index_test_page_other_error_500(client, monkeypatch):
    monkeypatch.setattr(P.os_path, "join", lambda *a,
                         **k: "/tmp/error/index_test.html", raising=True)
    def _boom(*_a, **_k):  # other error
        raise ValueError("bad")
    monkeypatch.setattr(P, "open", _boom, raising=True)

    r = client.get("/index_test/")
    assert r.status_code == 500
    assert r.json()["detail"] == "Error getting request"


# ---------- image routes ----------
def test_logo_ok_uses_fileresponse(client, monkeypatch):
    # make exists() return True and stub FileResponse so we don't need a real file
    monkeypatch.setattr(P.os_path, "exists", lambda p: True, raising=True)
    monkeypatch.setattr(
        P, "FileResponse", lambda p: JSONResponse({"ok": True, "path": p}), raising=True
    )

    r = client.get("/Documentation/Logos/SwaB_Logo.png")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["path"].endswith("SwaB_Logo.png")


def test_logo_missing_404(client, monkeypatch):
    monkeypatch.setattr(P.os_path, "exists", lambda p: False, raising=True)
    r = client.get("/Documentation/Logos/SwaB_Logo.png")
    assert r.status_code == 404
    assert r.json()["detail"] == "Image not found"


def test_action_hero_logo_ok(client, monkeypatch):
    monkeypatch.setattr(P.os_path, "exists", lambda p: True, raising=True)
    monkeypatch.setattr(
        P, "FileResponse", lambda p: JSONResponse({"ok": True, "path": p}), raising=True
    )
    r = client.get("/Documentation/Logos/Action_Hero_Cotton_Swab.png")
    assert r.status_code == 200
    assert r.json()["path"].endswith("Action_Hero_Cotton_Swab.png")


def test_action_hero_logo_missing_404(client, monkeypatch):
    monkeypatch.setattr(P.os_path, "exists", lambda p: False, raising=True)
    r = client.get("/Documentation/Logos/Action_Hero_Cotton_Swab.png")
    assert r.status_code == 404
    assert r.json()["detail"] == "Image not found"


# ---------- redirects ----------
def test_redirect_index_test_html(client):
    r = client.get("/index_test.html/", allow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "/index_test/"


def test_redirect_index_html(client):
    r = client.get("/index.html/", allow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "/index/"
