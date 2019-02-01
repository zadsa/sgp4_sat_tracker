#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

import time
import serial
import GetUserData
import GetSat
import GetLook
from Pelco_D import Tracker

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	context = {
		'lat': 0,
		'lon': 0,
		'alt': 0,
		'az': 0,
		'el': 0
	}
	return render_template('index.html', **context)

@app.route('/update', methods=['POST', "GET"])
def update():
	GetUserData.update("gui")
	res = {
		'az': "Update Done",
		'el': "	",
	}
	return jsonify(res)


@app.route('/predict', methods=['POST', "GET"])
def predict():
	receive = request.json

	Sat = str(receive['satname'])
	Lat = float(receive['lat'])
	Lon = float(receive['lon'])
	Alt = float(receive['alt'])

	line1, line2, Lat, Lon, Alt = GetUserData.get_user_data("gui", Sat, Lat, Lon, Alt)
	GetSat.generate(line1, line2)
	GetLook.generate(Lat, Lon, Alt)

	tt = time.time()
	eciSat = GetSat.get_eciSat(tt)
	AZ, EL = GetLook.GetLook(tt, eciSat)

	res = {
		'az': AZ,
		'el': EL
	}
	return jsonify(res)

@app.route('/newTracker', methods=['POST', "GET"])
def newTracker():
	global Tracker
	Tracker = Tracker("/dev/ttyUSB0",2400)
	return "ok"


@app.route('/setstep', methods=['POST', "GET"])
def setstep():

	receive = request.json

	global Tracker
	receive = request.json
	if receive['cmd'] == "LD":
		Tracker.down()
		Tracker.left()
	if receive['cmd'] != "LD":
		if receive['cmd'] == "up":
			Tracker.up()
		if receive['cmd'] == "down":
			Tracker.down()
		if receive['cmd'] == "left":
			Tracker.left()
		if receive['cmd'] == "right":
			Tracker.right()
		time.delay(0.5)
		Tracker.stop()

	return "ok"

@app.route('/track', methods=['POST', "GET"])
def track():
	receive = request.json
	if receive['lat'] == "update":
		GetUserData.update("gui")
		res = {
			'az': "Update Done",
			'el': "	",
		}

	return jsonify(res)

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0', 8080)
