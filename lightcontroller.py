import json
import requests
import time

baseurl = 'http://10.1.10.45/api/newdeveloper/'
maxHue = 65535

def applyStateToLight(num, state):
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(state));

def getOnLights():
	onLights = set()
	for i in range (0, getNumberOfLights()):
		if (getOnState(i+1)):
			onLights.add(i+1)
	return onLights

def getOnState(num):
	url = baseurl + 'lights/' + str(num)
	r = requests.get(url)
	state = json.loads(r.text)['state']
	return state['on']
	
def getNumberOfLights():
	url = baseurl + 'lights'
	r = requests.get(url)
	return len(json.loads(r.text))

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

		
def loopAllOnLights():
	increment = 1000
	delay = 0.1
	numLights = getNumberOfLights()
	i = 0
	running = True
	
	while running:
		running = False
		for j in range (0, numLights):
			running = running | setHue(j+1, (i + increment*j) % maxHue)
		i += increment
		time.sleep(delay)