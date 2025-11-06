# """
# Decrypts the security log. Uses the key in the env folder that is created when
# the project is first run. Will not decrypt if the log file is created on
# another machine.
# Throws FileNotFoundError if security.log is not found.
# Throws FileNotFoundError if encryption key is not found.
# """
# import os
# from rich import print as rich_print
# from cryptography.fernet import Fernet, InvalidToken
# from src.security.encrypt import init_key

# # Initialize cipher using the stored key
# cipher = Fernet(init_key())

# # Locate the security log file
# security_log_path = os.path.join(os.path.dirname(__file__), "security.log")
# if not os.path.exists(security_log_path):
#     raise FileNotFoundError("security.log not found")

# # Read and decrypt each line
# with open(security_log_path, 'rb') as file:
#     for line in file:
#         encrypted = line.strip()
#         if encrypted:
#             try:
#                 decrypted = cipher.decrypt(encrypted)
#                 colored = decrypted.decode().replace('<', '[').replace('>', ']')
#                 rich_print(colored)
#             except InvalidToken:
#                 rich_print(f"[red]Invalid or corrupted entry:[/red] {encrypted}")

import os
from rich import print as rich_print
from cryptography.fernet import InvalidToken
from src.security.decrypt import decrypt_message
from src.security.encrypt import init_key

# Load the key
key = init_key()

# Path to the encrypted log file
log_path = os.path.join(os.path.dirname(__file__), "security.log")
if not os.path.exists(log_path):
    raise FileNotFoundError("security.log not found")

# Read and decrypt each line
with open(log_path, 'rb') as file:
    for line in file:
        encrypted = line.strip()
        if encrypted.startswith(b'gAAAAA'):  # Fernet tokens start with this
            try:
                decrypted = decrypt_message(encrypted, key)
                colored = decrypted.replace('<', '[').replace('>', ']')
                rich_print(colored)
            except InvalidToken:
                rich_print(f"[red]Invalid or corrupted entry:[/red] {encrypted}")
        else:
            rich_print(f"[yellow]Skipping non-encrypted line:[/yellow] {encrypted.decode(errors='ignore')}")
