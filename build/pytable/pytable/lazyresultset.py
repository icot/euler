"""Lazy-load result-set (cursor-wrapper) for DB-API cursors"""
from __future__ import generators
import sys, threading, traceback, types

try:
	EXPECTED_STOP_ERRORS = (StopIteration, IndexError, GeneratorExit)
except NameError, err:
	EXPECTED_STOP_ERRORS = (StopIteration, IndexError)

class LazyResultSet (object):
	"""Wrapper around a DB-API cursor providing lazy-loading

	The LazyResultSet is intended to allow for interleaved
	iterations, and random access of a result set provided by
	a DB-API cursor.  The LazyResultSet builds a cache of
	loaded (and potentially wrapped) objects which are
	returned from the cursor.

	Performance Considerations:

		If your cursor does not support rowcount, then taking
		a len( ) of the LazyResultSet will require loading the
		entire result set.  The same applies to taking negative
		indices, as they require calculating length first.

		Doing an index or contains with the default rows (the
		raw DB-API sequences) will require comparing each row
		with the sample row sequentially until the row is found.

	Attributes:
		cursor -- pointer to the cursor provided at initialization
		cursorDescription -- the cursor's description at
			initialization
		count -- number of records to retrieve in a given block
		__loadLock -- reentrant lock protecting the reading functions
		_rowCache -- the cache of loaded (and wrapped) rows
		length -- length of the result-set (once calculated)
		
	"""
	length = -1
	def __init__(self, cursor, count = 100, *arguments, **named ):
		"""Initialize the LazyResultSet

		cursor -- DB-API cursor with the result set to be
			wrapped by the LazyResultSet
		count -- number of records to retrieve in a single
			call to fetchMany
		"""
		self.cursor = cursor
		self.count = count
		# cache this in case our cursor is destroyed/reused
		# before we are...
		self.cursorDescription = cursor.description
		self.__loadLock = threading.RLock()
		self._rowCache = []
		super( LazyResultSet, self).__init__( *arguments, **named )
	def __getattr__( self, key ):
		"""Delegate attribute lookup to our cursor where possible"""
		if key != 'cursor':
			try:
				return getattr( self.cursor, key )
			except (AttributeError,KeyError):
				pass
		raise AttributeError( "%r instance has no %r attribute"%(
			self.__class__, key,
		))

	def wrapRow( self, data, index ):
		"""Customization Point: Wrap a single row with our DBRow class

		This customization point is intended to allow for use
		with customized row classes such as seen in The OPAL
		Group's db_row, or pytable's DBRow classes.

		index -- index of this row in the result-set/cache
		data -- DB-API result-object (a python sequence)

		You can get at the cursor via self.cursor, and the
		cursor description via self.cursorDescription
		"""
		return data

	def forceLoad( self, toIndex=None ):
		"""Force loading of all rows up to toIndex

		This method is called to load up to the given
		index in the result set.  The method stops
		loading when there are no more results, or the
		cache is now long enough to index with toIndex.
		"""
		if toIndex is None:
			toIndex = sys.maxint
		self.__loadLock.acquire()
		try:
			if len(self._rowCache) > toIndex:
				# may have been satisfied while waiting for lock
				return
			results = self.fetchMany()
			while results and len(self._rowCache) < toIndex:
				self._rowCache.extend( results )
				if not results:
					# reached the end of the result-set,
					# shut down the cursor...
					self._releaseCursor()
					self.length = len(self._rowCache)
					break
				if len(self._rowCache) > toIndex:
					# avoid the extra fetchMany...
					break
				results = self.fetchMany()
			if not results:
				self.length = len( self._rowCache )
		finally:
			self.__loadLock.release()
	def fetchMany( self, count=None ):
		"""Fetch and return count rows from cursor

		Note: these rows are not cached, you should not likely
		call this method save in a sub-class from a customized
		forceLoad method.
		"""
		if not self.cursor:
			return []
		self.__loadLock.acquire()
		try:
			index = len( self._rowCache )
			result = []
			try:
				dataSet = self.cursor.fetchmany(count or self.count)
			except Exception, err:
				pass
			else:
				for data in dataSet:
					result.append( self.wrapRow( data, index ))
					index += 1
				if len(result) < (count or self.count):
					# did not retrieve as many as requested, 
					# have hit the end of the result-set...
					self._releaseCursor()
			return result
		finally:
			self.__loadLock.release()
	def _releaseCursor( self ):
		"""Release our references to our cursor"""
		self.cursor = None
		try:
			del self.cursorDescription
		except AttributeError, err:
			pass
		
	def calculateLength( self ):
		"""Calculation of rowset length

		Called by the __len__ method and other instances
		with the length of the entire result set is required,
		see performance note under __len__.
		"""
		try:
			if self.length < 0:
				if self.cursor and self.cursor.rowcount > -1:
					self.length = self.cursor.rowcount
				else:
					self.forceLoad()
					self.length = len( self._rowCache )
		except Exception, error:
			traceback.print_exc( 10 )
			### This should really be the driver-specific DB error class
			## but unfortunately that is not a single class, so it is
			## quite annoying to catch.
			self.length = max( (0,len(self._rowCache)))
		if self.length < 0:
			self.length = 0
		return self.length
		

	### Collection/list API
	def __getitem__( self, index ):
		"""Get a particular row in the table

		Retrieves a given row in the table. If the row is
		not yet in the cache, this will cause all rows up
		to and including the row to be retrieved into the
		row-cache.
		"""
		if isinstance( index, types.SliceType ):
			return self.__getslice__( index.start, index.stop, index.step )
		if index < 0:
			if self.length < 0:
				# forces full load quite likely...
				self.calculateLength()
			i = index + self.length
			if i < 0:
				raise IndexError( """Attempted to get index %s of %s length table"""%( index, self.length))
			index = i
		cache = self._rowCache
		if index >= len( cache ):
			# forces full load quite likely...
			self.calculateLength()
			if index >= self.length:
				raise IndexError( """Attempted to get index %s of %s length table"""%( index, self.length))
		# okay, so the index is supposedly within our table, and is positive...
		if index < len(cache):
			return cache[index]
		# need to grow the cache up to index
		self.forceLoad( index+1 )
		return cache[index]
	def __getslice__( self, start=0, stop=sys.maxint, step=1 ):
		"""Get slice from the result-set

		This returns a new list of records/objects/rows from
		the result-set, forcing loading of all objects in the
		slice.

		start=0, stop= sys.maxint, step=1
		"""
		if start < 0:
			start = len(self) + start
		if stop < 0:
			stop = len(self) + stop
		result = []
		for i in xrange( start, stop, step ):
			try:
				result.append( self[i] )
			except (IndexError,KeyError):
				break
		return result
	def index (self, row ):
		"""Return the index of the given row, uses == checking for rows

		Performance Note:
			If the row object has an "index" attribute, this
			method can short-circuit by checking if that index
			is == given row.  Otherwise (or if self[row.index]
			!= given row), needs to scan sequentially, which
			may trigger a full result-set load.
		"""
		if hasattr( row, 'index') and isinstance( row.index, int):
			try:
				if self[row.index] == row:
					return row.index
			except (TypeError, ValueError):
				pass
		for (i,item) in enumerate(self):
			if item == row:
				return i
		raise ValueError( """Row %r not found in result-set %r"""%( row, self))
	def __contains__( self, row ):
		"""Determine whether we contain the given row

		Performance Note:
			If the row object has an "index" attribute, this
			method can short-circuit by checking if that index
			is == given row.  Otherwise (or if self[row.index]
			!= given row), needs to scan sequentially, which
			may trigger a full result-set load.
		"""
		try:
			self.index( row )
			return 1
		except ValueError:
			return 0
	def __len__(self):
		"""Return length of the table (number of rows)

		Performance Note:
			If the cursor object does not support the rowcount
			attribute, then __len__ will force a full load of
			the result set.
		"""
		if self.length < 0:
			return self.calculateLength()
		return self.length
	def __iter__( self ):
		"""Iterate through this result-set sequentially

		You should be able to use multiple iterators
		simultaneously alongside random access operations without
		causing any problems.
		"""
		index = 0
		while 1:
			try:
				yield self[index]
				index += 1
			except EXPECTED_STOP_ERRORS, err:
				break
			except (Exception), err:
				traceback.print_exc()
				sys.stderr.write( """Unexpected Exception type %r during result-set iteration\n"""%(err,))
				break
	def append( self, row ):
		"""Append a row to the table

		raises TypeError

		Sub-classes that allow for creating new records may
		want to override this method.
		"""
		raise TypeError("""%r object doesn't support item appending"""%(self,))
	def __delitem__( self, index ):
		"""Delete row at index from the table

		raises TypeError

		Sub-classes that allow for deleting records may
		want to override this method.
		"""
		raise TypeError("""%r object doesn't support item deletion"""%(self,))


try:
	enumerate
except NameError:
	def enumerate (sequence):
		"""Enumerate on Python < 2.3"""
		i = 0
		while 1:
			try:
				yield (i,sequence[i])
				i += 1
			except (StopIteration, IndexError):
				break
