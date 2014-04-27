"""PyPgSQL PostgreSQL database driver"""
from pytable._postgresql import postgresdriver
from pyPgSQL import PgSQL
from basicproperty import common
from pytable import pypgsql
import decimal

class PGDriver( postgresdriver.PostgresDriver ):
	"""PyPgSQL PostgreSQL database driver

	This is the most commonly used driver for the
	PyTable module, and as such has had the most testing
	and debugging.  It provides basically all features,
	which are supported by PyTable, and is available
	under a Python-CNRI-style license.
	"""
	name = pypgsql.name
	### Required customization points (abstract methods)
	baseModule = PgSQL
	paramstyle = common.StringProperty(
		"paramstyle", """DBAPI 2.0 parameter-style value""",
		defaultValue = PgSQL.paramstyle,
	)
	threadsafety = common.IntegerProperty(
		"paramstyle", """DBAPI 2.0 threadsafety value XXX should be an enumeration!""",
		defaultValue = PgSQL.threadsafety,
	)
	apilevel = common.StringProperty(
		"apilevel", """DBAPI 2.0 apilevel value""",
		defaultValue = PgSQL.apilevel,
	)
	userDescription = """PostgreSQL database driver (via PyPgSQL)

Provides access to the open-source, cross-platform
server-based PostgreSQL database. This driver is
one of the preferred drivers for the system.

The homepages of PostgreSQL and PyPgSQL are:
	http://www.postgresql.org/
	http://pypgsql.sourceforge.net/
"""
	def getLastOID( cls, cursor ):
		"""Given a cursor, return last-inserted OID value

		This implementation overrides the base implementation to
		support the (non-standard) use of oidValue instead of
		lastrowid to store the OID value.
		"""
		try:
			oidValue = cursor.cursor.oidValue
		except AttributeError:
			oidValue = cursor.oidValue # may have been passed the raw cursor...
		return oidValue
	getLastOID = classmethod( getLastOID )

	localTypeRegistry = [
		(getattr(PgSQL,name), name[3:].lower())
		for name in dir(PgSQL)
		if (name.startswith( 'PG_' ) and name == name.upper())
	]
PGDriver.copyErrorsFromModule( PgSQL )

# XXX Hacky fix to PyPgSQL to allow it to deal with decimal.Decimal
# instances without constantly raising annoying errors...
if not getattr( PgSQL._quote, 'IS_OVERRIDE', False ):
	ORIGINAL_QUOTE = PgSQL._quote
	def _quote(value):
		"""Perform quoting on decimal.Decimal instances"""
		if isinstance( value, decimal.Decimal ):
			value = str( value )
		value = ORIGINAL_QUOTE( value )
		return value
	_quote.IS_OVERRIDE = True
	PgSQL._quote = _quote

