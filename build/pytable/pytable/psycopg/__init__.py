"""psycopg-compatible DBAPI 2.0 database driver

This package allows you to connect pytable to the
GPL psycopg driver.  This package (pytable.psycopg)
is under BSD license, but by including psycopg
driver in your application you *will* be inheriting
the constraints of the driver's license.

The psycopg interface is basically the same as the
PyPgSQL interface, save that it requires dsn-format
connection strings rather than allowing seperate
argument names.
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'psycopg',
	friendlyName = 'PostgreSQL via psycopg',
	value = 'pytable.psycopg.psycodriver.PsycoDriver',
)
