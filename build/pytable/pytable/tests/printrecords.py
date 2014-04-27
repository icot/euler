#! /usr/bin/env python
"""Print out the current records in a given table as a set of default records"""
from pytable import sqlquery, specifierfromoptions
import sys, pprint, itertools

query = sqlquery.SQLQuery( """SELECT * FROM %(tableName)s""" )

def fixValue( description, value, driver ):
	"""Given field description and value, return key,value"""
	try:
		type = driver.localToSQLType( description[1] )
	except Exception, err:
		pass 
	else:
		if type == 'bool' and value is not None:
			value = bool( value )
		elif type in ('timestamp','timestamptz','date') and value:
			value = value.Format( '%Y-%m-%d %H:%M:%S %Z' )
		elif type in ('numeric','decimal'):
			value = str(value)
	return description[0], value 

def withNames( record, recordSet ):
	driver = recordSet.connection.driver
	for description,value in zip( recordSet.description, record ):
		key,value = fixValue( description, value, driver )
		if value is not None:
			yield key,value

def formatRecords( specifier, tableName ):
	driver, connection = specifier.connect()
	recordSet = query( connection, tableName=tableName )
	result = ['%(tableName)s.defaultRecords = ['%locals()]
	for record in recordSet:
		result.append( '{' )
		for key,value in withNames( record, recordSet ):
			result.append( '\t%r : %r,'%( key,value) )
		result.append( '},' )
	result.append( ']' )
	return "\n".join( result )


if __name__ == "__main__":
	specifier = specifierfromoptions.specifierFromOptions()
	
	tables = sys.argv[1:]
	for table in tables:
		print formatRecords( specifier, table )
