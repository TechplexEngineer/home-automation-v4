#!/usr/bin/python

import relayBox as rb
import db
import sys

import os
if 'GATEWAY_INTERFACE' in os.environ:
	print ('Running from CGI. Must be called from command line!')
	sys.exit(-1)
# else:
#     print ('Not CGI. CLI?')

try:
	status = rb.allZoneStatus()

	con = db.DB()

	for z in status:
		con.insertStatus(z)
except:
	print "Unable to read zone statuses"
	sys.exit(-1)

# print 1
sys.exit(1)





