import json
import requests
import time

baseurl = 'http://10.1.10.45/api/newdeveloper/'

def setColor(num, hue):
	body = {"on":True, "sat":255, "bri":255, "hue":hue}
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(body));

	
def turnOff(num):
	body = {"on":False}
	url = baseurl + 'lights/' + str(num) + '/state'
	r = requests.put(url, data=json.dumps(body));

def loopColor(num):
	for i in range(0, 65535, 1000):
		setColor(num, i)
		time.sleep(0.1)


#setColor(5, 10000)
#turnOff(3)
loopColor(1)