import wiringpi as wpi
import math



ACC=wpi.wiringPiI2CSetup(0x18)
wpi.wiringPiI2CWriteReg8(ACC,0x20, 0x27)

while True:
	ACC_x = wpi.wiringPiI2CReadReg8(ACC, 0x28) << 8 | wpi.wiringPiI2CReadReg8(ACC, 0x29)
#
	ACC_y = wpi.wiringPiI2CReadReg8(ACC, 0x2a) << 8 | wpi.wiringPiI2CReadReg8(ACC, 0x2b)
#
	ACC_z = wpi.wiringPiI2CReadReg8(ACC, 0x2c) << 8 | wpi.wiringPiI2CReadReg8(ACC, 0x2d)
#
#
#
#
#
	if ACC_x > 32768:
		ACC_x = -(65535 - ACC_x + 1)
#
#
	if ACC_y > 32768:
		ACC_y = -(65535 - ACC_y + 1)
#
#
	if ACC_z > 32768:
		ACC_z = -(65535 - ACC_z + 1)
#		
	if ACC_x>15936:
		ACC_x=15936
	if ACC_x<-15936:
		ACC_x=-15936
#
#	angle = math.acos(float(yAccl)/float(1024))*180/5.0/math.pi
	#angle= math.atan2(ACC_y,ACC_x)* (180/3.14159265) + 180
#	angle
	AZ=90-math.acos(float(ACC_x)/float(15936))*180/math.pi
	AZ


#XAxis = (float(X) - xOffset) * mgPerDigit;
#YAxis = (float(Y) - yOffset) * mgPerDigit;
#ZAxis =  float(Z) * mgPerDigit;


import wiringpi as wpi
import math
import time

MAG=wpi.wiringPiI2CSetup(0x1e)
wpi.wiringPiI2CWriteReg8(MAG,0x00, 0x0c)#Minimum data output rate (Hz)
wpi.wiringPiI2CWriteReg8(MAG,0x01, 0x20)
wpi.wiringPiI2CWriteReg8(MAG,0x02, 0x00)


while True:
	MAG_x = wpi.wiringPiI2CReadReg8(MAG, 0x03) << 8 | wpi.wiringPiI2CReadReg8(MAG, 0x04)
#
	MAG_y = wpi.wiringPiI2CReadReg8(MAG, 0x05) << 8 | wpi.wiringPiI2CReadReg8(MAG, 0x06)
#
	MAG_z = wpi.wiringPiI2CReadReg8(MAG, 0x07) << 8 | wpi.wiringPiI2CReadReg8(MAG, 0x08)
#
#
#
#
	if MAG_x>32768:    
		MAG_x = -(65535 - MAG_x + 1)
#
#
	if MAG_y>32768:
		MAG_y = -(65535 - MAG_y + 1)
#
#
	if MAG_z>32768:
		MAG_z = -(65535 - MAG_z + 1)
#		
	heading = math.atan2(float(MAG_y), float(MAG_x))
	declinationAngle = (114.0 + (43.0 / 60.0)) / (180 / math.pi)
	heading = heading + declinationAngle
	print heading*180.0/math.pi
	time.sleep(0.5)


#
	print MAG_x,MAG_y,MAG_z
	angle= math.atan2(float(MAG_y),float(MAG_x))*(180/math.pi)+180
	angle



