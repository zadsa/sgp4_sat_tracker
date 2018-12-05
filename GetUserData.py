#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
#import sys


#Update Data
file_list = ('amateur.txt','noaa.txt','stations.txt')

def update(mode):

  if mode == "shell":
    print "Do you want to update the Satellite Data?[Y/n]"
    update = raw_input()

  if mode == "gui":
    update = 'Y'
  
  if update == 'Y' or update == 'y':
    for i in file_list:
      r=requests.get("http://www.celestrak.com/NORAD/elements/"+i)
      print "Downloding "+i
      #with open(sys.path[0]+"/"+i, "wb") as code:
      with open(i, "wb") as code:
       code.write(r.content)
    print "The Download is Complete."


#Serach Sat Data
def get_user_data(mode,Sat,Lat,Lon,Alt):

  global file_list

  if mode == "shell":

    print "Please enter the name of the Satellite:"
    name = str.upper(raw_input())

    for i in range(len(file_list)):
      f = open(file_list[i],"r")
      while True:
        line=f.readline()
        if line.find(name) != -1:
          line1 = f.readline()[0:68]
          line2 = f.readline()[0:68]
          f.close()
          break
        if line == "":
          break
      if ('line1' in dir())==False and i==len(file_list)-1:
        print "No date about this Sat.Please Enter The Correct Sat Name."
        name = str.upper(raw_input())



    #Site Data
    print "Please enter your Latitude(deg):"
    Lat = float(raw_input())
    print "Please enter your Longitude(deg):"
    Lon = float(raw_input())
    print "Please enter your Altitude:"
    Alt = float(raw_input())

    return line1,line2,Lat,Lon,Alt

  if mode == "gui":

    name = str.upper(Sat)

    for i in range(len(file_list)):
      f = open(file_list[i],"r")
      while True:
        line=f.readline()
        if line.find(name) != -1:
          line1 = f.readline()[0:68]
          line2 = f.readline()[0:68]
          f.close()
          break
        if line == "":
          break
      if ('line1' in dir())==False and i==len(file_list)-1:
        print "No date about this Sat.Please Enter The Correct Sat Name."
        name = str.upper(raw_input())
        
  return line1,line2,Lat,Lon,Alt