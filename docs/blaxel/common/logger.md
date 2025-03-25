Module blaxel.common.logger
===========================
This module provides a custom colored formatter for logging and an initialization function
to set up logging configurations for Blaxel applications.

Functions
---------

`init(log_level: str)`
:   Initializes the logging configuration for Blaxel.
    
    This function clears existing handlers for specific loggers, sets up a colored formatter,
    and configures the root logger with the specified log level.
    
    Parameters:
        log_level (str): The logging level to set (e.g., "DEBUG", "INFO").

Classes
-------

`ColoredFormatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)`
:   A custom logging formatter that adds ANSI color codes to log levels for enhanced readability.
    
    Attributes:
        COLORS (dict): A mapping of log level names to their corresponding ANSI color codes.
    
    Initialize the formatter with specified format strings.
    
    Initialize the formatter either with the specified format string, or a
    default as described above. Allow for specialized date formatting with
    the optional datefmt argument. If datefmt is omitted, you get an
    ISO8601-like (or RFC 3339-like) format.
    
    Use a style parameter of '%', '{' or '$' to specify that you want to
    use one of %-formatting, :meth:`str.format` (``{}``) formatting or
    :class:`string.Template` formatting in your format string.
    
    .. versionchanged:: 3.2
       Added the ``style`` parameter.

    ### Ancestors (in MRO)

    * logging.Formatter

    ### Class variables

    `COLORS`
    :

    ### Methods

    `format(self, record)`
    :   Formats the log record by adding color codes based on the log level.
        
        Parameters:
            record (LogRecord): The log record to format.
        
        Returns:
            str: The formatted log message with appropriate color codes.