#!/usr/bin/python

import relayBox as rb
import db
import sys

import os
# if 'GATEWAY_INTERFACE' in os.environ:
# 	print ('Running from CGI. Must be called from command line!')
# 	sys.exit(-1)
# else:
#     print ('Not CGI. CLI?')

error = False

# log zone statuses to database
try:
	status = rb.allZoneStatus()
	con = db.DB()
	for z in status:
		con.insertStatus(z)
except:
	print "Unable to read zone statuses"
	error = True

# resolve unfinished actions
try:
	d = db.DB()
	cur = d.findUnfinishedActions() # log in the db a row to move radio buttons back to thermostat

	for row in cur:
		msg = 0 # thermostat mode when upperbits are zero
		msg |= row['zone']
		rb.updateZones(msg) # this sets sone back to thermostat
		print row
except:
	print "Unable to resolve unfinished actions"
	error = True

if error:
	sys.exit(-1)

# print 1
sys.exit(1)

# @todo setup an MTA (mail transfer agent) so I get these errors as emails





