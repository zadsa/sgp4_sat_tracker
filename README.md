# SGP4_SAT_TRACKER

## Installation
For ```Python 2.7```
```
$ pip install sgp4 jdcal pyserial requests
```


## CLI Version
Run successfully on both Linux & Windows.  
```
$ python wri_sattrack.py
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

## sat_tracker(not complete)
Use SGP4 model,HMC5883L and MMA8452Q on Raspberry Pi  
And YD-3040 PTZ  
```
$ python track.py
```
![avatar](/image/RPi.jpg)
![avatar](/image/YD-3040.jpg)
## Author
BG6WRI  
 <bg6wri@gmail.com>  

