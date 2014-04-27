"""Data-description of table structure"""
from __future__ import generators
from basicproperty import propertied, common, basic, weak
from basictypes import list_types, callable
from pytable import sqlquery

class Schema( propertied.Propertied ):
	"""Base-class for Schema objects"""
	actions = common.ListProperty(
		'actions', """Actions defined for use with this schema-item

		Some possible actions:
			selectAll/refreshView
			revert:
				all
				row(s)
				row,field
			save data:
				update all rows
				update row
				commit
				append row
			insert row
			delete row
		""",
		baseType = callable.Callables,
		defaultFunction = lambda prop,client: [],
	)
	comment = common.StringProperty(
		"comment", """Optional comment/documentation for this schema item""",
		defaultValue = "",
		setDefaultOnGet = 0,
		dataType = 'str.long',
	)
	_Schema__namespace = weak.WeakProperty(
		"_Schema__namespace", """Weak ref to namespace in which we are defined""",
	)
	_Schema__names = common.DictionaryProperty(
		"_Schema__names", """Mapping from name: object for the schema""",
		defaultFunction = lambda property,client: client.buildNamespace(),
	)
	
	def actionByName( self, name ):
		"""Retrieve a particular action by name"""
		for action in self.actions:
			if hasattr( action, 'name'):
				actionName = action.name
			else:
				actionName = action.__name__
			if actionName == name:
				return action
		return None
	__repr__ = propertied.Propertied.toString
	def buildNamespace( self, ignoreDuplicates=1 ):
		"""Attempt to build namespace for this object"""
	def lookupName( self, name=None, requiredType=None, alreadySeen=None ):
		"""Try to find object of the given name/type

		name -- if specified, look for an object with the
			given name (only)
		requiredType -- if specified, look for an object
			with the given type.

		lookupName searches up the _Schema__names containment
		hierarchy looking for matches to the given name/type
		pair.  Note: the search is *and* if both are specified,
		that is, both must be satisfied to match.
		"""
		if isinstance( name, (str,unicode)):
			name = name.lower()
		elif name is None:
			if requiredType is None:
				return self
			if isinstance( self, requiredType ):
				return self
			elif self._Schema__namespace:
				if not alreadySeen:
					alreadySeen = {}
				alreadySeen[ id(self)] = True
				if not alreadySeen.has_key( id(self._Schema__namespace)):
					return self._Schema__namespace.lookupName( 
						requiredType=requiredType,
						alreadySeen = alreadySeen,
					)
			raise NameError( """Couldn't find any object of type %r in this namespace"""%(requiredType,))
		if hasattr(self, '_Schema__namespace'):
			if not alreadySeen:
				alreadySeen = {}
			alreadySeen[ id(self)] = True
			if not alreadySeen.has_key( id(self._Schema__namespace)):
				return self._Schema__namespace.lookupName( 
					name, requiredType =requiredType,
					alreadySeen = alreadySeen,
				)
		raise NameError( """Couldn't find name %r in the namespace(s) of %r object %r"""%(
			name,
			type(self),
			getattr(self, 'name',''),
		))
	def __iter__( self ):
		"""Iterate over our sub-elements"""
		if 0: yield self
	def findParent( self, requiredType=None ):
		"""Find our last parent of the given type, or None"""
		current = self
		lastParent = None
		while 1:
			# XXX is there any point in guarding against loops?
			current = getattr( current, '_Schema__namespace', None )
			if current is None:
				break
			else:
				if requiredType is not None and isinstance(current, requiredType):
					lastParent = current
				elif requiredType is None:
					lastParent = current
		return lastParent

class ParentSchema( Schema ):
	"""Base class for all Schemas which have children"""
	def lookupName( self, name=None, requiredType=None, alreadySeen=None ):
		"""Try to find object of the given name/type

		name -- if specified, look for an object with the
			given name (only)
		requiredType -- if specified, look for an object
			with the given type.

		lookupName searches up the _Schema__names containment
		hierarchy looking for matches to the given name/type
		pair.  Note: the search is *and* if both are specified,
		that is, both must be satisfied to match.
		"""
		if not self._Schema__names:
			self.buildNamespace()
		if isinstance( name, (str,unicode)):
			name = name.lower()
		elif name is None:
			if requiredType is None:
				return self
			if isinstance( self, requiredType ):
				return self
			elif self._Schema__namespace:
				if not alreadySeen:
					alreadySeen = {}
				alreadySeen[ id(self)] = True
				return self._Schema__namespace.lookupName( 
					requiredType =requiredType,
					alreadySeen = alreadySeen,
				)
			else:
				raise NameError( """Couldn't find any object of type %r in this namespace"""%(requiredType,))
		test = self._Schema__names.get( name )
		if test is not None:
			if not requiredType or (requiredType and isinstance(test, requiredType)):
				return test
		if hasattr(self, '_Schema__namespace'):
			if not alreadySeen:
				alreadySeen = {}
			if not alreadySeen.has_key( id(self._Schema__namespace)):
				alreadySeen[ id(self)] = True
				return self._Schema__namespace.lookupName( 
					name, requiredType =requiredType,
					alreadySeen = alreadySeen,
				)
		raise NameError( """Couldn't find name %r in the namespace(s) of %r object %r"""%(
			name,
			type(self),
			getattr(self, 'name',''),
		))
	def buildNamespace( self, ignoreDuplicates=1 ):
		"""Attempt to build namespace for this object"""
		self._Schema__names = names = {}
		for item in self:
			if names.has_key(item.name) and item.name:
				if not ignoreDuplicates:
					raise KeyError( """Item with name %r already exists in this namespace: conflict between %r and %r"""%(
						item.name, item, names.get(item.name),
					))
			if item.name:
				names[item.name.lower()] = item
			item.buildNamespace()
		return names

class ConstraintSchema( Schema ):
	"""Representation of a field or table constraint"""
	dbObjectType = "CONSTRAINT"
	name = common.StringProperty(
		'name', """Name of the constraint, often not specified""",
		defaultValue = "",
		setDefaultOnGet = 0,
	)
	fields = common.StringsProperty(
		"fields", """The list of fields affected by the constraint""",
	)
	deferrable = common.BooleanProperty(
		'deferrable', """Whether checking can be deferred to the end of the transaction""",
		defaultValue = 0,
	)
	deferred = common.BooleanProperty(
		'deferred', """Whether constraint is currently deferred""",
		defaultValue = 0,
	)
	def localFields( self ):
		"""Get field objects for the affected field(s)"""
		return [ self.lookupName(name) for name in self.fields]
	def resolve( self ):
		"""Attempt to resolve all field references"""
		for name in self.fields:
			self.lookupName( name )

class NotNullConstraint( ConstraintSchema ):
	"""A field's not-null constraint"""
	dbConstraintType = "NOT NULL"
class UniqueConstraint( ConstraintSchema ):
	"""(Possibly Multi-field) unique-value constraint"""
	dbConstraintType = "UNIQUE"
class PrimaryConstraint( UniqueConstraint ):
	"""(Possibly multi-field) primary-key unique constraint

	Implies both unique and NotNull
	"""
	dbConstraintType = "PRIMARY KEY"

def isPrimary( constraint ):
	"""Is the given object a primary-key constraint?"""
	return isinstance( constraint, PrimaryConstraint )
def isUnique( schema ):
	"""Does the given index/constraint create a unique or primary constraint?"""
	if isinstance( schema, (UniqueConstraint, PrimaryConstraint) ):
		return 1
	elif isinstance( schema, IndexSchema ) and schema.unique:
		return 1
	return 0

class CheckConstraint( ConstraintSchema ):
	"""An SQL-statement CHECK constraint"""
	dbConstraintType = "CHECK"
	expression = common.StringProperty(
		"expression", """The SQL-formatted expression to test on insertions/updates""",
		defaultValue = "",
	)

from basictypes import enumeration
actions = enumeration.EnumerationSet()
actions.new(
	value="NO ACTION",
	name = "noAction",
	friendlyName = "Do Nothing",
)
actions.new(
	value="CASCADE",
	name = "cascade",
	friendlyName = "Cascade Deletion",
)
actions.new(
	value="SET NULL",
	name = "null",
	friendlyName = "Set to NULL",
)
actions.new(
	value="SET DEFAULT",
	name = "default",
	friendlyName = "Set to Default",
)
class ActionProperty( enumeration.EnumerationProperty, basic.BasicProperty ):
	"""Class representing a constraint's action operation"""
	set = actions
del actions	
	

class ForeignKeyConstraint( ConstraintSchema ):
	"""Foreign-key constraint for a field or table"""
	dbConstraintType = "FOREIGN KEY"
	foreignTable = common.StringProperty(
		"foreignTable", """The name of the table which constrains us""",
		defaultValue = "",
	)
	foreignFields = common.StringsProperty(
		"foreignFields", """The fields which constrain us""",
	)
	onDelete = ActionProperty(
		"onDelete", """What to do when the constraint is violated

	CASCADE causes the local row to be deleted
	
	default is normally "NO ACTION", which raises
	errors.
	""",
	)
	onUpdate = ActionProperty(
		"onUpdate", """What to do when the referenced table.column changes

	CASCADE copies the new value
	
	default is normally "NO ACTION", which raises
	errors.
		""",
	)
	#queryAllForeignValues( )
	#viewForeign( )
	def resolve( self ):
		"""Attempt to resolve all field references"""
		super( ForeignKeyConstraint, self).resolve()
		table = self.lookupName( self.foreignTable, requiredType=BaseTableSchema )
		if self.foreignFields:
			for field in self.foreignFields:
				table.lookupName( field )
		elif hasattr( table, 'getUniqueKeys' ):
			assert table.getUniqueKeys(), """Foreign Key references table %r without specifying a field-name, table has no primary key"""%(
				self.foreignTable,
			)
		else:
			raise RuntimeError(
				"""Reference to foreign table %r retrieved a non-table object %r"""%(
					self.foreignTable,
					type(table),
				)
			)
	def getForeignFields( self ):
		"""Find the foreign field-name for the referenced table"""
		if self.foreignFields:
			return self.foreignFields
		else:
			table = self.lookupName( self.foreignTable )
			keys = table.getUniqueKeys()
			assert keys, """Foreign-key constraint %r references table %r which has no unique keys!"""%(
				self, table.name,
			)
			return keys[0]
			
	
def constraint_factories( cls ):
	return [ ForeignKeyConstraint, PrimaryConstraint, UniqueConstraint, CheckConstraint ]
ConstraintSchemas = list_types.listof(
	ConstraintSchema,
	name = "ConstraintSchemas",
	dataType = "list.ConstraintSchemas",
	factories = classmethod( constraint_factories ),
)

class SequenceSchema( Schema ):
	"""A sequence object used for implementing e.g. serial fields"""
	dbObjectType = "SEQUENCE"
	name = common.StringProperty(
		'name', """Name of the sequence""",
	)
	increment = common.IntegerProperty(
		'increment', """Amount to increment on each "next" call""",
		defaultValue = 1,
		setDefaultOnGet = 0,
	)
	ascending = basic.BasicProperty(
		"ascending", """Whether this is an ascending value""",
		_getValue = lambda property, client: client.increment > 0,
	)
	def defaultMinimum( property, client ):
		if client.ascending:
			return 1
		else:
			return -(2L**63)-1
	def defaultMaximum( property, client ):
		if client.ascending:
			return 2L**63-1
		else:
			return -1
	def defaultStart( property, client ):
		if client.ascending:
			return 1
		else:
			return -1
	minimumValue = common.IntegerProperty(
		'minimumValue', """Minimum value to which we will traverse""",
		defaultFunction = defaultMinimum,
		setDefaultOnGet = 0,
	)
	maximumValue = common.IntegerProperty(
		'maximumValue', """Maximum value to which we will traverse""",
		defaultFunction = defaultMaximum,
		setDefaultOnGet = 0,
	)
	start = common.IntegerProperty(
		'start', """Initial starting value""",
		defaultFunction = defaultStart,
		setDefaultOnGet = 0,
	)
	del defaultMinimum
	del defaultMaximum
	del defaultStart
	cycle = common.BooleanProperty(
		"cycle", """Whether to loop when reach end or produce errors""",
		defaultValue = 0,
	)
	
	
SequenceSchemas = list_types.listof(
	SequenceSchema,
	name = "SequenceSchemas",
	dataType = "list.SequenceSchema",
)

class FieldSchema(	ParentSchema ):
	"""Schema for a particular field of a table

	A field schema describes a particular field of
	a particular table (or view).  It is used to create
	descriptors (properties) which affect table rows
	(among other uses).
	"""
	dbObjectType = "COLUMN"
	name = common.StringProperty(
		'name', """Name of the field (required)""",
		defaultValue = "",
		setDefaultOnGet = 0,
	)
	def defaultFriendlyName( property, fieldSchema ):
		"""Get a reasonable property name for property of table"""
		try:
			tableSchema = fieldSchema.lookupName( requiredType = BaseTableSchema )
		except:
			return fieldSchema.name
		else:
			# okay, need to kludge it...
			base = fieldSchema.name.lower()
			table = tableSchema.name.lower()
			if base.startswith( table ):
				if len(base) != len(table):
					base = base[len(table):]
			base = base.replace( "_", " ")
			base = base.title()
			return base
	friendlyName = common.StringProperty(
		'friendlyName', """Name of the field (required)""",
		defaultFunction = defaultFriendlyName,
		setDefaultOnGet = 0,
	)
	del defaultFriendlyName
	index = common.IntegerProperty(
		'index', """Index of the field in its table/view""",
		defaultValue = -1,
		setDefaultOnGet = 0,
	)
	displaySize = basic.BasicProperty(
		'displaySize', """Text-mode display size of the value (can be a tuple)""",
		defaultValue = -1,
		setDefaultOnGet = 0,
	)
	internalSize = basic.BasicProperty(
		'internalSize', """Binary internal size of the value""",
		defaultValue = 1,
		setDefaultOnGet = 0,
	)
	def defaultSequenceName( prop, client ):
		"""Get default sequence name for the field"""
		if getattr( client, 'dbDataType', None ) in ('serial','bigserial'):
			try:
				tableSchema = client.lookupName( requiredType = BaseTableSchema )
			except:
				return '%s_seq'%(client.name,)
			else:
				# okay, need to kludge it...
				base = client.name.lower().replace( ".", "_")
				table = tableSchema.name.lower()
				return '%(table)s_%(base)s_seq'%locals()
		raise AttributeError( """Don't have a sequence name for %s"""%(
			client.name,
		))
	sequenceName = common.StringProperty(
		'sequenceName', """Sequence name for serial field data-types""",
		defaultFunction = defaultSequenceName,
	)
	del defaultSequenceName
	
	def defaultNullOk( property, client ):
		"""Search constraints for a NotNullConstraint"""
		for constraint in client.constraints:
			if isinstance( constraint, (NotNullConstraint,PrimaryConstraint) ):
				return 0
		return 1
	nullOk = common.BooleanProperty(
		'nullOk', """Whether value can be left null when inserting/updating

	This is actually just mirroring the presence of a
	NotNullConstraint in our constraints set.
	""",
		defaultFunction = defaultNullOk,
		setDefaultOnGet = 0,
	)
	del defaultNullOk
	defaultValue = basic.BasicProperty(
		"defaultValue","""A string representation of the default value for the field""",
	)
	constraints = common.ListProperty(
		'constraints', """Constraint objects which constrain this field""",
		baseType = ConstraintSchemas,
	)

	def defaultDataType( prop, client ):
		"""Try to get a default data-type for the field"""
		foreign = client.foreign()
		if foreign:
			# datatype is foreign.tablename.rest_of_type
			base = 'foreign.%s.'%( foreign.foreignTable, )
		else:
			base = ''
		try:
			databaseSchema = client.findParent( requiredType = DatabaseSchema )
		except NameError:
			databaseSchema = None
		else:
			if (
				databaseSchema and
				hasattr( databaseSchema, 'driver') and
				databaseSchema.driver
			):
				driver = databaseSchema.driver
				if driver and getattr( client, "dbDataType", None):
					return base + driver.sqlToDataType( client.dbDataType )
		if base:
			return base[:-1]
		raise AttributeError( """Schema %r doesn't define a dataType"""%(client,))
	dataType = common.StringProperty(
		'dataType', """wxoo string dataType declaration

	If not explicitly set, this value can normally be
	inferred from the database itself.  Explicitly
	setting the value allows for defining "special"
	dataTypes such as for a choice from a referenced
	table.
	""",
		defaultFunction = defaultDataType,
		setDefaultOnGet = 1,
	)
	del defaultDataType
	
	dbDataType = common.StringProperty(
		'dbDataType', """database's SQL dataType declaration""",
		defaultValue = "",
		setDefaultOnGet = 0,
	)
	def defaultPropertyClass( property, client ):
		"""Try to find the appropriate property class for given field"""
		if client.foreign():
			return "pytable.dbproperty.ReferenceProperty"
		return "pytable.dbproperty.DBProperty"
	propertyClass = common.ClassByNameProperty (
		"propertyClass","""The class used to represent this property object""",
		defaultFunction = defaultPropertyClass,
		setDefaultOnGet = 0,
	)
	del defaultPropertyClass
	baseClass = common.ClassByNameProperty (
		"baseClass","""The class used to represent items, also used for dataType and the like""",
	)
	control = common.ClassByNameProperty (
		"control","""Explicitly-set control class to use for this field""",
	)
	gridViewer = common.ClassByNameProperty (
		"gridViewer","""Explicitly-set gridViewer class to use for this field""",
	)
	gridEditor = common.ClassByNameProperty (
		"gridEditor","""Explicitly-set gridEditor class to use for this field

	Note: if this property is not set, but the control property
		is set, the control will be auto-wrapped as a grid editor.
	""",
	)
	
	def buildProperty( self ):
		"""Build a BasicProperty which uses this schema"""
		return self.propertyClass(
			name = self.name,
			schema = self,
		)
	def checkConstraint( self, constraint ):
		"""Check/ensure that constraint refers only to us"""
		if constraint.fields:
			if not constraint.fields == [self.name]:
				raise ValueError( """Constraint %r does not refer to the field in which it is defined %r"""%(
					constraint,
					self,
				))
		else:
			constraint.fields = [self.name]
		if hasattr( self, '_Schema__namespace'):
			constraint._Schema__namespace = self._Schema__namespace
	def __iter__( self ):
		"""Iterate over the sub-elements of this schema"""
		for constraint in self.constraints:
			self.checkConstraint( constraint )
			yield constraint

	def foreign( self ):
		"""Determine whether we have a foreign-key constraint"""
		for c in self.constraints:
			if c.dbConstraintType == ForeignKeyConstraint.dbConstraintType:
				return c
		return None


FieldSchemas = list_types.listof(
	FieldSchema,
	name = "FieldSchemas",
	dataType = "list.FieldSchemas",
)

class BaseTableSchema( ParentSchema ):
	"""Base-class for table-like schemas"""
	name = common.StringProperty(
		'name', """Name of the table (required)""",
		setDefaultOnGet = 0,
	)
	fields = common.ListProperty(
		'fields', """FieldSchema objects for the table""",
		baseType = FieldSchemas,
	)
	properties = common.DictionaryProperty(
		'properties', """Table/View's property-descriptor objects

		Created from fields via wrapping
		""",
		setDefaultOnGet = 0,
		defaultFunction = lambda property,client: client.buildProperties()
	)
	propertiesCalculated = common.BooleanProperty(
		'propertiesCalculated',
		"""Whether property-set was automatically calculated

	Used to determine whether to re-calculate if necessary
	""",
		defaultValue = 0,
		setDefaultOnGet = 0,
	)

	collectionClass = common.ClassByNameProperty(
		'collectionClass', """The class used to wrap result-sets as collection objects""",
		defaultValue = 'pytable.dbresultset.DBResultSet',
	)
	itemClass = common.ClassByNameProperty(
		'itemClass', """The class used to wrap result-set-row objects""",
		defaultFunction = lambda property,client: client.buildRowClass(),
		setDefaultOnGet = 1,
	)
	baseItemClass = common.ClassByNameProperty(
		'baseItemClass', """The default base-class for itemclass""",
		defaultValue = 'pytable.dbrow.DBRow',
		setDefaultOnGet = 0,
	)

	def buildRowClass( self ):
		"""Build a new row-class if we don't have an explicitly-specified one"""
		baseClasses = (self.baseItemClass,)
		if self.name:
			name = self.name
		else:
			name = 'QueryRow'
		properties = self.properties.copy()
		properties['schema'] = self
		for badchar in ('.','-'):
			name = name.replace( badchar, '_' )
		return type( str(name), baseClasses, properties)
		
	def buildProperties( self ):
		"""Build dbdescriptors for this table's properties/fields"""
		properties = {}
		for field in self.fields:
			new = field.buildProperty()
			properties[ new.name ] = new
		return properties



class TableSchema(BaseTableSchema):
	"""High-level representation of a table's structure/schema

	The TableSchema object encodes information about
	a particular table in the database.  It does not
	include information about, for instance, view-level
	joins or interdependencies, though it does (if
	possible) include information about relational
	integrity constraints such as references to other
	tables.
	"""
	dbObjectType = "TABLE"
	indices = common.ListProperty(
		'indices', """IndexSchema objects for indices on this table""",
		#baseType = IndexSchemas, # set below due to mutual dependencies
	)
	constraints = common.ListProperty(
		'constraints', """Constraint objects which constrain this table""",
		baseType = ConstraintSchemas,
	)
	# triggers
	inherits = common.StringsProperty(
		"inherits", """List of tables from which this table inherits
		
	Inherits is a PostgreSQL extension that creates an
	object-relational system with single and multiple
	inheritence types.  See PostgreSQL docs for details.
	""",
	)
	temporary = common.BooleanProperty(
		'temporary',
		"""Whether this table should be created in temporary storage

	Temporary tables do not persist across connections
	""",
		defaultValue = 0,
		setDefaultOnGet = 0,
	)
	withOIDs = common.BooleanProperty(
		"withOIDs", """Whether table should explicitly use OIDs (postgres only)""",
		defaultValue = False,
		setDefaultOnGet = False,
	)
	defaultRecords = common.ListProperty(
		"defaultRecords", """Set of default records to be included in table on creation""",
	)
	def defaultFriendlyNameField( property, client ):
		"""Try to figure out if there's a good candidate for friendlyName"""
		possibleNames = [ client.name + '_name', client.name+'name', 'name' ]
		for field in client.fields:
			if field.name.lower() in possibleNames:
				return field.name
		raise AttributeError( """Couldn't find a default friendlyName for table %r"""%(getattr(client, 'name', "<unknown table name>"),))
	friendlyNameField = common.StringProperty(
		"friendlyNameField", """Field to be used as friendly name for rows (i.e. used in UIs)""",
		defaultFunction = defaultFriendlyNameField,
	)
	del defaultFriendlyNameField

	_uniqueKeys = None
	def getUniqueKeys( self ):
		"""Get unique key-sets for this table

		Any of these key-sets can be used to uniquely
		identify a row in the table.
		"""
		if self._uniqueKeys is not None:
			return self._uniqueKeys
		primary = None
		sets = []
		for item in self:
			if isUnique( item ):
				if isPrimary( item ):
					primary = tuple( item.fields )
				else:
					sets.append( tuple( item.fields ))
		if primary:
			sets.insert(0, primary)
		self._uniqueKeys = sets
		return sets
	def __iter__( self ):
		"""Iterate over the sub-elements of this schema"""
		for field in self.fields:
			yield field
			for item in field:
				yield item
		for index in self.indices:
			index.table = self.name
			yield index
		for constraint in self.constraints:
			yield constraint
		

	def fromConnection( cls, connection, tableName, **named):
		"""Use introspection to build a table-structure object

		Relies on the connection's driver's action queries
		to provide the introspection features required for
		building the various sub-elements of the table
		structure.
		"""
		if hasattr( connection.driver, "tableStructure"):
			new = connection.driver.tableStructure(
				cursor = connection.cursor(),
				tableName = tableName,
				tableClass = cls,
				descriptorClass = FieldSchema,
				indexClass = IndexSchema,
				**named
			)
			new.propertiesCalculated = 1
			return new
		else:
			raise NotImplementedError("""The connection %r does not implement table structure queries"""%(connection,))
	fromConnection = classmethod(fromConnection)
	def resolve( self ):
		"""Attempt to resolve all references (check consistency)

		This will scan through each sub-element looking for
		name-references.  Each sub-element will have a pointer
		created for their active namespace, and each name will
		be checked in that namespace to determine that it does
		actually exist.  Sub-elements may perform additional
		checks (such as data-type agreement) as well.
		"""
		for item in self:
			item.buildNamespace()
		for item in self:
			item._Schema__namespace = self
			if hasattr( item, 'resolve'):
				item.resolve()
		if hasattr( self, 'friendlyNameField'):
			self.lookupName( self.friendlyNameField )
			
	actions = [
		sqlquery.SQLQuery(
			name="query",
			sql = """SELECT * FROM %(tableName)s;"""
		),
	]
	def query( self, query=None, connection = None, **named ):
		"""Do query returning records from this table/view

		query -- the sqlquery.SQLQuery to be run
		connection -- the connection to use to run the query
		named -- named arguments to pass to the query
		"""
		if query is None:
			query = self.actionByName( 'query' )
		elif isinstance( query, (str,unicode)):
			queryObject = self.actionByName( query )
			if queryObject:
				query = queryObject
			else:
				query = sqlquery.SQLQuery(sql = query, debug=named.get('debug',0))
		if not connection:
			raise TypeError( """Query %r called with a NULL connection %r"""%(query, connection,))
		if query:
			if not hasattr( named, 'tableName'):
				named['tableName'] = self.name
			cursor = query( connection, **named )
			return self.collectionClass(
				schema = self,
				cursor=cursor,
			)
		else:
			raise TypeError("""Called query on a view %r without a query action defined"""%(
				self,
			))


TableSchemas = list_types.listof(
	TableSchema,
	name = "TableSchemas",
	dataType = "list.TableSchemas",
)

class IndexSchema( Schema ):
	"""Schema for defining a particular index (on a particular table)

	properties are the participating properties for the index
	"""
	dbObjectType = "INDEX"
	name = common.StringProperty(
		'name', """Name of the index""",
		setDefaultOnGet = 0,
		defaultValue = "",
	)
	table = common.StringProperty(
		"table", """The table on which we are going to operate""",
	)
	fields = common.StringsProperty(
		'fields', """Set of field-names to index""",
	)
	unique = common.BooleanProperty(
		'unique', """Whether index values must be unique""",
		defaultValue = 1,
	)
	primary = common.BooleanProperty(
		'primary', """Whether index is a primary-key index""",
		defaultValue = 0,
	)
	accessMethod = common.StringProperty(
		"accessMethod", """The internal access method for the table

	Internally will likely default to "BTREE", but we
	specify default as "" to use the DB's default.

	This is not necessarily supported by your db, of course.
	""",
	)
	functionName = common.StringProperty(
		"functionName", """SQL function name taking fields and returning indexable value""",
	)
	where = common.StringProperty(
		"where", """SQL-formatted string defining a test expression

	Only records matching the where expression will be
	included in the index.
	""",
	)
	def resolve( self ):
		"""Attempt to resolve all references (check consistency)

		This will scan through each sub-element looking for
		name-references.  Each sub-element will have a pointer
		created for their active namespace, and each name will
		be checked in that namespace to determine that it does
		actually exist.  Sub-elements may perform additional
		checks (such as data-type agreement) as well.
		"""
		table = self.lookupName( self.table, requiredType=BaseTableSchema )
		assert table, """Couldn't get table for index %r"""%(self,)
		assert isinstance( table, BaseTableSchema ), """Table %r referenced by index %r appears not to be a table: %r!"""%(
			self.table, self, table,
		)
		for field in self.fields:
			try:
				table.lookupName( field )
			except NameError:
				raise NameError(
					"""Couldn't get field %r for index %r from table %r: known fields %s"""%(
						field,
						self,
						table.name,
						[f.name for f in getattr(table, 'fields',())]
					)
				)

IndexSchemas = list_types.listof(
	IndexSchema,
	name = "IndexSchemas",
	dataType = "list.IndexSchemas",
)
TableSchema.indices.baseType = IndexSchemas

class NamespaceSchema( ParentSchema ):
	"""Schema for a database namespace/sub-schema

	AFAIK only postgresql actually supports this
	feature, which creates a new namespace for views,
	indices, tables and sequences
	"""
	dbObjectType = "SCHEMA"
	name = common.StringProperty(
		'name', """Name of the schema/namespace""",
		defaultValue = "",
	)
	tables = common.ListProperty(
		'tables', """Tables in the schema""",
		baseType = TableSchemas,
	)
	sequences = common.ListProperty(
		"sequences", """Sequence/counter objects in the schema""",
		baseType = SequenceSchemas,
	)
	def __iter__( self ):
		"""Iterate over our sub-elements"""
		for table in self.tables:
			table._Schema__namespace = self
			yield table
		for sequence in self.sequences:
			sequence._Schema__namespace = self
			yield sequence
	def resolve( self ):
		"""Attempt to resolve all references (check consistency)

		This will scan through each sub-element looking for
		name-references.  Each sub-element will have a pointer
		created for their active namespace, and each name will
		be checked in that namespace to determine that it does
		actually exist.  Sub-elements may perform additional
		checks (such as data-type agreement) as well.
		"""
		# we can hold sequences, tables, views, sub-schemas
		for item in self:
			if not item.name.startswith( '%s.'%(self.name,)):
				item.name = '%s.%s'%(self.name, item.name)
		for item in self:
			item.buildNamespace()
		for item in self:
			item._Schema__namespace = self
			if hasattr( item, 'resolve'):
				item.resolve()
NamespaceSchemas = list_types.listof(
	NamespaceSchema,
	name = "NamespaceSchemas",
	dataType = "list.NamespaceSchemas",
)


class DatabaseSchema( NamespaceSchema ):
	"""Schema for an overall database object"""
	dbObjectType = "DATABASE"
	name = common.StringProperty(
		'name', """Name of the database""",
		defaultValue = "",
	)
	namespaces = common.ListProperty(
		"namespaces", """Sub-namespaces of the database""",
		baseType= NamespaceSchemas,
	)
	readOnly = common.BooleanProperty (
		"readOnly","""Disable all writing to the database if true""",
		defaultValue = 0,
	)
	driver = basic.BasicProperty(
		"driver", """Optional binding to the driver with which the schema works""",
	)
	def resolve( self, driver=None ):
		"""Attempt to resolve all references (check consistency)

		This will scan through each sub-element looking for
		name-references.  Each sub-element will have a pointer
		created for their active namespace, and each name will
		be checked in that namespace to determine that it does
		actually exist.  Sub-elements may perform additional
		checks (such as data-type agreement) as well.
		"""
		if driver:
			self.driver = driver
		self.buildNamespace()
		for item in self:
			item._Schema__namespace = self
			if hasattr( item, 'resolve'):
				item.resolve()
	def __iter__( self ):
		"""Iterate over our sub-elements"""
		for namespace in self.namespaces:
			yield namespace
		for value in super( DatabaseSchema, self ).__iter__():
			yield value
	def lookupName( self, name=None, requiredType=None, alreadySeen=None ):
		"""Lookup the name with schema-aware resolution"""
		if isinstance( name, (str,unicode)):
			if '.' in name:
				try:
					if alreadySeen is None:
						alreadySeen = {}
					alreadySeen[id(self)] = True
					namespace = super( DatabaseSchema, self ).lookupName(
						name = name.split( '.' )[0],
						alreadySeen = alreadySeen,
					)
				except NameError, err:
					pass
				else:
					return namespace.lookupName( 
						name=name, requiredType = requiredType,
						alreadySeen = alreadySeen 
					)
		return super( DatabaseSchema, self ).lookupName( 
			name=name, requiredType = requiredType,
			alreadySeen = alreadySeen
		)
	# procedures
	# users, groups, permissions
	# table-mapping name:schema
	def __repr__( self ):
		return """%s( name=%r, tables=[%s])"""%(
			self.__class__.__name__,
			self.name,
			",".join( [x.name for x in self.tables]),
		)
	__str__ = __repr__
	
