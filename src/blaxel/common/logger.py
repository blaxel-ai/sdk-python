"""
This module provides a custom colored formatter for logging and an initialization function
to set up logging configurations for Blaxel applications.
"""

import logging


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds ANSI color codes to log levels for enhanced readability.

    Attributes:
        COLORS (dict): A mapping of log level names to their corresponding ANSI color codes.
    """
    COLORS = {
        "DEBUG": "\033[1;36m",  # Cyan
        "INFO": "\033[1;32m",  # Green
        "WARNING": "\033[1;33m",  # Yellow
        "ERROR": "\033[1;31m",  # Red
        "CRITICAL": "\033[1;41m",  # Red background
    }

    def format(self, record):
        """
        Formats the log record by adding color codes based on the log level.

        Parameters:
            record (LogRecord): The log record to format.

        Returns:
            str: The formatted log message with appropriate color codes.
        """
        n_spaces = len("CRITICAL") - len(record.levelname)
        tab = " " * n_spaces
        color = self.COLORS.get(record.levelname, "\033[0m")
        record.levelname = f"{color}{record.levelname}\033[0m:{tab}"
        return super().format(record)

def init_logger(log_level: str):
    """
    Initializes the logging configuration for Blaxel.

    This function clears existing handlers for specific loggers, sets up a colored formatter,
    and configures the root logger with the specified log level.

    Parameters:
        log_level (str): The logging level to set (e.g., "DEBUG", "INFO").
    """
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter("%(levelname)s %(name)s - %(message)s"))
    logging.basicConfig(level=log_level, handlers=[handler])
