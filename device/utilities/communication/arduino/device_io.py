# Import standard python modules
import fcntl, io, os
from typing import Optional, Type, Callable, cast, Any, TypeVar
from types import TracebackType

import Adafruit_BBIO.UART as UART
import serial

# Import i2c package elements
from device.utilities.communication.arduino.exceptions import (
    InitError,
    WriteError,
    ReadError
)

# Import device utilities
from device.utilities.logger import Logger

def manage_io(func: F) -> F:
    """Manages opening/closing io stream."""

    def wrapper(*args, **kwds):  # type: ignore
        self = args[0]
        self.open()
        resp = func(*args, **kwds)
        self.close()
        return resp

    return cast(F, wrapper)


class DeviceIO(object):
    """Manages byte-level device IO."""

    def __init__(self, name: str) -> None:

        # Initialize parameters
        self.name = name

        # Initialize logger
        logname = "DeviceIO({})".format(name)
        self.logger = Logger(logname, __name__)

        # Verify io exists
        self.logger.debug("Verifying io stream exists")

        UART.setup("UART1")
        self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)

        self.open()
        self.close()

    def __del__(self) -> None:
        """Clean up any resources used by the I2c instance."""
        self.close()

    def __enter__(self) -> object:
        """Context manager enter function."""
        return self

    def __exit__(self, exc_type: ET, exc_val: EV, exc_tb: EB) -> bool:
        """Context manager exit function, ensures resources are cleaned up."""
        self.close()
        return False  # Don't suppress exceptions

    def open(self) -> None:
        """Opens io stream."""
        try:
            self.ser.open()
        except Exception as e:
            message = "Unable to open device io: {}".format(device_name)
            raise InitError(message, logger=self.logger) from e

    def close(self) -> None:
        """Closes io stream."""
        try:
            self.ser.close()
        except:
            self.logger.exception("Unable to close")

    @manage_io
    def write_output(self, pin: int, val: string) -> None:
        """This tells the Arduino to set a pin to a value"""
        try:
            self.send_to_ardunio("*w_{}_{}^".format(pin, val))
        except Exception as e:
            message = "Unable to write {}: write_output(pin={}, val={})".format(self.name, pin, val))
            raise WriteError(message) from e

    @manage_io
    def read_register(
        self, address: string, register: string
    ) -> string:
        """This informs the Arduino to read an I2C chip, and reports the value back"""
        try:
            resp = self.request_to_ardunio("*r_{}_{}^".format(address, register))
            return resp
        except Exception as e:
            message = "Unable to write {}: write_output(pin={}, val={})".format(self.name, pin, val))
            raise WriteError(message) from e

    @manage_io
    def write_register(
        self, address: string, register: string, message: string
    ) -> None:
        """This tells the Arduino to set a pin to a value"""
        try:
            self.send_to_ardunio("*r_{}_{}_{}^".format(address, register, message))
        except Exception as e:
            message = "Unable to write {}: write_output(pin={}, val={})".format(self.name, pin, val))
            raise WriteError(message) from e

    def send_to_ardunio(self, message):
        print("send to arduino: {}".format(message))

    def request_to_ardunio(self, message):
        resp = self.make_request(message)
        return resp

    def make_request(self, message):
        print("request to arduino: {}".format(message))
        return "response"
