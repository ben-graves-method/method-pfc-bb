# Import standard python libraries
import fcntl, io, time, logging, struct, threading

# # Import package elements
from device.utilities.communication.arduino.device_io import DeviceIO

# Import device utilities
from device.utilities.logger import Logger
from device.utilities.functiontools import retry


class Arduino(object):

    def __init__(
        self,
        name: str,
        arduino_lock: threading.RLock,
    ) -> None:

        # Initialize passed in parameters
        self.name = name
        self.arduino_lock = arduino_lock

        # Initialize logger
        logname = "Arduino({})".format(self.name)
        self.logger = Logger(logname, "arduino")
        self.logger.debug("Initializing communication")

        self.io = DeviceIO(name)

        # Successfully initialized!
        self.logger.debug("Initialization successful")

    @retry(tries=5, delay=0.2, backoff=3)
    def write_output(
        self, pin: string, val: string, retry: bool = True
    ) -> None:
        """This tells the Arduino to set a pin to a value"""
        with self.arduino_lock:
            self.logger.debug("{}: write_output(pin={}, val={})".format(self.name, pin, val))
            self.io.write_output(pin, val)

    @retry(tries=5, delay=0.2, backoff=3)
    def read_register(
        self, address: string, register: string
    ) -> string:
        """This informs the Arduino to read an I2C chip, and reports the value back"""
        with self.arduino_lock:
            self.logger.debug("{}: write_output(address={}, register={})".format(self.name, address, register))
            return self.io.read_register(address, register)

    @retry(tries=5, delay=0.2, backoff=3)
    def write_register(
        self, address: string, register: string, message: string
    ) -> None:
        """Similar to `read_register`, but this writes a message"""
        with self.arduino_lock:
            self.logger.debug("{}: write_register(address={}, register={}, message={})".format(self.name, address, register, message))
            self.io.write_register(self.address, register, message)
