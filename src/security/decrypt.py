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