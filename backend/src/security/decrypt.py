"""
decrypt.py

This module provides functionality to securely decrypt messages using symmetric encryption.
It uses the Fernet class from the cryptography library, which ensures message integrity
and confidentiality.

Dependencies:
    from cryptography.fernet import Fernet

Function:
    decrypt_message(encrypted_message: bytes, key: bytes) -> str
        Decrypts a message that was encrypted using the Fernet symmetric encryption scheme.

        Args:
            encrypted_message (bytes): The encrypted message in byte format.
            key (bytes): The secret key used for decryption. Must be a valid Fernet key.

        Returns:
            str: The original plaintext message after successful decryption.

        Raises:
            cryptography.fernet.InvalidToken: If the decryption fails due to an invalid key
            or corrupted message.
"""

from cryptography.fernet import Fernet


def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypts an encrypted message using the provided key.

    Args:
        encrypted_message (bytes): The encrypted message to decrypt.
        key (bytes): The decryption key.

    Returns:
        str: The decrypted message.
    """
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_message).decode()
    return decrypted
