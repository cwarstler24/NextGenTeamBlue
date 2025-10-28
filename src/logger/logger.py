import os
import sys
import shutil
import glob
import datetime
import configparser
from src.config import config as _config
from typing import Any
from loguru import logger as _logger
from cryptography.fernet import Fernet

# Encryption key for security logs (in production, use a secure key management)
key = Fernet.generate_key()
cipher = Fernet(key)

config_file = configparser.ConfigParser()
config_file.read('./config.ini')
log_config = config_file['log']
event_log_config = config_file['event_log']
security_log_config = config_file['security_log']
log_path = os.path.join(os.path.dirname(__file__), log_config['log_path'])


def security_sink(message):
    # message is the formatted log string

    security_log_backup_path = os.path.join(log_path, 'security')
    security_log_path = os.path.join(log_path, 'security.log')

    # Implement rotation: if file > 10 MB, rotate
    if os.path.exists(security_log_path):
        size = os.path.getsize(security_log_path)
        max_size = int(log_config['rotation_size']) * 1024 * 1024
        if size > max_size:
            # Rotate backups
            datetime_str = datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S")
            new = f"{security_log_backup_path}.{datetime_str}.log"
            shutil.move(security_log_path, new)

    # Implement retention: delete files older than 1 week
    now = datetime.datetime.now()
    retention_days = int(log_config['retention_time'])
    for logfile in glob.glob(f"{security_log_path}.*"):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(logfile))
        if (now - mtime).days > retention_days:
            os.remove(logfile)

    encrypted = cipher.encrypt(message.encode())
    with open(security_log_path, 'ab') as file:
        file.write(encrypted + b'\n')


# Remove default stderr handler
_logger.remove()

# Add security log
sink = security_sink
_logger.add(
        sink,
        level=security_log_config['file_level'],
        format=log_config['format'],
        filter=lambda record, name="security": record["extra"]
        .get("type") == name
        )

# Add event log
retention = f"{log_config['retention_time']} {log_config['retention_unit']}"
rotation = f"{log_config['rotation_size']} {log_config['rotation_unit']}"
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
