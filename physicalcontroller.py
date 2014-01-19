#!/usr/bin/python
import lightcontroller
import RPi.GPIO as GPIO
import time
import threading

shouldStop = threading.Event()
delay = 0.05

def listenForButton(pinNumber, function): # Assumes high value indicates button is pressed
	GPIO.setup(pinNumber, GPIO.IN)
	prevValue = 0
	while (not shouldStop.isSet()):
		value = GPIO.input(pinNumber)
		if((not prevValue) and value):
			function()
		prevValue = value
		time.sleep(delay)
		
def stop():
	shouldStop.set()
	
def start():
	GPIO.setmode(GPIO.BCM)
	threading.Thread(target=listenForButton, args=(7, lightcontroller.toggleColorLoop)).start()
	threading.Thread(target=listenForButton, args=(8, lightcontroller.toggleLights)).start()
	