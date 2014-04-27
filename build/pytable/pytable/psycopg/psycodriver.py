"""psycopg PostgreSQL database driver"""
from pytable._postgresql import postgresdriver
from pytable import psycopg as pytable_psycopg
from pytable import dbdriver
import psycopg
from basicproperty import common

class PsycoDriver( postgresdriver.PostgresDriver ):
	"""psycopg PostgreSQL database driver

	PsycoDriver is a minor customisation of the PyPgSQL
	driver to allow interoperation with psycopg.  Note that
	psycopg is a *GPL* licensed driver.  If you include it
	in your project you must abide by the restrictions of
	the GPL.

	The wrapper here includes no GPL code, so should not be
	under any GPL restrictions as long as it is not bundled
	with GPL code.
	"""
	name = pytable_psycopg.name
	baseModule = psycopg
	capabilities = dbdriver.DriverCapabilities(
		serial = 1, inherits = 1, queryUnicode = 0,
	)

	### Required customization points (abstract methods)
	paramstyle = common.StringProperty(
		"paramstyle", """DBAPI 2.0 parameter-style value""",
		defaultValue = psycopg.paramstyle,
	)
	threadsafety = common.IntegerProperty(
		"paramstyle", """DBAPI 2.0 threadsafety value XXX should be an enumeration!""",
		defaultValue = psycopg.threadsafety,
	)
	apilevel = common.StringProperty(
		"apilevel", """DBAPI 2.0 apilevel value""",
		defaultValue = psycopg.apilevel,
	)
	userDescription = """PostgreSQL database driver (via psycopg)

Provides access to the open-source, cross-platform
server-based PostgreSQL database.

WARNING:
	Because of GPL restrictions psycopg is not a
	prefered driver for the system, but it does
	connect to PostgreSQL, which is the prefered
	database, and should be functionally equivalent
	to PyPgSQL

The homepages of PostgreSQL and psycopg are:
	http://www.postgresql.org/
	http://initd.org/software/initd/psycopg
"""

	# psycopg stores numeric values of type-names in the values
	# attribute of the named objects, so we need to extend for
	# each of those
	localTypeRegistry = []
	for _name in [
		'BOOLEAN','BINARY','DATE','DATETIME',
		'FLOAT','INTEGER','INTERVAL',
		'LONGINTEGER','NUMBER','ROWID','STRING',
		'TIME',
	]:
		for _num in getattr(psycopg,_name).values:
			localTypeRegistry.append( (_num, _name.lower()))
	del _name, _num
		
PsycoDriver.copyErrorsFromModule( psycopg )
