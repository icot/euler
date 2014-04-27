"""Conversion maps to/from PgSQL and wxoo type declarations"""
from pyPgSQL import PgSQL
from wxoo import typeregistry

def _getInformation( propertyObject ):
	"""Place holder, will become a customisation point on dbtable eventually"""
	for typ, name in typeToRegistryName:
		if typ == propertyObject:
			return typeregistry.TypeRegistry.search( name )
	return None
	

def editorClass( propertyObject ):
	"""Get editor class for the given propertyObject"""
	information = _getInformation( propertyObject )
	if information:
		return information.gridEditor
	return None
def viewerClass( propertyObject ):
	"""Get viewer class for the given propertyObject"""
	information = _getInformation( propertyObject )
	if information:
		return information.gridViewer
	return None
	

typeToRegistryName = [
	(PgSQL.PG_DATE , 'mxDateTime') ,
	(PgSQL.PG_INTERVAL , 'mxDateTimeDelta') ,

	(PgSQL.PG_FLOAT , 'float') ,
	(PgSQL.PG_FLOAT4 , 'float') ,
	(PgSQL.PG_FLOAT8 , 'float') ,

	(PgSQL.PG_INT2 , 'int') ,
	(PgSQL.PG_INT4 , 'int') ,
	(PgSQL.PG_INT8 , 'long') ,
	(PgSQL.PG_BIGINT , 'long') ,
	(PgSQL.PG_INTEGER , 'int') ,
	(PgSQL.PG_SMALLINT , 'int') ,


	(PgSQL.PG_BYTEA , 'str.long') ,
	(PgSQL.PG_CHAR , 'str') ,
	(PgSQL.PG_TEXT , 'str.long') ,
	(PgSQL.PG_VARCHAR , 'str') ,

	(PgSQL.PG_BOOL , 'bool') ,

##	(PgSQL.PG_BLOB , '') ,
##	(PgSQL.PG_TIME , '') ,
##	(PgSQL.PG_TIMESTAMP , '') ,
##	(PgSQL.PG_TIMESTAMPTZ , '') ,
##	(PgSQL.PG_TINTERVAL , '') ,
##	(PgSQL.PG_ABSTIME , '') ,
##	(PgSQL.PG_RELTIME , '') ,
##	(PgSQL.PG_NUMERIC , '') ,
##	(PgSQL.PG_ACLITEM , '') ,
##	(PgSQL.PG_BOX , '') ,
##	(PgSQL.PG_BPCHAR , '') ,
##	(PgSQL.PG_CASH , '') ,
##	(PgSQL.PG_CID , '') ,
##	(PgSQL.PG_CIDR , '') ,
##	(PgSQL.PG_CIRCLE , '') ,
##	(PgSQL.PG_INET , '') ,
##	(PgSQL.PG_INT2VECTOR , '') ,
##	(PgSQL.PG_LINE , '') ,
##	(PgSQL.PG_LSEG , '') ,
##	(PgSQL.PG_MACADDR , '') ,
##	(PgSQL.PG_MONEY , '') ,
##	(PgSQL.PG_NAME , '') ,
##	(PgSQL.PG_OID , '') ,
##	(PgSQL.PG_OIDVECTOR , '') ,
##	(PgSQL.PG_PATH , '') ,
##	(PgSQL.PG_POINT , '') ,
##	(PgSQL.PG_POLYGON , '') ,
##	(PgSQL.PG_REFCURSOR , '') ,
##	(PgSQL.PG_REGPROC , '') ,
##	(PgSQL.PG_ROWID , '') ,
##	(PgSQL.PG_TID , '') ,
##	(PgSQL.PG_UNKNOWN , '') ,
##	(PgSQL.PG_VARBIT , '') ,
##	(PgSQL.PG_XID , '') ,
##	(PgSQL.PG_ZPBIT , '') ,

]

if __name__ == "__main__":
	def setupPGConnection(
		dsn='',
		user="mike",
		password="pass",
		host="localhost",
		database="test",
	):
		from pyPgSQL import PgSQL
		connection = PgSQL.connect(
			dsn=dsn,user=user,password=password,host=host,database=database,
		)
		return connection

	connection = setupPGConnection()
	cursor = connection.cursor()
	cursor.execute( """select * from temp;""")
	for row in cursor.description:
		print row[0], editorClass(row[1])
	
