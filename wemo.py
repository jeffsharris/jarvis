#!/usr/bin/python

import time
from ouimeaux.environment import Environment
from ouimeaux.signals import statechange, receiver

timeoutTime = 1800 # Wait 30 minutes without motion before turning off the volcano
waitTime = 60 # Check if it has timed out every 60 seconds 
	
env = Environment()
env.start()

switch = env.get_switch('Volcano')
motion = env.get_motion('Living Room')

lastMovedTime = time.time()

@receiver(statechange, sender=motion)
def motion_detected(state, sender, signal):
	global lastMovedTime
	if (state == 1):
		print "Motion detected"
		lastMovedTime = time.time()
		
@receiver(statechange, sender=switch)
def switch_detected(state, sender, signal):
	global lastMovedTime
	if (state == 1):
		print "Switch detected"
		lastMovedTime = time.time()

def start():
	print "Waiting for events"
	while True:
		env.wait(waitTime)
		print "Switch state is: ", switch.basicevent.GetBinaryState()['BinaryState']
		if (time.time() - lastMovedTime > timeoutTime) & (switch.basicevent.GetBinaryState()['BinaryState'] == "1"):
			print "Turning switch off"
			switch.basicevent.SetBinaryState(BinaryState=0)
