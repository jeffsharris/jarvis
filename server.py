import web
import lightcontroller

urls = (
	'/', 'index',
	'/loop', 'loop',
	'/alloff', 'alloff',
	'/allon', 'allon',
	'/toggle', 'toggle',
	'/allbrightness/(.+)', 'allbrightness'
)

class index:
    def GET(self):
		return "Hello, world!"
		
class loop:
	def GET(self):
		lightcontroller.loopAllOnLights()
		
class alloff:
	def GET(self):
		lightcontroller.setAllOff()

class allon:
	def GET(self):
		lightcontroller.setAllOn()

class toggle:
	def GET(self):
		print "Toggling"
		lightcontroller.toggleLights()

class allbrightness:
	def GET(self, brightness):
		print "Setting all brightness to: " + brightness
		lightcontroller.setAllBrightness(int(brightness))
		
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()