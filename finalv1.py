#!/usr/bin/env python

# arhn.eu subscription counter for ZEROSEG sample
# Based on the ZEROSEG example libraries
#
# This script requires the ZeroSeg library
# located at
# https://github.com/AverageManVsPi/ZeroSeg

import ZeroSeg.led as led
import time
import random
from datetime import datetime
import urllib.request
import json
import RPi.GPIO as GPIO
import threading
switch1 = 17
switch2 = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch1, GPIO.IN)
GPIO.setup(switch2, GPIO.IN) 

tick = 0
auto = 0
		
def autogo():
	global mode
	threading.Timer(10.0, autogo).start()
	global auto
	if auto == 1:
		mode += 1
		if mode == 3:
			mode = 1
		print "Auto Switch: ", mode
		
		
device = led.sevensegment(cascaded=2)

autogo()


time.sleep(2)
mode = 1;
level = 1;
device.brightness(level)
refresh = 99;
anim = 8;		

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def get_song():
	with urllib.request('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Olimpus444&api_key=5c7c79f93961f31c57d4f2cf349e027a&format=json&nowplaying=true') as response:
		response = response.read()
		artistAndTitle = response.recenttracks.track[0].name + response.recenttracks.track[0].artist['#text']

		device.show_message(artistAndTitle, delay=0.1)

while True:
	if mode == 1:
		set_interval(get_song(), 10)
	# now = datetime.now()
	# if mode == 1:
	# 	hour = now.hour
	# 	minute = now.minute
	# 	second = now.second
	# 	dot = second % 2 == 0
	# 	# Set hours
	# 	device.letter(1, 8, int(hour / 10))     # Tens
	# 	device.letter(1, 7, hour % 10)     # Ones
	# 	device.letter(1, 6, " ", 1)
	# 	# Set minutes
	# 	device.letter(1, 5, int(minute / 10))   # Tens
	# 	device.letter(1, 4, minute % 10)        # Ones
	# 	device.letter(1, 3, " ", 1)
	# 	# Set seconds
	# 	device.letter(1, 2, int(second / 10))   # Tens
	# 	device.letter(1, 1, second % 10)        # Ones
	# if mode == 2:
	# 	day = now.day
	# 	month = now.month
	# 	year = now.year - 2000

	# 	# Set day
	# 	device.letter(1, 8, int(day / 10))     # Tens
	# 	device.letter(1, 7, day % 10)          # Ones
	# 	device.letter(1, 6, '-')               # dash
	# 	# Set day
	# 	device.letter(1, 5, int(month / 10))     # Tens
	# 	device.letter(1, 4, month % 10)     # Ones
	# 	device.letter(1, 3, '-')               # dash
	# 	# Set day
	# 	device.letter(1, 2, int(year / 10))     # Tens
	# 	device.letter(1, 1, year % 10)     # Ones
	if mode == 3:
		auto = 1;	
		mode = 1;
	
	if not GPIO.input(switch2):
		if auto == 1:
			auto = 0
			mode = 1
			print "Auto Off"
		elif mode < 4:
			mode += 1
		else:
			mode = 1
		if mode == 1:
			device.write_text(1, "CZAS")
		if mode == 2:
			device.write_text(1, "DATA")
		if mode == 3:
			device.write_text(1, "AUTO")
		time.sleep(1)
	#wskaznik jasnosci
	elif not GPIO.input(switch1):
		if level <= 2:
			level = 5
		elif level == 5:
			level = 10
		elif level == 10:
			level = 14
		elif level >= 14:
			level = 1
		device.brightness(level)
		print "Poziom jasnosci:", level
		time.sleep(0.5);
