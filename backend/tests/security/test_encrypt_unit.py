import os
import pytest
from cryptography.fernet import Fernet
from src.security import encrypt as E

pytestmark = pytest.mark.unit


def _redirect_key_path(tmp_path, monkeypatch):
    """
    Make E.init_key() write to <tmp>/env/key by intercepting ONLY the join
    that uses '../../env/key'. This avoids patching dirname/exists, which
    can cause recursive calls elsewhere.
    """
    target = tmp_path / "env" / "key"

    real_join = E.os.path.join  # keep original

    def join_guard(a, b, *rest):
        # The code under test does: os.path.join(os.path.dirname(__file__), "../../env/key")
        if b == "../../env/key":
            return str(target)
        return real_join(a, b, *rest)

    monkeypatch.setattr(E.os.path, "join", join_guard, raising=True)
    return target


def test_key_initialization_creates_file(tmp_path, monkeypatch):
    key_path = _redirect_key_path(tmp_path, monkeypatch)
    key = E.init_key()
    assert key_path.exists()
    assert len(key) == 44  # Fernet key size


def test_key_initialization_returns_same_key(tmp_path, monkeypatch):
    _redirect_key_path(tmp_path, monkeypatch)
    k1 = E.init_key()
    k2 = E.init_key()
    assert k1 == k2


def test_encrypt_and_decrypt_round_trip(tmp_path, monkeypatch):
    _redirect_key_path(tmp_path, monkeypatch)
    key = E.init_key()
    msg = "Encrypt this!"
    token = E.encrypt_message(msg, key)
    out = Fernet(key).decrypt(token).decode()
    assert out == msg


def test_invalid_existing_key_triggers_regeneration(tmp_path, monkeypatch):
    key_path = _redirect_key_path(tmp_path, monkeypatch)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_bytes(b"invalid-key-data")  # bad size/format

    new_key = E.init_key()
    assert len(new_key) == 44
    assert key_path.read_bytes() == new_key  # file overwritten


def test_encrypt_with_invalid_key_raises(tmp_path, monkeypatch):
    _redirect_key_path(tmp_path, monkeypatch)
    with pytest.raises(ValueError):
        E.encrypt_message("test", b"short")
