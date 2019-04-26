# Import standard python modules
import time, threading

# Import python types
from typing import NamedTuple, Optional, Dict

# Import device utilities
from device.utilities.logger import Logger
from device.utilities import bitwise
from device.utilities.communication.i2c.main import I2C
from device.utilities.communication.i2c.exceptions import I2CError
from device.utilities.communication.i2c.mux_simulator import MuxSimulator

# Import driver elements
from device.peripherals.common.mcp23017.simulator import MCP23017Simulator
from device.peripherals.common.mcp23017 import exceptions


class MCP23017Driver:
    """Driver for MCP23017 digital to analog converter."""

    def __init__(
        self,
        name: str,
        i2c_lock: threading.RLock,
        bus: int,
        address: int,
        mux: Optional[int] = None,
        channel: Optional[int] = None,
        simulate: bool = False,
        mux_simulator: Optional[MuxSimulator] = None,
    ) -> None:
        """Initializes MCP23017."""

        # Initialize logger
        logname = "MCP23017({})".format(name)
        self.logger = Logger(logname, __name__)

        # Check if simulating
        if simulate:
            self.logger.info("Simulating driver")
            Simulator = MCP23017Simulator
        else:
            Simulator = None

        # Initialize I2C
        try:
            self.i2c = I2C(
                name="MCP23017-{}".format(name),
                i2c_lock=i2c_lock,
                bus=bus,
                address=address,
                mux=mux,
                channel=channel,
                mux_simulator=mux_simulator,
                PeripheralSimulator=Simulator,
            )
        except I2CError as e:
            raise exceptions.InitError(logger=self.logger) from e

    def kth_pin_set(self, n, k):
        return n & (1 << (k))

    def write(self, pin, value):
        pins = self.i2c.read_register(0x14)
        # pins = 0x00

        self.logger.info("PIN VALUES BEFORE")
        self.logger.info(format(pins, '#010b'))

        if value == 1 and not self.kth_pin_set(pins, pin):
            self.logger.info("Turning pin {} on".format(pin))
            pins += 2 ** pin

        elif value == 0 and self.kth_pin_set(pins, pin):
            self.logger.info("Turning pin {} off".format(pin))
            pins -= 2 ** pin
            
        self.i2c.write_register(0x12, hex(pins))

        self.logger.info("PIN VALUES AFTER")
        self.logger.info(format(pins, '#010b'))

    def set_high(self, channel: Optional[int] = None, retry: bool = True) -> None:
        """Sets channel high, sets all channels high if no channel is specified."""
        self.logger.debug("Setting channel {} high".format(channel))
        try:
            self.write(channel, 1)  # type: ignore
        except exceptions.WriteOutputError as e:
            raise exceptions.SetHighError(logger=self.logger) from e

    def set_low(self, channel: Optional[int] = None) -> None:
        """Sets channel low, sets all channels low if no channel is specified."""
        self.logger.debug("Setting channel {} low".format(channel))
        try:
            self.write(channel, 0)  # type: ignore
        except exceptions.WriteOutputError as e:
            raise exceptions.SetLowError(logger=self.logger) from e
