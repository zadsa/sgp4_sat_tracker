from flask import Flask
from flask import render_template, redirect,url_for
from flask import request

import time
import serial
import GetUserData
import GetSat
import GetLook

app = Flask(__name__)



@app.route('/track', methods=['POST','GET'])
def track():
	error = None
	if request.method == 'POST':

		Sat=str(request.form['satname'])
		Lat=float(request.form['lat'])
		Lon=float(request.form['lon'])
		Alt=float(request.form['alt'])

		line1,line2,Lat,Lon,Alt = GetUserData.get_user_data("gui",Sat,Lat,Lon,Alt)
		GetSat.generate(line1,line2)
		GetLook.generate(Lat,Lon,Alt)

		tt = time.time()
		eciSat = GetSat.get_eciSat(tt)
		AZ,EL = GetLook.GetLook(tt,eciSat)



		if request.form['satname']=='SO-50':
			print AZ,EL

		context={
			'az':AZ,
			'el':EL
		}
		return render_template('track.html',**context)




	return render_template('track.html', error=error)




if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0',80)