"""PyGreSQL PostgreSQL database driver"""
from pytable._postgresql import postgresdriver
import pgdb
from basicproperty import common
from pytable import pygresql

class PGDriver( postgresdriver.PostgresDriver ):
	"""PyGreSQL PostgreSQL database driver

	This driver is based on the PyGreSQL DB-API layer,
	which, though supported, is apparently not the most
	commonly used interface to PyGreSQL.  However, it
	*should* be fully functional, and provide all of the
	features of PyTable.  It's license is the same as
	PostgreSQL itself (it was formerly part of
	PostgreSQL).
	"""
	name = pygresql.name
	capabilities = postgresdriver.PostgresDriver.capabilities.clone(
		queryUnicode = False,
	)
	### Required customization points (abstract methods)
	baseModule = pgdb
	usesIntDescriptionTypes = False
	paramstyle = common.StringProperty(
		"paramstyle", """DBAPI 2.0 parameter-style value""",
		defaultValue = pgdb.paramstyle,
	)
	threadsafety = common.IntegerProperty(
		"paramstyle", """DBAPI 2.0 threadsafety value XXX should be an enumeration!""",
		defaultValue = pgdb.threadsafety,
	)
	apilevel = common.StringProperty(
		"apilevel", """DBAPI 2.0 apilevel value""",
		defaultValue = pgdb.apilevel,
	)
	userDescription = """PostgreSQL database driver (via PyGreSQL)

Provides access to the open-source, cross-platform
server-based PostgreSQL database.

The homepages of PostgreSQL and PyGreSQL are:
	http://www.postgresql.org/
	http://www.pygresql.org/
"""
	def getLastOID( cls, cursor ):
		"""Given a cursor, return last-inserted OID value

		This implementation overrides the base implementation to
		support the (non-standard) use of oidstatus() instead of
		lastrowid to store the OID value.
		"""
		try:
			oidValue = cursor.cursor.lastrowid
		except AttributeError:
			oidValue = cursor.lastrowid # may have been passed the raw cursor.
		return oidValue
	getLastOID = classmethod( getLastOID )

	localTypeRegistry = [
		(name, name) for name in [
			'int2', 'int4', 'serial','serial', 'int8',
			'float4', 'float8',
			'numeric','money', 
			'bool',
			'abstime', 'reltime', 'tinterval','date', 'time',
			'timespan', 'timestamp', 'timestamptz', 'interval',
			'oid', 'oid8',
		]
	]
PGDriver.copyErrorsFromModule( pgdb )
