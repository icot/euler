"""Actions for the PostgreSQL table

These are meta-queries/actions, they tell us about
the structure of the database schema by directly
querying the postgresql system catalogs.  They are
therefor entirely non-portable, evil things, but
they do appear to get the job done :) .
"""
from pytable import sqlquery, dbschema
from basicproperty import common
import traceback

def intSetToTuple( source ):
	"""Convert PyGreSQL's raw {1,2,3} set strings into lists

	These really should be getting converted to lists
	automatically by the driver, but it doesn't seem to
	want to do so :( .
	"""
	if isinstance( source, (str,unicode)):
		items = source[1:-1]
		items = items.split(',')
		result = []
		for item in items:
			if item:
				try:
					item = int(item)
				except ValueError, err:
					try:
						item = float(item)
					except ValueError, err:
						raise ValueError( """Could not convert item %r of set %r to an integer or float value"""%(
							item, source,
						))
					else:
						result.append( item )
		return result
	return source

class ListDatabases( sqlquery.SQLQuery ):
	"""Queries PostgreSQL server for list of database-names

	returns a simple list of string names
	"""
	sql = """SELECT datname FROM pg_database
	WHERE datname != 'template1' AND datname != 'template0';"""
	def processResults( self, cursor, **namedarguments ):
		"""Read database name list from cursor"""
		return [ row[0] for row in cursor.fetchall() ]

class ListDatatypes( sqlquery.SQLQuery ):
	"""Queries PostgreSQL server for list of base data-type names

	Only lists the set of defined, non-array base data-types

	returns typname:oid mapping
	"""
	sql = """SELECT
		typname, oid
	FROM
		pg_type
	WHERE
		typtype = 'b' -- base types only
	AND
		typisdefined='t' -- is actually available
	AND
		typelem=0 -- is not an array type
	;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read database name list from cursor"""
		return dict([ (row[0],row[1]) for row in cursor.fetchall() ])

class ListTables( sqlquery.SQLQuery ):
	"""Queries connection/cursor for list of table-names

	returns a simple list of string names
	"""
	sql = """
	SELECT 
	  c.relname
	FROM pg_catalog.pg_class c
		 LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
	WHERE c.relkind IN ('r','v','')
		  AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
		  AND pg_catalog.pg_table_is_visible(c.oid)
	ORDER BY c.relname;
	"""
	def processResults( self, cursor, **namedarguments ):
		"""Read table name list from cursor"""
		result = [ row[0] for row in cursor.fetchall() ]
		return result

class ListNamespaces( sqlquery.SQLQuery ):
	"""List sub-namespaces in the database"""
	sql = """SELECT
		ns.nspname
	FROM
		pg_namespace ns
	WHERE
		ns.nspname NOT LIKE 'pg_%%%%'
	AND
		ns.nspname !='information_schema'
	AND
		ns.nspname != 'public'
	;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read schema names list from cursor"""
		return [ row[0] for row in cursor.fetchall() ]
	

class ListNamespaceTables( sqlquery.SQLQuery ):
	"""List sub-namespace tables in the database

	That is, tables not in the public catalog, which therefor
	require a namespace prefix to reference.

	Returns a simple list of (namespace,tablename) tuples
	"""
	sql = """SELECT
		t.schemaname,t.tablename
	FROM
		pg_namespace ns,
		pg_tables t
	WHERE
		ns.nspname NOT LIKE 'pg_%%%%'
	AND
		ns.nspname !='information_schema'
	AND
		ns.nspname != 'public'
	AND
		t.schemaname = ns.nspname
	AND
		t.tablename NOT LIKE 'pg_%%%%'
	ORDER BY t.schemaname, t.tablename
	;"""
	def processResults( self, cursor, **namedarguments ):
		"""Read table name list from cursor"""
		result = [ (row[0],row[1]) for row in cursor.fetchall() ]
		return result


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
	LIMIT 1; -- this will hopefully optimize the query somewhat
	"""
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
			try:
				extras[ 'baseClass' ] = cursor.connection.driver.sqlToBaseType(
					extras['dbDataType']
				)
			except KeyError:
				pass
			new = dbschema.FieldSchema(
				name = description [0],
				index = index,
				table = table,
				internalSize = description[3] or -1, # can be None
				displaySize = description[2] or -1, # can be None
				**extras
			)
			if not description [6]: # "null ok"
				new.constraints.append( dbschema.NotNullConstraint())
			descriptors.append( new )
			nameMap[new.name] = new
		table.fields = descriptors
		
		### POSTGRES' extra META-DATA
		## Get internal attribute indices
		localNameSet = AttributeNumbers()( cursor, tableName = tableName )

		## Get foreign constraints on the table
		## XXX should get per-field constraints too at some point
		try:
			for columnNumber, defaultString in AttributeDefaultValue()(
				tableName = tableName,
				cursor = cursor,
			).items():
				##if defaultString != "''":
				nameMap[localNameSet.get(columnNumber)].defaultValue = defaultString
		except:
			traceback.print_exc()
		try:
			tableDescription = ForeignConstraints() (cursor, tableName= tableName)
		except:
			print """Unable to retrieve foreign constraints"""
			traceback.print_exc()
		else:
			constraints = []
			for localIndices, foreignTable, foreignIndices,foreignNamespace in tableDescription:
				if foreignNamespace != 'public':
					foreignTable="%s.%s"%(foreignNamespace,foreignTable)
				localIndices = intSetToTuple( localIndices )
				foreignIndices = intSetToTuple( foreignIndices )
				localFields = [ localNameSet[int(i)] for i in localIndices ]
				foreignNameSet = AttributeNumbers()(
					cursor,
					tableName = foreignTable,
				)
				foreignFields = [ foreignNameSet[int(i)] for i in foreignIndices ]
				new = dbschema.ForeignKeyConstraint(
					fields = localFields,
					foreignFields = foreignFields,
					foreignTable = foreignTable,
				)
				constraints.append( new )
			if constraints:
				table.constraints = constraints
			
		## now get the index objects...
		indices = []
		
		for id, fieldNums, unique, primary, name in ListIndices()(
			cursor, tableName=tableName,
		):
			# fieldNums is 1-indexed, or, if I'm right, it's actually
			# including the oid field :(
			skipIndex = 0
			for number in fieldNums.split():
				if int(number) <= 0:
					skipIndex = 1
			if skipIndex:
				continue
			try:
				fields = [
					nameMap[ localNameSet[ int(i)]].name
					for i in fieldNums.split()
				]
				indices.append(dbschema.IndexSchema(
					name = name,
					unique = unique,
					primary=primary,
					fields = fields,
				))
			except KeyError, err:
				print """Failure getting fields for index: %s"""%(err,), (id, fieldNums, unique, primary, name,localNameSet)
		if indices:
			table.indices = indices
		return table
	
class ExpandTableName(sqlquery.SQLQuery):
	""" Provides tableName to namespace + tableName expansion
	
	"""
	def __call__(self,cursor,tableName,namespace=None,**named):
		""" Override to provide default namespace"""
				
		if '.' in tableName:
			namespace,tableName=tableName.split('.',1)
		if not namespace:
			namespace='public'
			
		return super(ExpandTableName,self).__call__(
			cursor=cursor,tableName=tableName,namespace=namespace,**named
		)
	
class ListIndices( ExpandTableName ):
	"""Get index-data-records for a given table

	namespace -- namespace where the table is defined, default is "public"
	tableName -- name of the table
	
	XXX Should build actual Index objects here, not
		just return data-values for interpretation.
	"""
	sql = """
		SELECT
			i.indexrelid, -- the key-ID of the index
			i.indkey, -- list of field-indices participating
			i.indisunique, -- whether unique or not
			i.indisprimary, -- whether a primary-key index or not
			c2.relname -- index name
		FROM
			pg_class c, -- looking up table-name
			pg_class c2, -- looking up index-name
			pg_index i, -- getting extra index-specific information
			pg_namespace n -- looking up namespace
		WHERE
			n.nspname=%%(namespace)s AND -- the given namespace
			n.oid=c.relnamespace AND -- table reference to namespace
			c.relname=%%(tableName)s AND -- the given table's row in catalog
			c.oid = i.indrelid AND -- index entry refers to given table
			i.indexrelid=c2.oid -- lookup of index row key in table catalog
		ORDER BY
			c2.relname;
	"""	
	def processResults(self, cursor, **named ):
		"""returns results of the selection as an unadorned set"""
		return cursor.fetchall()
			

class AttributeNumbers( ExpandTableName ):
	"""Query attnum:attname for a table
	
	namespace -- namespace where the table is defined, default is "public"
	tableName -- name of the table
	
	returns a dictionary of number:name
	"""
		
	sql = """
		SELECT
			a.attname, a.attnum
		FROM
			pg_attribute a,
			pg_class c,
			pg_namespace n -- looking up namespace
		WHERE
			n.nspname=%%(namespace)s AND -- the given namespace
			n.oid=c.relnamespace AND -- table reference to namespace
			c.relname=%%(tableName)s AND
			c.oid = a.attrelid
			-- This excludes oid and other system columns, which means that
			-- we can't deal with oid indices...
			-- AND a.attnum > 0
		ORDER BY
			a.attnum;
	"""
		
	def processResults( self, cursor, **named ):
		set = {}
		for name, number in cursor.fetchall():
			set[int(number)] = name
		return set

class AttributeDefaultValue( ExpandTableName ):
	"""Queries for attribute default values

	tableName -- name of the table
	"""
	sql = """
		SELECT
			a.adnum,
			a.adsrc
		FROM
			pg_attrdef a,
			pg_class c,
			pg_namespace n -- looking up namespace
		WHERE
			n.nspname=%%(namespace)s AND -- the given namespace
			n.oid=c.relnamespace AND -- table reference to namespace
			c.relname=%%(tableName)s AND
			c.oid = a.adrelid;
	"""
	def processResults( self, cursor, **named ):
		set = {}
		for number, value in cursor.fetchall():
			set[int(number)] = value
		return set

class ForeignConstraints( ExpandTableName ):
	sql = """
	SELECT 
		con.conkey, -- local key-columns
		-- con.confrelid, -- remote table id
		c2.relname, -- remote table name
		con.confkey, -- remote key-columns
		n2.nspname -- remote table namespace
	FROM
		pg_constraint con,
		pg_class c,
		pg_class c2,
		pg_namespace n1,
		pg_namespace n2
	WHERE
		n1.nspname=%%(namespace)s AND -- the given namespace
		n1.oid=c.relnamespace AND -- table reference to namespace
		c.relname=%%(tableName)s AND
		c.oid = con.conrelid AND
		con.contype = 'f' AND
		c2.oid = con.confrelid AND
		c2.relnamespace=n2.oid
	;"""
	def processResults( self, cursor, **named ):
		return cursor.fetchall()

class AttrNamesFromNumbers( ExpandTableName ):
	"""Get attr names from table-oid and set of attr indices"""
	sql = """
		SELECT
			a.adnum,
			a.adsrc
		FROM
			pg_attrdef a,
			pg_class c,
			pg_namespace n -- looking up namespace
		WHERE
			n.nspname=%%(namespace)s AND -- the given namespace
			n.oid=c.relnamespace AND -- table reference to namespace
			c.relname=%%(tableName)s AND
			c.oid = a.adrelid AND
			a.attnum IN %%(set)s;
	"""
	def processResults( self, cursor, **named ):
		return cursor.fetchall()

class AttributeFromNumber ( ExpandTableName ):
	"""Get full field definition information for a single field

	This is normally only used for the system fields which are
	not normally part of the table definition...
	"""
	sql = """
		SELECT
			pg_attribute.attname,
			pg_attribute.attnum,
			pg_attribute.attlen AS internallength,
			pg_attribute.atttypmod AS length,
			pg_attribute.attnotnull AS notnull,
			pg_attribute.atthasdef AS hasdefault,
			pg_attrdef.adsrc AS defaultvalue,
		FROM
			pg_attribute,
			pg_attrdef,
			pg_class,
			pg_namespace n -- looking up namespace
		WHERE
			n.nspname=%%(namespace)s AND -- the given namespace
			n.oid=c.relnamespace AND -- table reference to namespace
			pg_class.relname=%%(tableName)s
		AND
			pg_class.oid = pg_attrdef.adrelid
		AND
			pg_class.oid = pg_attribute.attrelid
		AND
			pg_attrdef.adnum = %%(attributeNumber)s
		AND
			pg_attribute.attnum = %%(attributeNumber)s
		AND
			pg_attrdef.attisdropped = False
		;
	"""
	def processResults( self, cursor, **named ):
		return cursor.fetchall()

"""
# Get list of type-names from the database server
SELECT
	oid, -- the oid of the type
	typname, -- name
	typlen, -- data-length
	typelem -- if non-0, is the oid of sub-type entry for array-type
FROM
	pg_type
WHERE
	typtype = 'b' AND
	typname !~'^_'
ORDER BY
	typname;

	

"""

class SequenceName( sqlquery.SQLQuery ):
	"""Retrieve sequence name for a given field"""
	sql = """SELECT
		pg_attrdef.adsrc
	FROM
		pg_attrdef,
		pg_class,
		pg_attribute
	WHERE
		pg_attrdef.adnum = pg_attribute.attnum
	AND 
		pg_attrdef.adrelid = pg_class.oid
	AND 
		pg_attribute.attrelid = pg_class.oid
	AND 
		pg_attribute.attname = %(field)s
	AND 
		pg_class.relname = %(table)s
	"""
