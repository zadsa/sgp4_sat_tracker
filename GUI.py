#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import sys
import time
import serial
import threading
import GetUserData
import GetSat
import GetLook

#Stop Tracking
def stop():
	global stop
	stop = 1

#Update Data
def update():
	GetUserData.update("gui")

#Quit GUI & Shell
def quit():
	
	global timer
	if ( stop==0 or stop==1 ):
		timer.cancel()
	
	root.destroy()


#Passing time & max EL angle
'''
def passing(EL):

	if EL>=5:
		print "Passing Now ..."
		var_pass_time.set("Passing Now ...")

	if EL<5:
		pass_time , maxEL = GetLook.GetPassData(tt,eciSat)
		local_time = time.localtime(pass_time)
		print "Next Passing Time:"+ time.asctime(local_time)
		var_pass_time.set(str(local_time.tm_year)+"/"+str(local_time.tm_mon)+"/"+str(local_time.tm_mday)+" "+str(local_time.tm_hour)+":"+str(local_time.tm_min)+":"+str(local_time.tm_sec))
		var_maxEL.set(str(maxEL))
	var_pass_time = StringVar()
	var_maxEL = StringVar()
'''
#

#Start Tracking
def start():

#	i=language.get()

	global stop
	stop = 0

	Sat=e1.get()
	Lat=float(e2.get())
	Lon=float(e3.get())
	Alt=float(e4.get())

	global ser

	if mode.get() == 2 or mode.get() == 3 :
		if sys.platform == "win32":
			ser=serial.Serial("COM"+e5.get(),2400,timeout=0.5)
		if sys.platform == "linux2":
			ser=serial.Serial("/dev/ttyUSB"+e5.get(),2400,timeout=0.5)

	print "You are tracking : "		+str.upper(Sat)+"."
	print "You are at Lat : "		+str(Lat) +\
					" Lon : "		+str(Lon)+\
					" Altitude :"	+str(Alt)+"m"

	line1,line2,Lat,Lon,Alt = GetUserData.get_user_data("gui",Sat,Lat,Lon,Alt)
	GetSat.generate(line1,line2)
	GetLook.generate(Lat,Lon,Alt)

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	if EL>=5:
		#pass_time , maxEL = GetLook.GetPassData(tt,eciSat)
		print "Passing Now ..."
		var_pass_time.set("Passing Now ...")
		#var_maxEL.set(str(maxEL))

	if EL<5:
		pass_time , maxEL = GetLook.GetPassData(tt,eciSat)
		local_time = time.localtime(pass_time)
		print "Next Passing Time:" + time.asctime(local_time)
		var_pass_time.set(str(local_time.tm_year)+"/"+str(local_time.tm_mon)+"/"+str(local_time.tm_mday)+" "+str(local_time.tm_hour)+":"+str(local_time.tm_min)+":"+str(local_time.tm_sec))
		var_maxEL.set(str(maxEL))


	#global timer
	timer = threading.Timer(0.1, fun_timer)
	timer.start()

#Language Choosen GUI
def fun_timer():

	global timer
	global ser

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)

	#Screen Output
	if mode.get() == 1 or mode.get()==3 :

		AZ_flash.set(str(AZ))
		EL_flash.set(str(EL))
	
	#Serial Output
	if mode.get() == 2 or mode.get() ==3 :
		serial_str="AZ"+str(AZ)+" EL"+str(EL)+" Easycomm"
		ser.write(serial_str)

	if stop == 1:
		if mode.get() == 2 or mode.get() == 3 :
			ser.close()

	#Stop fun_timer(y)
	if stop == 0:
		timer = threading.Timer(0.1, fun_timer)
		timer.start()

#Main GUI

root = Tk()
root.title("WRI_Sat_Tracker")
root.wm_minsize(400, 360) 
#	if sys.platform == "win32":
#		root.iconbitmap(sys.path[0]+"/radio.ico")


#Button
ButtonStart = Button(	root, text="Start",			command=start)
ButtonStop = Button(	root, text="Stop",			command=stop)
ButtonUpdate = Button(	root, text="Update Data",	command=update)
#ButtonUpdate = Button(	root, text="Update Data",	command=lambda:update)


ButtonStart.grid(   row=0, column=0, padx=30, pady=5)
ButtonStop.grid(    row=0, column=1, padx=20, pady=5)
ButtonUpdate.grid(  row=0, column=2, padx=20, pady=5)

#UserData
Label(root, text="Sat Name:").	grid(row=1)
Label(root, text="Lat:").		grid(row=2)
Label(root, text="Lon:").		grid(row=3)
Label(root, text="Alt:").		grid(row=4)
Label(root, text="Serial COM").	grid(row=4, column=2)

global e1,e2,e3,e4,e5

e1 = Entry(root, width=10)
e2 = Entry(root, width=10)
e3 = Entry(root, width=10)
e4 = Entry(root, width=10)
e5 = Entry(root, width=10)

e1.grid(row=1, column=1, padx=20, pady=5)
e2.grid(row=2, column=1, padx=20, pady=5)
e3.grid(row=3, column=1, padx=20, pady=5)
e4.grid(row=4, column=1, padx=20, pady=5)
e5.grid(row=5, column=2, padx=20, pady=5)

e1.insert(0,"SO-50")
e2.insert(0,"30")
e3.insert(0,"30")
e4.insert(0,"0")

#Passing Situation

Label(root, text="Passing Time :").grid(row=8, column=0,columnspan=2)
Label(root, text="Max EL :").grid(row=10, column=0,columnspan=2)
global var_pass_time
global var_maxEL
var_pass_time = StringVar()
var_maxEL = StringVar()
Label(root, textvariable=var_pass_time).grid(row=9, column=0,columnspan=2)
Label(root, textvariable=var_maxEL).grid(row=11, column=0,columnspan=2)


#Joke
Label(root, text="Author : BG6WRI").	grid(row=7, column=2)
Label(root, text="From WITARC").		grid(row=8, column=2)
#ButtonJoke = Button(root, text="一键日卫星", command=lambda:var.set("和我没关系啊，你找OpenATS去"))
#ButtonJoke.grid(row=8, column=2)
#var = StringVar()
#Label(root, textvariable=var).grid(	row=9, column=2)


#Output

#Scereen Ready
Label(root,text="AZ").	grid(row=5,column=0)
Label(root,text="EL").	grid(row=5,column=1)

global AZ_flash
global EL_flash

AZ_flash=IntVar()
AZ_flash.set("")
EL_flash=IntVar()
EL_flash.set("")
Entry(root, textvariable=AZ_flash, width=10).grid(row=6, column=0)
Entry(root, textvariable=EL_flash, width=10).grid(row=6, column=1)

#Mode Choose
group = LabelFrame(root, text="Output Mode", padx=5, pady=5)
group.grid(row=1, column=2, padx=10, pady=10, rowspan=3)
LANGS = [("Screen", 1), ("Serial", 2),("Both", 3)]
global mode
mode = IntVar()
mode.set(1)

for lang, num in LANGS:
	b = Radiobutton(group, text=lang, variable=mode, value=num)
	b.pack(anchor=W)


root.bind('<Escape>', lambda e: root.destroy())
root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()
