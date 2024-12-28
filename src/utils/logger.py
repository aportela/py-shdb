from typing import Any, Optional, Union
import inspect
import logging

class Logger:

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    def __init__(self, name: Optional[str] = None):
        """
        Initializes a logger with a specified name or deduces it from the calling class.
        If no name is provided and the calling class cannot be determined,
        the logger will be named 'Unknown'.

        :param name: The name of the logger. If None, the calling class's name is used.
        """
        if name is None:
            try:
                # Use inspect to determine the calling class's name
                frame = inspect.currentframe()
                if frame is not None:  # Safeguard against None
                    caller_frame = frame.f_back
                    class_instance = caller_frame.f_locals.get('self', None)

                    if class_instance:
                        name = class_instance.__class__.__name__
                    else:
                        module_name = caller_frame.f_globals.get('__name__', 'Unknown')
                        function_name = caller_frame.f_code.co_name
                        name = f"{module_name}.{function_name}"
                else:
                    name = "Unknown"
            except Exception as e:
                # Fallback in case introspection fails
                name = "Unknown"
                logging.warning(f"Logger: Failed to introspect caller class: {e}")

        # Initialize the logger with the determined or provided name
        self.__log = logging.getLogger(name)

    @staticmethod
    def parse_level(level: Optional[str] = None):
        """
        Parses the provided log level string and returns the corresponding logging level constant.

        :param level: The log level as a string (e.g., 'INFO', 'DEBUG', 'ERROR', etc.).
        :return: Corresponding logging level constant (e.g., Logger.INFO).
        """

        # Dictionary mapping log level strings to constants
        level_map = {
            "CRITICAL": Logger.CRITICAL,
            "ERROR": Logger.ERROR,
            "WARNING": Logger.WARNING,
            "INFO": Logger.INFO,
            "DEBUG": Logger.DEBUG,
            "NOTSET": Logger.NOTSET
        }

        # If level is provided, convert it to uppercase and check if it is in the level_map
        if level:
            level = level.upper()  # Convert to uppercase to handle case-insensitivity
            return level_map.get(level, Logger.NOTSET)  # Return the corresponding log level, or default to Logger.NOTSET if not found

        # If no level is provided, return the default level NOTSET
        return Logger.NOTSET

    @staticmethod
    def configure_global(
        level: int = logging.INFO,
        format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ):
        """
        Configures the global logging system. Should be called once at the start of the application.

        :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :param format: Format string for log messages.
        """
        try:
            logging.basicConfig(level=level, format=format)
        except Exception as e:
            logging.error(f"Logger: Failed to configure global logging: {e}")

    def info(self, message: Union[str, Any]):
        """Logs an informational message."""
        self.__log.info(self._prepare_message(message))

    def warning(self, message: Union[str, Any]):
        """Logs a warning message."""
        self.__log.warning(self._prepare_message(message))

    def error(self, message: Union[str, Any]):
        """Logs an error message."""
        self.__log.error(self._prepare_message(message))

    def debug(self, message: Union[str, Any]):
        """Logs a debug message."""
        self.__log.debug(self._prepare_message(message))

    def critical(self, message: Union[str, Any]):
        """Logs a critical message."""
        self.__log.critical(self._prepare_message(message))

    def _prepare_message(self, message: Any) -> str:
        """
        Converts the given message to a string for logging.

        :param message: The message to log.
        :return: The string representation of the message.
        """
        try:
            return str(message)
        except Exception as e:
            return f"Logger: Failed to convert message to string: {e}"
