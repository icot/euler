import unittest, traceback
from pytable import dbspecifier, dbschema, sqlquery, specifierfromoptions

testSpec = specifierfromoptions.specifierFromOptions()

primarySpecifiers = specifiers = [
	testSpec,
]

class ConnectTest( unittest.TestCase ):
	def testConnect( self ):
		failed = []
		for specifier in specifiers:
			try:
				specifier.connect()
			except Exception, err:
				failed.append( (specifier,err) )
		if failed:
			raise IOError( '''Couldn't connect: %s'''%failed )
	def testListDB( self ):
		"""Test to see if we can list the database for each connection"""
		for specifier in specifiers:
			driver, connection = specifier.connect()
			if hasattr( driver, 'listDatabases'):
				result = driver.listDatabases( connection )
				assert result, """0 databases on server? %s"""%(specifier)
			if hasattr( driver, 'listTables' ):
				tables = driver.listTables( connection )
				if hasattr( driver, 'listIndices' ):
					for table in tables:
						result = driver.listIndices( connection, tableName=table )
				if hasattr( driver, 'attrDescription'):
					for table in tables:
						cursor = driver.attrDescription( connection, tableName=table )
				if hasattr( driver, 'attrDefault'):
					for table in tables:
						cursor = driver.attrDefault( connection, tableName=table )
	def testQueryTableStructure(self):
		"""Test whether the TableStructure object can introspect"""
		for specifier in specifiers:
			driver, connection = specifier.connect()
			if hasattr( driver, 'listTables' ):
				tables = driver.listTables( connection )
				for table in tables:
					result = dbschema.TableSchema.fromConnection(
						connection, tableName = table,
					)
					if not result.getUniqueKeys():
						print """Table %s doesn't have a unique index"""%(table)
					repr(result) # check that the object has a valid repr method
					str(result) # check that the object has a valid str method
					
	def testViewBuildProperties( self ):
		views = []
		for specifier in primarySpecifiers:
			driver, connection = specifier.connect()
			for table in driver.listTables(connection):
				view = dbschema.TableSchema.fromConnection(
					connection, tableName = table,
				)
				view.buildProperties() # build property descriptors
				resultSet = view.query(connection=connection) # build a result-set object/wrapper
				resultSet.forceLoad() # ForceLoad, FetchMany, WrapRow
				limiter = 0
				for item in resultSet:
					# each record as an object...
					props = item.getProperties()
					assert props, """Item %r has no properties"""%(item)
					# now test setattr functioning...
					for attr in props:
						current = getattr(item, attr.name)
						if isinstance( current, int ):
							setattr(item, attr.name, current+1)
							assert getattr(item, attr.name) == current+1, """Attribute %s not updated on set for %s"""%(attr,item)
							assert item.dirty(), """Row item %r not dirty after setting value"""%(item)
							item.abort()
						elif isinstance( current, (str,unicode)):
							nm = attr.name
							setattr(item, nm, current[:-1])
							assert getattr(item, attr.name) == current[:-1], """Attribute %s not updated on set for %s: expected %s got %s"""%(attr,item, current[:-1], getattr(item, attr.name))
							assert item.dirty(), """Row item %r not dirty after setting value"""%(item)
							item.abort()
						else:
							item.abort()
						assert not item.dirty(), """Row %r abort didn't clear dirty flag"""%(item,)
					limiter += 1
					if limiter > 20:
						break
				if view.getUniqueKeys():
					resultSet.commit()
				views.append( view )
		return views

suite = unittest.TestSuite((
	unittest.makeSuite(ConnectTest,'test'),
))


if __name__ == "__main__":
	 unittest.TextTestRunner().run( suite )
