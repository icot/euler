"""Mechanisms for generating SQL from DBSchema objects

Currently supported:
	Create:
		database, table, field, index, default records,
		table/field constraints
	Drop/Grant/Revoke:
		everything

XXX Should eventually allow for "database diff", that is
	generating SQL for adding new fields, indices,
	constraints etc.
"""
from pytable import sqlquery, dbschema, sqlutils
from basicproperty import propertied, common, basic

class SQLStatements( propertied.Propertied ):
	"""Base-class for SQL-generating objects

	XXX Should be doing a topological sort in order to
		resolve any dependencies between items.
	"""
	def __init__( self, driver=None, **named ):
		"""Initialise the statement-generator

		Driver will be used to determine features for
		generation (when that's implemented).
		"""
		super( SQLStatements, self).__init__(
			driver = driver,
			**named
		)
	def __call__( self, schema, *arguments, **named ):
		"""Create SQL creation statements for given schema

		Returns the statements as a series of strings.
		"""
		return self.dispatch( schema, *arguments, **named )
	def dispatch( self, schema, *arguments, **named ):
		"""Dispatch to the appropriate handler and return value"""
		for classObject in schema.__class__.__mro__:
			handler = self.dispatchMapping.get(classObject)
			if handler:
				return handler.__get__(self)(schema, *arguments, **named)
		raise TypeError( """unrecognised schema type %s, don't know how to generate SQL for this type"""%(type(schema)))
	def expand( self, schema, *arguments, **named ):
		"""Get the results of all items within an item"""
		results = []
		for item in schema:
			try:
				result = self.dispatch( item, *arguments, **named )
			except TypeError:
				pass
			else:
				if isinstance(result, (str,unicode)):
					results.append( result )
				else:
					results.extend( result )
		return results
	dispatchMapping = {
	}

class SQLCreateStatements( SQLStatements ):
	"""Class providing schema-SQL-create-statements for SQL databases"""
	tableSQLTemplate = """CREATE TABLE %(temporary)s %(tableName)s (
	%(subelements)s
) %(inherits)s %(withoids)s;"""
	fieldSQLTemplate = """%(fieldName)s %(dbDataType)s %(default)s %(constraints)s"""
	def preCreationSQL( self, schema ):
		return getattr( schema, 'preCreationSQL', [])
	def postCreationSQL( self, schema ):
		return getattr( schema, 'postCreationSQL', [])
	
	def database( self, schema, *arguments, **named ):
		"""Generate SQL for a whole database schema (minus database setup itself)"""
		fragments = []
		fragments.extend( self.preCreationSQL( schema ))
		fragments.extend([
			self.dispatch( s,*arguments,**named)
			for s in schema.sequences
		])
		for s in schema.tables:
			fragments.extend(self.dispatch( s,*arguments,**named))
		fragments.extend([
			self.dispatch( s,*arguments,**named)
			for s in getattr(schema,'namespaces',())
		])
		fragments.extend( self.postCreationSQL( schema ))
		return fragments
	def namespace( self, schema, **named ):
		"""Generate SQL to create a namespace"""
		return [
			"""CREATE SCHEMA %s;"""%(schema.name.lower(),)
		] + self.database( schema )
		
	def table( self, schema, **named ):
		"""Generate SQL to create table in database"""
		if schema.temporary:
			temporary = "TEMPORARY"
		else:
			temporary = ""
		tableName = schema.name.lower()
		if not tableName:
			raise AttributeError("""No name property for table schema %r"""% (schema,))
		inherits = ""
		withoids = ""
		if schema.withOIDs and self.driver.capabilities.oids:
			withoids = 'WITH OIDS'
		# now create the sub elements
		elements = []
		for field in schema.fields:
			elements.append(self.tableField( field, **named ))
		for constraint in schema.constraints:
			elements.append( self.tableConstraint( constraint, schema))
		subelements = ",\n\t".join( elements )
		items = []
		if schema.indices:
			for index in schema.indices:
				items.append( self.tableIndex( index, schema ))
		if hasattr( schema, 'defaultRecords'):
			try:
				items.extend(self.records( schema, schema.defaultRecords ))
			except Exception, err:
				err.args += (tableName, )
				raise
		return [ self.tableSQLTemplate % locals () ] + items
	def recordReference( self, table, field, value ):
		"""Create reference to given subrecord value in given table"""
		if isinstance( value, dict ):
			wheres = []
			for key,value in [ 
				item for item in value.items() 
				if item[0] != '__create'
			]:
				if isinstance( value, dict ):
					# recursive reference to a far-off field...
					remoteReference = table.lookupName( key ).foreign()
					remoteField = remoteReference.getForeignFields()[0]
					remoteTableName = remoteReference.foreignTable
					remoteTable = table.lookupName( remoteTableName )
					valueSQL = self.recordReference(
						remoteTable, remoteTable.lookupName( remoteField ),
						value,
					)
				else:
					valueSQL = sqlutils.sqlEscape( 
						value, 
						dbDataType = table.lookupName(key).dbDataType 
					)
				wheres.append(
					'%s = %s'%(
						key,
						valueSQL,
					),
				)
			wheres = ' AND '.join( wheres )
			foreignField = field.name
			foreignTable = table.name
			sqlValue = '(SELECT %(foreignField)s FROM %(foreignTable)s WHERE %(wheres)s)'%locals()
		else:
			sqlValue = sqlutils.sqlEscape( value, dbDataType = field.dbDataType )
		return sqlValue

	def createSubRecords( self, table, field, record ):
		"""Create sub-records (recursively)
		
		Iterate over children of a dictionary record and
		create any children or children-of-children that
		will be needed to create the top-level record.
		"""
		# create any sub-records first...
		result = []
		if record.get( '__create', True ):
			items = [ 
				(k,v) for (k,v) in record.items() if k != '__create'
			]
			for key,value in items:
				if isinstance( value, dict ):
					remoteReference = table.lookupName( key ).foreign()
					remoteField = remoteReference.getForeignFields()[0]
					remoteTableName = remoteReference.foreignTable
					remoteTable = table.lookupName( remoteTableName )
					result.extend( self.createSubRecords( 
						remoteTable, remoteTable.lookupName( remoteField ),
						value,
					) )
			# now create the top-level record...
			fields = ",".join( [i[0] for i in items])
			values = []
			for key,value in items:
				try:
					field = table.lookupName( key, requiredType = dbschema.FieldSchema )
				except NameError, err:
					raise NameError(
						"""Couldn't find field %r for table %s defined fields: %s"""%(
							key, table.name, [getattr(x,'name',None) for x in table.fields],
						)
					)
				if isinstance( value, dict ):
					remoteReference = table.lookupName( key ).foreign()
					remoteField = remoteReference.getForeignFields()[0]
					remoteTableName = remoteReference.foreignTable
					remoteTable = table.lookupName( remoteTableName )
					sqlValue = self.recordReference( 
						remoteTable, remoteTable.lookupName( remoteField ), 
						value
					)
				else:
					sqlValue = self.recordReference( table, field, value )
				values.append(sqlValue)
			values = ",".join( values )
			tableName = table.name
			result.append(
				"""INSERT INTO %(tableName)s(%(fields)s) VALUES (%(values)s);"""%locals()
			)
		return result
		
	def records( self, table, dictionaries ):
		"""Create SQL to insert record in dictionary into table"""
		fragments = []
		tableName = table.name
		for dictionary in dictionaries:
			fragments.extend(
				self.createSubRecords( table, None, dictionary )
			)
		return fragments
	def tableField( self, schema, **named):
		"""Generate in-table fragment for generating a field"""
		fieldName = schema.name.lower()
		if not fieldName:
			raise AttributeError("""No name property for field schema %r"""%(schema,))

		dbDataType = self.fieldDataType( schema )
		if hasattr( schema, "defaultValue"):
			if not (
				self.driver and 
				self.driver.capabilities.serial and
				getattr( schema, 'dbDataType', None ) in ('serial','bigserial')
			):
				# database will not automatically generate a "default" statement
				default = "DEFAULT %s"%( schema.defaultValue,)
			else:
				default = ''
		else:
			default = ""
		constraints = []
		if not schema.nullOk:
			constraints.append( "NOT NULL" )
		for constraint in schema.constraints:
			constraints.append( self.fieldConstraint( constraint, schema))
		if self.driver and not self.driver.capabilities.serial:
			if getattr( schema, 'dbDataType', None ) in ('serial','bigserial'):
				constraints.append( 'AUTO_INCREMENT' )
		constraints = " ".join( constraints )
		return self.fieldSQLTemplate%locals()
	
	fieldPrefixToTypeMap = [
		('int','INT'),
		('float','FLOAT'),
		('bool','BOOLEAN'),
		('str.classname', 'VARCHAR'),
	]
	def fieldDataType( self, schema ):
		"""Create the data type declaration for the field"""
		dataType = schema.dbDataType
		if not dataType:
			for (prefix,dbType) in self.fieldPrefixToTypeMap:
				if schema.dataType.startswith( prefix ):
					dataType = dbType
					break
			if not dataType:
				raise AttributeError( """Don't know and can't guess the database data-type for field %s"""%(schema,))
		if dataType in ('serial','bigserial'):
			if self.driver and not self.driver.capabilities.serial:
				if dataType == 'serial':
					dataType = 'int'
				else:
					dataType = 'bigint'
		if schema.displaySize not in (0,None,-1):
			if isinstance( schema.displaySize, tuple ):
				dataType = "%s%s"%( dataType, schema.displaySize)
			else:
				dataType = "%s(%s)"%( dataType, schema.displaySize)
		return dataType.upper()
	def fieldConstraint( self, constraint, target ):
		"""Create constraint-specifying SQL code fragment"""
		self.constraintCheck( constraint, target )
		fragments = []
		if constraint.name:
			fragments.append( 'CONSTRAINT %s'%constraint.name.lower())
		if constraint.dbConstraintType in (
			'UNIQUE','NULL','PRIMARY KEY'
		):
			# simple constraint types...
			fragments.append( constraint.dbConstraintType )
		elif constraint.dbConstraintType == 'NOT NULL':
			pass
		elif constraint.dbConstraintType == 'CHECK':
			fragments.append( constraint.dbConstraintType )
			fragments.append( '(%s)'%(constraint.expression,) )
		elif constraint.dbConstraintType == 'FOREIGN KEY':
			fragments.append( self.foreignKey(
				constraint, target
			))
		else:
			raise TypeError( """Unrecognised constraint-type %s for constraint %r"""%(
				constraint.dbConstraintType,
				constraint,
			))
		return " ".join( fragments )

	def tableConstraint( self, constraint, target ):
		"""Create constraint-specifying SQL code fragment"""
		self.constraintCheck( constraint, target )
		fragments = []
		if constraint.name:
			fragments.append( 'CONSTRAINT %s'%constraint.name.lower())
		if constraint.dbConstraintType in (
			'UNIQUE','PRIMARY KEY', 'FOREIGN KEY',
		):
			# simple constraint types...
			fragments.append( constraint.dbConstraintType )
			fragments.append( '(%s)'%(", ".join(constraint.fields)))
			if constraint.dbConstraintType == 'FOREIGN KEY':
				fragments.append( self.foreignKey( constraint, target ))
		elif constraint.dbConstraintType == 'CHECK':
			fragments.append( constraint.dbConstraintType )
			fragments.append( '(%s)'%(constraint.expression,) )
		else:
			raise TypeError( """Unrecognised constraint-type %s for constraint %r"""%(
				constraint.dbConstraintType,
				constraint,
			))
		return " ".join( fragments )

	def constraintCheck( self, constraint, target ):
		"""Check that the constraint is applicable to the target

		Will also fix up the constraint so that it
		matches the target's name if there is no
		declared field-name and the target is a field.
		"""
		if isinstance( target, dbschema.FieldSchema ):
			if len(constraint.fields) > 1:
				raise ValueError( """Constraint %r on field %r specifies more than one affected field"""%(constraint,target) )
			elif constraint.fields:
				field = constraint.fields[0]
				if field.lower() != target.name.lower():
					raise ValueError(
						"""Constraint %r on field %r specifies different field name, specifies %s, should be %s"""%(
							constraint,
							target,
							constraint.fields,
							[target.name,],
					))
			else: # fix up the spec to include the field-name
				constraint.fields.append( target.name )
		else:
			return

	def foreignKey( self, constraint, target ):
		"""Generate constraint sub-clause for foreign-key"""
		fragments = [ "REFERENCES", constraint.foreignTable ]
		if constraint.foreignFields:
			if isinstance( target, dbschema.FieldSchema ) and len(constraint.foreignFields) > 1:
				raise ValueError( """Field Foreign Key constraint references multiple fields: %r"""%(
					constraint,
				))
			fragments.append( "(%s)"%( ", ".join( constraint.foreignFields )))
		if hasattr( constraint, "onDelete" ):
			fragments.append( "ON DELETE" )
			fragments.append( constraint.onDelete )
		if hasattr( constraint, "onUpdate" ):
			fragments.append( "ON UPDATE" )
			fragments.append( constraint.onUpdate )
		return " ".join( fragments )

	def tableIndex( self, schema, target=None ):
		"""Generate SQL to create index described by schema"""
		if not hasattr(schema, "table"):
			if not target:
				target = schema.lookupName( requiredType = dbschema.TableSchema )
				if not target:
					raise ValueError( """Index %r created without a specified table target"""%(self,))
			schema.table = target.name 
		fragments = ["CREATE"]
		if schema.unique:
			fragments.append( "UNIQUE" )
		fragments.append( "INDEX" )
		if not schema.name:
			schema.name = (
				"_".join([
					n.lower() 
					for n in [schema.table]+schema.fields
				]) + '_idx'
			).replace( '.', '_' )
		fragments.append( schema.name.lower())
		fragments.append( "ON" )
		fragments.append( schema.table )
		if hasattr( schema, "accessMethod"):
			fragments.append( "USING %s"%( schema.accessMethod ,))
		if hasattr( schema, 'functionName'):
			fragments.append( "(%s(%s))"%(schema.functionName, ",".join(schema.fields)))
		else:
			fragments.append( "(%s)"%( ",".join(schema.fields)))
		if hasattr( schema, "where"):
			fragments.append( "WHERE %s"%( schema.where ,))
		fragments.append( ';')
		return " ".join(fragments)
	dispatchMapping = {
		dbschema.FieldSchema: tableField,
		dbschema.TableSchema: table,
		dbschema.IndexSchema: tableIndex,
		dbschema.DatabaseSchema: database,
		dbschema.NamespaceSchema: namespace,
	}

class SQLDropStatements( SQLStatements ):
	"""Class generating SQL drop statements for schemas"""
	standAlone_template = "DROP %(dbObjectType)s %(name)s %(cascade)s;"""
	def standAlone( self, schema, *arguments, **named ):
		"""Drop a stand-alone object"""
		dbObjectType = schema.dbObjectType
		name = schema.name
		if named.get( 'cascade' ):
			cascade = 'CASCADE'
		else:
			cascade = ''
		return self.standAlone_template % locals()
	dispatchMapping = {
		dbschema.TableSchema: standAlone,
		dbschema.IndexSchema: standAlone,
		dbschema.NamespaceSchema: standAlone,
		dbschema.DatabaseSchema: SQLStatements.expand,
	}

class SQLGrantStatements( SQLStatements ):
	"""Class generating SQL grant statements for schemas"""
	privileges = common.StringsProperty(
		"privileges", """List of strings specifying the privileges to grant

	Tables: select, insert, update, delete, rule, references, trigger
	Databases: create, temporary, temp
	Functions: execute
	Languages: usage
	Schemas: create, usage

	ALL or ALL privileges grants all for the type, and
	is the default value for the property.  That is, by
	default all privileges will be granted to the user.
	""",
		defaultValue = ( "ALL privileges", ),
	)
	users = common.StringsProperty(
		"users", """List of users/groups to which to grant privileges

	'PUBLIC' refers to everyone, otherwise is just the
	user-name/group-name, groups are specified as 'group groupname',
	regular users are just 'username'
	""",
		defaultValue = (),
	)
	isGroup = common.BooleanProperty(
		'isGroup', """Whether 'user' is a group, rather than a regular user""",
		defaultValue = 0,
	)
	template = """GRANT %(privileges)s ON %(dbObjectType)s %(name)s TO %(users)s;"""
	def general( self, schema, *arguments, **named ):
		"""Get the results of all items within an item"""
		if not self.privileges:
			raise ValueError( """Attempt to grant no privileges, use ALL to grant everything""" )
		privileges = ",".join(self.privileges)
		dbObjectType = schema.dbObjectType
		if not filter( None, self.users):
			raise ValueError( """Attempt to grant privileges to no groups/users: use PUBLIC to grant to everyone""" )
		users = ",".join( self.users )
		name = schema.name
		return self.template % locals()
	
	dispatchMapping = {
		dbschema.TableSchema: general,
		dbschema.IndexSchema: general,
		dbschema.DatabaseSchema: SQLStatements.expand,
	}
class SQLRevokeStatements( SQLGrantStatements ):
	"""Class generating SQL revoke statements for schemas"""
	template = """REVOKE %(privileges)s ON %(dbObjectType)s %(name)s FROM %(users)s;"""
