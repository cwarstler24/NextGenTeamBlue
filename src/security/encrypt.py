import os
from cryptography.fernet import Fernet
# from decrypt import decrypt_message

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message using the provided key.

    Args:
        message (str): The message to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted message.
    """
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())
    return encrypted

def init_key() -> bytes:
    """
    Initializes or retrieves the encryption key from a file.

    Returns:
        bytes: The encryption key.
    """
    encryption_key_path = os.path.join(os.path.dirname(__file__), "../../env/key")
    os.makedirs(os.path.dirname(encryption_key_path), exist_ok=True)

    key = None

    if os.path.exists(encryption_key_path):
        with open(encryption_key_path, 'rb') as file:
            key = file.read()
        try:
            Fernet(key)  # Validate the key
        except Exception:
            key = Fernet.generate_key()
            with open(encryption_key_path, 'wb') as file:
                file.write(key)
    else:
        key = Fernet.generate_key()
        with open(encryption_key_path, 'wb') as file:
            file.write(key)

    return key


# key = init_key()

# message = "hello"
# encrypted_message = encrypt_message(message, key)

# print(f"Encrypted message: {encrypted_message}")

# print(f"Decrypted message: {decrypt_message(encrypted_message, key)}")

# def init_key() -> bytes:
#     """
#     Initializes or retrieves the encryption key from a file.

#     Returns:
#         bytes: The encryption key.
#     """
#     encryption_key_path = os.path.join(os.path.dirname(__file__),
#                                        "../../env/key")

#     # ensure directory exists before opening
#     os.makedirs(os.path.dirname(encryption_key_path), exist_ok=True)

#     if os.path.exists(encryption_key_path):
#         with open(encryption_key_path, 'rb') as file:
#             key = file.read()
#         if len(key) != 44:
#             key = Fernet.generate_key()
#             with open(encryption_key_path, 'wb') as file:
#                 file.write(key)
#     else:
#         key = Fernet.generate_key()
#         touch_dir = os.path.dirname(encryption_key_path)
#         if not os.path.exists(touch_dir):
#             os.makedirs(touch_dir)
#         with open(encryption_key_path, 'wb') as file:
#             file.write(key)

#     return key