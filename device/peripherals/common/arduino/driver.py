# Import standard python modules
import time, threading

# Import python types
from typing import List
# Import device utilities
from device.utilities.logger import Logger
from device.utilities.communication.i2c.main import I2C
from device.utilities.communication.i2c.exceptions import I2CError


from device.peripherals.common.arduino import exceptions


class ArduinoCommsDriver:

    def __init__(
        self,
        name: str,
        i2c_lock: threading.RLock,
    ) -> None:
        """Initializes ArduinoComms"""

        # Initialize logger
        logname = "ArduinoComms({})".format(name)
        self.logger = Logger(logname, __name__)

        self.bus = 2
        self.address = 0x08

        self.name = name

        # Initialize I2C
        try:
            self.i2c = I2C(
                name="Arduino-{}".format(name),
                i2c_lock=i2c_lock,
                bus=self.bus,
                address=self.address,
                mux=None
            )
        except I2CError as e:
            raise exceptions.InitError(logger=self.logger) from e

    def write_output(self, value, pin=None, pins=None):
        if pin:
            self.i2c.write(bytes("*w_{}_{}^".format(pin, value), 'utf-8'))
            self.logger.debug("{} write_output: *w_{}_{}^".format(self.name, pin, value))        
        elif pins:
            for p in pins:
                self.i2c.write(bytes("*w_{}_{}^".format(p, value), 'utf-8'))
                self.logger.debug("{} write_output: *w_{}_{}^".format(self.name, p, value))
        else:
            raise exceptions.WriteOutputError(logger=self.logger)
        # for pin in self.pins:
        #     self.logger.debug("{} write_output: *w_{}_{}^".format(self.name, pin, value))
        #     self.i2c.write(bytes("*w_{}_{}^".format(pin, value), 'utf-8'))



    # def read_register(self, register):
    #     self.i2c.write(bytes("*r_{}_{}^".format(self.address, register), 'utf-8'))
    #
    #     num_bytes = 1
    #     self.i2c.read(num_bytes)
    #
    # def write_register(self, register, message):
    #     self.i2c.write(bytes("*r_{}_{}_{}^".format(self.address, register, message), 'utf-8'))

    def write_outputs(self, output_values):
        for pin, value in output_values.items():
            self.write_output(value, pin=pin)


    def set_high(self, pin=None, pins=None) -> None:
        if pin:
            self.write_output(255, pin=pin)
            self.logger.debug("Setting pin {} high".format(pin))
        elif pins:
            self.write_output(255, pins=pin)
            self.logger.debug("Setting pins {} high".format(pins))
        else:
            raise exceptions.SetHighError(logger=self.logger)

        # try:
        #     self.write_output(1)  # type: ignore
        # except exceptions.WriteOutputError as e:
        #     raise exceptions.SetHighError(logger=self.logger) from e

    def set_low(self, pin=None, pins=None) -> None:
        if pin:
            self.write_output(0, pin=pin)
            self.logger.debug("Setting pins {} low".format(pin))
        elif pins:
            self.write_output(0, pin=pins)
            self.logger.debug("Setting pins {} low".format(pins))
        else:
            raise exceptions.SetLowError(logger=self.logger)
        
        # try:
        #     self.write_output(0)  # type: ignore
        # except exceptions.WriteOutputError as e:
        #     raise exceptions.SetLowError(logger=self.logger) from e
