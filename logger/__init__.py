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
from typing import Any
from loguru import logger as _logger
from cryptography.fernet import Fernet

# Encryption key for security logs (in production, use a secure key management)
key = Fernet.generate_key()
cipher = Fernet(key)

def security_sink(message):
    # message is the formatted log string
    encrypted = cipher.encrypt(message.encode())
    security_log_path = os.path.join(os.path.dirname(__file__), '..', 'security.log')
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
            filter=lambda record, name=log_config['name']: record["extra"].get("type") == name
        )
    else:
        _logger.add(
            log_config['file'],
            level=log_config['level'],
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
