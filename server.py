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

app = Flask(__name__)


@app.route('/track', methods=['GET'])
def index():
    context = {
        'lat': 0,
        'lon': 0,
        'alt': 0,
        'az': 0,
        'el': 0
    }
    return render_template('track.html', **context)


@app.route('/tracker', methods=['POST', "GET"])
def track():
    receive = request.json
    if receive['lat'] == "update":
        GetUserData.update("gui")
        res = {
            'az': "Update Done",
            'el': "	",
        }
    else:
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


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 8080)
