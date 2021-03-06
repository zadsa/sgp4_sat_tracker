# SGP4_SAT_TRACKER

## Installation
For ```Python 2.7```
```
$ sudo apt-get install python-pip git
$ sudo pip install sgp4 jdcal pyserial requests wiringpi
$ git clone https://github.com/BG6WRI/sgp4_sat_tracker
$ cd sgp4_sat_tracker
```


## CLI Version
Run successfully on both Linux & Windows.  
```
$ python CLI.py
```
Follow the guide to enter the name of the Sat you want to track and enter your Coordinates.  


## GUI Version
Run successfully on both Linux & Windows.   
But just on ```Python 2``` because of the ‘Tkinter’ package.  
```
$ sudo apt-get install python-tk
(only for Linux ↑）

$ python GUI.py
```
Output Mode include Screen,Serial,or both of them.  

## WEB Version(not complete)
As a example, Visit http://bg6wri.tk:8080  
```
$ sudo pip install Flask
$ python server.py
```
On PC, Then visit http://127.0.0.1:8080 to use the web Tracker.  
On Raspberry Pi, Then visit http://raspberrypi:8080 to use the web Tracker.  

## Hardware
Use SGP4 model,HMC5883L MMA8452Q and LSM303DLH on Raspberry Pi  
And YD-3040 PTZ  
![avatar](/image/RPi.jpg)
![avatar](/image/YD-3040.jpg)  
![avatar](/image/HMC5883L.jpg)
![avatar](/image/MMA8452Q.jpg)
![avatar](/image/LSM303DLH.jpg)  
## Acknowledgements

- All credit goes to [OpenATS](https://github.com/OpenATS) , Thanks for his work.
- Thanks to [HaveTwoBrush](https://github.com/HaveTwoBrush) .


## Author
BG6WRI  
 <bg6wri@gmail.com>  

