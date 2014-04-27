from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier, specifierfromoptions
import unittest, new, traceback

testSpec = specifierfromoptions.specifierFromOptions()

cats = database(
	"kitties",
	tables = [
		table(
			"cats",
			(
				field("cat_id", "integer", 0, "Unique cat identifier",
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
				{'cat_id':0, "cat_name":"Felix", "declawed":'t' },
				{'cat_id':1, "cat_name":"Ginger", "declawed":'f' },
				{'cat_id':2, "cat_name":"Robusta", "declawed":'t' },
			],
		),
	],
)
cats.resolve()
items = []

class CatsTest( unittest.TestCase ):
	specifier = testSpec
	def setUp( self ):
		self.driver,self.connection = self.specifier.connect()
		cursor = self.connection.cursor()
		generator = sqlgeneration.SQLDropStatements(self.driver)
		schema = cats.lookupName( 'cats' )
		query= sqlquery.SQLQuery(
			sql = generator( schema ),
			debug=1,
		)
		try:
			query( cursor=cursor )
		except Exception, err:
			print 'cats does not exist, reconnecting'
			self.connection.reconnect()
			cursor = self.connection.cursor()
		generator = sqlgeneration.SQLCreateStatements(self.driver)
		query= sqlquery.SQLQuery(
			sql = generator( schema ),
			debug=1,
		)
		query( cursor )
	def testDBRowDataType( self ):
		query= sqlquery.SQLQuery(
			sql = """select * from cats;""",
			debug=1,
		)
		schema = cats.lookupName( 'cats' )
		resultSet = schema.collectionClass(
			cursor = query( self.connection ),
			schema = schema,
		)
		cats.driver = self.driver
		for item in resultSet:
			for prop in item.getProperties():
				assert prop.dataType, """Property %r didn't find a data-type specifier"""%(prop,)
	def tearDown( self ):
		try:
			self.connection.rollback()
		except Exception, err:
			pass

if __name__ == "__main__":
	unittest.main()