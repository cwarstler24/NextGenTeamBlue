from logger import logger

def do_something():
    logger.event("Doing something in core.utils")
    logger.security("Security check passed")
    logger.security("Security warning issued", level="warning")
    logger.event("Event occurred in utils")
    logger.event("Critical event happened", level="error")