from types import SimpleNamespace
import builtins
import pytest

from src.security import sanitize as S


def test_sanitize_string_html_and_quotes(loguru_capture):
    # includes HTML + single quotes that should be escaped/doubled
    raw = "'<script>alert(1)</script>'"
    out = S.sanitize_data(raw)

    # bleach should HTML-escape tags
    assert "<script>" not in out and "</script>" not in out
    assert "&lt;script&gt;" in out

    # single quotes doubled for SQL safety
    assert "''" in out

    # confirm the security log mentions string sanitization
    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("String data sanitized successfully" in m for m in msgs)


def test_sanitize_dict_recursive(loguru_capture):
    raw = {
        "name": "<b>Bob</b>",
        "note": "it's fine",
        "nested": {"x": "<img onerror=1>", "y": "O'Reilly"},
    }
    out = S.sanitize_data(raw)

    # structure preserved (dict stays dict, nested dict stays dict)
    assert isinstance(out, dict)
    assert set(out.keys()) == {"name", "note", "nested"}
    assert isinstance(out["nested"], dict)

    # values are sanitized
    assert out["name"] == "Bob"  # <b>... removed by bleach.clean default
    assert "''" in out["note"]   # single quotes doubled

    # nested fields sanitized
    assert "onerror" not in out["nested"]["x"]
    assert "&lt;img" in out["nested"]["x"]
    assert "''" in out["nested"]["y"]

    # confirm logging hit dictionary branch
    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("Dictionary data sanitized successfully" in m for m in msgs)


def test_sanitize_list_recursive(loguru_capture):
    raw = ["<i>ok</i>", "O'Brien", {"k": "<script>bad()</script>"}]
    out = S.sanitize_data(raw)

    # list preserved, elements sanitized
    assert isinstance(out, list)
    assert out[0] == "ok"  # <i> removed
    assert out[1] == "O''Brien"
    assert isinstance(out[2], dict)
    assert "&lt;script&gt;" in out[2]["k"]

    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("List data sanitized successfully" in m for m in msgs)


@pytest.mark.parametrize("val", [123, 45.6, True, False, None])
def test_sanitize_primitive_passthrough(val, loguru_capture):
    out = S.sanitize_data(val)
    assert out is val  # returned as-is

    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("Non-string, non-collection data returned as is" in m for m in msgs)


def test_sanitize_error_fallback(monkeypatch, loguru_capture):
    # Force bleach.clean to raise to hit the except fallback path.
    def boom(_s):
        raise RuntimeError("boom")

    monkeypatch.setattr(S.bleach, "clean", boom, raising=True)

    raw = "O'Reilly <b>bold</b>"
    out = S.sanitize_data(raw)

    # On error, it returns str(input).replace("'", "''") without HTML cleaning
    assert out == "O''Reilly <b>bold</b>"

    msgs = [rec.record["message"] for rec in loguru_capture]
    assert any("Data sanitization failed:" in m for m in msgs)
