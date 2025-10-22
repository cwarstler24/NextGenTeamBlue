"""
Logger package for the project.

This package configures loguru logger based on config.json.

Available logging methods:
- logger.security(message, level="info"): Logs security-related messages to security.log at the specified level. Messages are encrypted for security.
- logger.event(message, level="info"): Logs event-related messages to event.log at the specified level.

Supported levels (default is "info"): "trace" (most verbose), "debug", "info", "success", "warning", "error", "critical" (least verbose).

Usage: from logger import logger; logger.security("Security alert", level="warning"); logger.event("Event occurred")
"""

import json
import os
import sys
import shutil
import glob
import datetime
from typing import Any
from loguru import logger as _logger
from cryptography.fernet import Fernet

# Encryption key for security logs (in production, use a secure key management)
key = Fernet.generate_key()
cipher = Fernet(key)


def security_sink(message):
    # message is the formatted log string

    security_log_backup_path = os.path.join(os.path.dirname(__file__), '..', 'security')
    security_log_path = os.path.join(os.path.dirname(__file__), '..', 'security.log')

    # Implement rotation: if file > 10 MB, rotate
    if os.path.exists(security_log_path):
        size = os.path.getsize(security_log_path)
        #TODO: read from config
        max_size = int(config['security_rotation']) * 1024 * 1024
        if size > max_size: 
            # Rotate backups
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new = f"{security_log_backup_path}.{datetime_str}.log"
            shutil.move(security_log_path, new)

    # Implement retention: delete files older than 1 week
    now = datetime.datetime.now()
    retention_days = int(config['security_retention'])
    for logfile in glob.glob(f"{security_log_path}.*"):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(logfile))
        if (now - mtime).days > retention_days:
            os.remove(logfile)

    encrypted = cipher.encrypt(message.encode())
    with open(security_log_path, 'ab') as file:
        file.write(encrypted + b'\n')


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path) as f:
    config = json.load(f)

# Remove default stderr handler
_logger.remove()

for log_config in config.get('additional_logs', []):
    if log_config['name'] == 'security':
        sink = security_sink
        _logger.add(
            sink,
            level=log_config['level'],
            format=config['format'],
            filter=lambda record, name=log_config['name']: record["extra"]
            .get("type") == name
        )
    else:
        _logger.add(
            log_config['file'],
            level=log_config['level'],
            retention=config['retention'],
            rotation=config['rotation'],
            format=config['format'],
            filter=lambda record, name=log_config['name']: record["extra"].get("type") == name
        )

# Configure separate console (stdout) logging levels for security and event
console_levels = config.get('console_levels', {})
_logger.add(sys.stderr, level=console_levels.get('security', 'DEBUG'), filter=lambda record: record["extra"].get("type") == "security", format=config['format'])
_logger.add(sys.stderr, level=console_levels.get('event', 'DEBUG'), filter=lambda record: record["extra"].get("type") == "event", format=config['format'])

class Logger:
    def __init__(self):
        self._logger = _logger

    def security(self, message: str, level: str = "info", *args: Any, **kwargs: Any) -> None:
        getattr(self._logger.bind(type="security"), level)(message, *args, **kwargs)

    def event(self, message: str, level: str = "info", *args: Any, **kwargs: Any) -> None:
        getattr(self._logger.bind(type="event"), level)(message, *args, **kwargs)

logger = Logger()
