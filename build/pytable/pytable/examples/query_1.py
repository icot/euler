import build, example_schema
from pytable import sqlquery

query = sqlquery.SQLQuery(
    sql = """INSERT INTO
        pets(pet_name,pet_age)
    VALUES
        (%%(pet_name)s,%%(pet_age)s);""",
)
    
query(
    build.connection,
    pet_name = 'Tweety',
    pet_age = 3,
)

cursor = sqlquery.SQLQuery(
    sql = """SELECT * FROM pets %(whereClause)s;""",
)(
    build.connection,
    whereClause = "WHERE pet_name = %(name)s",
    name = "Tweety",
)
for row in cursor:
    print 'Row:', row
	