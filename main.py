import time
from discovery import Discovery
from lib.qhue.qhue import Bridge, QhueException
from lib.pcduino import gpio

bridges = Discovery.find()
b = None
uname = None

btnPin = 'gpio8'

def authBridge():
	global uname
	b = Bridge(bridges[0])
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

def toggleLight():
	isOn = b.lights[1]()['state']['on']
	b.lights[1].state(on=!isOn)

def setup():
	global b
	searchKey()
	b = Bridge(bridges[0], uname)
	'''
	b.lights[1].state(on=True, bri=255)
	time.sleep(1)
	b.lights[1].state(on=False)
	print "End here " + uname
	toggleLight()
	'''
	gpio.pin_mode(btnPin, gpio.INPUT)

def loop():
	read = gpio.digital_read(btnPin)
	if read:
		toggleLight()
		print "Light 1 toggled"
	time.sleep(.5)

def main():
	setup()
	while True:
		loop()

main()
