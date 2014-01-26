#!/usr/bin/python
import lightcontroller
import RPi.GPIO as GPIO
import time
import threading

shouldStop = threading.Event()
delay = 0.05
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 22

class Potentiometer:
	def __init__(self, analogPinNumber, maxValue, tolerance):
		self.analogPinNumber = analogPinNumber
		self.lastValue = 0
		self.normalizer = 1024 / maxValue
		self.tolerance = tolerance

	def isNew(self):
		reading = int((readadc(self.analogPinNumber, SPICLK, SPIMOSI, SPIMISO, SPICS) / self.normalizer))
		if abs(reading - self.lastValue) > self.tolerance:
			self.lastValue = reading
			return True
		else:
			return False

	def getLastValue(self):
		return self.lastValue


def listenForButton(pinNumber, function): # Assumes high value indicates button is pressed
	GPIO.setup(pinNumber, GPIO.IN)
	prevValue = 0
	while (not shouldStop.isSet()):
		value = GPIO.input(pinNumber)
		if((not prevValue) and value):
			function()
		prevValue = value
		time.sleep(delay)
		
def listenForAnalog():
	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)

	brightness = Potentiometer(0, 255, 10)
	saturation = Potentiometer(1, 255, 10)

	while (not shouldStop.isSet()):
		if brightness.isNew():
			lightcontroller.setAllBrightness(brightness.getLastValue())
		if saturation.isNew():
			lightcontroller.setAllSaturation(saturation.getLastValue())
		time.sleep(delay)


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


def stop():
	shouldStop.set()
	
def start():
	GPIO.setmode(GPIO.BCM)
	shouldStop.clear()
	threading.Thread(target=listenForButton, args=(7, lightcontroller.toggleLights)).start()
	threading.Thread(target=listenForButton, args=(8, lightcontroller.toggleColorLoop)).start()
	threading.Thread(target=listenForButton, args=(25, lightcontroller.toggleColorStrobe)).start()
	threading.Thread(target=listenForAnalog).start()
	
if __name__ == "__main__":
    start()
