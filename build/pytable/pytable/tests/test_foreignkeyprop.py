"""Test for foreign-key property operations"""
from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier
from pytable import dbproperty, specifierfromoptions
import unittest, new, traceback

testSpec = specifierfromoptions.specifierFromOptions()

cats = database(
	"kitties",
	tables = [
		table(
			"ownersforeignkey",
			(
				field( "owner_id", "integer", 0, "Unique owner identifier",
					constraints = (notNull(),primary()),
				),
				field( "owner_name", "text", 0, """Owner's first name""",
					constraints = (notNull(),),
				),
			),
			"""Table for storing owner information""",
			friendlyNameField = "owner_name",
			defaultRecords = [
				{ "owner_id":1, "owner_name":"Tim" },
				{ "owner_id":2, "owner_name":"John" },
				{ "owner_id":3, "owner_name":"Jerry" },
				{ "owner_id":4, "owner_name":"Mike" },
			],
		),
		table(
			"dogsforeignkey",
			(
				field("dog_id", "integer", 0, "Unique dog identifier",
					constraints = (notNull(),primary()),
				),
				field(
					"dog_name", "varchar", 255, "The dog's name",
					constraints = (notNull(),),
				),
			),
			"""Primary table for storing critical info about cats""",
			defaultRecords = [
				{'dog_id':0, "dog_name":"Felix2"},
				{'dog_id':1, "dog_name":"Ginger2"},
				{'dog_id':2, "dog_name":"Robusta2"},
			],
		),
		table(
			"catsforeignkey",
			(
				field("cat_id", "integer", 0, "Unique cat identifier",
					constraints = (notNull(),primary()),
				),
				field(
					"cat_name", "varchar", 255, "The cat's name",
					constraints = (notNull(),),
				),
				field( "declawed", "bool", 0, "Poor lil' kitty"),
				field( "owner", "integer", 0, "Owner of the kitty",
					   constraints = (notNull(), foreignKey(
						   foreignTable = "ownersforeignkey",
						   foreignFields = "owner_id",
						)),
				),
				field( "chasedby", "integer", 0, "Kitty's exercise maven",
					   constraints = [ foreignKey(
						   foreignTable = "dogsforeignkey",
						   foreignFields = "dog_id",
						
						)],
				),
				
			),
			"""Primary table for storing critical info about cats""",
			defaultRecords = [
				{'cat_id':0, "cat_name":"Felix", "declawed":'t', "owner":1 },
				{'cat_id':1, "cat_name":"Ginger", "declawed":'f', "owner":2 },
				{'cat_id':2, "cat_name":"Robusta", "declawed":'t', "owner":3 },
			],
		),
	],
)
cats.resolve()

items = []
class ForeignKeyTest( unittest.TestCase ):
	driver, connection = testSpec.connect()

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
		query= sqlquery.SQLQuery(
			sql = """select * from catsforeignkey;""",
		)
		schema = cats.lookupName( 'catsforeignkey' )
		resultSet = schema.collectionClass(
			cursor = query( self.connection ),
			schema = schema,
		)
		self.resultSet = resultSet
	def testHaveCorrectProperty( self ):
		# okay, now, see what we've got...
		record = self.resultSet[0]
		assert record.owner
		assert isinstance( type(record).owner, dbproperty.DBProperty ), str(type(record).owner)
		assert isinstance( type(record).owner, dbproperty.ReferenceProperty ), str(type(record).owner)
		assert type(record).chasedby
		assert isinstance( type(record).chasedby, dbproperty.DBProperty ), str(type(record).chasedby)
		assert isinstance( type(record).chasedby, dbproperty.ReferenceProperty ), str(type(record).chasedby)
	def testCommonValues( self ):
		record = self.resultSet[0]
		common = type(record).owner.commonValues(self.connection)
		assert len(common) == len( cats.tables[0].defaultRecords )
		# check that friendly-name was included...
		assert len(common[0]) == 2, common[0]
	def testCommonValuesNoFriendly( self ):
		record = self.resultSet[0]
		common = type(record).chasedby.commonValues(self.connection)
		assert len(common) == len( cats.tables[1].defaultRecords )
		# check that friendly-name was included, i.e. the key was
		# included twice
		assert len(common[0]) == 2, common[0]
		
		
		

if __name__ == "__main__":
	unittest.main()
