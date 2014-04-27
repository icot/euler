from pytable import dbspecifier
import traceback


queries = [
	"""DROP INDEX temp_first_second;""",
	"""DROP TABLE temp2;""",
	"""DROP TABLE temp;""",

	"""CREATE TABLE temp (
		id int4 NOT NULL PRIMARY KEY,
		abc varchar(64),
		bcd decimal NOT NULL,
		cde float8 NOT NULL DEFAULT 0.999,
		efg int8
	);
	""",
	"""CREATE TABLE temp2 (
		id int4 NOT NULL PRIMARY KEY,
		temp_id int4 NOT NULL REFERENCES temp (id),
		name varchar(32) NOT NULL
	);
	""",
	"""CREATE UNIQUE INDEX temp_first_second ON temp (abc, bcd);""",

	"""INSERT into temp values (1,'blah',23,.34, 55);""",
	"""INSERT into temp values (2,'hi there',25,4.34, 54);""",
	"""INSERT into temp2 values (1,1, 'blah');""",
	"""INSERT into temp2 values (2,2, 'blunder');""",

]
	
spec = dbspecifier.DBSpecifier(
	drivername= "PyPgSQL",
	user= "mike",
	password= "pass",
	host= "localhost",
	database= "test",
)

driver, connection = spec.connect()
cursor = connection.cursor()

for SQL in queries:
	try:
		cursor.execute( SQL )
	except Exception:
		if SQL[:4] != 'DROP':
			traceback.print_exc()
			print SQL

connection.commit()
