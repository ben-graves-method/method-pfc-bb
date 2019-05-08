# Import standard python libraries
import logging, threading, time
from unittest import TestCase

# Import utilities
from lib.utilities.bitwise import byte_str

# Import i2c elements
from lib.i2c.main import I2C
from lib.i2c.exceptions import ReadError, WriteError
from lib.i2c.mux_simulator import MuxSimulator
from lib.i2c.peripheral_simulator import PeripheralSimulator

# Enable logging output
logging.basicConfig(level=logging.DEBUG)

addr = 0x27
chan = 1

def test_init():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )


def test_read_empty():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )
    bytes_ = i2c.read(2)
    assert bytes_[0] == 0x00
    assert bytes_[1] == 0x00


def test_write_unknown():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )
    i2c.write([0x01])


def test_write_read():
    class CustomPeripheralSimulator(PeripheralSimulator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.writes = {byte_str(bytes([0x01])): bytes([0x02])}

    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=addr,
        mux=0x77,
        channel=chan,
#        mux_simulator=MuxSimulator(),
#        PeripheralSimulator=CustomPeripheralSimulator,
    )
    i2c.write(bytes([0x01]))
    bytes_ = i2c.read(1)
    logging.info(bytes_)
    assert bytes_[0] == 0x02


def test_write_register():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )
    i2c.write_register(0x01, 0x02)


def test_read_empty_register():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )
    byte = i2c.read_register(0x01)


def test_write_read_register():
    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=PeripheralSimulator,
    )
    i2c.write_register(0x01, 0x02)
    byte = i2c.read_register(0x01)
    assert byte == 0x02


def test_read_custom_register():
    class CustomPeripheralSimulator(PeripheralSimulator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.registers = {0xE7: 0x00}

    i2c = I2C(
        name="Test",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x40,
        mux=0x77,
        channel=4,
        mux_simulator=MuxSimulator(),
        PeripheralSimulator=CustomPeripheralSimulator,
    )
    assert i2c.read_register(0xE7) == 0x00


#test_write_read()
def relay_test():
    i2c = I2C(
        name="Relays",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x27,
        mux=None,
        channel=1,
#        mux_simulator=MuxSimulator(),
#        PeripheralSimulator=CustomPeripheralSimulator,
    )

    # one-time setup
    i2c.write_register(0x00, 0x00) # set pins 0-7 to output
    i2c.write_register(0x01, 0x00) # set pins 8-15 to output
    i2c.write_register(0x12, 0x00) # set outputs 0-7 to off
    i2c.write_register(0x13, 0x00) # set outputs 8-15 to off
    time.sleep(.5)

    while True :
        # write and read testing
        i2c.write_register(0x12, 0xFF) # set outputs 0-7 to on
        i2c.write_register(0x13, 0xFF) # set outputs 8-15 to on
        time.sleep(2)
        logging.info(i2c.read_register(0x14)) # read current MCP pin setting for pins 0-7
        logging.info(i2c.read_register(0x15)) # read current MCP pin setting for pins 8-15
        time.sleep(2)
        i2c.write_register(0x12, 0x00) # set outputs 0-7 to off
        i2c.write_register(0x13, 0x00) # set outputs 8-15 to off
        time.sleep(2)


#relay_test();

def read_light_sensor():
    TSL2561_control = 0x80
    TSL2561_timing = 0x81
    TSL2561_Interrupt = 0x86
    TSL2561_Channal0L = 0x8C
    TSL2561_Channal0H = 0x8D
    TSL2561_Channal1L = 0x8E
    TSL2561_Channal1H = 0x8F

    TSL2561_Address =  0x29       # device address

    i2c = I2C(
        name="Arduino",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x29,
        mux=None
    )
#read_light_sensor()

def talk_to_arduino():
    i2c = I2C(
        name="Arduino",
        i2c_lock=threading.RLock(),
        bus=2,
        address=0x08,
        mux=None
    )

    i2c.write(bytes("*w_3_0^", 'utf-8'))
    

talk_to_arduino()

def test_if_device_exists():
    ad = 0x08
    logging.info(ad)

    i2c = I2C(
        name="Device",
        i2c_lock=threading.RLock(),
        bus=2,
        address=ad,
        mux=None
    )

    i2c.write(bytes("i"))

    

# test_if_device_exists()