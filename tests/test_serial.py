import Adafruit_BBIO.UART as UART
import serial
 
UART.setup("UART1")
 
ser = serial.Serial(port = "/dev/ttyO1", baudrate=115200)
ser.close()
ser.open()
if ser.isOpen():
	print ("Serial is open!")
	ser.write("*w_1_10_^")
ser.close()
