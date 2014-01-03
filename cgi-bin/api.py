#!/usr/bin/python
import cgitb; cgitb.enable() #helps with debugging
import sys
import relayBox as rb
import db

def getValidZone():
	zone = form.getvalue("zone")
	if zone == None: # not sure if this is a good idea
		return None
	zone = int(zone)
	if 0 <= zone < rb.numZones:
		return zone
	raise Exception("Invalid zone")

def printUsage():
	print "Content-type: text/html"
	print 
	print "<title> Home Heating System API </title>"
	print "@todo Pring Usage Info"

import cgi
form = cgi.FieldStorage()
action = form.getvalue("action")

if action == None:
	printUsage()
	sys.exit(0)
else:
	action = action.lower()
if action == "read":
	fmt = form.getvalue("fmt")
	zone = getValidZone()
	if (fmt != None and fmt == "raw"):
		print rb.bus.read_byte(rb.address)
	elif zone == None:
		for z in rb.allZoneStatus():
			print z
	else:
		print rb.zoneStatus(zone)
elif action == "numzones":
	print rb.numZones
elif getValidZone() != None:
	message = 0
	if action == "on":
		message |= 1<<4;
	elif action == "off":
		message |= 1<<5;
	# else:
	#	assume thermostat and set 0

	con = db.DB()
	con.insertAction((getValidZone(),action))

	message |= getValidZone()
	
	try:
		rb.bus.write_byte(rb.address, message)
		print 1
	except:
		print -1
else:
	printUsage()

