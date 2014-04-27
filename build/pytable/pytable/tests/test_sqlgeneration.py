from pytable import dbschema, sqlgeneration
import unittest, re

field1 = dbschema.FieldSchema(
	name = "field1",
	dbDataType = "text",
	defaultValue = "'default'",
)
fieldNoDefault = dbschema.FieldSchema(
	name = "fieldNoDef",
	dbDataType = "text",
)
fieldNoNULL = dbschema.FieldSchema(
	name = "fieldNoNULL",
	dbDataType = "text",
	nullOk = 0,
)
fieldNoNULL2 = dbschema.FieldSchema(
	name = "fieldNoNULL2",
	dbDataType = "text",
	constraints = [
		dbschema.NotNullConstraint(
			fields = "fieldNoNULL2",
		)
	],
)
fieldSized = dbschema.FieldSchema(
	name = "fieldSized",
	dbDataType = "varchar",
	displaySize = 23,
)
tableSimple = dbschema.TableSchema(
	name = "tableSimple",
	fields = [
	],
)
fieldForeign = dbschema.FieldSchema(
	name = "fieldForeign",
	dbDataType = "text",
	constraints = [
		dbschema.ForeignKeyConstraint(
			foreignFields = 'something_id',
			foreignTable = 'something',
		)
	],
)
tableFieldsOnly = dbschema.TableSchema(
	name = "table1",
	fields = [
		field1,
		fieldNoDefault,
		fieldNoNULL,
		fieldNoNULL2,
		fieldSized,
		fieldForeign,
	],
)
tUniqueConstraint = dbschema.UniqueConstraint(
	fields = "field1",
)
tPrimaryConstraint = dbschema.PrimaryConstraint(
	fields = ["fieldNoNULL2","fieldSized"],
)
tCheckConstraint = dbschema.CheckConstraint(
	expression = "field1 > 23",
)
tForeignConstraint = dbschema.ForeignKeyConstraint(
	fields = "fieldNoNULL",
	foreignFields = 'something_id',
	foreignTable = 'something',
)


tableConstraints = dbschema.TableSchema(
	name = "table1",
	fields = [
		field1,
		fieldNoDefault,
		fieldNoNULL,
		fieldNoNULL2,
		fieldSized,
		fieldForeign,
	],
	constraints = [
		tUniqueConstraint,
		tPrimaryConstraint,
		tCheckConstraint,
		tForeignConstraint,
	],
)

index = dbschema.IndexSchema(
	name = "",
	unique = 1,
	fields = ('a','b','c'),
	table = "that",
	where = "b > 32 and c < 15",
	accessMethod = "BTREE",
)
tableRecords = dbschema.TableSchema(
	name = "table1",
	fields = [
		field1,
		fieldNoDefault,
	],
	defaultRecords = [
		{ field1.name: "test" },
		{ fieldNoDefault.name: "test2"},
	],
)


class FieldGenerateTest (unittest.TestCase):
	def setUp( self ):
		self.creator = sqlgeneration.SQLCreateStatements()
	def testSimple(self):
		result = self.creator.tableField(
			schema = field1,
		)
		assert result.find(field1.name.lower()) > -1, result
		assert result.find(field1.dbDataType.upper()) > -1, result
		assert result.find(field1.defaultValue) > -1, result
	def testNoDefault(self):
		result = self.creator.tableField(
			schema = fieldNoDefault,
		)
		assert result.find(fieldNoDefault.name.lower()) > -1, result
		assert result.find(fieldNoDefault.dbDataType.upper()) > -1, result
		assert not (result.lower().find("default") > -1), result
	def testNoNULL(self):
		result = self.creator.tableField(
			schema = fieldNoNULL,
		)
		assert result.find(fieldNoNULL.name.lower()) > -1, result
		assert result.find(fieldNoNULL.dbDataType.upper()) > -1, result
		assert result.find("NOT NULL") > -1, result
	def testNoNULLConstraint(self):
		result = self.creator.tableField(
			schema = fieldNoNULL2,
		)
		assert result.find(fieldNoNULL2.name.lower()) > -1, result
		assert result.find(fieldNoNULL2.dbDataType.upper()) > -1, result
		assert result.find("NOT NULL") > -1, result
	def testSize (self):
		result = self.creator.tableField(
			schema = fieldSized,
		)
		assert result.find(fieldSized.name.lower()) > -1, result
		predicted = ("%s(%s)"%(fieldSized.dbDataType.upper(),fieldSized.displaySize)).upper()
		assert result.find(predicted) > -1, result
	def testFailNoType( self ):
		self.failUnlessRaises(
			AttributeError,
			self.creator.tableField,
			schema = dbschema.FieldSchema(
				name = "test",
				displaySize = 23,
			),
		)
	def testFailNoName( self ):
		self.failUnlessRaises(
			AttributeError,
			self.creator.tableField,
			schema = dbschema.FieldSchema(
				dbDataType="int",
			),
		)
	def testGuessType(self):
		for prefix, type in self.creator.fieldPrefixToTypeMap:
			result = self.creator.tableField(
				cursor = None,
				schema = dbschema.FieldSchema(
					name="test",
					dataType = prefix,
				),
			)
			assert result.find(type) > -1, result
	def testForeign( self ):
		result = self.creator.tableField(
			cursor = None,
			schema = fieldForeign,
		)
		match = re.match(
			"(\w+)\W+(\w+)\W+REFERENCES\W+\w+\W+\((.*)\)",
			result,
			re.I|re.M|re.DOTALL,
		)
		assert match, result
		for foreign in fieldForeign.constraints[0].foreignFields:
			assert match.group(3).find( foreign ) > -1, """Field %s not in result"""%( foreign, )
	
	
	
class TableGenerateTest (unittest.TestCase):
	"""Tests of the table-creation-SQL-generation mechanisms"""
	def setUp( self ):
		self.creator = sqlgeneration.SQLCreateStatements()
	def testSimple(self):
		result = self.creator(
			tableSimple
		)
		assert len(result) == 1, """More than one statement for simple table"""
		result = result[0]
		assert result.find(tableSimple.name.lower()) > -1, result
		match = re.match(
			"CREATE\W+TABLE\W+(\w+)\W+\(\W+\)\W*;",
			result,
			re.I|re.M|re.DOTALL,
		)
		assert match, result
	def testIncludesFields (self):
		"""Test that field values are included in table SQL"""
		result = self.creator(
			tableFieldsOnly
		)
		assert len(result) == 1, """More than one statement for simple table"""
		result = result[0]
		match = re.match(
			"CREATE\W+TABLE\W+(\w+)\W+\((.*)\)\W*;",
			result,
			re.I|re.MULTILINE|re.DOTALL,
		)
		assert match, result
		for field in tableFieldsOnly.fields:
			assert match.group(2).find(self.creator.tableField( field )) > -1, """Field %r definition isn't present in result %r"""%( field.name, result)
	def testTConstraints( self ):
		for constraint, pattern in [
			(tUniqueConstraint, "UNIQUE\W*\(.*\)"),
			(tPrimaryConstraint, "PRIMARY\W+KEY\W*\(.*\)"),
			(tForeignConstraint, "FOREIGN\W+KEY\W*\(.*\)\W*REFERENCES\W+\w+"),
			(tCheckConstraint, "CHECK\W*\(.*\)"),
		]:
			result = self.creator.tableConstraint(
				constraint, tableConstraints
			)
			match = re.match(
				pattern,
				result,
				re.I|re.MULTILINE|re.DOTALL,
			)
			assert match, """Table Constraint %s didn't match expected pattern: got %s"""%(constraint, result)
		
			
	def testTableConstraints( self ):
		result = self.creator(
			tableConstraints
		)
		assert len(result) == 1, """More than one statement for simple table"""
		result = result[0]
		match = re.match(
			"CREATE\W+TABLE\W+(\w+)\W+\((.*)\)\W*;",
			result,
			re.I|re.MULTILINE|re.DOTALL,
		)
		for constraint in tableConstraints.constraints:
			assert match.group(2).find(self.creator.tableConstraint(
				constraint,
				target=tableConstraints,
			)) > -1, """Constraint %r definition isn't present in result %r"""%( constraint.name, result)
	def testTableRecords( self ):
		result = self.creator(
			tableRecords
		)
		# this is a multiple-value set
		assert isinstance( result, list )
		assert len( result ) == 3, """Expected 3 statements for this table, got %r: %r"""%(len(result), result)
		assert result[0].startswith( "CREATE TABLE" )
		for result,record in map(None, result[1:],tableRecords.defaultRecords):
			tableName = tableRecords.name
			fieldName = record.keys()[0]
			search = re.compile(
				"INSERT\W+INTO\W+%(tableName)s+\W*\(.*%(fieldName)s.*\)\W+VALUES\W+(\((.+)\))?\W*;"%locals(),
				re.I|re.MULTILINE|re.DOTALL,
			)
			value = search.search( result )
			assert value
				
		
		
class IndexGenerateTest(unittest.TestCase):
	"""Tests of the table-creation-SQL-generation mechanisms"""
	def setUp( self ):
		self.creator = sqlgeneration.SQLCreateStatements()
	def testSimple(self):
		result = self.creator(
			index
		)
		match = re.match(
			"CREATE\W+UNIQUE\W+INDEX\W+(.+)\W+ON\W+\w+\W+USING\W+BTREE\W*\(.*\)\W+WHERE.*;",
			result,
			re.I|re.MULTILINE|re.DOTALL,
		)
		assert match, result
		

if __name__ == "__main__":
	unittest.main ()
	
