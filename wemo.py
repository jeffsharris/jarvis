#!/usr/bin/python

import time
from ouimeaux.environment import Environment
from ouimeaux.signals import statechange, receiver

timeoutTime = 1800 # Wait 30 minutes without motion before turning off the volcano
reactivateTime = 300 # If motion is detected within 5 minutes of turning off, then turn on again. Must be less than timeoutTime
waitTime = 60 # Check if it has timed out every 60 seconds 

def on_motion(motion):
	print "Motion found!", motion.name

def on_switch(switch):
	print "Switch found!", switch.name

env = Environment(on_switch, on_motion)
env.start()
env.discover(seconds=10)

switch = env.get_switch('Volcano')
motion = env.get_motion('Living Room')

lastMovedTime = time.time()
timedOut = False

@receiver(statechange, sender=motion)
def motion_detected(state, sender, signal):
	global lastMovedTime
	if (state == 1):
		print "Motion detected"
		lastMovedTime = time.time()
		
@receiver(statechange, sender=switch)
def switch_detected(state, sender, signal):
	global lastMovedTime
	global timedOut
	if (state == 1):
		print "Switch detected"
		lastMovedTime = time.time()
		timedOut = False
		

print "Waiting for events"
while True:
	env.wait(waitTime)
	print "Switch state is: ", switch.basicevent.GetBinaryState()['BinaryState']
	if ((time.time() - lastMovedTime) > timeoutTime) & (switch.basicevent.GetBinaryState()['BinaryState'] == "1"):
		print "Turning switch off"
		switch.basicevent.SetBinaryState(BinaryState=0)
		timedOut = True
		
	if timedOut & ((time.time() - lastMovedTime) < reactivateTime):
		print "Turning switch back on"
		switch.basicevent.SetBinaryState(BinaryState=1)
		timedOut = False
