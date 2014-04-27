from pytable.schemabuilder import *
from pytable import dbschema, sqlgeneration, sqlquery, dbspecifier
import unittest

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
		field( "declawed", "boolean", 0, "Poor lil' kitty"),
	),
	"""Primary table for storing critical info about cats""",
)

class CatsTest( unittest.TestCase ):
	def testKeys( self ):
		assert cats.getUniqueKeys() == [("cat_id",)]
	def testKeys2( self ):
		t = table( "blah", ( ), constraints = (
			unique( fields=("whatever",)),
		),)
		assert t.getUniqueKeys() == [("whatever",)]
	def testKeys3( self ):
		t = table( "blah", ( ), indices = (
			index( unique=1, fields=("whatever",)),
		),)
		assert t.getUniqueKeys() == [("whatever",)]
	def testPrimaryFirst( self ):
		t = table(
			"blah", ( ),
			indices = (
				index( unique=1, fields=("whatever",)),
			),
			constraints= (
				primary( fields = ("whatever2",)),
			),
		)
		assert t.getUniqueKeys() == [("whatever2",),("whatever",)]
		
		
if __name__ == "__main__":
	unittest.main ()
		
