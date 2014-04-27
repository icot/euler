from pytable import dbdescriptor
from wxoo import typeregistry
from basicproperty import common


def defaultDataType( property, client ):
	"""Get a data-type value for client (a property descriptor)"""
	typ = client.description[1]
	for typCode, name in client.typeToRegistryName:
		if typ == typCode:
			return name
	return ""

class PGDescriptor( dbdescriptor.DBDescriptor ):
	"""Property descriptor for PyPgSQL drivers
	"""
	dataType = common.StringProperty(
		'dataType', """String value declaring a unique type for editor lookups""",
		defaultFunction = defaultDataType,
	)
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

##		(PgSQL.PG_BLOB , '') ,
##		(PgSQL.PG_TIME , '') ,
##		(PgSQL.PG_TIMESTAMP , '') ,
##		(PgSQL.PG_TIMESTAMPTZ , '') ,
##		(PgSQL.PG_TINTERVAL , '') ,
##		(PgSQL.PG_ABSTIME , '') ,
##		(PgSQL.PG_RELTIME , '') ,
##		(PgSQL.PG_NUMERIC , '') ,
##		(PgSQL.PG_ACLITEM , '') ,
##		(PgSQL.PG_BOX , '') ,
##		(PgSQL.PG_BPCHAR , '') ,
##		(PgSQL.PG_CASH , '') ,
##		(PgSQL.PG_CID , '') ,
##		(PgSQL.PG_CIDR , '') ,
##		(PgSQL.PG_CIRCLE , '') ,
##		(PgSQL.PG_INET , '') ,
##		(PgSQL.PG_INT2VECTOR , '') ,
##		(PgSQL.PG_LINE , '') ,
##		(PgSQL.PG_LSEG , '') ,
##		(PgSQL.PG_MACADDR , '') ,
##		(PgSQL.PG_MONEY , '') ,
##		(PgSQL.PG_NAME , '') ,
##		(PgSQL.PG_OID , '') ,
##		(PgSQL.PG_OIDVECTOR , '') ,
##		(PgSQL.PG_PATH , '') ,
##		(PgSQL.PG_POINT , '') ,
##		(PgSQL.PG_POLYGON , '') ,
##		(PgSQL.PG_REFCURSOR , '') ,
##		(PgSQL.PG_REGPROC , '') ,
##		(PgSQL.PG_ROWID , '') ,
##		(PgSQL.PG_TID , '') ,
##		(PgSQL.PG_UNKNOWN , '') ,
##		(PgSQL.PG_VARBIT , '') ,
##		(PgSQL.PG_XID , '') ,
##		(PgSQL.PG_ZPBIT , '') ,

	]
	
