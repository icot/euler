from pytable import dbspecifier
import traceback

SQL = [
	"""SHOW DATABASES;""",
	"""SHOW TABLES;""",
	"""SHOW INDEX FROM temp;""",
	"""SHOW INDEX FROM temp2;""",
	"""SHOW COLUMNS FROM temp;""",
	"""SHOW COLUMNS FROM temp2;""",
	
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

for item in SQL:
	try:
		cursor.execute( item )
		result = cursor.fetchall()
		if cursor.description and result:
			print item
			print "|".join( [d[0] for d in cursor.description])
			for line in result:
				print line
			print
	except:
		traceback.print_exc()
	
