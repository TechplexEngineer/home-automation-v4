#!/usr/bin/python

import relayBox as rb
import db
import sys

import os
if 'GATEWAY_INTERFACE' in os.environ:
	print ('CGI')
	sys.exit(-1)
# else:
#     print ('Not CGI. CLI?')

try:
	status = rb.allZoneStatus()

	con = db.DB()

	for z in status:
		con.insertStatus(z)
except:
	print -1
	sys.exit(-1)

print 1
sys.exit(1)





