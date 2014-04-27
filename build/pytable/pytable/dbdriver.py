"""Base class for database driver implementations"""
from basicproperty import propertied, common, basic
from basictypes import enumeration

DriverNameSet = enumeration.EnumerationSet.coerce( [
	# Each driver class should have a name attribute pointing to
	# a DriverName instance registered in this set.

	# add new drivers with calls to new( name, friendlyName, value )
	# add new default drivers to defaultdrivers.py module
])

class DriverName( enumeration.Enumeration ):
	"""Specifier for a driver-name enumeration value"""
	datatype = 'enumeration.DriverName'
	set = DriverNameSet

class DriverCapabilities( propertied.Propertied ):
	"""Object storing set of driver capability declarations

	At the moment, this is a fairly limited set of capability
	declarations, mostly because the system only supports
	a small number of features which are not considered
	important enough to be implemented across all supported
	databases.
	"""
	serial = common.BooleanProperty(
		"serial", """Whether we have native support for serial datatype

	If the serial datatype is not supported, we'll have to
	generate code to create a sequence, track the name of
	that sequence and potentially rewrite the defaultValue
	field of the schema.
	""",
		defaultValue = 0,
		setDefaultOnGet = 0,
	)
	inherits = common.BooleanProperty(
		"inherits", """Whether we support PostgreSQL-style inheritance on tables

	Inherits is an object-relational database feature that
	provides (multiple) inheritance for database tables. If
	it's available, we can model object hierarchies more
	naturally.  If not, we need to do (complex, slow) joins
	across multiple tables to load base-class and sub-class
	data.
	""",
		defaultValue = 0,
		setDefaultOnGet = 0,
	)
	queryUnicode = common.BooleanProperty(
		"queryUnicode", """Whether can accept Unicode for query strings

	If this is false, then sqlquery needs to translate queries into
	strings, which it will do using utf-8 encodings.
	""",
		defaultValue = 1,
		setDefaultOnGet = 0,
	)
	queryPyformat = common.BooleanProperty(
		"queryPyformat", """Whether can handle pyformat paramstyle, if not will use pyformatsupport""",
		defaultValue = 1,
	)
	schemaSupport = common.BooleanProperty(
		"schemaSupport", """Whether the database supports sub-namespace/sub-schemas

		AFAIK only PostgreSQL actually supports the feature
	""",
		defaultValue = 0,
		setDefaultOnGet = 0,
	)
	lastRowID = common.BooleanProperty(
		"lastRowID", """Whether the database supports last-row-id reporting""",
		defaultValue = True,
		setDefaultOnGet = 0,
	)
	oids = common.BooleanProperty(
		"oids", """PostgreSQL concept of OID columns on tables""",
		defaultValue = False,
		setDefaultOnGet = 0,
	)

class DBDriver( propertied.Propertied):
	"""Base class for database driver implementations

	The DBDriver object is roughly analogous to the DB-API
	module.  In addition, it allows for resolving data types
	from native driver-data-type-declarations to basicproperty/
	basictypes/wxoo-style declarations.

	Subclasses will generally provide a considerable number of
	common query objects for use in introspection queries.
	
	Each DBDriver subclass is known by a specifier string which
	is a key in the DriverName enumeration.  The specifier
	strings are specified in the DBSpecifier object to select
	the appropriate DBDriver run-time class.

	Where appropriate, the DBDriver sub-class should
	allow for querying to determine "system" databases,
	such as ODBC named data sources.
		See: getSystemSpecifiers()
	"""
	capabilities = DriverCapabilities()
	name = basic.BasicProperty(
		'name', """DriverName enumeration identifying the driver in DBSpecifiers""",
		baseType = DriverName,
	)
	connections = common.WeakValueDictionaryProperty(
		"connections","""Mapping of specifier objects to live connections

	The DBDriver retains weak references to all active
	connections, to allow for connection sharing and/or
	properly shutting down all connections on exit.
	""",
		setDefaultOnGet = 1,
	)
	defaultConnectionClass = common.ClassByNameProperty(
		'defaultConnectionClass', """Default DBConnection sub-class to be used for this driver""",
		defaultValue = 'pytable.dbconnection.DBConnection',
	)
	friendlyName = common.StringProperty(
		"friendlyName", """Friendly name of the DBDriver type""",
		defaultValue = "",
	)
	paramstyle = common.StringProperty(
		"paramstyle", """DBAPI 2.0 parameter-style value""",
		defaultValue = "pyformat",
	)
	threadsafety = common.IntegerProperty(
		"paramstyle", """DBAPI 2.0 threadsafety value XXX should be an enumeration!""",
		defaultValue = 0,
	)
	apilevel = common.StringProperty(
		"apilevel", """DBAPI 2.0 apilevel value""",
		defaultValue = "2.0",
	)
	systemDBName = common.StringProperty(
		"systemDBName", """Default name for driver's system database (for listDatabases connections)""",
		defaultValue = "",
	)

	queries = {}
	userDescription = ""
	# properties which may be specified for a connection
	# file-based drivers likely will only have dsn in this set
	connectionProperties = ("dsn", "host","user","password", "database")
	fileBased = 0
	usesIntDescriptionTypes = True


	def copyErrorsFromModule( cls, source ):
		"""Method to copy Error/Class names from source to the driver class"""
		for name in (
			'Warning','Error','InterfaceError',
			'DatabaseError','DataError','OperationalError',
			'IntegrityError', 'InternalError','ProgrammingError',
			'NotSupportedError',
		):
			setattr(cls,name,getattr(source,name,StandardError))
		for name in (
			'Date','Time','Timestamp',
			'DateFromTicks','TimeFromTicks','TimestampFromTicks',
			'Binary',
			'STRING','BINARY','NUMBER','DATETIME','ROWID',
			'BOOLEAN',
		):
			setattr(cls,name,getattr(source,name,None))
	copyErrorsFromModule = classmethod( copyErrorsFromModule )
	def connect(self, specifier = None, share=1, **namedarguments):
		"""Connect using this driver to the specified database

		specifier -- the DBSpecifier object encoding the connection
			information to be used in establishing the connection
		
			If specifier is None, then create a new DBSpecifier
			using the named arguments as arguments to the DBSpecifier
			constructor.  Note: drivers with driver-specific specifier
			classes may construct those specific classes instead of
			the base DBSpecifier class.

			If specifier is not None, but there are namedarguments,
			the specifier will be cloned (copied) with the passed
			namedarguments as parameters to the clone method.  The
			result will be that the named argument values will override
			the specifier object's values.

		share -- if true, the connection will be shared with any existing
			connection which matches the calculated final specifier
		"""
		specifier = self.unifySpecifier(specifier, **namedarguments)
		if share:
			for spec,conn in self.connections.iteritems():
				if specifier == spec and not conn.invalid:
					self.connections[specifier] = conn
					return conn
		connection = self.establishConnection(specifier)
		connection = self.wrapConnection( connection )
		self.connections[specifier] = connection
		connection.specifier = specifier
		return connection
	def reconnect( self, connection ):
		"""Reconnect the given DBConnection object"""
		spec = None
		for spec,conn in self.connections.iteritems():
			if conn is connection:
				del self.connections[ spec ]
				break
		# prefer use of the connection's specifier attribute
		# use our local copy otherwise
		spec = getattr( connection, 'specifier', spec )
		if not spec:
			raise ValueError( """Attempting to reconnect a connection which is neither known to the system nor provides a 'specifier' property: %s"""%(
				connection,
			))
		rawConnection = self.establishConnection( spec )
		connection.connection = rawConnection
		return connection
	def unifySpecifier(self, specifier, **namedarguments):
		"""Given specifier and named arguments create finalSpecifier

		specifier -- DBSpecifer or None
		named -- dictionary of attribute name to attribute value

		See DBDriver.connect for discussion of the semantics
		"""
		if specifier is None:
			specifier = self.createSpecifier( **namedarguments )
		elif namedarguments:
			specifier = specifier.clone( **namedarguments )
		return specifier
				
	
	def createSpecifier(self, **namedarguments):
		"""Create a new specifier object for this driver

		namedarguments -- applied to the constructor of the
			DBSpecifier

		Note:
			the drivername property will be set to our name
			property's value
		"""
		from pytable import dbspecifier
		namedarguments["drivername"] = self.name
		return dbspecifier.DBSpecifier( **namedarguments )
	def getSystemSpecifiers(self,*arguments,**namedarguments):
		"""Customization Point: return list of system specifiers

		For APIs which have system-registered data sources,
		such as ODBC, this method should be overwritten to provide
		system specifiers for the system-registered data sources.
		"""
		return []
	def wrapConnection( self, connection ):
		"""Wrap the connection with a driver-aware connection object"""
		return self.defaultConnectionClass(
			connection = connection,
			driver = self,
		)

	### Required customization points (abstract methods)
	def establishConnection(self, fullSpecifier):
		"""Abstract Method: Connect using the fully specified specifier passed

		fullSpecifier -- a specifier with all arguments unified
			and ready to be connected.  This specifier should
			include everything required to do the actual
			connection (including passwords or the like).

		All sub-classes must override this method!
		"""
		raise NotImplementedError("""DBDriver sub-class %s does not define an establishConnection method"""% (self.__class__.__name__,))

	_dataTypeRegistry = None
	def sqlToDataType( self, source ):
		"""Convert given SQL data-type to the desired data-type specifier

		source -- the source specifier, an SQL identifier

		returns a wxoo specifier or raises KeyError, only returns
		the first-registered data-type, so sub-classes that want
		to override the defaults need to prepend their dataTypeRegistry
		to the dbdriver.DBDriver.dataTypeRegistry list.
		"""
		if not self._dataTypeRegistry:
			self._dataTypeRegistry = {}
			for dbtype,wxootype,basetype in self.dataTypeRegistry:
				self._dataTypeRegistry.setdefault( dbtype, []).append( (wxootype,basetype) )
		source = source.lower()
		item = self._dataTypeRegistry.get(source, [('',object)])[0][0]
		if not item:
			raise KeyError( """Driver %r doesn't know how to calculate wxoo specifier for data-type %r"""%(
				self,source,
			))
		return item
	def sqlToBaseType( self, source ):
		"""Convert given SQL data-type to a property-base-type

		source -- the source specifier, an SQL identifier

		returns a base-type suitable for use in basicproperty
		properties to control the property's operation.
		"""
		if not self._dataTypeRegistry:
			self._dataTypeRegistry = {}
			for dbtype,wxootype,basetype in self.dataTypeRegistry:
				self._dataTypeRegistry.setdefault( dbtype, []).append( (wxootype,basetype) )
		source = source.lower()
		item = self._dataTypeRegistry.get(source, [('',object)])[0][1]
		if not item:
			raise KeyError( """Driver %r doesn't know how to calculate wxoo specifier for data-type %r"""%(
				self,source,
			))
		return item

	_localTypeRegistry = None
	def localToSQLType( self, source ):
		"""Convert a local numeric data-type to an SQL string data-type

		source -- the source specifier

		returns an sql data-type for the given local SQL type, the
		sub-class must provide the actual implementation.
		"""
		if not self._localTypeRegistry:
			self._localTypeRegistry = {}
			for key,value in self.localTypeRegistry:
				self._localTypeRegistry.setdefault( key, []).append( value )
		if self.usesIntDescriptionTypes:
			# everything save PyGreSQL, at the moment...
			source = int(source)
		item = self._localTypeRegistry.get( source, [''])[0]
		if not item:
			raise KeyError( """Driver %r doesn't know how to calculate SQL specifier for data-type %r"""%(
				self,source,
			))
		return item

			
	localTypeRegistry = [
		# sub-classes will have to create a table to override this...
	]
	dataTypeRegistry = [
		# partial registry of common SQL name -> wxoo name values...
		("float", 'float', float) ,
		("float4", 'float', float) ,
		("float8" , 'float', float) ,

		("int2", 'int', int) ,
		("int4", 'int', int) ,
		("int8", 'long', long) ,
		("integer", 'int', int) ,
		
		#("bytea", 'str.long', str) ,
		("char", 'str', str) ,
		("text", 'str.long', str) ,
		("varchar", 'str', str) ,

		("bool", 'bool', 'basictypes.booleanfix.bool') ,

		("blob", 'str.locale', str) ,
		("bpchar", 'str.locale', str) ,

		("date" , 'datetime', 'mx.DateTime.DateTimeType') ,
		("interval" , 'datetimedelta', 'mx.DateTime.DateTimeDeltaType') ,
		("time", 'timeofday', 'basictypes.datemx_types.mxTimeOfDay') ,
		("timestamp", 'datetime', 'mx.DateTime.DateTimeType') ,
		("timestamptz", 'datetime', 'mx.DateTime.DateTimeType') , # missing zone info here

		# these 4 aren't mapped to anything useful yet
		("cash", 'decimal', int), 
		("money", 'decimal', int),
		("decimal", "decimal", int ),
		("numeric", 'decimal', int),
	]
