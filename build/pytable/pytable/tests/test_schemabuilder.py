from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier, specifierfromoptions
import unittest

testSpec = specifierfromoptions.specifierFromOptions()

cats = table(
	"cats",
	(
		field("cat_id", "int8", 0, "Unique cat identifier",
			constraints = (notNull(),primary()),
		),
		field(
			"cat_name", "varchar", 255, "The cat's name",
			constraints = (notNull(),),
		),
		field( "declawed", "bool", 0, "Poor lil' kitty"),
	),
	"""Primary table for storing critical info about cats""",
)

class CatsTest( unittest.TestCase ):
	def testTable( self ):
		assert cats.name == 'cats'
		assert cats.comment == """Primary table for storing critical info about cats"""
		assert len(cats.fields) == 3
	def testCorrectClass( self ):
		assert isinstance( field("a","b"), dbschema.FieldSchema)
		assert isinstance( table("a"), dbschema.TableSchema)
		assert isinstance( index("a"), dbschema.IndexSchema)
		assert isinstance( notNull(), dbschema.NotNullConstraint )
		assert isinstance( primary(), dbschema.PrimaryConstraint )
		assert isinstance( unique(), dbschema.UniqueConstraint )
		assert isinstance( check("a>b"), dbschema.CheckConstraint )
	def testCreate( self ):
		driver,connection = testSpec.connect()
		generator = sqlgeneration.SQLDropStatements(driver)
		sql = generator( cats, cascade=1 )
		query= sqlquery.SQLQuery(
			sql = sql,
		)
		try:
			query( connection )
		except Exception, err:
			connection.rollback()
			print err
		generator = sqlgeneration.SQLCreateStatements(driver)
		query= sqlquery.SQLQuery(
			sql = generator( cats ),
		)
		query( connection )
		connection.commit()
		
		
if __name__ == "__main__":
	unittest.main ()
		
