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

def _init_():
#Normal Mode
	GetUserData.update("shell")
	line1,line2,Lat,Lon,Alt = GetUserData.get_user_data("shell",'','','','' )
#Test Mode
#	line1 = "1 27607U 02058C   18338.87750224 -.00000040  00000-0  15328-4 0  9993"
#	line2 = "2 27607  64.5552 288.2486 0079235 293.7328  65.5477 14.75502172858143"
#	Lat,Lon,Alt = 30,30,0


	GetSat.generate(line1,line2)
	GetLook.generate(Lat,Lon,Alt)


#	print "You are tracking : "+str.upper(Sat)+"."
	print "You are at Lat : "+str(Lat) +\
					" Lon : "+str(Lon)+\
					" Altitude :"+str(Alt)+"m\n"


	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	if EL>=5:
		raw_input("Passing Now,Press ENTER to continue tracking ...")

	if EL<5 :
		pass_time = GetLook.GetPassTime(tt,eciSat)
		local_time = time.localtime(pass_time)
		print "Next Pass Time:     " + time.asctime(local_time)+"\n"
		raw_input("Press ENTER to continue tracking ...\n\n")





_init_()

while True:

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	serial_str="AZ"+str(AZ)+" EL"+str(EL)+" Easycomm"
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





