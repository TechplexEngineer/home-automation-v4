#!/usr/bin/python
import cgitb; cgitb.enable() #helps with debugging
import smbus

bus = smbus.SMBus(1)
address = 0x04
numZones = 6

def allZoneStatus():
	data = bus.read_byte_data(address, 1)
	for z in range(0,numZones):
		yield z, bool(data&(1<<z))

print "Content-type: text/html"
print 
print "<title>Home Heating System Status</title>"

for z in allZoneStatus():
	print z