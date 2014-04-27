"""PyPgSQL-based DBAPI 2.0 database driver
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'PyPgSQL',
	friendlyName = 'PostgreSQL via PyPgSQL',
	value = 'pytable.pypgsql.pgdriver.PGDriver',
)
