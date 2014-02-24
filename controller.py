#!/usr/bin/python

import physicalcontroller
import server
import threading
import wemo

if __name__ == "__main__":
	threading.Thread(target=physicalcontroller.start).start()
	threading.Thread(target=server.start).start()
	threading.Thread(target=wemo.start).start()
