#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import time
import jdcal

import GetSat

F                        =        1.0 / 298.26
XKMPER_WGS72             =        6378.135
EPOCH_JAN1_12H_2000      =        2451545.0
SEC_PER_DAY              =        86400.0
OMEGA_E                  =        1.00273790934



class Eci(object):
	Position=[]
	Velocity=[]


Site	=	Eci()



def generate(Lat,Lon,Alt):
	Site.Position =    [ Lat*math.pi/180 , Lon*math.pi/180 , Alt/1000 ]

#Old Version
#def generate(Lat,Lon,kmAlt):
#	Site.Position =    [ Lat*math.pi/180 , Lon*math.pi/180 , kmAlt ]


def getJulian(tt):
	tg = time.gmtime(tt)
	date_now_julian = sum(jdcal.gcal2jd(tg.tm_year,tg.tm_mon,tg.tm_mday))+tg.tm_hour/24.0+tg.tm_min/24.0/60.0+tg.tm_sec/24.0/3600.0
	return date_now_julian

#get pass time & max EL
def GetPassData(tt,eciSat):
#bug : GetPassData() when passing,the maxEL is wrong.

	i=0
	ELmax = 5

	while True:

		eciSat = GetSat.get_eciSat(tt)
		AZ,EL = GetLook(tt,eciSat)

		if EL>5 and i==0:
			ttpass = tt
			i=1

		if EL>ELmax :
			ELmax = EL
		elif EL>5 and EL<ELmax:
			return ttpass,ELmax

		tt = tt + 1


def GetLook(tt,eciSat):

	date_now = getJulian(tt)

	eciSite = Eci()

#------------cSite::GetLookAngle()-------------

#------------cEci.cpp-----------------------------


	lat  = Site.Position[0];
	lon  = Site.Position[1];
	alt  = Site.Position[2];

#----------------date.ToLmst()
	UT   = math.fmod(date_now + 0.5, 1.0);
	TU   = (date_now - EPOCH_JAN1_12H_2000 - UT) / 36525.0;

	GMST = 24110.54841 + TU * (8640184.812866 + TU * (0.093104 - TU * 6.2e-06));
	GMST = math.fmod(GMST + SEC_PER_DAY * OMEGA_E * UT, SEC_PER_DAY);

	if (GMST < 0.0):
	   GMST += SEC_PER_DAY;  # "wrap" negative modulo value
#----------------date.ToLmst()

	theta = math.fmod((2*math.pi * (GMST / SEC_PER_DAY))+lon,2*math.pi)
	c     = 1.0 / math.sqrt(1.0 + F * (F - 2.0) * math.pow(math.sin(lat),2))
	s     = math.pow((1.0 - F),2) * c;
	achcp = (XKMPER_WGS72 * c + alt) * math.cos(lat)

	eciSite.Position = [achcp * math.cos(theta),
	   					achcp * math.sin(theta),
						(XKMPER_WGS72 * s + alt) * math.sin(lat),   # km
	                    math.sqrt(   math.pow(achcp * math.cos(theta),2) 
	                               + math.pow(achcp * math.sin(theta),2)
	                               + math.pow((XKMPER_WGS72 * s + alt) * math.sin(lat),2)   )]

	mfactor = math.pi*2 * (OMEGA_E / SEC_PER_DAY)

	eciSite.Velocity= [ - mfactor * eciSite.Position[1],
	                   	  mfactor * eciSite.Position[0], 
	                      0.0, 
	                      math.sqrt(    math.pow(-mfactor * eciSite.Position[1],2)
	                     		      + math.pow( mfactor * eciSite.Position[0],2)  )]
#---------cEci.cpp--------------------
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


	top_s = (     sin_lat * cos_theta * vecRange[0] 
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

#------------cSite::GetLookAngle()-------------
	return round(az,2),round(el,2)