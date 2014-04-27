from pytable import dbspecifier

SQL = """SELECT 
	con.conkey, -- local key-columns
	con.confrelid, -- remote table id
	c2.relname, -- remote table name
	con.confkey -- remote key-columns
	
FROM
	pg_constraint con,
	pg_class c,
	pg_class c2
WHERE
	c.relname='temp2' AND
	c.oid = con.conrelid AND
	con.contype = 'f' AND
	c2.oid = con.confrelid
;
"""
##SQL = """SELECT
##		pg_index.indkey FROM
##		pg_index WHERE
##		pg_index.indexrelid = 17018
##	;
##
##"""

spec = dbspecifier.DBSpecifier(
	drivername= "PyPgSQL",
	user= "mike",
	password= "pass",
	host= "localhost",
	database= "test",
)

driver, connection = spec.connect()
cursor = connection.cursor()

cursor.execute( SQL )
print cursor.fetchall()

	
