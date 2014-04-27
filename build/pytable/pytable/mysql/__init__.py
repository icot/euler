"""MySQLdb-based DBAPI 2.0 database driver
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'MySQL',
	friendlyName = 'MySQL via MySQLdb',
	value = 'pytable.mysql.mydriver.MyDriver',
)
