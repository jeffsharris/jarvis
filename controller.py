#!/usr/bin/python

import physicalcontroller
import server
import threading

if __name__ == "__main__":
	threading.Thread(target=physicalcontroller.start).start()
	threading.Thread(target=server.start).start()