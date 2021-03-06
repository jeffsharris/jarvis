#!/usr/bin/python
import web
import lightcontroller

urls = (
	'/', 'index',
	'/colorloop', 'colorloop',
	'/colorstrobe', 'colorstrobe',
	'/alloff', 'alloff',
	'/allon', 'allon',
	'/toggle', 'toggle',
	'/allbrightness/(\d+)', 'allbrightness'
)

class index:
    def GET(self):
		return "Hello, world!"
		
class colorloop:
	def GET(self):
		lightcontroller.toggleColorLoop()
		
class colorstrobe:
	def GET(self):
		lightcontroller.toggleColorStrobe()
		
class alloff:
	def GET(self):
		lightcontroller.setAllOff()

class allon:
	def GET(self):
		lightcontroller.setAllOn()

class toggle:
	def GET(self):
		lightcontroller.toggleLights()

class allbrightness:
	def GET(self, name):
		lightcontroller.setAllBrightness(int(name))

def start():
	app = web.application(urls, globals())
	app.run()

if __name__ == "__main__":
    start()
