from core.utils import do_something
from logger import logger

if __name__ == "__main__":
    logger.event("Starting main application")
    # Demo of all log levels
    logger.event("Trace level demo", level="trace")
    logger.event("Debug level demo", level="debug")
    logger.event("Info level demo", level="info")
    logger.event("Success level demo", level="success")
    logger.event("Warning level demo", level="warning")
    logger.event("Error level demo", level="error")
    logger.event("Critical level demo", level="critical")
    do_something()
    logger.event("Main application finished")