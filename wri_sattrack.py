#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import jdcal
import sys
import serial
import GetUserData
import GetSat
import GetLook


'''
#if you want to use serial.
port_num=raw_input("Please Enter Your Serial Port Number:\n")

if sys.platform == "linux2":
	ser=serial.Serial("COM"+porn_num,9600,timeout=0.5)
if sys.platform == "win32":
	ser=serial.Serial("/dev/ttyUSB"+port_num,9600,timeout=0.5)
'''


GetUserData.update("shell")

line1,line2,Lat,Lon,kmAlt = GetUserData.get_user_data("shell",'','','','' )

GetSat.generate(line1,line2)
GetLook.generate(Lat,Lon,kmAlt)

while True:

	tt = time.time()
	tg = time.gmtime(tt)
	eciSat = GetSat.get_eciSat(tt)
	date_now_julian = sum(jdcal.gcal2jd(tg.tm_year,tg.tm_mon,tg.tm_mday))+tg.tm_hour/24.0+tg.tm_min/24.0/60.0+tg.tm_sec/24.0/3600.0
	AZ,EL = GetLook.GetLook(date_now_julian,eciSat)

	print AZ,EL
	
'''	
	#if you want to use serial
	ser.write("Whatever you need")
	#For example:   ser.write(AZ,EL)

	#If you need to control the frequency of date out:
	time.sleep()                 #Second
'''