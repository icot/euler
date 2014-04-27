"""Generate DB structure from manual declaration

This example imports the previously created
example schema and generates the SQL statements
required to build that schema.

The sqlgeneration module provides the actual SQL
statement generation.  The sqlquery module is
used to run the SQL statements.
"""
from pytable import dbspecifier, sqlgeneration, sqlquery
import example_schema

specifier = dbspecifier.DBSpecifier(
    drivername = "PyPgSQL",
    host = "localhost",
    user = "test",
    password = "password",
    database = "test",
)

driver, connection = specifier.connect( )

generator = sqlgeneration.SQLCreateStatements(
    # driver can be used to customise what's generated...
    driver,
)
# call the generator with the schema as argument
statements = generator( example_schema.schema )
for statement in statements:
    print statement # just so we see what's being executed
    sqlquery.SQLQuery( sql = statement )( connection )

# as with the DB-API, autoCommit is false by default, so
# everything we've done will disappear when we exit...
