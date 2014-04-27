from pytable import dbtable
from basicproperty import common

class MkTable( dbtable.DBTable ):
	"""Metakit table"""
	propertyClass = common.ClassByNameProperty(
		'propertyClass', """The class used for creating property objects""",
		defaultValue = "pytable.metakit.mkdescriptor.MkDescriptor",
	)
