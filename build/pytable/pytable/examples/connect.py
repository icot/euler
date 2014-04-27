"""Simple connection example

This just shows how to use a dbspecifier
object to connect to a particular database.

Note: you need a database named test running
on the specified host, with given user and
password to run this script!
"""
from pytable import dbspecifier

specifier = dbspecifier.DBSpecifier(
	drivername = "PyPgSQL",
	host = "localhost",
	user = "test",
	password = "password",
	database = "test",
)

driver, connection = specifier.connect( )
print "Driver:", driver
print "Connection:", connection
cursor = connection.cursor()
cursor.execute( """SELECT 42;""" )
print "Life:", cursor.fetchall()