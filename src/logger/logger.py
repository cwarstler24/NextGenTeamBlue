"""
Logger module that provides a wrapper around the loguru logger.
Provides methods for logging security and event-related messages.
Configuration is read from config.ini.
"""
import os
import sys
import configparser
from typing import Any
from loguru import logger as _logger
from cryptography.fernet import Fernet

CIPHER = None
LOG_CONFIG = None


def encrypt_message(message: str) -> bytes:
    encrypted = CIPHER.encrypt(message.encode())
    return encrypted


def encrypted_formatter(record):
    formatted = LOG_CONFIG['format'].format(**record)
    encrypted = CIPHER.encrypt(formatted.encode())
    return encrypted.decode() + '\n'


def init_key():
    encryption_key_path = os.path.join(os.path.dirname(__file__),
                                       "../../env/log_key")

    # ensure directory exists before opening
    os.makedirs(os.path.dirname(encryption_key_path), exist_ok=True)

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

    global CIPHER
    CIPHER = Fernet(key)


def init_logger():
    """
    Initializes the logger.
    """
    init_key()

    config_file = configparser.ConfigParser()
    config_file.read('./config.ini')
    global LOG_CONFIG
    LOG_CONFIG = config_file['log']
    event_log_config = config_file['event_log']
    security_log_config = config_file['security_log']
    log_path = os.path.join(os.path.dirname(__file__), LOG_CONFIG['log_path'])

    # Remove default stderr handler
    _logger.remove()

    reten = f"{LOG_CONFIG['retention_time']} {LOG_CONFIG['retention_unit']}"
    rotation = f"{LOG_CONFIG['rotation_size']} {LOG_CONFIG['rotation_unit']}"

    # Add security log
    security_log_file = os.path.join(log_path, security_log_config['file'])
    _logger.add(
            security_log_file,
            rotation=rotation,
            retention=reten,
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
            retention=reten,
            rotation=rotation,
            format=LOG_CONFIG['format'],
            filter=lambda record,
            name=event_log_config['name']: record["extra"]
            .get("type") == name
            )

    # Configure separate console (stdout) logging levels for security and event
    _logger.add(sys.stderr, level=event_log_config['console_level'],
                filter=lambda record:
                record["extra"].get("type") == "security",
                format=LOG_CONFIG['format'])
    _logger.add(sys.stderr, level=security_log_config['console_level'],
                filter=lambda record: record["extra"].get("type") == "event",
                format=LOG_CONFIG['format'])


class Logger:
    """
    Logger class for the project.
    """

    def __init__(self):
        """
        Initializes the logger.
        """
        self._logger = _logger

    def security(self, message: str, *args: Any, level: str = "info",
                 **kwargs: Any) -> None:
        """
        Logs security-related messages to security.log at the specified level.
        Messages are encrypted for security.
        Args:
            message (str): The message to log.
            level (str, optional): The log level. Defaults to "info".
        """
        getattr(self._logger.bind(type="security").opt(depth=1), level)(
                message, *args, **kwargs)

    def event(self, message: str, *args: Any, level: str = "info",
              **kwargs: Any) -> None:
        """
        Logs event-related messages to event.log at the specified level.
        Args:
            message (str): The message to log.
            level (str, optional): The log level. Defaults to "info".
        """
        getattr(self._logger.bind(type="event").opt(depth=1), level)(
                message, *args, **kwargs)
