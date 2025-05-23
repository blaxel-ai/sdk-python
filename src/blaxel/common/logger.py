"""
This module provides a custom colored formatter for logging and an initialization function
to set up logging configurations for Blaxel applications.
"""
import json
import logging
import os

from opentelemetry import trace
from opentelemetry import context as context_api


class JsonFormatter(logging.Formatter):
    """
    A logger compatible with standard json logging.
    """
    def __init__(self):
        super().__init__()
        self.trace_id_name = os.environ.get('BL_LOGGER_TRACE_ID', 'trace_id')
        self.span_id_name = os.environ.get('BL_LOGGER_SPAN_ID', 'span_id')
        self.labels_name = os.environ.get('BL_LOGGER_LABELS', 'labels')
        self.trace_id_prefix = os.environ.get('BL_LOGGER_TRACE_ID_PREFIX', '')
        self.span_id_prefix = os.environ.get('BL_LOGGER_SPAN_ID_PREFIX', '')
        self.task_index = os.environ.get('BL_TASK_KEY', 'TASK_INDEX')
        self.task_prefix = os.environ.get('BL_TASK_PREFIX', '')
        self.execution_key = os.environ.get('BL_EXECUTION_KEY', 'BL_EXECUTION_ID')
        self.execution_prefix = os.environ.get('BL_EXECUTION_PREFIX', '')

    def format(self, record):
        """
        Formats the log record by converting it to a JSON object with trace context and environment variables.
        """
        log_entry = {
            'message': record.getMessage(),
            'severity': record.levelname,
            self.labels_name: {}
        }

        # Try to get the current span from context
        # Get current span - try multiple approaches
        current_span = trace.get_current_span()
        
        if current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry[self.trace_id_name] = f"{self.trace_id_prefix}{span_context.trace_id}"
            log_entry[self.span_id_name] = f"{self.span_id_prefix}{span_context.span_id}"

        # Add task ID if available
        task_id = os.environ.get(self.task_index)
        if task_id:
            log_entry[self.labels_name]['blaxel-task'] = f"{self.task_prefix}{task_id}"

        # Add execution ID if available
        execution_id = os.environ.get(self.execution_key)
        if execution_id:
            log_entry[self.labels_name]['blaxel-execution'] = f"{self.execution_prefix}{execution_id.split('-')[-1]}"

        return json.dumps(log_entry)


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
    # Disable urllib3 logging
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    handler = logging.StreamHandler()

    logger_type = os.environ.get("BL_LOGGER", "http")
    if logger_type == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(ColoredFormatter("%(levelname)s %(name)s - %(message)s"))
    logging.basicConfig(level=log_level, handlers=[handler])
