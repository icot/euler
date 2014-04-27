from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier, specifierfromoptions
import unittest

testSpec = specifierfromoptions.specifierFromOptions()

driver,connection = testSpec.connect()
if driver.capabilities.schemaSupport:
	cats = database(
		"cats",
		namespaces = [
			namespace(
				name = "eft",
			)
		],
		tables = [
			table(
				"eft.ownersforeignkey",
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
				"eft.dogsforeignkey",
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
				"eft.catsforeignkey",
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
							   foreignTable = "eft.ownersforeignkey",
							   foreignFields = "owner_id",
							)),
					),
					field( "chasedby", "integer", 0, "Kitty's exercise maven",
						   constraints = [ foreignKey(
							   foreignTable = "eft.dogsforeignkey",
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

	class NamespaceTest( unittest.TestCase ):
		def setUp( self ):
			"""Setup the schema in the database"""
			driver,connection = testSpec.connect()
			generator = sqlgeneration.SQLDropStatements(driver)
			sql = generator( cats, cascade=1 )
			for q in sql:
				query= sqlquery.SQLQuery(
					sql = q,
				)
				try:
					query( connection )
					connection.commit()
				except Exception, err:
					connection.rollback()
			generator = sqlgeneration.SQLCreateStatements(driver)
			query= sqlquery.SQLQuery(
				sql = generator( cats ),
			)
			query( connection )
			connection.commit()
		def testLookup( self ):
			"""Do name lookups work for foreign keys?"""
			table = cats.lookupName( 'eft.catsforeignkey' )
			field = table.lookupName( 'chasedby' )
			other = cats.lookupName( field.foreign().foreignTable )
		def testInsert( self ):
			"""Can we properly insert an instance of a table in a namespace?"""
			driver,connection = testSpec.connect()
			owner = cats.lookupName( "eft.ownersforeignkey" )
			instance = owner.itemClass(
				owner_id = 30,
				owner_name = 'Wanda',
			)
			instance.insertQuery( connection )
			instance.refreshQuery( connection )
			instance.deleteQuery( connection )
			connection.rollback()
		def testTableClassName( self ):
			"""Is the table's class-name Python-compatible?"""
			owner = cats.lookupName( "eft.ownersforeignkey" )
			assert owner.itemClass.__name__ == 'eft_ownersforeignkey', owner.itemClass.__name__
		def testListing( self ):
			"""Can we list the namespaces from the driver?"""
			driver,connection = testSpec.connect()
			result = driver.listNamespaces( connection )
			expected = ['eft']
			assert result == expected, """Don't seem to have retrieved the namespace list properly, should be %r, was %r"""%(expected, result)
		def testTableListing( self ):
			"""Can we list the namespace'd tables from the driver?"""
			driver,connection = testSpec.connect()
			result = driver.listNamespaceTables( connection )
			expected = [
				('eft','catsforeignkey'),
				('eft','dogsforeignkey'),
				('eft','ownersforeignkey'),
			]
			assert result == expected, """Don't seem to have retrieved the namespace table list properly, should be %r, was %r"""%(expected, result)
	
	
if __name__ == "__main__":
	unittest.main ()
		
