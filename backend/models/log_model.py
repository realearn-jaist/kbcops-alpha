import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


def configure_logging():
    """Configure app logging.

    Returns:
        logger (logging.Logger): The logger object
    """
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Define the log file path pattern with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_directory, f"app_{current_date}.log")

    # Create a logger
    logger = logging.getLogger("KBCOps")
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

        # Create a TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=7
        )
        handler.suffix = "%Y-%m-%d"  # Add date to the filename
        handler.setLevel(logging.DEBUG)  # Set the logging level for this handler

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)
        logging.shutdown()
    return logger
