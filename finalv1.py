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
mode = 1
level = 1
device.brightness(level)
refresh = 99
anim = 8	

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def get_song():
	global mode
	url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Olimpus444&api_key=5c7c79f93961f31c57d4f2cf349e027a&format=json&limit=1&nowplaying=true'
	data = json.load(urllib.request(url))
	if 'recenttracks' in data:
		if 'track' in data['recenttracks']:
			if '@attr' in data['recenttracks']['track'][0]:
				print('jest')
				mode = 1
				artistAndTitle = data['recenttracks']['track'][0]['name'] + ' --BY-- ' + data['recenttracks']['track'][0]['artist']['#text']
				return artistAndTitle
			else:
				mode = 2
	
def render_content():
	songString = get_song()
	if (mode == 1):
		device.show_message(songString.upper())
	else:
		now = datetime.now()
		hour = now.hour
		minute = now.minute
		second = now.second
		dot = second % 2 == 0
		# Set hours
		device.letter(1, 8, int(hour / 10))     # Tens
		device.letter(1, 7, hour % 10)     # Ones
		device.letter(1, 6, " ", 1)
		# Set minutes
		device.letter(1, 5, int(minute / 10))   # Tens
		device.letter(1, 4, minute % 10)        # Ones
		device.letter(1, 3, " ", 1)
		# Set seconds
		device.letter(1, 2, int(second / 10))   # Tens
		device.letter(1, 1, second % 10)        # Ones

set_interval(render_content(), 30)