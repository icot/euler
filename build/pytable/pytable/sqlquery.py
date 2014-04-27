"""Callable query objects for SQL databases"""
from basicproperty import propertied
try:
	from basictypes import debug
except ImportError:
	from wxoo import debug
log  = debug.Log( "pytable.sql" )
#log.setLevel( debug.DEBUG )
from pytable import pyformatsupport

class SQLQuery( propertied.Propertied ):
	"""An SQL query to be run against a cursor

	This is a callable object which is primarily
	defined by an SQL query-string.  Currently only
	supports pyformat-style query arguments.

	Attributes of note:
		sql -- SQL query string template, see the
			__call__ method for details, basically the
			template uses Python extended-string
			substitution on the query %(name)s, so you
			will need to escape % signs in the query.
		debug -- per-query debugging flag.  If true, then
			this particular query will log to the
			"wxoo.sql" debug-module Log.
	"""
	sql = ""
	debug = 0
	name = ""
	def __init__( self, sql=None, debug=None, **named ):
		"""Initialise the SQLQuery

		sql -- sql string or None to use class' sql value
		debug -- if provided (not None), override class' debug flag
		"""
		if sql is not None:
			named[ "sql" ] = sql
		if debug is not None:
			named[ "debug" ] = debug
		super( SQLQuery, self ).__init__( **named )
	def __call__( self, cursor, **namedarguments ):
		"""Execute with cursor

		cursor -- the pytable.dbcursor object to be
			used for executing the query.  Note that the
			query will attempt to automatically coerce a
			dbdriver or dbconnection object to a cursor
			using that driver/connection.  A log warning
			will be returned if passing a driver (which
			is not recommended, as it will result in
			significant setup overhead (connections are
			expensive to create for a single execution)).
		namedarguments -- will be substituted using
			python string substitution into the template
			query string in order to create the final
			query string. For single-execution queries
			(SQLQuery), the namedarguments also represent
			the row from which query arguments will be
			taken.  For multiple-execution queries
			(SQLMultiQuery), the namedargument "dataSet"
			is used as the executemany argument.

		The "do" method takes care of the actual execution
		of the query after cursor-coercion and query
		substitution.

		The "processResults" method takes the cursor and
		returns the final result-set for the query which
		will be the value returned from this function.
		By default, this is simply a pointer to the cursor
		used to execute the query.
		"""
		# add optional logging...
		if not hasattr( cursor, 'execute'):
			if hasattr( cursor, 'connect' ):
				if self.debug:
					log.warn( 'Query %s got specifier %s, opening temp connection', self, cursor)
				driver, cursor = cursor.connect()
			if hasattr( cursor, 'cursor' ):
				if self.debug:
					log.info( 'Query %s got connection %s, creating temp cursor', self, cursor)
				cursor = cursor.cursor()
		if isinstance( self.sql, (list, tuple)):
			results = []
			for statement in self.sql:
				query = statement%namedarguments
				if self.debug:
					log.warn( "%s -> %s"%( query, namedarguments) )
				self.do( cursor=cursor, query=query, **namedarguments)
				result = self.processResults( cursor, **namedarguments )
				results.append( result )
			return results
		else:
			try:
				query = self.sql%namedarguments
			except KeyError, err:
				raise KeyError( err, self.sql )
			if self.debug:
				log.warn( "%s -> %s"%( query, namedarguments) )
			self.do( cursor=cursor, query=query, **namedarguments)
			try:
				result = self.processResults( cursor, **namedarguments )
			except KeyError, err:
				raise
			except Exception, err:
				log.info(
					"Failuring processing results for query %s: %s",
					query, log.getException(err),
				)
				raise
			return result
	def do( self, cursor, query, **namedarguments ):
		"""Do the actual processing of the query (execute)

		cursor -- a dbcursor object
		query -- a final SQL query string, must be fully
			substituted so that decree will operate properly
			with the given cursor.
		namedarguments -- for the single-query version,
			(SQLQuery, this version), used as the dictionary
			source for named and pyformat query arguments.
			These are the same arguments passed to the
			__call__ method.

		Note: encodeQuery and translateQuery are both called
			on the query.  All queries are assumed to want
			pyformat support to allow for consistent usage,
			so the pyformatsupport module will be used to
			provide such support if the DB driver is declared
			not to support pyformat (see dbdriver.DriverCapabilities).

		returns the result of the cursor's execute method,
		which is currently ignored by the __call__ method.
		"""
		try:
			query = self.encodeQuery(query,cursor).strip()
			query, converter = self.translateQuery(cursor, query)
			if converter is not None:
				namedarguments = converter.retrieveValues( namedarguments )
		except Exception, err:
			log.info(
				"Failure executing query %s: %s",
				query, log.getException(err),
			)
			raise err.__class__( """(SQLQuery) %s\nQuery: %s\nArguments: %s"""%(
				str(err),
				query.strip(),
				namedarguments,
			))
		try:
			return cursor.execute( query, namedarguments )
		except (
			cursor.connection.driver.OperationalError,
			# ProgrammingError is *not* supposed to be here,
			# but pypgsql has a bug in that it reports db connection
			# failures as ProgrammingError
			cursor.connection.driver.ProgrammingError,
		), err:
			cursor.connection.invalid = 1
			raise err.__class__( """(SQLQuery) %s\nQuery: %s\nArguments: %s"""%(
				str(err),
				query.strip(),
				namedarguments,
			))
		except Exception, err:
			raise err.__class__( """(SQLQuery) %s\nQuery: %s\nArguments: %s"""%(
				str(err),
				query.strip(),
				namedarguments,
			))
	def encodeQuery( self, query, cursor=None ):
		"""Encode query for use by the given cursor"""
		if (
			cursor and
			not cursor.connection.driver.capabilities.queryUnicode and
			isinstance( query, unicode)
		):
			query = query.encode( 'utf-8' )
		return query
	def processResults( self, cursor, **namedarguments ):
		"""Convert the query results to desired format

		cursor -- a dbcursor object which has just executed
			this query. Note that the query may have
			returned an empty or null resultset, so this code
			should deal with that eventuality.
		namedarguments -- These are the same arguments
			passed to the __call__ method.

		This method provides post-processing of the query
		results into application-specific data formats.
		
		By default, simply returns the cursor.
		"""
		return cursor
	def translateQuery( self, cursor, query ):
		"""Translate the given query to format understood by database

		returns newQuery, converter, where converter is an object
		which has a retrieveValues( values ) method which returns
		a suitable data-set for the rewritten query OR is None, for
		queries that don't require rewriting.
		"""
		driver = cursor.connection.driver
		if not driver.capabilities.queryPyformat:
			pf = pyformatsupport.PyFormatSupport( driver.paramstyle )
			newQuery = pf.convertQuery( query )
			return newQuery, pf
		return query, None
		
class SQLMultiQuery( SQLQuery ):
	"""Multiple-execution version of an SQLQuery object

	SQLMultiQuery overrides the "do" method of the SQLQuery
	to use the cursor's executemany method, which allows for
	efficient execution of identical queries against multiple
	data set values.  It requires a named argument "dataSet"
	to be passed to the __call__ method which will provide
	the set of data to be passed to the executemany method.
	"""
	def do( self, cursor, query, dataSet, **namedarguments ):
		"""Do the actual processing of the query (executemany)

		cursor -- a dbcursor object
		query -- a final SQL query string, must be fully
			substituted so that decree will operate properly
			with the given cursor.
		dataSet -- must have been passed to the __call__ method
			as a named argument.  Should be a sequence of
			objects suitable for use as argument-sources for the
			cursor's executemany method.
		namedarguments -- unused in this version, these are the
			same arguments passed to the __call__ method.

		returns the result of the cursor's executemany method,
		which is currently ignored by the __call__ method.
		"""
		class Iterator( object ):
			def __init__( self, client, converter=None ):
				self.last = None
				self.iter = iter( client )
				self.converter = converter
			def __iter__( self ):
				return self
			def next( self ):
				"""Get next item from dataSet, store for error reporting"""
				self.last = value = self.iter.next()
				if self.converter is not None:
					value = self.converter.retrieveValues( value )
				return value
		query, converter = self.translateQuery( cursor, query )
		try:
			iterator = Iterator( dataSet, converter )
			return cursor.executemany( self.encodeQuery(query, cursor).strip(), iterator )
		except (
			cursor.connection.driver.OperationalError,
			# ProgrammingError is *not* supposed to be here,
			# but pypgsql has a bug in that it reports db connection
			# failures as ProgrammingError
			cursor.connection.driver.ProgrammingError,
		), err:
			cursor.connection.invalid = 1
			raise err.__class__( """(SQLMultiQuery) %s\nQuery: %s\nLast Record: %s"""%(
				str(err),
				query.strip(),
				repr(iterator.last)[:200],
			))
		except Exception, err:
			raise err.__class__( """(SQLMultiQuery) %s\nQuery: %s\nLast Record: %s"""%(
				str(err),
				query.strip(),
				repr(iterator.last)[:200],
			))
	def translateQuery( self, cursor, query ):
		"""Translate the given query to format understood by database

		Because we are doing multiple-value queries, we don't
		pass in a single value, instead the pyformatsupport will
		be used to do a retrieveValues() for each item in the
		result-set.
		"""
		driver = cursor.connection.driver
		if not driver.capabilities.queryPyformat:
			pf = pyformatsupport.PyFormatSupport( driver.paramstyle, multiple=True )
			newQuery = pf.convertQuery( query )
			return newQuery, pf
		return query, None
