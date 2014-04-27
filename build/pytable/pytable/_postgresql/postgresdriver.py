"""Base class for PostgreSQL database drivers"""
from pytable import dbdriver, sqlquery
from pytable._postgresql import tableactions
from basicproperty import common

class PostgresDriver( dbdriver.DBDriver ):
	"""Base PostgreSQL database driver
	"""
	baseModule = None
	capabilities = dbdriver.DriverCapabilities(
		serial = 1, inherits = 1, queryUnicode = 1,
		schemaSupport = 1, oids=1,
	)
	systemDBName = common.StringProperty(
		"systemDBName", """Default name for driver's system database (for listDatabases connections)""",
		defaultValue = "template1",
	)
	def establishConnection(self, fullSpecifier):
		"""Connect using the fully specified specifier

		fullSpecifier -- a specifier with all arguments unified
			and ready to be connected.  This specifier should
			include everything required to do the actual
			connection (including passwords or the like).

		All sub-classes must override this method!
		"""
		set = {}
		for name in ['dsn','database','user','password','host']:
			value = getattr( fullSpecifier, name )
			if value:
				set[name] = value
		return self.baseModule.connect( ** set )
	
	## Scripts/actions...
	def __getattr__( self, key ):
		"""Search for an action-script of the given name in actionScripts"""
		if key != 'queries':
			script = self.queries.get( key )
			if script:
				return script
		raise AttributeError( """%r object has no attribute %r"""%(self,key))

	def getInsertedRow( self, cursor, tableName, fields=None ):
		"""Select fields for the last insert on cursor

		cursor -- pytable.dbcursor instance which has had
			an insert query run as its last query.

			In this implementation, the cursor.cursor.lastrowid
			attribute will be used to specify the row to
			retrieve. Note: it is possible for this field
			not to be available if the user has explicitly
			suppressed oid generation for the table.
		tableName -- name of the table to be selected from
		fields -- sequence of field names to select from the
			table, uses * by default

		returns cursor for the given selection query, note
		that in error cases this may not have any records, and
		that there may be errors raised if the table or fields
		given are not part of the database.

		Note:
			This method implements the driver-specific mechanism
			for retrieving the results of the last insertion to the
			database.  This is an SQL problem area where it is
			generally difficult to determine what particular record
			has been inserted by giving query.  Each database tends
			to have its own method for doing such a query,
			reporting the data required to do to query, etc.
		"""
		from pytable import sqlquery
		if not fields:
			fields = ['*']
		fieldNames = ",".join( fields )
		oidValue = self.getLastOID( cursor )
		if not isinstance( oidValue, (int,long)):
			raise ValueError("""oidValue for getInsertedRow is not an integer, did the insert work? %r"""%(
				oidValue,
			))
		newCursor = sqlquery.SQLQuery(
			sql = """SELECT %(fieldNames)s FROM %(tableName)s
			WHERE oid = %(oidValue)s;"""
		)(
			cursor.connection, # note use of fresh cursor
			tableName = tableName,
			fieldNames = fieldNames,
			oidValue = oidValue,
		)
		return newCursor

	def getLastOID( cls, cursor ):
		"""Given a cursor, return last-inserted OID value

		This base implementation assumes the use of the DB-API
		standard lastrowid, though the most common PyTable driver
		(PyPgSQL actually uses oidValue)
		"""
		try:
			oidValue = cursor.cursor.lastrowid
		except AttributeError:
			oidValue = cursor.lastrowid # may have been passed the raw cursor...
		return oidValue
	getLastOID = classmethod( getLastOID )

	queries = {
		'listDatabases': tableactions.ListDatabases(),
		'listTables': tableactions.ListTables(),
		'listNamespaces': tableactions.ListNamespaces(),
		'listNamespaceTables': tableactions.ListNamespaceTables(),
		'listIndices': tableactions.ListIndices(),
		'attrDefault': tableactions.AttributeDefaultValue(),
		"tableStructure": tableactions.TableStructure(),
		"foreignConstraints":tableactions.ForeignConstraints(),
		"listDatatypes": tableactions.ListDatatypes(),
	}


	dataTypeRegistry = dbdriver.DBDriver.dataTypeRegistry + [
		("bigint", 'long', long) ,
		("smallint", 'int', int) ,
		("double precision", 'float', float),
		
		("serial", "id.int.serial", int),
		("serial4", "id.int.serial", int),
		("bigserial", "id.long.serial", long),
		("serial8",  "id.long.serial", long),

		("boolean", 'bool', 'basictypes.booleanfix.bool') ,

		("blob", 'str.locale', str) ,
		("bytea", 'str.locale', str) ,
		("bpchar", 'str.locale', str) ,

		("date" , 'datetime', 'mx.DateTime.DateTimeType') ,
		("interval" , 'datetimedelta','mx.DateTime.DateTimeDeltaType') ,
		("time", 'timeofday', 'basictypes.datemx_types.mxTimeOfDay') ,
		("timestamp", 'datetime', 'mx.DateTime.DateTimeType') ,
		("timestampz", 'datetime', 'mx.DateTime.DateTimeType') , # missing zone info here
		("tinterval", 'datetimedelta', 'mx.DateTime.DateTimeDeltaType') ,
		("abstime", 'datetime', 'mx.DateTime.DateTimeType') ,
		("reltime", 'datetimedelta','mx.DateTime.DateTimeDeltaType') ,

##		("aclitem", '') ,
##		("box", '') ,
##
##		("cid", '') ,
##		("circle", '') ,

		("inet", 'str.ipaddress', 'basictypes.domainname.DomainName') ,
		("cidr", 'str.netmask', str) ,
		("macaddr", 'str.macaddr', str) ,

		("int2vector", 'list.int', 'basictypes.list_types.listof_ints') ,
##		("line", '') ,
##		("lseg", '') ,
##		("name", '') ,
##		("oid", 'oid') ,
##		("oidvector", 'list.oid') ,
##		("path", '') ,
##		("point", '') ,
##		("polygon", '') ,
##		("refcursor", '') ,
##		("regproc", 'oid') ,
##		("rowid", '') ,
##		("tid", '') ,
##		("unknown", '') ,
##		("varbit", '') ,
##		("xid", '') ,
##		("zpbit", '') ,

		# Extension types...
		('chkpass', 'str.password', str ),
	]
