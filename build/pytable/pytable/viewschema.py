"""(incomplete) Schemas describing query/view structures"""
from basicproperty import propertied, common, basic
from basictypes import list_types, callable
from pytable import dbschema

class ViewFieldSchema( dbschema.FieldSchema ):
	"""A view-field description, adds source table and field props

	Basically, a default ViewField is going to use
	these extra properties to forward all actions to
	the source-table's field for standard editing
	actions.
	"""
	sourceTable = basic.BasicProperty(
		'sourceTable', """The source-table schema for this field (may be null)""",
		baseType = dbschema.TableSchema,
	)
	sourceField = basic.BasicProperty(
		'sourceField', """The source-field schema for this field (may be null)""",
		baseType = dbschema.FieldSchema,
	)

ViewFieldSchemas = list_types.listof(
	ViewFieldSchema,
	name = "ViewFieldSchemas",
	dataType = "list.ViewFieldSchemas",
)

class JoinTable( dbschema.Schema ):
	"""A Join of a table, basically just a name:table item"""
	name = common.StringProperty(
		'name', """Name of the table (required)""",
		defaultFunction = lambda prop, client: client.table.name,
	)
	table = basic.BasicProperty(
		'table', """Table object which participates in the schema""",
		baseType = dbschema.TableSchema,
	)
	def check( cls, value ):
		"""Check that value is a proper instance of this class"""
		if isinstance( value, cls ):
			if hasattr( value, table ):
				return 1
		return 0
	check = classmethod( check )
	def coerce( cls, value ):
		"""Coerce a value to an instance of this class"""
		if cls.check( value ):
			return value
		if isinstance( value, dbschema.TableSchema ):
			return cls( table = value )
		else:
			raise TypeError("""%r couldn't be converted to a %s"""%(value, cls.__name__))
	coerce = classmethod( coerce )

JoinTables = list_types.listof(
	JoinTable,
	name = "JoinTables",
	dataType = "list.JoinTables",
)

class ViewSchema( dbschema.BaseTableSchema ):
	"""A query-view table-structure/schema

	This is the structure/schema for a query,
	and as such it may involve multiple tables,
	may include joins, indices and the like.

	At it's most basic, a view schema can
	just be:
	
		select * from tableName;

	but it can be ridiculously more complex,
	with huge numbers of sub-elements interacting
	to produce a real-world query-set.
	"""
	tables = common.ListProperty(
		'tables', """List of JoinTable objects which participate in the schema""",
		baseType = JoinTables,
	)
	fields = common.ListProperty(
		'fields', """FieldSchema objects for the table""",
		baseType = ViewFieldSchemas,
	)

ViewSchemas = list_types.listof(
	ViewSchema,
	name = "ViewSchemas",
	dataType = "list.ViewSchemas",
)

