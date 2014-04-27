"""PyGreSQL-based DBAPI 2.0 database driver
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'PyGreSQL',
	friendlyName = 'PostgreSQL via PyGreSQL',
	value = 'pytable.pygresql.pgdriver.PGDriver',
)
