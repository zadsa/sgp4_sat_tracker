#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import serial
import GetUserData
import GetSat
import GetLook


'''
#if you want to use serial.

	#Linux
ser=serial.Serial("COM1",9600,timeout=0.5)
	#Windows
ser=serial.Serial("/dev/ttyUSB0",9600,timeout=0.5)
'''


GetUserData.update("shell")

line1,line2,Lat,Lon,kmAlt = GetUserData.get_user_data("shell",'','','','' )

GetSat.generate(line1,line2)
GetLook.generate(Lat,Lon,kmAlt)

while True:

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	serial_str="AZ"+str(AZ)+" EL"+str(EL)+" Easycomm Mode"
	print serial_str
	
'''	
	#if you want to use serial
	ser.write("Whatever you need")
	#For example:   ser.write(serial_str)
'''

'''
	#If you need to control the frequency of date out:
	time.sleep()                 #Second
'''