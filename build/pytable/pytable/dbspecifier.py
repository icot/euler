"""Class specifying parameters for a database connection"""
from basicproperty import propertied, common, basic
from pytable import dbdriver, defaultdrivers

class DBSpecifier( propertied.Propertied):
	"""Class specifying database connection using a DBDriver

	The DBSpecifier provides specification of a connection to
	a given database.  The format of the specifier mimics
	the DBAPI 2.0 connect function's recommended parameter
	names.

	The drivername property specifies (as a string) a particular
	registered DBDriver which provides a uniform interface to
	the database driver.  Calling myDBDriver.connect( specifier )
	should return a connection object for the specifier.

	DBDrivers should return DBSpecifier objects when queried
	for the list of "system" specifiers (if they provide that
	functionality).

	The application should manipulate specifier objects, rather
	than connection parameters to allow for, for instance,
	changing drivers databases, users or passwords for the
	specifier from within the interface (i.e. if an error is
	encountered, the error should report the specifier, and
	potentially allow for altering the specifier and then
	re-connecting).

	Note:
		Many database systems will not require all of the
		data values described.  They might require extra
		properties as well.  Unused properties should be
		ignored by the driver.  Properties which are
		needed should be added to sub-classes, rather than
		the base class here.

		XXX There should be a registry of sub-classes
		from which we can create factories for the specifiers!
	"""
	drivername = basic.BasicProperty(
		'drivername', """The database driver name to use in connecting to the database""",
		baseType = dbdriver.DriverName,
		### XXX this is wrong, wrong wrong!
		## should have an interface on the class allowing us to
		## query for whether there's a default or not, and then
		## get it if there is!
		defaultValue = 'PyPgSQL',
		setDefaultOnGet = 0,
		friendlyName = "Driver",
	)
	dsn = common.StringProperty(
		'dsn', """Database specifier name, the system-specific name for this database""",
		defaultValue = "",
		friendlyName = "Data Source",
	)
	database = common.StringProperty(
		'database', """The name of the database within the database server""",
		defaultValue = "",
		friendlyName = "Database Name",
	)
	user = common.StringProperty(
		'user', """The username used to connect to the database""",
		defaultValue = "",
		friendlyName = "User Name",
	)
	password = common.StringProperty(
		'password', """The password used to connect to the database""",
		defaultValue = "",
		friendlyName = "Password",
	)
	host = common.StringProperty(
		'host', """The network address of the database""",
		defaultValue = "",
		friendlyName = "Server Name",
	)
	_keyValues = common.ListProperty(
		'_keyValues', """List of values which are the "identity" of a specifier""",
		defaultFunction = lambda a,b: [ "drivername","dsn","database","user","host"],
	)
	def __str__( self ):
		"""Convert to a string representation"""
		result = []
		for key in self._keyValues:
			value = self.__dict__.get( key )
			if value:
				result.append( '%s=%r'%(key, value))
		return """%s( %s )"""%( self.__class__.__name__, ", ".join(result))
	def __add__( self, other ):
		"""Add the values in other to our values

		If there is no change, returns self, otherwise returns
		a new instance of our class with the updated values.
		"""
		if not other:
			return self
		otherValues = other.getCloneProperties()
		otherValues[ "drivername" ] = self.drivername
		return self.clone( **otherValues )
	def _getKey( self ):
		"""Get a key-value for this specifier"""
		return tuple([getattr(self,name) for name in self._keyValues])
	def __cmp__( self, other ):
		"""Compare this specifier to the other specifier

		If the other isn't a specifier, always returns -1

		Otherwise compares:
			drivername,dsn,database,user,host
		"""
		if not isinstance( other, DBSpecifier ):
			return -1
		# note that password is not included!
		return cmp( self._getKey(),other._getKey() )
	def getDriver( self ):
		"""Get driver instance for this specifier"""
		driver = self.drivername.value()
		from basictypes import latebind
		driverClass = latebind.bind( driver )
		driver = driverClass()
		return driver
	def connect( self, share=1, **arguments ):
		"""Connect to the database specified, return (driver,connection)

		See DBDriver.connect for argument semantics.

		Will raise ImportError if can't find our driver's
		class.
		"""
		driver = self.getDriver()
		connection = driver.connect( self, share= share, **arguments )
		return driver, connection
		
