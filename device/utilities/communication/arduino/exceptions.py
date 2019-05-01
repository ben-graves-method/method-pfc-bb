# Import python types
from typing import Optional

# Import device utilities
from device.utilities.logger import Logger


class ArduinoError(Exception):
    """Base class for errors raised by Arduino."""

    def __init__(self, message: str, logger: Optional[Logger] = None) -> None:
        self.message = message
        if logger != None:
            logger.error(message)  # type: ignore


class InitError(ArduinoError):
    pass


class ReadError(ArduinoError):
    pass


class WriteError(ArduinoError):
    pass
