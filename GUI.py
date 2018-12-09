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


def start():

	i=language.get()

	global stop
	stop = 0

	Sat=e1.get()
	Lat=float(e2.get())
	Lon=float(e3.get())
	Alt=float(e4.get())

	global ser

	if mode.get() == 2 or mode.get() == 3 :
		if sys.platform == "win32":
			ser=serial.Serial("COM"+e5.get(),9600,timeout=0.5)
		if sys.platform == "linux2":
			ser=serial.Serial("/dev/ttyUSB"+e5.get(),9600,timeout=0.5)

	print "You are tracking : "*i+u"正在追踪: "*(not i)+str.upper(Sat)+"."
	print "You are at Lat : "*i+u"旋转器纬度: "*(not i)+str(Lat)+" Lon : "*i+u" 经度: "*(not i)+str(Lon)+" Altitude :"*i+u" 高度: "*(not i)+str(Alt)+"m"

	line1,line2,Lat,Lon,Alt = GetUserData.get_user_data("gui",Sat,Lat,Lon,Alt)
	GetSat.generate(line1,line2)
	GetLook.generate(Lat,Lon,Alt)

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ,EL = GetLook.GetLook(tt,eciSat)
	
	if EL>=5:
		print "Passing Now ..."*i+u"正在过境 ..."*(not i)
		var.set("Passing Now ..."*i+u"正在过境 ..."*(not i))

	if EL<5:
		pass_time = GetLook.GetPassTime(tt,eciSat)
		local_time = time.localtime(pass_time)
		print "Next Passing Time:"*i+u"过境时间:"*(not i)+time.asctime(local_time)
		var.set(time.asctime(local_time))


	#global timer
	timer = threading.Timer(0.1, fun_timer)
	timer.start()


def stop():
	global stop
	stop = 1

def update():
	GetUserData.update("gui")

def fun_timer():

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
		serial_str="AZ"+str(AZ)+" EL"+str(EL)+"Easycomm Mode"
		ser.write(serial_str)

	if stop == 0:
		timer = threading.Timer(0.1, fun_timer)
		timer.start()

def root_gui():

	i=language.get()
	lang_choose.destroy()

	root = Tk()
	root.title("WRI_Sat_Tracker")
	root.wm_minsize(400, 360) 
#	if sys.platform == "win32":
#		root.iconbitmap(sys.path[0]+"/radio.ico")


	#Button
	ButtonStart = Button(	root, text="Start"*i+u"启动"*(not i),			command=start)
	ButtonStop = Button(	root, text="Stop"*i+u"停止"*(not i),				command=stop)
	ButtonUpdate = Button(	root, text="Update Data"*i+u"更新星历"*(not i),	command=update)
	#ButtonUpdate = Button(	root, text="Update Data",	command=lambda:update)


	ButtonStart.grid(   row=0, column=0, padx=30, pady=5)
	ButtonStop.grid(    row=0, column=1, padx=20, pady=5)
	ButtonUpdate.grid(  row=0, column=2, padx=20, pady=5)

	#UserData
	Label(root, text="Sat Name:"*i+u"目标卫星"*(not i)).grid(	row=1)
	Label(root, text="Lat:"*i+u"纬度"*(not i)).grid(				row=2)
	Label(root, text="Lon:"*i+u"经度"*(not i)).grid(				row=3)
	Label(root, text="Alt:"*i+u"高度"*(not i)).grid(				row=4)
	Label(root, text="Serial COM"*i+u"串口号"*(not i)).grid(		row=4, column=2)

	global e1,e2,e3,e4,e5

	e1 = Entry(root, width=10)
	e2 = Entry(root, width=10)
	e3 = Entry(root, width=10)
	e4 = Entry(root, width=10)
	e5 = Entry(root, width=10)


#	e1.insert(0,"SO-50")
#	e2.insert(0,"30")
#	e3.insert(0,"30")
#	e4.insert(0,"0")

	e1.grid(row=1, column=1, padx=20, pady=5)
	e2.grid(row=2, column=1, padx=20, pady=5)
	e3.grid(row=3, column=1, padx=20, pady=5)
	e4.grid(row=4, column=1, padx=20, pady=5)
	e5.grid(row=5, column=2, padx=20, pady=5)


	#Passing Situation

	Label(root, text="Passing Time :"*i+"过境时间 :"*(not i)).grid(row=8, column=0,columnspan=2)
	global var
	var = StringVar()
	Label(root, textvariable=var).grid(row=9, column=0,columnspan=2)



	#Joke
	Label(root, text="Design by BG6WRI").grid(		row=7, column=2)
	Label(root, text="From WITARC").grid(	row=8, column=2)
	#ButtonJoke = Button(root, text="一键日卫星", command=lambda:var.set("和我没关系啊，你找OpenATS去"))
	#ButtonJoke.grid(row=8, column=2)
	#var = StringVar()
	#Label(root, textvariable=var).grid(	row=9, column=2)
	

	#Output

	#Scereen Ready
	Label(root,text="AZ"*i+"方位角"*(not i)).grid(row=5,column=0)
	Label(root,text="EL"*i+"仰角"*(not i)).grid(row=5,column=1)
	global AZ_flash
	global EL_flash
	AZ_flash=IntVar()
	AZ_flash.set("")
	EL_flash=IntVar()
	EL_flash.set("")
	Entry(root, textvariable=AZ_flash, width=10).grid(row=6, column=0)
	Entry(root, textvariable=EL_flash, width=10).grid(row=6, column=1)

	#Mode Choose
	group = LabelFrame(root, text="output Mode"*i+u"输出模式"*(not i), padx=5, pady=5)
	group.grid(row=1, column=2, padx=10, pady=10, rowspan=3)
	LANGS = [("Screen"*i+u"屏幕"*(not i), 1), ("Serial"*i+u"串口"*(not i), 2),("Both"*i+u"俩都"*(not i), 3)]
	global mode
	mode = IntVar()
	mode.set(1)

	for lang, num in LANGS:
		b = Radiobutton(group, text=lang, variable=mode, value=num)
		b.pack(anchor=W)

	root.mainloop()


#----lang_choose_gui----
lang_choose = Tk()
lang_choose.title("language_choose")
#lang_choose.wm_minsize(400, 360)

#Readme
#readme="Thanks to : \n\nOpenATS\nTurbo\nBG0AUB"
#Label(lang_choose, text=readme).grid(row=2, column=1)


#Language Choose

lang_group = LabelFrame(lang_choose, text="Language/语言", padx=5, pady=5)
lang_group.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
LANGUAGES = [(u"English/英文", 1), (u"Chinese/中文", 0),]

language = IntVar()
language.set(1)

for lang, lang_num in LANGUAGES:
	c = Radiobutton(lang_group, text=lang, variable=language, value=lang_num)
	c.pack(anchor=W)

#global i
#i=language.get()

ButtonLangChoose = Button(lang_choose, text="Start/启动",command=lambda:root_gui())
ButtonLangChoose.grid(row=3, column=0, padx=30, pady=5)

lang_choose.mainloop()
