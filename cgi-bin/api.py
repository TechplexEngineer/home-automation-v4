#!/usr/bin/python


import relayBox as rb

print "Content-type: text/html"
print "" #blank line indicates end of headers
print "<title> Home Heating System API </title>"

def getValidZone():
	zone = form.getvalue("zone")
	if zone == None: # not sure if this is a good idea
		return None
	zone = int(zone)
	if 0 <= zone < rb.numZones:
		return zone
	raise Exception("Invalid zone")

import cgi
form = cgi.FieldStorage()
action = form.getvalue("action")

if action == None:
	print "Documentation to come"
elif action == "read":
	zone = getValidZone()
	if zone == None:
		for z in rb.allZoneStatus():
			print z
	else:
		print rb.zoneStatus(zone)
elif getValidZone() != None:
	message = 0
	if action == "on":
		message |= 1<<4;
	elif action == "off":
		message |= 1<<5;
	# else:
	#	assume thermostat and set 0

	message |= getValidZone()
	print hex(message)

	rb.bus.write_byte(rb.address, message)
else:
	print "Usage"