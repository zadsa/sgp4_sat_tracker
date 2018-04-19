#import os
#import re
#import sys
import serial

#from doctest import DocTestSuite, ELLIPSIS
#from unittest import TestCase

import math
from numpy import deg2rad

from sgp4.earth_gravity import wgs72
from sgp4.ext import invjday, newtonnu, rv2coe
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4


class Eci(object):
	position=[]
	velocity=[]

F                        =        1.0 / 298.26
XKMPER_WGS72             =        6378.135
EPOCH_JAN1_12H_2000      =        2451545.0
SEC_PER_DAY              =        86400.0
OMEGA_E                  =        1.00273790934


#ser=serial.Serial("/dev/ttyAMA0",115200,timeout=0.5) #使用树莓派的GPIO口连接串行口
#ser=serial.Serial("/dev/ttyUSB0",115200,timeout=0.5) #使用树莓派的GPIO口连接串行口

#print ser.name#打印设备名称
#print ser.port#打印设备名
#ser.open()
#打开端口
#s = ser.read(10)#从端口读10个字节
#ser.write("hello")#向端口些数据
#ser.close()#关闭端口
 #       data = ser.read(20) #是读20个字符

  #      data = ser.readline() #是读一行，以/n结束，要是没有/n就一直读，阻塞。

  #      data = ser.readlines()和ser.xreadlines()#都需要设置超时时间

 #       ser.baudrate = 9600 #设置波特率

 #       ser.isOpen() #看看这个串口是否已经被打开


#ser.write(chr(40))


#print( c + " 的ASCII 码为", ord(c))
#print( a , " 对应的字符为", chr(a))

line1 = ('1 00005U 58002B   00179.78495062  '
          '.00000023  00000-0  28098-4 0  4753')
line2 = ('2 00005  34.2682 348.7242 1859667 '
          '331.7664  19.3264 10.82419157413667')

satellite = twoline2rv(line1, line2, wgs72)


eciSat  = Eci()

P,V = satellite.propagate(2000, 6, 28, 0, 50, 19.733567)


##list & tuple
eciSat.Position = list(P)
eciSat.Velocity = list(V)

Site    = Eci()
eciSite = Eci()
#  Site.Position =[ deg2rad(Lat),deg2rad(Lon),kmAlt ]
Site.Position =[ deg2rad(30) , deg2rad(30) , 20 ]

#GetLook
date = satellite.jdsatepoch
date = date + 0.25

def GetLook(date,eciSat,Site):

#cEci
lat = Site.Position[0];
lon = Site.Position[1];
alt = Site.Position[2];

   #Calculate Local Mean Sidereal Time (theta)

#ToLmst

UT = math.fmod(date + 0.5, 1.0);
TU = (date - EPOCH_JAN1_12H_2000 - UT) / 36525.0;

GMST = 24110.54841 + TU * (8640184.812866 + TU * (0.093104 - TU * 6.2e-06));
GMST = math.fmod(GMST + SEC_PER_DAY * OMEGA_E * UT, SEC_PER_DAY);
if (GMST < 0.0):
   GMST += SEC_PER_DAY;  # "wrap" negative modulo value

theta = math.fmod((2*math.pi * (GMST / SEC_PER_DAY))+lon,2*math.pi)

#End ToLmstS

#back to cEci

c = 1.0 / math.sqrt(1.0 + F * (F - 2.0) * math.pow(math.sin(lat),2))
s = math.pow((1.0 - F),2) * c;
achcp = (XKMPER_WGS72 * c + alt) * math.cos(lat)

eciSite.Position = [achcp * math.cos(theta),
   					achcp * math.sin(theta),
					(XKMPER_WGS72 * s + alt) * math.sin(lat),   # km
                    math.sqrt(   math.pow(achcp * math.cos(theta),2) 
                               + math.pow(achcp * math.sin(theta),2)
                               + math.pow((XKMPER_WGS72 * s + alt) * math.sin(lat),2)   )]
   #Determine velocity components due to earth's rotation
mfactor = math.pi*2 * (OMEGA_E / SEC_PER_DAY)

eciSite.Velocity= [ - mfactor * eciSite.Position[1],
                   	  mfactor * eciSite.Position[0], 
                      0.0, 
                      math.sqrt(    math.pow(-mfactor * eciSite.Position[1],2)
                     		      + math.pow( mfactor * eciSite.Position[0],2)  )]

#End cEci

#back to GetLook
vecRgRate = [  eciSat.Velocity[0] - eciSite.Velocity[0],
               eciSat.Velocity[1] - eciSite.Velocity[1],
               eciSat.Velocity[2] - eciSite.Velocity[2]]

x = eciSat.Position[0] - eciSite.Position[0];
y = eciSat.Position[1] - eciSite.Position[1];
z = eciSat.Position[2] - eciSite.Position[2];

w = math.sqrt(	  math.pow(x,2)
 				+ math.pow(y,2)
 			    + math.pow(z,2))

vecRange = [x, y, z, w]



sin_lat   = math.sin(lat)
cos_lat   = math.cos(lat)
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)

top_s = (    sin_lat * cos_theta * vecRange[0] 
           + sin_lat * sin_theta * vecRange[1]
           - cos_lat * vecRange[2])
top_e = ( 	- sin_theta * vecRange[0]
            + cos_theta * vecRange[1])
top_z = (     cos_lat * cos_theta * vecRange[0] 
            + cos_lat * sin_theta * vecRange[1]
            + sin_lat * vecRange[2])



az    = math.atan(-top_e / top_s);

if (top_s > 0.0):
   az += math.pi

if (az < 0.0):
   az += 2.0*math.pi

az = az * 180 / math.pi



el   = math.asin(top_z / vecRange[3]);
el   = el * 180 / math.pi

return az,el




'''
          satellite.epochyr
          2000
          satellite.epochdays
          179.78495062
          satellite.jdsatepoch
          2451723.28495062
          satellite.epoch
          datetime.datetime(2000, 6, 27, 18, 50, 19, 733567)
'''
