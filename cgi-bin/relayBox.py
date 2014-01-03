import smbus

bus = smbus.SMBus(1)
address = 0x04
numZones = 6	# must be less than 16

def allZoneStatus():
	data = bus.read_byte(address)
	for z in range(0,numZones):
		yield z, bool(data&(1<<z))

def zoneStatus(zone):
	data = bus.read_byte(address)
	return zone, bool(data&(1<<zone))