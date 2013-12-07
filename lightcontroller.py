import json
import requests
import time

baseurl = 'http://10.1.10.45/api/newdeveloper/'
maxHue = 65535

def setColor(num, hue):
	body = {"on":True, "sat":255, "bri":255, "hue":hue}
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(body));
	
def setAllToColor(hue):
	for i in range (0, countLights()):
		setColor(i + 1, hue)

def toggleLight(num, on):
	body = {"on":on}
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(body));
	
def turnOff(num):
	toggleLight(num, False)
	
def turnAllOff():
	for i in range (0, countLights()):
		turnOff(i+1)
		
def turnOn(num):
	toggleLight(num, True)

def turnAllOn():
	for i in range (0, countLights()):
		turnOn(i+1)
		
	
def countLights():
	url = baseurl + 'lights'
	r = requests.get(url)
	return len(json.loads(r.text))

def loopColor(num):
	for i in range(0, maxHue, 1000):
		setColor(num, i)
		time.sleep(0.1)
		
def loopAllLights():
	increment = 1000
	delay = 0.1
	numLights = countLights()
	i = 0
	
	while True:
		for j in range (0, numLights):
			setColor(j+1, (i + increment*j) % maxHue)
		i += increment
		time.sleep(delay)
	


#setColor(5, 10000)
#turnOff(3)
#loopColor(1)
loopAllLights()
setAllToColor(10000)