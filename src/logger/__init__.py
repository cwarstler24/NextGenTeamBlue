"""
Logger package for the project.

This package configures loguru logger based on config.json.

Available logging methods:
- logger.security(message, level="info"): Logs security-related messages to
security.log at the specified level. Messages are encrypted for security.
- logger.event(message, level="info"): Logs event-related messages to event.log
at the specified level.

Supported levels (default is "info"): "trace" (most verbose), "debug", "info",
"success", "warning", "error", "critical" (least verbose).

Usage: from logger import logger; logger.security("Security alert",
level="warning"); logger.event("Event occurred")
"""
from .logger import Logger
logger = Logger()
