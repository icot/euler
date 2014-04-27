"""Tests of dbrow objects"""
import unittest, traceback, new
from pytable import sqlquery, lazyresultset, sqlgeneration, specifierfromoptions
from pytable.schemabuilder import *

testSpec = specifierfromoptions.specifierFromOptions()

cats = table(
	"cats",
	(
		field("cat_id", "serial", 0, "Unique cat identifier",
			constraints = (notNull(),primary()),
		),
		field(
			"cat_name", "varchar", 255, "The cat's name",
			constraints = (notNull(),),
		),
		field( "declawed", "bool", 0, "Poor lil' kitty"),
	),
	"""Primary table for storing critical info about cats""",
	defaultRecords = [
		{ 'cat_name':"felis", "declawed":1 },
		{ 'cat_name':"boris", "declawed":1 },
	],
)

class DBRowTests( unittest.TestCase ):
	"""Tests for the lazy result-set functionality"""
	driver, connection = testSpec.connect()
	if driver.capabilities.serial:
		def setUp( self ):
			schema = cats
			generator = sqlgeneration.SQLDropStatements(self.driver)
			query= sqlquery.SQLQuery(
				sql = generator( schema ),
				debug=1,
			)
			try:
				query( cursor=self.connection )
			except Exception, err:
				print 'cats does not exist, reconnecting'
				self.connection.reconnect()
			try:
				sqlquery.SQLQuery(
					sql = sqlgeneration.SQLCreateStatements(driver=self.driver)(
						cats,
					),
					debug=1,
				)( self.connection )
			except:
				traceback.print_exc()
		def testGet( self ):
			rows = cats.query( "select * from cats;", self.connection )
			for x in rows:
				assert x.schema is cats
				assert x.getConnection()
				x.cat_name = "hello"
				assert x.dirty()
				assert x.getUniqueKeys()
				
		def testActionLookup( self ):
			cat = cats.itemClass(
				schema = cats,
				connection = self.connection,
			)
			cat.cat_name = 'test'
			cat.insertQuery(self.connection)
			assert hasattr(cat, "cat_id"), """Didn't automatically retrieve primary key"""
			cat.cat_name = "test2"
			cat.updateQuery(self.connection)
			cat.abort()
		def testProperties( self ):
			cat = cats.itemClass(
				schema = cats,
				connection = self.connection,
			)
			assert len( cat.getProperties()) == 3
		

if __name__ == "__main__":
	unittest.main()
