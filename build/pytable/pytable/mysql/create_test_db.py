from pytable import dbspecifier
import traceback


queries = [
	"""ALTER TABLE temp DROP INDEX temp_first_second;""",
	"""DROP TABLE temp2;""",
	"""DROP TABLE temp;""",
	"""DROP TABLE whatnot;""",

	"""CREATE TABLE temp (
		id int4 NOT NULL,
		abc varchar(64) PRIMARY KEY,
		bcd decimal NOT NULL,
		cde float8 NOT NULL DEFAULT 0.999,
		efg int8
	);""",
	"""CREATE TABLE temp2 (
		id int4 NOT NULL PRIMARY KEY,
		temp_id int4 NOT NULL REFERENCES temp (id),
		name varchar(32) NOT NULL
	);""",
	"""CREATE TABLE whatnot (
		row_id INT PRIMARY KEY,
		name VARCHAR(128),
		temp INT REFERENCES temp.row_id
	);""",
	"""INSERT INTO whatnot values (0,'this', 0);""",
	"""INSERT INTO whatnot values (1,'this such', 0);""",
	"""INSERT INTO whatnot values (2,'those and', 1);""",

	"""ALTER TABLE temp ADD COLUMN INDEX temp_first_second (abc, bcd);""",

	"""INSERT into temp values (1,'blah',23,.34, 55);""",
	"""INSERT into temp values (2,'hi there',25,4.34, 54);""",
	"""INSERT into temp2 values (1,1, 'blah');""",
	"""INSERT into temp2 values (2,2, 'blunder');""",

]
	
spec = dbspecifier.DBSpecifier(
	drivername= "MySQL",
	user= "mike",
	password= "password",
	host= "localhost",
	database= "test",
)

driver, connection = spec.connect()
cursor = connection.cursor()

for SQL in queries:
	print SQL
	try:
		cursor.execute( SQL )
		connection.commit()
	except Exception, err:
		if SQL[:4] != 'DROP':
			traceback.print_exc()
		else:
			print err

connection.commit()
