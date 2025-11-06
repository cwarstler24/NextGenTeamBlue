import unittest
from cryptography.fernet import Fernet, InvalidToken
from src.security.decrypt import decrypt_message  # adjust import path as needed

class TestDecryptMessage(unittest.TestCase):

    def setUp(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.message = "This is a secret"
        self.encrypted = self.cipher.encrypt(self.message.encode())

    def test_valid_decryption(self):
        decrypted = decrypt_message(self.encrypted, self.key)
        self.assertEqual(decrypted, self.message)

    def test_invalid_key(self):
        wrong_key = Fernet.generate_key()
        with self.assertRaises(InvalidToken):
            decrypt_message(self.encrypted, wrong_key)

    def test_corrupted_message(self):
        corrupted = self.encrypted[:-10] + b"1234567890"
        with self.assertRaises(InvalidToken):
            decrypt_message(corrupted, self.key)

    def test_empty_message(self):
        with self.assertRaises(InvalidToken):
            decrypt_message(b"", self.key)

if __name__ == "__main__":
    unittest.main()
