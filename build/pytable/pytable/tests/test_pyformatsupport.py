import unittest, traceback
from pytable import dbspecifier, dbschema, sqlquery, specifierfromoptions, pyformatsupport

testSpec = specifierfromoptions.specifierFromOptions()

primarySpecifiers = specifiers = [
	testSpec,
]

class PyFormatTest( unittest.TestCase ):
	def testQmark1( self ):
		"""Does qmark support produce expected result"""
		query = """SELECT * FROM x WHERE this = %(this)s
		AND that = %(that)s"""
		values = { 'this': 23, 'that': 24 }
		pf = pyformatsupport.PyFormatSupport( values, 'qmark' )
		newQuery = query%pf
		assert newQuery == """SELECT * FROM x WHERE this = ?
		AND that = ?"""
		assert len(pf.sequential) == 2
		assert pf.sequential == [23,24]
		pf.finishBuilding()
		result = newQuery%pf
		assert len(pf.sequential) == 2
	def testQmark2( self ):
		"""Does support for multiple refs to same value"""
		query = """SELECT * FROM x WHERE this = %(this)s
		AND that = %(this)s"""
		values = { 'this': 23, 'that': 24 }
		pf = pyformatsupport.PyFormatSupport( values, 'qmark' )
		newQuery = query%pf
		assert newQuery == """SELECT * FROM x WHERE this = ?
		AND that = ?"""
		assert len(pf.sequential) == 2
		assert pf.sequential == [23,23]
		pf.finishBuilding()
		result = newQuery%pf
		assert len(pf.sequential) == 2
	def testFormat( self ):
		"""Does format support produce expected result"""
		query = """SELECT * FROM x WHERE this = %(this)s
		AND that = %(that)s AND this2 = %(this)s"""
		values = { 'this': 23, 'that': 24 }
		pf = pyformatsupport.PyFormatSupport( values, 'format' )
		newQuery = query%pf
		assert newQuery == """SELECT * FROM x WHERE this = %s
		AND that = %s AND this2 = %s""", newQuery
		assert len(pf.sequential) == 3
		assert pf.sequential == [23,24,23]
		pf.finishBuilding()
		result = newQuery%tuple(pf)
		assert len(pf.sequential) == 3
		assert result == """SELECT * FROM x WHERE this = 23
		AND that = 24 AND this2 = 23""", result
	def testNumeric( self ):
		"""Does numeric support produce expected result"""
		query = """SELECT * FROM x WHERE this = %(this)s
		AND that = %(that)s AND this2 = %(this)s"""
		values = { 'this': 23, 'that': 24 }
		pf = pyformatsupport.PyFormatSupport( values, 'numeric' )
		newQuery = query%pf
		assert newQuery == """SELECT * FROM x WHERE this = :0
		AND that = :1 AND this2 = :2""", newQuery
		assert len(pf.sequential) == 3
		assert pf.sequential == [23,24,23]
		pf.finishBuilding()
		result = newQuery%pf
		assert len(pf.sequential) == 3
	def testNamed( self ):
		"""Does named support produce expected result"""
		query = """SELECT * FROM x WHERE this = %(this)s
		AND that = %(that)s AND this2 = %(this)s"""
		values = { 'this': 23, 'that': 24 }
		pf = pyformatsupport.PyFormatSupport( values, 'named' )
		newQuery = query%pf
		assert newQuery == """SELECT * FROM x WHERE this = :this
		AND that = :that AND this2 = :this""", newQuery
		assert len(pf.sequential) == 3
		assert pf.sequential == [23,24,23]
		pf.finishBuilding()
		result = newQuery%pf
		assert len(pf.sequential) == 3

if __name__ == "__main__":
	unittest.main()
	
