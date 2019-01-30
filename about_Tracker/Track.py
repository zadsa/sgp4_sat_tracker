#!/usr/bin/python
# -*- coding: utf-8 -*-

#Not Completed

from Pelco_D import Tracker
from HMC5883L import HMC5883L
from MMA8452Q import MMA8452Q


import GetSat
import GetLook
import time
import math
import serial


#Change the System Time to Test.
#os.system('sudo date  --s="2018-05-27 19:59:00"')


#---setup----

'''
#if you want to use serial.

	#Windows
ser=serial.Serial("COM1",2400,timeout=0.5)
	#Linux
ser=serial.Serial("/dev/ttyUSB0",2400,timeout=0.5)
'''

azimuth		= HMC5883L()
elevation	= MMA8452Q()
Tracker		= Tracker("/dev/ttyUSB0", 2400)
#Tracker	= Tracker("COM1")

#----------------Big Loop----------------
while True:

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	AZ_now = azimuth.read()     #azimuth
	EL_now = elevation.read()   #elevation


#-----------------Move-------------------
	
	
	AZ_old = AZ
	EL_old = EL


	time.sleep(0.1)





