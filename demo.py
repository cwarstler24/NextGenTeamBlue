from core.utils import do_something
from logger import logger

if __name__ == "__main__":
    logger.info("Starting main application")
    do_something()
    logger.info("Main application finished")
