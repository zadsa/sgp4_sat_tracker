# SGP4_SAT_TRACKER
Author: BG6WRI  
Email: <bg6wri@gmail.com>  


Whatever version you need,you should run this at first:
```
$ pip install sgp4 jdcal pyserial requests
(use “sudo pip” on Linux)
```


## wri_sattrack
Run successfully on both Linux & Windows.  
Just python it!  


```
$ python wri_sattrack.py
```
Follow the guide to enter the name of the Sat you want to track and enter your Coordinates.  


## GUI Version
This program can be run in both Opration Systems.  
But on Windows,Just ‘Python 2.7’ can run it well because of the ‘Tkinter’ package.  

```
$ sudo apt-get install python-tk
(only for Linux ↑）

$ python GUI.py
```
Output Mode include Screen,Serial,or both of them.  
You can choose it freely. 

## sat_tracker
Use SGP4 model,HMC5883L and MMA8452Q on Raspberry Pi  

```
$ python track.py
```