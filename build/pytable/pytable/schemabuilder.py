"""Convenience module for manually creating schemas

Basically this module provides short form names for
the various schema objects defined in dbschema.py. The
functions often allow for positional arguments, which
is useful when manually generating a schema.
"""
from pytable import dbschema

def database( name, tables=(), comment="", **named ):
	"""Create a new database schema"""
	named.update(locals())
	del named['named']
	return dbschema.DatabaseSchema( **named )

namespace = schema = dbschema.NamespaceSchema

def table( name, fields=(), comment="", **named ):
	"""Create a new table schema"""
	named.update(locals())
	del named['named']
	return dbschema.TableSchema( **named )
def field( name, dbDataType, displaySize=0, comment="", **named ):
	"""Create a new field schema"""
	named.update(locals())
	del named['named']
	return dbschema.FieldSchema( **named )
notNull = dbschema.NotNullConstraint
unique = dbschema.UniqueConstraint
primary = dbschema.PrimaryConstraint
primaryKey = primary
check = dbschema.CheckConstraint
def check( expression, **named ):
	"""Create a new field schema"""
	named.update(locals())
	del named['named']
	return dbschema.CheckConstraint( **named )
def foreignKey( foreignTable, foreignFields=(), comment="", **named ):
	"""Create a new field schema"""
	named.update(locals())
	del named['named']
	return dbschema.ForeignKeyConstraint( **named )
references = foreign = foreignKey
def sequence( name, comment="", **named ):
	"""Create a new sequence schema"""
	named.update(locals())
	del named['named']
	return dbschema.SequenceSchema( **named )
count = sequence

def index( fields=(), unique=1, **named ):
	"""Create a new index schema"""
	named.update(locals())
	del named['named']
	return dbschema.IndexSchema( **named )
