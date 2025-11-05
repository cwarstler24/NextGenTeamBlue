import unittest
import os
import shutil
from cryptography.fernet import Fernet
from src.security.encrypt import encrypt_message, init_key

class TestEncryptModule(unittest.TestCase):

    def setUp(self):
        # Create a temporary env directory for testing
        self.env_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../env"))
        self.key_path = os.path.join(self.env_dir, "key")
        if os.path.exists(self.env_dir):
            shutil.rmtree(self.env_dir)
        os.makedirs(self.env_dir, exist_ok=True)

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(self.env_dir):
            shutil.rmtree(self.env_dir)

    def test_key_initialization_creates_file(self):
        key = init_key()
        self.assertTrue(os.path.exists(self.key_path))
        self.assertEqual(len(key), 44)

    def test_key_initialization_returns_same_key(self):
        key1 = init_key()
        key2 = init_key()
        self.assertEqual(key1, key2)

    def test_encrypt_and_decrypt_round_trip(self):
        key = init_key()
        message = "Encrypt this!"
        encrypted = encrypt_message(message, key)
        decrypted = Fernet(key).decrypt(encrypted).decode()
        self.assertEqual(decrypted, message)

    def test_invalid_key_triggers_regeneration(self):
        # Write an invalid key to the file
        with open(self.key_path, 'wb') as file:
            file.write(b"invalid-key-data")
        key = init_key()
        self.assertEqual(len(key), 44)
        self.assertNotEqual(key, b"invalid-key-data")

    def test_encrypt_with_invalid_key_raises(self):
        with self.assertRaises(ValueError):
            encrypt_message("test", b"short")

if __name__ == "__main__":
    unittest.main()
