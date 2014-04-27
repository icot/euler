from pytable import dbspecifier, specifierfromoptions, dbschema
import traceback, re
CLASS_NAME_LOOKUP={
	'TableSchema':'table','FieldSchema':'field',
	'ForeignKeyConstraint':'references',
	'IndexSchema':'index', 'NotNullConstraint': 'notNull',
	'UniqueConstraint': 'unique',
	'PrimaryConstraint': 'primaryKey',
}

sequenceStartMatcher = re.compile( r"""nextval\((.*)\:\:regclass\)""" )


def reprObject(self, indentation= "", alreadyDone = None, indentString='\t'):
	"""Produce a representation of the database in human-friendly code
	
	The purpose of this function is to produce a cleaned up code
	representation of the object "self".

	indentation -- current string indentation level
	alreadyDone -- set of object ids which are already finished
	"""
	properties = [p for p in self.getProperties() if not p.name.startswith('_')]
	if alreadyDone is None:
		alreadyDone = {}
	if alreadyDone.has_key( id(self) ):
		if hasattr( self, 'name' ):
			return """%s( name = %r)"""%( self.__class__.__name__, self.name)
		return """<Already Done %s@%s>"""%(self.__class__.__name__, id(self))
	alreadyDone[id(self)] = 1
	def sorter( x,y ):
		if x.name == 'name':
			return -1
		if y.name == 'name':
			return -1
		return cmp( x.name, y.name )
	def reprChild( x, indentation= "", alreadyDone=None ):
		"""Get representation of child at indentation level if possible"""
		if hasattr( x, 'getProperties'):
			try:
				return reprObject(
					self=x,indentation=indentation,alreadyDone=alreadyDone
				)
			except TypeError,err:
				# for instance if the object is a class
				traceback.print_exc()
				return ""
		elif isinstance( x, (unicode)):
			if str(x) == x:
				x = str(x)
		return repr(x)
	properties.sort( sorter )
	if CLASS_NAME_LOOKUP.has_key(self.__class__.__name__):
		value=CLASS_NAME_LOOKUP.get(self.__class__.__name__)
		fragments=['%s('%(value,)]
	else:	
		fragments = ['%s('%(self.__class__.__name__)]
		
	indentation = indentation + indentString
	dictionary = self.__dict__

	if self.__class__.__name__ == 'NotNullConstraint':
		return "notNull()"
	elif self.__class__.__name__ =='FieldSchema':
		#import pdb; pdb.set_trace()
		regular_properties=[property for property in properties if property.name not in ('name','dbDataType','internalSize','comment')]
		if not dictionary.has_key( 'dbDataType' ):
			dataType = 'XXX Unknown type!'
		else:
			dataType = dictionary[ 'dbDataType' ] 
		#assert dictionary.has_key( 'dbDataType' ), dictionary
		fragments.append(
			"""%s%r,%r,%r,\n%s%r,"""%(
				indentation,
				str(dictionary.get('name','unnamed')),
				str(dataType),
				dictionary.get('internalSize',0),
				indentation,
				dictionary.get('comment',''),
			)
		)
	else:
		regular_properties=properties
	
	for property in regular_properties:
		if dictionary.has_key( property.name ):
			value = dictionary.get( property.name )
			if (
				hasattr( property, 'default' ) and 
				hasattr( property.default, 'value' ) and 
				property.default.value == value 
			):
				pass
			elif isinstance( value, list) and not value:
				fragments.append( '%s%s = [],'%(indentation, property.name))
			elif isinstance( value, list ):
				start = '%s%s='%(indentation,property.name)
				if (
					[x for x in value if isinstance(x,(str,unicode))] == value and
					len(repr(value)) < (80-len(start))
				):
					# all strings...
					fragments.append('%s%s,'%(start,repr([str(x) for x in value])))
				else:
					start += '['
					fragments.append( start )
					indentation = indentation + indentString
					for item in value:
						fragments.append( '%s%s,'%(indentation,reprChild( item, indentation, alreadyDone)))
					indentation = indentation[:-(len(indentString))]
					fragments.append( '%s],'%(indentation))
			else:
				fragments.append(
					'%s%s = %s,'%(
						indentation,
						property.name,
						reprChild( value, indentation, alreadyDone )
				))
	indentation = indentation[:-(len(indentString))]
	fragments.append( '%s)'%(indentation))
	return "\n".join(fragments)
			
def printTable( driver, connection, tableName ):
	"""Get somewhat simplified view of the table specified"""
	table = driver.tableStructure( connection, tableName = tableName )
	for field in table.fields:
		for attribute in ('internalSize','displaySize'):
			if getattr(field,attribute,0) <= 0:
				try:
					delattr( field, attribute )
				except AttributeError, err:
					pass
		for attribute in ('dataType','index','baseClass'):
			try:
				delattr( field, attribute )
			except AttributeError, err:
				pass 
		if (
			getattr( field, 'dbDataType', None ) == 'int4' and
			getattr( field, 'defaultValue', '')
		):
			default = getattr( field, 'defaultValue', '')
			match = sequenceStartMatcher.match( default )
			if match:
				field.dbDataType = 'serial'
				field.sequenceName = match.group(1)
		if getattr(field, 'dbDataType', None) in (
			'serial','int4','bool','timestamp','timestamptz','date',
			'int8','bigint',
		):
			try:
				field.internalSize=0
			except AttributeError, err:
				pass
		if getattr( field, 'dbDataType', None) == 'int4':
			field.dbDataType = 'int'
		elif getattr( field, 'dbDataType', None) == 'bpchar':
			field.dbDataType = 'char'
	for constraint in table.constraints[:]:
		if isinstance( constraint, (dbschema.ConstraintSchema, dbschema.UniqueConstraint) ):
			if len(constraint.fields) == 1:
				field = table.lookupName( constraint.fields[0] )
				field.constraints.append( constraint )
				table.constraints.remove( constraint )
				del constraint.fields
	if not table.constraints:
		del table.constraints
	for index in table.indices[:]:
		try:
			del index.table 
		except AttributeError, err:
			pass
		if (index.unique or index.primary) and (len(index.fields) == 1):
			field = table.lookupName( index.fields[0] )
			if index.primary:
				new = dbschema.PrimaryConstraint()
			else:
				new = dbschema.UniqueConstraint()
			field.constraints.append(
				new
			)
			table.indices.remove( index )
	if not table.indices:
		del table.indices
	output=reprObject(table)
	return output, table
def formatStructure( specifier ):
	driver,conn = specifier.connect()
	result = [
		"'Auto-generated schema'",
		'from pytable.dbschema import *',
		'from pytable.schemabuilder import *'
	]
	tables = []
	tableNames = list(driver.listTables(conn))
	tableNames.sort()
	for tableName in tableNames:
		try:
			definition,table  = printTable( driver, conn, tableName )
		except Exception, err:
			result.append( '# XXX Unable to retrieve definition for table %r'%(tableName,))
		else:
			result.append( '%s = %s'%( tableName, definition ) )
			tables.append( tableName )
	current = None
	nsTables = []
	namespaceTables = list(driver.listNamespaceTables( conn ))
	namespaceTables.sort()
	for namespace,tableName in namespaceTables:
		if namespace != current:
			if nsTables:
				result.append(
					'%s.tables = [\n\t%s\n]'%( current, ",\n\t".join( nsTables ))
				)
				del nsTables[:]
			result.append( '%s = NamespaceSchema( name= %r )'%( namespace, namespace ) )
			current = namespace
		fullName = '%s.%s'%(namespace,tableName)
		nsTables.append( fullName )
		definition,table = printTable( driver, conn, fullName )
		result.append( '%s = %s'%( fullName, definition ) )
	if nsTables:
		result.append(
			'%s.tables = [\n\t%s\n]'%( current, ",\n\t".join( nsTables ))
		)
		del nsTables[:]
	result.append( '''schema = database(
	%r,
	comment = 'Schema automatically extracted from running database',
	tables=[
		%s
	],
	namespaces=[
		%s
	],
)'''%(
		specifier.database,
		',\n\t\t'.join( tables ),
		',\n\t\t'.join( [n[0] for n in dict(namespaceTables).items()] )
	))
	result.append( 'schema.resolve()' )
	return "\n".join( result )

if __name__ == "__main__":
	specifier = specifierfromoptions.specifierFromOptions()
	print formatStructure( specifier )
