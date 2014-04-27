"""Basic Object-Relational-like Database Row class"""
from basicproperty import propertied, common, basic, weak
from pytable import dbresultset, sqlquery
import traceback

try:
	from basictypes import debug
except ImportError:
	from wxoo import debug
log  = debug.Log( "pytable.dbrow" )
##log.setLevel( debug.DEBUG )


class DBRow( propertied.Propertied ):
	"""An individual row in a result-set

	The DBRow uses the resultSet for the majority of its
	operation, basically just storing the per-row values
	here, with the database connection all provided by
	the result-set.

	Normally the DBRow class is *subclassed* to create
	a Row class for a particular table of the database.

	XXX This is a very heavy implementation compared to the
		one in OPAL's systems, we may need to move to a lighter
		implementation eventually, but we will need to retain
		the ability to use read/write operations as we do.

	XXX There are currently a number of issues regarding
		namespace collisions that need to be fixed fairly
		soon, as the database's schema can readily create
		collisions with the row's method names, for instance
		with an "update" field.
	"""
	__allow_access_to_unprotected_subobjects__ = 1
	_DBRow__data = basic.BasicProperty(
		'_DBRow__data', """The original data for this row, from the data-base""",
	)
	_DBRow__newValues = common.DictionaryProperty(
		'_DBRow__newValues', """Newly set, but not-yet committed values""",
	)
	_DBRow__wrappedValues = common.DictionaryProperty(
		'_DBRow__wrappedValues', """Retrieved and wrapped versions for data-values""",
	)
	def __getattr__( self, key ):
		"""Delegate attribute lookup to our resultSet or schema"""
		for target in ( 'schema', ):
			if key != target:
				source = (
					self.__dict__.get( target ) or 
					getattr(self.__class__, target, None)
				)
				try:
					return getattr( source, key )
				except AttributeError:
					pass
		if key != "_DBRow__data":
			try:
				return self._DBRow__data[ key ]
			except Exception:
				pass
		raise AttributeError( """%s instance does not have %r attribute"""%(
			self.__class__.__name__,
			key,
		))
	
	def setValue( self, fieldSchema, value ):
		"""Set the field's value for this row"""
		if getattr( self,'readOnly', None):
			raise AttributeError( """Attempt to set property %r of a read-only %s object"""%(
				fieldSchema.name, self.__class__.__name__,
			))
		self._DBRow__newValues[ fieldSchema.name ] = value
		self._DBRow__wrappedValues[ fieldSchema.name ] = value
		return value
	def getValue( self, fieldSchema ):
		"""Get the field's value for this row"""
		if self._DBRow__newValues.has_key( fieldSchema.name ):
			value = self._DBRow__newValues.get( fieldSchema.name )
			if value is DELETED:
				raise AttributeError( """%r instance' %r field has been deleted"""%(
					self.__class__.__name__,
					fieldSchema.name,
				))
			return value
		elif self._DBRow__wrappedValues.has_key( fieldSchema.name ):
			return self._DBRow__wrappedValues.get( fieldSchema.name )
		else:
			if hasattr( self, '_DBRow__data'):
				for possible in (fieldSchema.name, fieldSchema.name.lower(), fieldSchema.name.upper()):
					value = self._DBRow__data.get(possible)
					if value is not None:
						break
				if value is not None:
					if hasattr( fieldSchema, 'baseClass'):
						if hasattr( fieldSchema.baseClass, 'dbLoad' ):
							value = fieldSchema.baseClass.dbLoad( value )
							self._DBRow__wrappedValues[fieldSchema.name] = value
						elif hasattr(fieldSchema.baseClass, 'coerce'):
							value = fieldSchema.baseClass.coerce( value )
							self._DBRow__wrappedValues[fieldSchema.name] = value
					return value
			raise AttributeError( """%r instance has no %r field value"""%(
				self.__class__.__name__,
				fieldSchema.name,
			))
	def delValue( self, fieldSchema ):
		"""Delete field's value for this row"""
		found = 0
		value = None
		if not (fieldSchema.nullOk or hasattr(fieldSchema, 'defaultValue')):
			raise TypeError(
				"""%r instance field %s requires a non-null value and has no defaultValue, cannot delete"""%(
					self.__class__.__name__,
					fieldSchema.name,
				))
		for source in (
			'_DBRow__data',
			'_DBRow__wrappedValues',
			'_DBRow__newValues',
		):
			dictionary = getattr( self, source, None )
			if dictionary and dictionary.has_key( fieldSchema.name ):
				value = dictionary.get( fieldSchema.name )
				del dictionary[ fieldSchema.name ]
				found =1
			elif source=='_DBRow__data':
				for key in ( fieldSchema.name.lower(), fieldSchema.name.upper()):
					if dictionary.has_key( key ):
						value = dictionary.get( key )
						del dictionary[ key ]
						found =1
						break
		if not found:
			raise AttributeError( """%r instance has no attribute %r to delete"""%(
				self.__class__.__name__,
				fieldSchema.name,
			))
		self._DBRow__newValues[ fieldSchema.name ] = DELETED
		return value

	def insertQuery( self, cursor, *arguments, **named ):
		"""Insert this object as a new row in it's table

		cursor -- cursor/connection to use for update
		arguments, named -- passed to the query, though
			using arguments will almost certainly raise a
			TypeError, as the client argument is normally
			the second positional argument...

		This method will first see if you have an explicitly
		specified "insert" callable in your schema.  If you
		do not, will use a generic update query defined later
		in this module (RowUpdate).  Once it has determined
		which callable to use, will call the callable with:
			action( cursor, client=self, *arguments, **named )
		"""
		query = self.schema.actionByName( "insert" ) or RowInsert()
		if named.has_key( 'debug' ):
			try:
				setattr( query, 'debug', named.get('debug'))
			except (ValueError,TypeError):
				pass
		return query( cursor, client=self, *arguments, **named )
	def updateQuery( self, cursor, *arguments, **named ):
		"""Flush any changes to this row to the database

		cursor -- cursor/connection to use for update
		arguments, named -- passed to the query, though
			using arguments will almost certainly raise a
			TypeError, as the client argument is normally
			the second positional argument...

		This method will first see if you have an explicitly
		specified "update" callable in your schema.  If you
		do not, will use a generic update query defined later
		in this module (RowUpdate).  Once it has determined
		which callable to use, will call the callable with:
			action( cursor, client=self, *arguments, **named )
		"""
		query = self.schema.actionByName( "update" ) or RowUpdate()
		if named.has_key( 'debug' ):
			try:
				setattr( query, 'debug', named.get('debug'))
			except (ValueError,TypeError):
				pass
		return query( cursor, client=self, *arguments, **named )
	def abort( self, *arguments, **named ):
		"""Abort any changes to this row

		This simply clears the newValues dictionary for the row
		"""
		self._DBRow__newValues.clear()
	def deleteQuery( self, cursor, *arguments, **named ):
		"""Delete row from table
		
		cursor -- cursor/connection to use for update
		arguments, named -- passed to the query, though
			using arguments will almost certainly raise a
			TypeError, as the client argument is normally
			the second positional argument...

		This method will first see if you have an explicitly
		specified "delete" callable in your schema.  If you
		do not, will use a generic update query defined later
		in this module (RowUpdate).  Once it has determined
		which callable to use, will call the callable with:
			action( cursor, client=self, *arguments, **named )
		"""
		query = self.schema.actionByName( "delete" ) or RowDelete()
		if named.has_key( 'debug' ):
			try:
				setattr( query, 'debug', named.get('debug'))
			except (ValueError,TypeError):
				pass
		return query( cursor, client=self, *arguments, **named )
	def refreshQuery( self, cursor, *arguments, **named ):
		"""Refresh row from database
		
		cursor -- cursor/connection to use for refresh
		arguments, named -- passed to the query, though
			using arguments will almost certainly raise a
			TypeError, as the client argument is normally
			the second positional argument...

		This method will first see if you have an explicitly
		specified "refresh" callable in your schema.  If you
		do not, will use a generic refresh query defined later
		in this module (RowRefresh).  Once it has determined
		which callable to use, will call the callable with:
			action( cursor, client=self, *arguments, **named )
		"""
		query = self.schema.actionByName( "refresh" ) or RowRefresh()
		if named.has_key( 'debug' ):
			try:
				setattr( query, 'debug', named.get('debug'))
			except (ValueError,TypeError):
				pass
		return query( cursor, client=self, *arguments, **named )
	def currentQuery( self, cursor, *arguments, **named ):
		"""Retrieve (separate) row from database matching our keys
		
		cursor -- cursor/connection to use for refresh
		arguments, named -- passed to the query, though
			using arguments will almost certainly raise a
			TypeError, as the client argument is normally
			the second positional argument...
		"""
		query = self.schema.actionByName( "current" ) or RowCurrent()
		if named.has_key( 'debug' ):
			try:
				setattr( query, 'debug', named.get('debug'))
			except (ValueError,TypeError):
				pass
		return query( cursor, client=self, *arguments, **named )

	def dirty( self ):
		"""Return value indicating whether we have been changed"""
		return len(self._DBRow__newValues)

	def getProperties( cls ):
		"""Get (dbproperty) properties for this object"""
		base = super(DBRow,cls).getProperties()
		base = [
			item for item in base
			if not item.name.startswith( '_DBRow__')
		]
		# reorder in schema order...
		map = dict([(x.name,x) for x in base])
		result = [
			map.pop(schema.name)
			for schema in cls.schema.fields
			if map.has_key( schema.name )
		]
		result += map.values()
		return result
	getProperties = classmethod( getProperties)
	def _keyToFieldSchema( self, key ):
		"""Get a particular field schema by integer or string key"""
		props = self.schema.fields
		if isinstance( key, int ):
			return props[ key ]
		elif isinstance( key, (str,unicode)):
			try:
				return self.schema.lookupName( key )
			except NameError:
				raise KeyError( """Unknown field %s for schema %s"""%(key, self.schema))
		else:
			raise TypeError( """Don't know how to get field Schema for %r"""%(key))
	def __getitem__( self, key ):
		"""Provide dictionary/list-like indexing"""
		try:
			prop = self._keyToFieldSchema( key )
		except KeyError:
			if hasattr( self, key ):
				return getattr(self, key)
			raise KeyError( """%s instance has no %r field defined"""%(
				self.__class__.__name__, key,
			))
		else:
			return self.getValue( prop )
	def get( self, key, default=None ):
		"""Retrieve property value by name/index or return default"""
		try:
			prop = self._keyToFieldSchema( key )
		except KeyError:
			pass
		else:
			try:
				value = self.getValue( prop )
			except (AttributeError,KeyError,ValueError,TypeError):
				pass
		return getattr( self, key, default )
	def has_key( self, key ):
		"""Retrieve property value by name/index or return default"""
		return hasattr( self, key )
	def __setitem__( self, key, value ):
		"""Provide dictionary/list-like assignment"""
		try:
			prop = self._keyToFieldSchema( key )
		except KeyError:
			setattr( self, key, value )
			return value
		else:
			return self.setValue( prop, value )
	def setdefault( self, key, default ):
		"""Get current, setting to default if not currently set"""
		try:
			return self[ key ]
		except (KeyError,AttributeError), err:
			pass
		self[key] = default
		return self[key]
	def getConnection( self ):
		"""Try to get the database connection we should use

		If for some reason the connection isn't available will
		return None.  Note that this does *not* check that the
		connection is still valid!
		"""
		try:
			return self.cursor.connection
		except AttributeError:
			try:
				return self.connection
			except AttributeError:
				try:
					return self.application.getDBConnection()
				except AttributeError:
					pass
		return None
	def foreignSimpleRef( cls, key ):
		"""Retrieve table and field schemas for foreign key"""
		if isinstance( key, (str,unicode)):
			field = cls.schema.lookupName( key )
		else:
			field = key
		foreignRef = field.foreign()
		if foreignRef:
			foreignFields = foreignRef.getForeignFields()
			if len(foreignFields) == 1:
				foreignTable = cls.schema.lookupName(
					foreignRef.foreignTable
				)
				foreignField = foreignFields[0]
				return foreignTable, foreignTable.lookupName( foreignField )
		return None, None
	foreignSimpleRef = classmethod( foreignSimpleRef )
	def fromDict( cls,  dictionary ):
		"""Create class isntance from dictionary-of-values"""
		return cls( **dict([
			(k,v) for (k,v) in dictionary.iteritems()
			if k != '__create'
		]) )
	fromDict = classmethod( fromDict )
	def createSubRecords( self, key, value ):
		"""Create sub-records for this field-value reference
		
		key -- field or field-name
		value -- dictionary or DBRow instance
		"""
		foreignTable, foreignField = self.foreignSimpleRef( key )
		originalValue = value
		doInsert = True
		if foreignTable:
			if isinstance( value, dict ):
				doInsert = value.get( '__create', True )
				value = foreignTable.itemClass.fromDict( value )
			# we know what we are trying to reference
			try:
				value.currentQuery( connection )
			except KeyError, err:
				if doInsert:
					value.insertQuery( connection )
				else:
					raise KeyError(
						"""Subrecord reference without __create = True for %s (%s) did not find referenced record: %s"""%(
							key, originalValue, err,
						)
					)
			else:
				if value.dirty():
					value.updateQuery( connection )
			return value
		return value
	def referenceSubRecord( cls, key, record, fullPrefix=None ):
		"""Create SQL referencing string for given sub-record"""
		log.info( 'referenceSubRecord: %s %s  %s', key,record, fullPrefix )
		foreignTable, foreignField = cls.foreignSimpleRef( key )
		if not foreignTable:
			foreignTable = cls.schema
			foreignField = foreignTable.lookupName( key )
		
		if isinstance( record, dict ):
			record = foreignTable.itemClass( **record )
		_, properties = RowAction().getObjectSpec( record )
		
		if record.has_key( foreignField.name ):
			otherField = record[ foreignField.name ]
			if not isinstance( otherField, (dict,DBRow,SQLString)):
				log.info( 'directly returning value: %s', otherField )
				return otherField
		
		foreignFieldName = foreignField.name
		foreignTableName = foreignTable.name
		result = {}
		keySetFragments = []
		for subKey,subValue in properties.items():
			subKeyFull = str('%s.%s'%(fullPrefix or key,subKey))
			log.info( ' subKeyFull: %s', subKeyFull )
			if isinstance( subValue, (dict,DBRow)):
				log.info( ' sub-record')
				# recursive sub-record reference...
				# record is our remote table, so we want *its*
				# reference to the sub-record
				subRecordResult = foreignTable.itemClass.referenceSubRecord(
					subKey, subValue, subKeyFull,
				)
				if isinstance( subRecordResult, dict ):
					log.info( '  dictionary result: %s', subRecordResult )
					subValue = subRecordResult.pop( subKey )
					result.update( subRecordResult )
					#subValue = result[ subKeyFull ]
				else:
					subValue = subRecordResult
			log.info( '     %s = %s', subKeyFull, subValue )
			result[subKeyFull] = subValue
			subValueRef = asValueReference( subKeyFull, subValue )
			log.info( '     %s => %s', subKeyFull, subValueRef )
			keySetFragments.append( 
				'%(subKey)s = %(subValueRef)s'%locals() 
			)
		keySetFragments = " AND ".join( keySetFragments )
		record = SQLString( ('''(
			SELECT %(foreignFieldName)s FROM 
			%(foreignTableName)s WHERE %(keySetFragments)s
		)'''%locals()).replace( '\t', ' ').replace( '\n',' ' ) )
		log.info( '  setting query key %s to %s', key, record )
		result[ key ] = record
		return result
	referenceSubRecord = classmethod( referenceSubRecord )
	def all( cls ):
		"""Return the set of all instances"""
		order = getattr( cls.schema, 'DEFAULT_ORDER', '' )
		if order:
			order = 'ORDER BY %s'%( order, )
		return findTable( cls.schema.name ).query( 
			"""SELECT * FROM %(table)s %(order)s""",
			connection,
			table = cls.schema.name,
			order = order,
		)
	all = classmethod( all )

class SQLString( object ):
	"""Produces SQL string un-altered as string value"""
	def __init__( self, data ):
		self.data = data
	def __str__( self ):
		return self.data
	__repr__ = __str__
	def __nonzero__( self ):
		return bool( self.data )

class _MockValue( object ):
	def __init__( self, name ):
		self.name = name
	def __str__( self ):
		return self.name
	__repr__ = __str__
	def __nonzero__( self ):
		return False

DELETED = _MockValue( 'DEFAULT' )
NULL = _MockValue( 'NULL' )

def asValueReference( key, value ):
	"""Return a value-reference for given key:value pair
	
	Expands sub-record (dictionary, SQLstring etceteras)
	dropping any dictionary sub-keys into the properties 
	dictionary
	"""
	if isinstance( value, SQLString ):
		return str(value )
	else:
		return '%%(%s)s'%( key, )

class RowAction( sqlquery.SQLQuery ):
	"""Base-class for dbrow action queries

	This just provides the getObjectSpec method
	which scans through the unique keys sets looking
	for a set which is completely available from the
	client object.
	"""
	CREATE_SUBRECORDS = False
	def getObjectSpec( self, client, originalOnly=0 ):
		"""Get uniquely identifying client specifier

		return value is (tableName, keyProperties)
		where keyProperties is a dictionary mapping
		field name to (resolved/wrapped) field value
		"""
		from pytable import dbschema
		set = []
		err = None
		for keySet in client.getUniqueKeys():
			set = []
			for field in keySet:
				try:
					fieldValue = self.getFieldValue( client,field,originalOnly )
					if fieldValue is None:
						raise TypeError(  """Can't use a NULL as a key""" )
					set.append( fieldValue )
				except (KeyError,ValueError,TypeError,AttributeError),err:
					del set[:]
					break
			if set:
				break
		if not set:
			raise ValueError( "%r instance doesn't have enough data to fill any of it's key-sets, can't create a unique ID for it: %s"%(
				type(client).__name__,
				err,
			))
		return (
			client.schema.name,
			dict(set)
		)
	def getFieldValue( self, client, field, originalOnly ):
		"""Retrieve field value for the given field on client"""
		notNull = not getattr( client.__class__, field ).nullOk
		if originalOnly and hasattr( client, '_DBRow__data'):
			if notNull:
				value = client._DBRow__data[field]
			else:
				value = client._DBRow__data.get(field)
		else:
			if notNull:
				value = getattr(client, field)
			else:
				value = getattr( client, field, None )
		if type(value).__name__ == 'PgInt8':
			class Wrap:
				def __init__( self, value ):
					self.value = value
				def __str__( self ):
					return "%s::int8"%(self.value,)
				__repr__ = __str__
			value = Wrap(value)
		return str(field), value
		
	def createSubRecords( self, client, set ):
		"""Process property-set to replace references"""
		# do recursive insertion of dictionary/row types...
		newSet = {}
		for key,value in set.items():
			if isinstance( value, (dict, DBRow)):
				if self.CREATE_SUBRECORDS:
					value = client.createSubRecords( key, value )
				log.info( 'referenceSubRecords top-level for field %s', key)
				newValue = client.referenceSubRecord( key, value )
				log.info( 'referenceSubRecords top-level for field %s -> %s', key, value )
				if newValue is not None:
					value = newValue
			newSet[key] = value
		return newSet
	def keySetProperties( self, properties ):
		"""Produce set of fragments and arguments to select given row"""
		keySetFragments = []
		for k in properties.keys():
			if isinstance( properties[k], dict ):
				for subKey,subValue in properties[k].items():
					properties[subKey] = subValue
			if properties[k] is None:
				comparison = ' IS '
			else:
				comparison = ' = '
			keySetFragments.append(
				"%s%s%s"%( k, comparison, asValueReference( k, properties[k]) ),
			)
		return keySetFragments

class RowInsert( RowAction ):
	"""Default query to insert a DBRow object into database

	This default query does a very simple insert using
	all fields of the row's schema for which there is
	an attribute for the row.

	Note:
		Very slow inserts can result from situations where
		you have not defined a unique key!  The RowInsert
		action will attempt to find a unique identifier for
		the row by using the OID returned from the insertion
		to lookup the record.  This can take a few seconds
		on even very small tables!
	"""
	CREATE_SUBRECORDS = True
	sql = """INSERT INTO
		%(tableName)s
			%(tableColumns)s
	%(VALUE_TYPE)s
		%(tableColumnSubs)s
	;"""
	#debug = 1
	def __call__( self, cursor, client, doResolveQuery=None, doFullQuery=0, **named ):
		"""Update this single client instance in the database

		client -- the client object (a DBRow) being serviced
		doResolveQuery -- whether to do the database query to
			retrieve missing key-values, None indicates that the
			system should only do the query if it's needed, any
			other false value suppresses it, any true value forces
			it.  The query is considered required if there are no
			unique keys available on the client.
		doFullQuery -- if true, force a complete select of the
			record after insertion (which retrieves database-provided
			default values, for instance).
		"""
		# XXX need to catch no-fields-defined case and handle specially!
		if hasattr( cursor, 'cursor' ):
			cursor = cursor.cursor()
		properties = {}
		for field in client.schema.fields:
			if hasattr( client, field.name ):
				try:
					value = getattr( client, field.name )
				except AttributeError, err:
					if getattr( client, '_DBRow__newValues', {}).get( field.name ) is DELETED:
						value = DELETED
					else:
						raise
				properties[ str(field.name) ] = value
		if doResolveQuery is None:
			try:
				self.getObjectSpec( client )
				doResolveQuery = 0
			except ValueError:
				# don't have enough information to uniquely identify...
				doResolveQuery = 1
		if doResolveQuery or doFullQuery:
			# general query can be done without OIDs *IFF* we have
			# a full set of unique keys...
			try:
				table,fields = self.getObjectSpec( client )
			except (ValueError,KeyError), err:
				# okay, can we get the values/default values for a key-set?
				# this allows for serial data-types in databases that don't
				# provide for get-last-row semantics...
				connection = cursor.connection
				for keySet in client.getUniqueKeys():
					set = []
					toAssign = []
					toSetOnClient = []
					for field in keySet:
						try:
							set.append( 
								self.getFieldValue( client,field,originalOnly=False )
							)
						except (KeyError,ValueError,TypeError,AttributeError),err:
							field = getattr( client.__class__, field )
							try:
								log.debug( """Checking for nextValue on field %s""", field.name )
								newKeyValue = field.nextValue(connection)
								set.append( (str(field.name), newKeyValue) )
								toSetOnClient.append( (field.name,newKeyValue))
							except (AttributeError,ValueError, KeyError,TypeError ), err:
								log.debug( 'Error retrieving nextValue %s: %s', err, log.getException( err ) )
								del set[:]
								del toSetOnClient[:]
								break
							else:
								toAssign.append( str(field.name) )
					if set:
						if toSetOnClient:
							for key,value in toSetOnClient:
								setattr( client, str(key), value )
						break
				if set:
					for key,value in set:
						properties[key] = value
					for key in toAssign:
						setattr( client, key, properties[key] )
					assert self.getObjectSpec( client ), client
		if not properties:
			tableColumnSubs = tableColumns = ""
			VALUE_TYPE = 'DEFAULT VALUES'
		else:
			columnNames = properties.keys()
			tableColumns = '(%s)'%( ",".join( columnNames ), )
			properties = self.createSubRecords( client, properties )
			tableColumnSubs = []
			for k in columnNames:
				v = properties[k]
				if isinstance( v, dict ):
					for subKey,subValue in v.items():
						properties[subKey] = subValue
					properties[k] = v[k]
				tableColumnSubs.append( asValueReference( k, properties[k]) )
			tableColumnSubs = '(%s)'%(",".join( tableColumnSubs ) )
			VALUE_TYPE = 'VALUES'
		properties = self.createSubRecords( client, properties)
		return super( RowInsert, self ).__call__(
			cursor,
			tableName = client.schema.name,
			tableColumns = tableColumns,
			tableColumnSubs = tableColumnSubs,
			clientObject = client,
			doResolveQuery = doResolveQuery,
			doFullQuery = doFullQuery,
			VALUE_TYPE = VALUE_TYPE,
			**properties
		)
	def processResults( self, cursor, clientObject, doResolveQuery=0, doFullQuery=0, **named ):
		"""Process the result-set to set the key-values on the row

		Moves newValues to wrapped values
		Clears newValues
		if doResolveQuery:
			Updates data from resolution query
			Eliminates wrapped versions of data so updated
		if doFullQuery:
			Updates data from a full re-query
			Eliminates wrapped versions of data so updated.
		"""
		clientObject._DBRow__wrappedValues.update( clientObject._DBRow__newValues )
		clientObject._DBRow__newValues.clear()
		if doResolveQuery or doFullQuery:
			# general query can be done without OIDs *IFF* we have
			# a full set of unique keys...
			try:
				table,fields = self.getObjectSpec( clientObject )
			except (ValueError,KeyError), err:
				# have to use OIDs or similar driver-level query...
				try:
					fields = clientObject.getUniqueKeys()[0]
				except (IndexError, KeyError):
					fields = None
				if doFullQuery:
					fields = None
				newCursor = cursor.connection.driver.getInsertedRow(
					cursor,
					tableName = clientObject.schema.name,
					fields=fields,
				)
				data = dict(map( None, [x[0] for x in newCursor.description], newCursor.fetchone()))
				if not hasattr( clientObject, "_DBRow__data"):
					clientObject._DBRow__data = {}
				clientObject._DBRow__data.update( data )
				wrapped = clientObject._DBRow__wrappedValues
				for key,value in data.items():
					try:
						del wrapped[key]
					except KeyError:
						pass
			else:
				clientObject.refreshQuery(cursor.connection)
		return clientObject

class RowCurrent( RowAction ):
	"""Query to retrieve the current row-record for an instance"""
	CREATE_SUBRECORDS = False
	sql = """SELECT
		*
	FROM 
		%(tableName)s
	WHERE
		%(keySetFragments)s
	;"""
#	debug=1
	def __call__( self, cursor, client, **named ):
		"""Update this single client instance in the database

		client -- the client object (a DBRow) being serviced
		"""
		tableName, properties = self.getObjectSpec( client )
		expanded = self.createSubRecords( client, properties)
		keySetFragments = self.keySetProperties( expanded )
		keySetFragments = " AND ".join(keySetFragments )
		return super( RowCurrent, self ).__call__(
			cursor,
			tableName= tableName,
			keySetFragments = keySetFragments,
			clientObject = client,
			**expanded
		)
	def processResults( self, cursor, clientObject, **named ):
		"""Process the results by updating the clientObject"""
		row = cursor.fetchone()
		if row is None:
			raise KeyError( """Object %s no longer appears to be in the database, refresh query returned null result-set"""%(
				clientObject,
			))
		names = [ item[0] for item in cursor.description]
		data = dict( map(None, names, row))
		return clientObject.__class__(
			_DBRow__data = data,
		)
	
class RowRefresh( RowCurrent ):
	"""Query to do a refresh of database values for a dbrow object"""
	CREATE_SUBRECORDS = False
	def processResults( self, cursor, clientObject, **named ):
		"""Process the results by updating the clientObject"""
		row = cursor.fetchone()
		if row is None:
			raise KeyError( """Object %s no longer appears to be in the database, refresh query returned null result-set"""%(
				clientObject,
			))
		newData = dict(map( None, [x[0] for x in cursor.description], row))
		if not hasattr( clientObject, "_DBRow__data"):
			clientObject._DBRow__data = {}
		raw = clientObject._DBRow__data
		wrapped = clientObject._DBRow__wrappedValues
		new = clientObject._DBRow__newValues
		# clear out mock objects that hide previously set values
		for key,value in new.items():
			if isinstance(value, _MockValue ):
				for d in (raw,wrapped,new):
					try:
						del d[key]
					except KeyError:
						pass
		# clear out any wrapped/new values shadowing newly-queried values
		for key,value in newData.items():
			try:
				del wrapped[key]
			except KeyError:
				pass
			try:
				del new[key]
			except KeyError:
				pass
		# update the raw dictionary with the new values
		raw.update( newData )
		return clientObject
	
		
class RowUpdate( RowAction ):
	"""Query to do an update/commit for dbrow object

	This default query takes into account the possibility
	that the fields being used for uniquely identifying
	a row are themselves being changed, so goes through some
	contortions to create data sets which are able to
	specify both the original and changed values.
	"""
	CREATE_SUBRECORDS = True
	sql = """UPDATE
		%(tableName)s
	SET
		%(columnFragments)s
	WHERE
		%(keySetFragments)s
	;"""
	#debug=0
	def __call__( self, cursor, client, **named ):
		"""Update this single client instance in the database

		client -- the client object (a DBRow) being serviced
			must have non-null _DBRow__newValues attribute.
		"""
		if not client._DBRow__newValues:
			raise ValueError(
				"""Update called on %r which has no new data"""%(client,),
			)
		tableName, properties = self.getObjectSpec( client, originalOnly=1 )
		expanded = self.createSubRecords( client, properties)
		keySetFragments = " AND ".join(self.keySetProperties( expanded ))
		
		def unusedName( d, baseName ):
			count = 0
			name = baseName
			while d.has_key( name ):
				count += 1
				name = "%s%d"%( baseName, count )
			return name
		
		# now get any non-key-set changed values...
		columns = []
		columnFragments = []
		for key,value in client._DBRow__newValues.items():
			setName= unusedName( expanded, str(key) )
			
			if value is DELETED:
				schema = getattr(getattr(client.__class__, key, None), 'schema', None)
				if schema is None:
					value = NULL
				else:
					value = getattr( schema,'defaultValue', NULL)
				if value is NULL:
					if not schema.nullOk:
						continue # XXX issue a warning!
				if isinstance( value, (dict, DBRow )):
					# XXX will be failures if there is a conflicting
					# id reference!
					if self.CREATE_SUBRECORDS:
						value = client.createSubRecords( key, value )
					newExpanded = client.referenceSubRecord( key, value )
					value = newExpanded[ key ]
					del newExpanded[ key ]
					expanded.update(
						newExpanded
					)
					if self.CREATE_SUBRECORDS:
						value = client.createSubRecords( key, value )
					value = client.referenceSubRecord( key, value )
				
				if value is not NULL: # is the default, which is in SQL syntax form...
					columnFragments.append( "%s=%s"%(
						key,
						value,
					))
				else:
					columnFragments.append( "%s=%%(%s)s"%(
						key, # actual field name...
						setName, # may be different if we're changing an id key
					))
			else:
				if isinstance( value, (dict, DBRow )):
					# XXX will be failures if there is a conflicting
					# id reference!
					if self.CREATE_SUBRECORDS:
						value = client.createSubRecords( key, value )
					newExpanded = client.referenceSubRecord( key, value )
					if isinstance( newExpanded, dict ):
						value = newExpanded[ key ]
						del newExpanded[ key ]
						expanded.update(
							newExpanded
						)
					else:
						value = newExpanded
					columnFragments.append(
						'%s=%s'%( 
							key, 
							asValueReference( setName, value ) 
						)
					)
				else:
					columnFragments.append( "%s=%%(%s)s"%(
						key, # actual field name...
						setName, # may be different if we're changing an id key
					))
			
			expanded[setName] = value
		columnFragments = ",".join( columnFragments )
		return super( RowUpdate, self ).__call__(
			cursor, tableName = tableName,
			columnFragments = columnFragments,
			keySetFragments = keySetFragments,
			clientObject = client,
			**expanded
		)
	def processResults( self, cursor, clientObject, **named ):
		"""Process the result-set to set the key-values on the row

		Moves newValues to wrapped values
		Clears newValues
		"""
		clientObject._DBRow__wrappedValues.update( clientObject._DBRow__newValues )
		clientObject._DBRow__newValues.clear()
		return clientObject

class RowDelete( RowAction ):
	"""Delete a row from the table"""
	CREATE_SUBRECORDS = False
	sql = """DELETE FROM %(tableName)s WHERE %(keySetFragments)s;"""
	def __call__( self, cursor, client, **named ):
		"""Delete this single client instance in the database"""
		tableName, properties = self.getObjectSpec( client )
		keySetFragments = " AND ".join([
			"%s=%%(%s)s"%(key,key)
			for key in properties.keys()
		])
		return super( RowDelete, self ).__call__(
			cursor,
			tableName= tableName,
			keySetFragments = keySetFragments,
			clientObject = client,
			**properties
		)
	
