import time
from discovery import Discovery
from lib.qhue.qhue import Bridge, QhueException

bridges = Discovery.find()
uname = None

def authBridge():
	global uname
	bridgePressed = False
	while not bridgePressed:
		try:
			resp = b(devicetype="pcduino-hue-control", http_method="post")
			bridgePressed = True
			print "Successfully authenticated!"
			uname = resp[0]['success']['username']
			fileKey = open('.huekey', 'w')
			fileKey.write(uname)
			fileKey.close()
		except QhueException, e:
			print e
			bridgePressed = False

def searchKey():
	global uname
	try:
		keyFile = open('.huekey', 'r')
		uname = keyFile.read()
		keyFile.close()
	except Exception, e:
		print "File not found; authenticate now."
		authBridge()

searchKey()
b = Bridge(bridges[0], uname)

b.lights[1].state(on=True, bri=255)
time.sleep(1)
b.lights[1].state(on=False)
print "End here " + uname
