#!/usr/bin/python

import sqlite3
import sys

class DB:
	def __init__(self):
		self.con = sqlite3.connect('/var/www/db/log.db')
		self.con.row_factory = sqlite3.Row #dict_factory

		if not _tableExitsts('zone_log', self.con) and not _tableExitsts('zone_action', self.con):
			print "Remember to 'sudo chgrp www-data log.db' and 'sudo chmod g+rw log.db'"
		# if not _tableExitsts('zone_log', self.con):
		# 	print 'creating zone_log'
		cur = self.con.cursor()
		cur.execute('''
		CREATE TABLE IF NOT EXISTS zone_log(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			zone INTEGER,
			status VARCHAR(24),
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
		);
		''')
		self.con.commit()

		# if not _tableExitsts('zone_action', self.con):
		# 	print 'creating zone_action'
		cur = self.con.cursor()
		cur.execute('''
		CREATE TABLE IF NOT EXISTS zone_action(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			zone INTEGER,
			action VARCHAR(24),
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			expiration DATETIME,
			finished INTEGER DEFAULT 0
		);
		''')
		self.con.commit()

		cur = self.con.cursor()
		cur.execute('''
			CREATE VIEW IF NOT EXISTS last_zone_action AS 
			SELECT * FROM zone_action GROUP BY zone ORDER BY timestamp;
		''')
		self.con.commit()

	def tableExitsts(self, table):
		return _tableExitsts(table, self.con)

	# Status is the table which stores the status of each zone (called from cron)
	# @todo when user uses ctrl panel, should the new zone state be recorded?
	def insertStatus(self, status):
		cur = self.con.cursor()
		cur.execute('''
			INSERT INTO zone_log (zone, status)
			VALUES (%d,"%s");
		'''%status)
		self.con.commit()

	# zone_Action is a log of all the actions taken from the control panel
	# returns the expiration time
	def insertAction(self, status):
		cur = self.con.cursor()
		a = cur.execute('''
			INSERT INTO zone_action (zone, action, expiration)
			VALUES (%d,"%s", (SELECT datetime('now', '1 hours')));
		'''%status)
		self.con.commit()
		cur.execute('''
			SELECT expiration FROM zone_action WHERE id=%d;
			'''%(a.lastrowid))
		return cur.fetchone()['expiration']
		

	# finds unfinished actions which have expired {# and sets their finished flag #}
	def findUnfinishedActions(self):
		cur = self.con.cursor()
		a = cur.execute('''
			SELECT * FROM last_zone_action 
			WHERE NOT finished 
			AND action IS NOT 'thermostat' 
			AND expiration < (SELECT datetime('now'));
		''')
		# return a
		for row in a:
			yield row
			cur = self.con.cursor()
			a = cur.execute('''
				UPDATE zone_action SET finished = 1
				WHERE id = %d
				'''%(row['id']))
			self.con.commit()

			cur = self.con.cursor()
			cur.execute('''
				INSERT INTO zone_action (zone, action, expiration, finished)
				VALUES (%d,"%s", (SELECT datetime('now'),1));
			'''%(row['zone'],'thermostat'))
			self.con.commit()
		# @todo it would be nice to have a +-15 min window as the cron job only runs every 30 mins

# This is outside the class so it can be used within the consructor
def _tableExitsts(table, con):
		cur = con.cursor()
		exists = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='%s' GROUP BY name;'''%(table)
		cur.execute(exists)
		data = cur.fetchone()

		if data == None:
			return False
		return True

# When called from the command line make sure the tables exist
if __name__ == "__main__":
	d = DB()