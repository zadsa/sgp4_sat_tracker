import serial

up		=	0xff,0x01,0x00,0x10,0x00,0xff,0x10
down	=	0xff,0x01,0x00,0x08,0x00,0xff,0x08
left	=	0xff,0x01,0x00,0x04,0xff,0x00,0x04
right	=	0xff,0x01,0x00,0x02,0xff,0x00,0x02
stop	=	0xff,0x01,0x00,0x00,0x00,0x00,0x01

'''
how to use:
from Pelco_D import Tracker
Tracker = Tracker("/dev/ttyUSB0",2400)
'''


class Tracker:

	def __init__(self, add, baud_rate):
		self.ser=serial.Serial("/dev/ttyUSB0",baud_rate,timeout=0.5)

	def up(self):
		self.ser.write(up)

	def down(self):
		self.ser.write(down)

	def left(self):
		self.ser.write(left)

	def right(self):
		self.ser.write(right)

	def stop(self):
		self.ser.write(stop)

	def close(self):
		self.ser.close()

	def write(self, data):
		self.ser.write(data)
