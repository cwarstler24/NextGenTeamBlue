"""
Logger package for the project.

This package configures loguru logger based on config.json.

Available logging methods:
- logger.trace(): Very detailed, low-level debugging.
- logger.debug(): Debugging information.
- logger.info(): General informational messages.
- logger.success(): Successful operations.
- logger.warning(): Warnings that don't stop execution.
- logger.error(): Errors that occur but don't crash the program.
- logger.critical(): Critical errors that may cause program failure.
- logger.exception(): Logs an exception with traceback.
- logger.log(level, message): Logs at a custom integer level.

Usage: from logger import logger; logger.info("Message")
"""

import json
import os
from typing import Any
from loguru import logger as _logger

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path) as f:
    config = json.load(f)
_logger.add(
    config['log_file'],
    level=config['log_level'],
    format=config['format'],
    rotation=config['rotation'],
    retention=config['retention']
)

class Logger:
    def __init__(self):
        self._logger = _logger

    def trace(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.trace(message, *args, **kwargs)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(message, *args, **kwargs)

    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.success(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.exception(message, *args, **kwargs)

    def log(self, level: int, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.log(level, message, *args, **kwargs)

logger = Logger()