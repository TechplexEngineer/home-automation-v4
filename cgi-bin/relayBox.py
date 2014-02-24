import smbus

bus = smbus.SMBus(1)
arduinoI2CAddy = 0x04
boxTempAddy = 0x49
numZones = 6	# must be less than 16

def allZoneStatus():
	data = bus.read_byte(arduinoI2CAddy)
	for z in range(0,numZones):
		yield z, bool(data&(1<<z))

def zoneStatus(zone):
	data = bus.read_byte(arduinoI2CAddy)
	return zone, bool(data&(1<<zone))

def getZoneStatus():
	return bus.read_byte(arduinoI2CAddy)

def updateZones(message):
	bus.write_byte(arduinoI2CAddy, message)

def c2f(tempc):
	return round((9.0/5.0 * tempc + 32), 2)

def getInternalTemp():
	tempc = bus.read_byte(boxTempAddy)
	return c2f(tempc)

def getTopTemp():
	tempc = bus.read_byte(0x4F)
	return c2f(tempc)

def getMidTemp():
	tempc = bus.read_byte(0x4E)
	return c2f(tempc)

def getBotTemp():
	tempc = bus.read_byte(0x4D)
	return c2f(tempc)