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

def getInternalTemp():
	tempc = bus.read_byte(boxTempAddy)
	tempf = round((9.0/5.0 * tempc + 32), 2)
	return tempf