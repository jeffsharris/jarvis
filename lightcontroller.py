#!/usr/bin/python

import json
import requests
import time
import threading

baseurl = 'http://10.1.10.45/api/newdeveloper/'
maxHue = 65535
threadInProgress = threading.Event()


def applyStateToLight(num, state):
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(state));
	
def getHue(num):
	return getStateProperty(num, 'hue')

def getOnLights():
	onLights = set()
	for i in range (0, getNumberOfLights()):
		if (getOnState(i+1)):
			onLights.add(i+1)
	return onLights

def getOnState(num):
	return getStateProperty(num, 'on')
	
def getNumberOfLights():
	url = baseurl + 'lights'
	r = requests.get(url)
	return len(json.loads(r.text))
	
def getStateProperty(num, property):
	url = baseurl + 'lights/' + str(num)
	r = requests.get(url)
	state = json.loads(r.text)['state']
	return state[property]

# Concurrency hack. Keep looping through the lights in case something else is touching them.
def setAllOff():
	while (len(getOnLights()) > 0): 
		for i in getOnLights():
			setOff(i)

def setAllOn():
	for i in range (0, getNumberOfLights()):
		setOn(i+1)

def setAllToColor(hue):
	for i in range (0, getNumberOfLights()):
		setHue(i + 1, hue)

def setAllToWhite():
	for i in range (0, getNumberOfLights()):
		setSaturation(i+1, 0)
		
def setBrightness(num, brightness):
	if(getOnState(num)):
		applyStateToLight(num, {"bri":brightness})
		return True
	return False
	
def setAllBrightness(brightness):
	for i in range(0, getNumberOfLights()):
		setBrightness(i+1, brightness)

# Returns True if color was set. False if the light was already off.
def setHue(num, hue):
	if(getOnState(num)):
		body = {"hue":hue}
		applyStateToLight(num, body)
		return True
	return False
	
def setSaturation(num, saturation):
	if(getOnState(num)):
		body = {"sat":saturation}
		applyStateToLight(num, body)
		return True
	return False

def setLightOnOff(num, on):
	body = {"on":on}
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(body));
	
def setOff(num):
	setLightOnOff(num, False)	
		
def setOn(num):
	setLightOnOff(num, True)
	
def toggleLights():
	if len(getOnLights()) > 0:
		setAllOff()
	else:
		setAllOn()

def toggleColorLoop():
	if (threadInProgress.isSet()):
		threadInProgress.clear()
	else:
		threadInProgress.set()
		threading.Thread(target=loopColors, args = (2000,0.1)).start()
	
def loopColors(increment, delay):
	i = 0
	numLights = getNumberOfLights()
	while threadInProgress.isSet():
		for j in range (0, numLights):
			setHue(j+1, (i + increment*j) % maxHue)
		i += increment
		time.sleep(delay)	
	
