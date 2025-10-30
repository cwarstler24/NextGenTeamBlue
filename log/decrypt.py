"""
Decrypts the security log. Uses the key in the env folder that is created when
the project is first run. Will not decrypt if the log file is created on
another machine.
Throws FileNotFoundError if security.log is not found.
Throws FileNotFoundError if encryption key is not found.
"""
from cryptography.fernet import Fernet
import os
from rich import print as rich_print

encryption_key_path = os.path.join(os.path.dirname(__file__), "../env/log_key")
if os.path.exists(encryption_key_path):
    with open(encryption_key_path, 'rb') as file:
        key = file.read()
else:
    raise FileNotFoundError("Encryption key not found")

cipher = Fernet(key)

security_log_path = os.path.join(os.path.dirname(__file__), "security.log")
if not os.path.exists(security_log_path):
    raise FileNotFoundError("security.log not found")
with open(security_log_path, 'rb') as file:
    for line in file:
        encrypted = line.strip()
        if encrypted:
            decrypted = cipher.decrypt(encrypted)
            colored = decrypted.decode().replace('<', '[').replace('>', ']')
            rich_print(colored)
