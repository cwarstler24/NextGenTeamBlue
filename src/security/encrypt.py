"""
Encryption utilities for secure message handling.

This module provides functions to:
- Encrypt messages using Fernet symmetric encryption
- Initialize or retrieve a persistent encryption key stored in the `env/key` file

The key is generated once and reused across sessions. It is stored in a file
relative to the module path to ensure consistent access across environments.

Dependencies:
- cryptography.fernet for encryption
- os for file and path operations
"""

import os
from cryptography.fernet import Fernet

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the provided Fernet key.

    Args:
        message (str): The plaintext message to encrypt.
        key (bytes): A valid Fernet encryption key (44-byte base64-encoded).

    Returns:
        bytes: The encrypted message as a Fernet token.
    """
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())
    return encrypted

def init_key() -> bytes:
    """
    Initializes or retrieves the encryption key from a file.

    If the key file exists and contains a valid 44-byte Fernet key, it is returned.
    If the file is missing or invalid, a new key is generated and saved.

    Returns:
        bytes: A valid Fernet encryption key.
    
    Raises:
        ValueError: If the existing key file contains an invalid key length.
    """
    # Path to the key file relative to this module
    encryption_key_path = os.path.join(os.path.dirname(__file__), "../../env/key")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(encryption_key_path), exist_ok=True)

    key = None

    if os.path.exists(encryption_key_path):
        # Read the existing key
        with open(encryption_key_path, 'rb') as file:
            key = file.read()

        # Validate key length
        if len(key) != 44:
            key = Fernet.generate_key()
            with open(encryption_key_path, 'wb') as file:
                file.write(key)


        # Validate key format
        try:
            Fernet(key)
        except (ValueError, TypeError):
            # Regenerate key if invalid
            key = Fernet.generate_key()
            with open(encryption_key_path, 'wb') as file:
                file.write(key)
    else:
        # Generate and save a new key
        key = Fernet.generate_key()
        with open(encryption_key_path, 'wb') as file:
            file.write(key)

    return key
