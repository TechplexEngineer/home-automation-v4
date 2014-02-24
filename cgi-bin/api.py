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
	print "@todo Print Usage Info"

def printJsonHeader():
	print "Content-type: application/json"
	print 

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
		print rb.getZoneStatus()
	elif zone == None:
		for z in rb.allZoneStatus():
			print z
	else:
		print rb.zoneStatus(zone)
elif action == "numzones":
	print rb.numZones
elif action == "temp":
	printJsonHeader()
	data = dict()
	data['internal'] = rb.getInternalTemp();
	data['tank_top'] = rb.getTopTemp();
	data['tank_mid'] = rb.getMidTemp();
	data['tank_bot'] = rb.getBotTemp();
	data['boiler_supply'] = 50;
	data['boiler_return'] = 50;
	import json
	print json.dumps(data)
elif getValidZone() != None:
	message = 0
	if action == "on":
		message |= 1<<4;
	elif action == "off":
		message |= 1<<5;
	# else:
	#	assume thermostat and set 0

	con = db.DB()
	exp = con.insertAction((getValidZone(),action))

	message |= getValidZone()
	
	# try:
	rb.updateZones(message)
	print exp
	# except:
	# 	print -1
else:
	printUsage()

