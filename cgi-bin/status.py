#!/usr/bin/python
import cgitb; cgitb.enable() #helps with debugging
import relayBox as rb

print "Content-type: text/html"
print 
print "<title>Home Heating System Status</title>"

for z in rb.allZoneStatus():
	print z