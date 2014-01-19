import RPi.GPIO as GPIO
import time
import lightcontroller

onOffPinNum = 8
colorLoopPinNum = 7
GPIO.setmode(GPIO.BCM)


GPIO.setup(onOffPinNum, GPIO.IN)
GPIO.setup(colorLoopPinNum, GPIO.IN)
prevOnOffInput = 0
prevColorLoopInput = 0

while True:
    onOffInput = GPIO.input(onOffPinNum)
    if ((not prevOnOffInput) and onOffInput):
        lightcontroller.toggleLights()
    prevOnOffInput = onOffInput

    colorLoopInput = GPIO.input(colorLoopPinNum)
    if ((not prevColorLoopInput) and colorLoopInput):
        lightcontroller.toggleColorLoop()
    prevColorLoopInput = colorLoopInput

    time.sleep(0.05)
