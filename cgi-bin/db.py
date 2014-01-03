#!/usr/bin/python

import sqlite3 as lite
import sys

class DB:
	def __init__(self):
		self.con = lite.connect('/var/www/db/log.db')

		if not _tableExitsts('zone_log', self.con):
			print 'creating zone_log'
			cur = self.con.cursor()
			cur.execute('''
			CREATE TABLE zone_log(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				zone INTEGER,
				status VARCHAR(24),
				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
			);
			''')
			self.con.commit()
		if not _tableExitsts('zone_action', self.con):
			print 'creating zone_action'
			cur = self.con.cursor()
			cur.execute('''
			CREATE TABLE zone_action(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				zone INTEGER,
				action VARCHAR(24),
				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
			);
			''')
			self.con.commit()

	def tableExitsts(self, table):
		return _tableExitsts(table, self.con)
	def insertStatus(self, status):
		cur = self.con.cursor()
		cur.execute('''
			INSERT INTO zone_log (zone, status)
			VALUES (%d,"%s");
		'''%status)
		self.con.commit()
	def insertAction(self, status):
		cur = self.con.cursor()
		cur.execute('''
			INSERT INTO zone_action (zone, action)
			VALUES (%d,"%s");
		'''%status)
		self.con.commit()

def _tableExitsts(table, con):
		cur = con.cursor()
		exists = '''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='%s' GROUP BY name;'''%(table)
		cur.execute(exists)
		data = cur.fetchone()

		if data == None:
			return False
		return True

if __name__ == "__main__":
	d = DB()