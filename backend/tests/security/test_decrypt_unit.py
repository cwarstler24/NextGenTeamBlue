import pytest
from cryptography.fernet import Fernet, InvalidToken
from src.security import decrypt as D

pytestmark = pytest.mark.unit


def test_valid_decryption():
    key = Fernet.generate_key()
    cipher = Fernet(key)
    msg = "This is a secret"
    token = cipher.encrypt(msg.encode())

    out = D.decrypt_message(token, key)
    assert out == msg


def test_invalid_key_raises_invalidtoken():
    key = Fernet.generate_key()
    wrong = Fernet.generate_key()
    token = Fernet(key).encrypt(b"msg")

    with pytest.raises(InvalidToken):
        D.decrypt_message(token, wrong)


def test_corrupted_message_raises_invalidtoken():
    key = Fernet.generate_key()
    token = Fernet(key).encrypt(b"hello world")
    corrupted = token[:-10] + b"0123456789"

    with pytest.raises(InvalidToken):
        D.decrypt_message(corrupted, key)


def test_empty_message_raises_invalidtoken():
    key = Fernet.generate_key()
    with pytest.raises(InvalidToken):
        D.decrypt_message(b"", key)
