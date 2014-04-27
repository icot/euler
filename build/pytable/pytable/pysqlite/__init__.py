"""MySQLdb-based DBAPI 2.0 database driver
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'SQLite',
	friendlyName = 'SQLite via PySQLite',
	value = 'pytable.pysqlite.sqlitedriver.SQLiteDriver',
)
