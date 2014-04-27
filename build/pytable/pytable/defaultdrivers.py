"""Import packages for all default DBDrivers

This module simply imports the packages for each known
DBDriver.  The Package's __init__ then takes care of
registering the module as being available.

Note: no attempt is made to see if the underlying
	database-driver module is available, so you can't
	take this module's import as meaning the drivers
	are *usable*, only *known*.
"""
from pytable import pypgsql
from pytable import psycopg
from pytable import mysql
from pytable import mk
from pytable import pysqlite
from pytable import pygresql

if __name__ == "__main__":
	fh = open('defaultdrivers.html','w')
	for name in globals().keys():
		module = globals()[name]
		if hasattr( module, 'name' ) and isinstance( module, type(pypgsql)):
			driver = getattr(module,'name')
			fh.write(
				'<tr valign="top"><th align="left">%s</th><td>%s</td><td>%s</td></tr>\n'%(
					driver.name,
					driver.value,
					driver.friendlyName,
				)
			)
			del driver
		del module
	