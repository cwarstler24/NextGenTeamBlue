import os
import sys
import configparser
from typing import Any
from loguru import logger as _logger
from cryptography.fernet import Fernet


encryption_key_path = os.path.join(os.path.dirname(__file__),
                                   "../../env/log_key")
if os.path.exists(encryption_key_path):
    with open(encryption_key_path, 'rb') as file:
        key = file.read()
    if len(key) != 44:
        key = Fernet.generate_key()
        with open(encryption_key_path, 'wb') as file:
            file.write(key)
else:
    key = Fernet.generate_key()
    touch_dir = os.path.dirname(encryption_key_path)
    if not os.path.exists(touch_dir):
        os.makedirs(touch_dir)
    with open(encryption_key_path, 'wb') as file:
        file.write(key)

cipher = Fernet(key)
# Encryption key for security logs (in production, use a secure key management)

config_file = configparser.ConfigParser()
config_file.read('./config.ini')
log_config = config_file['log']
event_log_config = config_file['event_log']
security_log_config = config_file['security_log']
log_path = os.path.join(os.path.dirname(__file__), log_config['log_path'])


def encrypt_message(message: str) -> bytes:
    encrypted = cipher.encrypt(message.encode())
    return encrypted


def encrypted_formatter(record):
    formatted = log_config['format'].format(**record)
    encrypted = cipher.encrypt(formatted.encode())
    return encrypted.decode() + '\n'


# Remove default stderr handler
_logger.remove()

retention = f"{log_config['retention_time']} {log_config['retention_unit']}"
rotation = f"{log_config['rotation_size']} {log_config['rotation_unit']}"

# Add security log
security_log_file = os.path.join(log_path, security_log_config['file'])
_logger.add(
        security_log_file,
        rotation=rotation,
        retention=retention,
        level=security_log_config['file_level'],
        format=encrypted_formatter,
        filter=lambda record, name="security": record["extra"]
        .get("type") == name
        )

# Add event log
event_log_file = os.path.join(log_path, event_log_config['file'])
_logger.add(
        event_log_file,
        level=event_log_config['file_level'],
        retention=retention,
        rotation=rotation,
        format=log_config['format'],
        filter=lambda record, name=event_log_config['name']: record["extra"]
        .get("type") == name
        )

# Configure separate console (stdout) logging levels for security and event
_logger.add(sys.stderr, level=event_log_config['console_level'],
            filter=lambda record: record["extra"].get("type") == "security",
            format=log_config['format'])
_logger.add(sys.stderr, level=security_log_config['console_level'],
            filter=lambda record: record["extra"].get("type") == "event",
            format=log_config['format'])


class Logger:
    """
    Logger class for the project.
    """

    def __init__(self):
        """
        Initializes the logger.
        """
        self._logger = _logger

    def security(self, message: str, level: str = "info",
                 *args: Any, **kwargs: Any) -> None:
        """
        Logs security-related messages to security.log at the specified level.
        Messages are encrypted for security.
        """
        getattr(self._logger.bind(type="security"), level)(message, *args,
                                                           **kwargs)

    def event(self, message: str, level: str = "info", *args: Any,
              **kwargs: Any) -> None:
        """
        Logs event-related messages to event.log at the specified level.
        """
        getattr(self._logger.bind(type="event"), level)(message,
                                                        *args, **kwargs)
