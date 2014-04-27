"""Property object using dbschema.FieldSchema for definition"""
import sys, traceback
from basictypes import typeunion
from basicproperty import propertied, common, basic
from pytable import dbschema, viewschema, sqlquery, dbrow

def _getDriver( client ):
	"""Utility to get the driver for a given client field"""
	try:
		databaseSchema = client.schema.findParent( requiredType = dbschema.DatabaseSchema )
	except NameError:
		pass
	else:
		if (
			databaseSchema and
			hasattr( databaseSchema, 'driver') and
			databaseSchema.driver
		):
			return databaseSchema.driver

def _defaultBaseType( prop,client ):
	"""Attempt to get base type from the client's schema"""
	if hasattr( client.schema, 'baseClass'):
		return client.schema.baseClass
	driver = _getDriver( client )
	if driver and hasattr( client.schema, "dbDataType") and client.schema.dbDataType:
		return driver.sqlToBaseType( client.schema.dbDataType )
	return object # generic default

def _defaultDataType( prop,client ):
	"""Attempt to get the data type from the client's schema"""
	possible = getattr(client.schema, 'dataType', None )
	if possible:
		return possible
	raise AttributeError( """Schema %r doesn't define a dataType for client %s"""%(client.schema, client))

class DBProperty( basic.BasicProperty ):
	"""Database-row-object properties

	BasicProperty objects which defer most of their
	operation to a schema object.  The Schema object
	is of the type provided by the dbschema module,
	which can be either reverse engineer from the
	database, or declared manually using the
	schemabuilder module.
	"""
	schema = basic.BasicProperty(
		'schema', """The controlling schema for this field""",
		baseType= typeunion.TypeUnion( (
			dbschema.FieldSchema,
			viewschema.ViewFieldSchema
		)),
	)
	name = common.StringProperty(
		'name', """Name of the field (required)""",
		defaultFunction = lambda prop,client: client.schema.name,
		setDefaultOnGet = 0,
	)
	friendlyName = common.StringProperty(
		'friendlyName', """Friendly field-name for GUI presentations""",
		defaultFunction = lambda prop,client: client.schema.friendlyName,
		setDefaultOnGet = 0,
	)
	baseType = common.ClassByNameProperty(
		'baseType', """The base-type of the field, often merely None""",
		defaultFunction = _defaultBaseType,
		setDefaultOnGet = 1,
	)
	dataType = common.StringProperty(
		'dataType', """String data-type for the field's values""",
		defaultFunction = _defaultDataType,
		setDefaultOnGet = 1,
	)
	documention = common.StringProperty(
		'documention', """The documentation for the field""",
		defaultFunction = lambda prop,client: client.schema.comment,
		setDefaultOnGet = 0,
	)
	setDefaultOnGet = 0

	def __set__( self, client, value ):
		"""Set the current value of the property for the client

		This overrides to make setting a NULL value (None) do
		a delete instead of a set.
		"""
		if value is None:
			try:
				return self.__delete__( client )
			except AttributeError, err:
				# wasn't defined anyway
				return None
		else:
			return super( DBProperty, self ).__set__( client, value )
	def _getValue( self, client ):
		"""Perform a low-level retrieval of the "raw" value for the client
		"""
		return client.getValue( self.schema )
		
	def _setValue( self, client, value ):
		"""Perform a low-level set of the "raw" value for the client
		"""
		return client.setValue( self.schema, value )
	def _delValue( self, client ):
		"""Perform a low-level delete of the value for the client
		"""
		return client.delValue( self.schema )
	def __getattr__( self, key ):
		"""Delegate attribute lookup to our schema if it's available"""
		if key != 'schema':
			try:
				return getattr(self.schema, key )
			except (AttributeError,ValueError,TypeError), err:
				pass
		raise AttributeError( """%s instance does not not have an attribute %r"""%(self.__class__.__name__,key))
	def nextValue( self, connection ):
		"""Attempt to retrieve the next default value in our sequence"""
		if getattr(self.schema,'defaultValue',None):
			for row in sqlquery.SQLQuery(
				"""SELECT %(value)s"""
			)( connection, value = self.schema.defaultValue ):
				return row[0]
		if getattr(self.schema,'sequenceName',None):
			# this is postgresql specific
			for row in sqlquery.SQLQuery(
				"""SELECT nextval(%%(sequenceName)s)"""
			)( connection, sequenceName = self.schema.sequenceName ):
				return row[0]
		raise AttributeError(
			"""Sorry, don't seem to have a default value or sequence name for %s"""%(
				self.schema.name,
			)
		)
	

class ReferenceProperty(DBProperty):
	"""Property representing a foreign-key reference to another object

	The foreign key reference will be used to produce a reference
	to the remote object, rather than returning the key itself.
	"""
	def __set__( self, client, value ):
		"""Set the current value of the property for the client

		This overrides to make setting a DBRow instance do a
		lookup to find our referenced field in the set value
		to set that instead.
		"""
		if isinstance( value, dbrow.DBRow):
			# we set the refered-to value, not the object itself
			constraint = self.schema.foreign()
			fields = constraint.getForeignFields()
			assert len(fields) == 1, """Attempt to set %r to %r, this is a multi-field constraint somehow?"""%(
				self.name, value,
			)
		return super( ReferenceProperty, self ).__set__( client, value )
	def commonValues( self, connection ):
		"""Get sequence of common values for this property"""
		constraint = self.schema.foreign()
		assert constraint
		fields = constraint.foreignFields[:]
		foreignTable = constraint.lookupName( constraint.foreignTable )
		if hasattr( foreignTable, 'friendlyNameField'):
			sql = """SELECT
				%(friendlyNameField)s,%(fields)s
			FROM
				%(foreignTable)s
			ORDER BY
				UPPER( %(friendlyNameField)s );"""
			friendlyNameField = foreignTable.friendlyNameField
		else:
			sql = """SELECT
				%(friendlyNameField)s,%(fields)s
			FROM
				%(foreignTable)s
			ORDER BY
				%(friendlyNameField)s;"""
			friendlyNameField = fields[0]
		fields = ",".join(fields)
		records = sqlquery.SQLQuery(
			sql=sql,
			#debug = 1,
		)( connection, fields=fields,
			foreignTable=constraint.foreignTable,
			friendlyNameField=friendlyNameField,
		).fetchall()
		return records
		   
class OneToXProperty( DBProperty ):
	"""Property representing a seperate table providing 1:X mapping"""
	localKey = None
	
