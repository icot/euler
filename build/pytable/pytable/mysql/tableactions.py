"""Actions for the MySQL table

These are meta-queries/actions, they tell us about
the structure of the database schema by directly
querying the postgresql system catalogs.  They are
therefor entirely non-portable, evil things, but
they do appear to get the job done :) .
"""
from pytable import sqlquery, dbschema
from basicproperty import common

class TableStructure (sqlquery.SQLQuery ):
	"""Reverse-engineer table structure/schema from database

	This is a very heavy mechanism for design-time use
	which attempts to describe a table in the database
	using the dbschema objects which would normally
	be used to proactively define how we interact with
	the table.

	There are actually three different queries being
	done during the TableStructure query.  The first
	is the base query, which simply retrieves the
	DB API 2.0 column descriptions.  These provide
	much of the basic information required.

	The second stage retrieves the foreign-key
	constraints for the table.  Eventually this should
	also return general constraints (check restraints)
	to allow for automatically setting up constraint
	numeric and/or string data types.

	The third stage retrieves information about indices
	on the table.  This includes primary, unique and
	multi-field indices, but not check indices.
	"""
	sql = """
	SELECT *
	FROM %(tableName)s
	LIMIT 1;"""
	def processResults(
		self, cursor, tableName,
		**namedarguments ):
		"""Build Table and Field descriptors through introspection
		"""
		table = dbschema.TableSchema( name=tableName )
		descriptors = []
		nameMap = {}
		tableDescription = cursor.description
		
		for index,description in zip(range(len(tableDescription)),tableDescription):
			extras = {}
			try:
				extras['dbDataType'] = cursor.connection.driver.localToSQLType(
					description [1]
				)
			except KeyError:
				pass
			else:
				try:
					extras['dataType'] = cursor.connection.driver.sqlToDataType(
						extras['dbDataType']
					)
				except KeyError:
					pass
			new = dbschema.FieldSchema(
				name = description [0],
				nullOk = description [6],
				index = index,
				table = table,
				internalSize = description[3] or -1, # can be None
				displaySize = description[2] or -1, # can be None
				**extras
			)
			descriptors.append( new )
			nameMap[new.name] = new
		table.fields = descriptors
		
		## now get the index information
		indices = {}
		# XXX primary keys apparently can't be multi-column? <shrug>
		for item in ListIndices()( cursor, tableName=tableName ):
			name = item[2]
			unique = not item[1] # non-unique is the column spec
			fieldPosition = item[3] # position of the field in the column spec
			field = nameMap[ item[4]] # the field object...
			# we don't currently use collation or sub-part
			indices.setdefault( name, (name,unique,name=='PRIMARY',[]))[-1].append(
				(fieldPosition, item[4]),
			)
		#Okay, now build the actual index objects...
		indices = indices.values()
		indices.sort( )
		newIndices = []
		for name, unique,primary, fields in indices:
			fields.sort()
			fields = [ field[1] for field in fields ]
			new = dbschema.IndexSchema(
				name = name,
				unique = unique,
				primary=primary,
				fields = fields,
			)
			newIndices.append(new)
		if newIndices:
			table.indices = newIndices
		return table


class ListDatabases( sqlquery.SQLQuery ):
	"""Queries PostgreSQL server for list of database-names

	returns a simple list of string names
	"""
	sql = """SHOW DATABASES;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read database name list from cursor"""
		return [ row[0] for row in cursor.fetchall() ]

class ListTables( sqlquery.SQLQuery ):
	"""Queries connection/cursor for list of table-names

	returns a simple list of string names
	"""
	sql = """SHOW TABLES;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read table name list from cursor"""
		return [ row[0] for row in cursor.fetchall() ]


class ListIndices( sqlquery.SQLQuery ):
	"""Get index-data-records for a given table

	Returns a mysql-specific table format...
	"""
	sql = """SHOW INDEX FROM %(tableName)s;"""
	def processResults(self, cursor, **named ):
		"""returns results of the selection as an unadorned set"""
		return cursor.fetchall()
	
