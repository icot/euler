from pytable import sqlquery, dbschema
from basicproperty import common

try:
	enumerate
except NameError:
	def enumerate( sequence ):
		index = 0
		for item in sequence:
			yield (index, item)
			item += 1

class TableStructure (sqlquery.SQLQuery ):
	"""Reverse-engineer table structure/schema from database"""
	sql = """PRAGMA table_info(%(tableName)s);"""
	def processResults(
		self, cursor, tableName,
		**namedarguments ):
		"""Build Table and Field descriptors through introspection
		"""
		table = dbschema.TableSchema( name=tableName )
		descriptors = []
		nameMap = {}

		for index, (cid, name, dbDataType, notNull, defaultValue, primary) in enumerate(cursor.fetchall()):
##			print (cid, name, dbDataType, notNull, defaultValue, primary)
			extras = {}
			constraints = []
			try:
				extras['dbDataType'] = dbDataType
			except KeyError:
				pass
			else:
				try:
					extras['dataType'] = cursor.connection.driver.sqlToDataType(
						extras['dbDataType']
					)
				except KeyError:
					pass
			if notNull:
				constraints.append(
					dbschema.NotNullConstraint( fields=(name,))
				)
			if primary:
				constraints.append(
					dbschema.PrimaryConstraint( fields=(name,))
				)
			if defaultValue is not None:
				extras['defaultValue'] = defaultValue
			if constraints:
				extras['constraints']= constraints
			new = dbschema.FieldSchema(
				name = name,
				nullOk = not notNull,
				index = index,
				table = table,
				internalSize = 0,
				displaySize = 0,
				**extras
			)
			descriptors.append( new )
			nameMap[new.name] = new
		table.fields = descriptors
		
		## now get the index information
		newIndices = self.buildIndices( cursor, tableName, nameMap )
		if newIndices:
			table.indices = newIndices
		return table

	def buildIndices( self, cursor, tableName, nameMap ):
		newIndices = []
		for (name,masterRecord,fields) in ListIndices()( cursor, tableName=tableName ):
			unique = self.isUniqueIndex( nameMap, name, masterRecord, fields )
			if unique > 1:
				primary = True
			else:
				primary = False
			fields = [fieldName for (cid,table_cid,fieldName) in fields]
			new = dbschema.IndexSchema(
				name = name,
				unique = unique,
				primary=primary,
				fields = fields,
			)
			newIndices.append(new)
		return newIndices
	
	def isUniqueIndex( self, nameMap, name, masterRecord, fields ):
		"""Determine whether this is a unique index

		returns 0 -> not unique, 1 -> unique or 2 -> primary
		"""
		if masterRecord[4]:
			for word in masterRecord[4].upper().split( None, 5 ):
				if word == 'UNIQUE':
					return 1
				elif word == 'PRIMARY':
					return 2
			return 0
		else:
			# is automatically generated, so either primary or unique contraint on the field
			# record on the field object while we're at it...
			if len(fields) != 1:
				raise RuntimeError(
					"""An index record %r with no definition has more than one field, cannot reverse engineer schema, please report this! %r %r"""%(
						name, masterRecord, fields,
					),
				)
			fieldName = fields[0][2]
			field = nameMap.get( fieldName )
			if field is None:
				raise RuntimeError( """Field %r, which is declared as part of index %r doesn't appear to exist"""%(
					fieldName, name,
				))
			returnValue = 1
			found = False
			for constraint in field.constraints:
				if dbschema.isPrimary( constraint ):
					returnValue = 2
					found = True
				elif dbschema.isUnique( constraint ):
					# already specified
					returnValue = 1
					found = True
			if not found:
				field.constraints.append( dbschema.UniqueConstraint(fields=(fieldName,)))
			return returnValue



class ListDatabases( sqlquery.SQLQuery ):
	"""Queries PostgreSQL server for list of database-names

	returns a simple list of string names
	"""
	sql = """PRAGMA database_list;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read database name list from cursor"""
		return [ row[1] for row in cursor.fetchall() ]

class _ListTables( sqlquery.SQLQuery ):
	"""Queries connection/cursor for list of table-names

	returns a simple list of string names
	"""
	sql = """SELECT * FROM sqlite_master %(whereFragments)s
	UNION
SELECT * FROM sqlite_temp_master %(whereFragments)s;"""
	def __call__( self, cursor, type='table', name=None, **named ):
		"""Return given tables (or indices)"""
		whereFragments = []
		if type is not None:
			whereFragments.append( 'type = %(type)s' )
			named['type'] = type
		if name is not None:
			whereFragments.append( 'name = %(name)s' )
			named['name'] = name
		if whereFragments:
			whereFragments = " WHERE %s" % (
				" AND ".join(whereFragments),
			)
			named['whereFragments' ] = whereFragments
		return super( _ListTables, self ).__call__( cursor, **named )
class ListTables( _ListTables ):
	def processResults( self, cursor, **namedarguments ):
		"""Read table name list from cursor"""
		return [ record[1] for record in cursor.fetchall()]

class ListIndices( sqlquery.SQLQuery ):
	"""Get index names for a given table

	Returns a list of simple string names
	"""
	sql = """PRAGMA index_list(%(tableName)s);"""
	def processResults(self, cursor, **named ):
		"""returns results of the selection as an unadorned set"""
		lt = _ListTables()
		ii = IndexInfo()
		return [
			(
				row[1],
				lt( cursor, type='index', name=row[1]).fetchone(),
				list(ii(cursor, indexName=row[1])),
			)
			for row in cursor.fetchall()
		]

class IndexInfo( sqlquery.SQLQuery ):
	"""Get index-data-records for a given table

	Returns a sqlite-specific table format...
	"""
	sql = """PRAGMA index_info(%(indexName)s);"""
	def processResults(self, cursor, **named ):
		"""returns results of the selection as an unadorned set"""
		return cursor.fetchall()

