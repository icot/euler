"""wxoo.table adapter for DB-API databases"""
from basicproperty import propertied, common, basic
from wxoo.table import adapter
from wxoo import propertydescriptor

class DBAPIAdapter( adapter.Adapter ):
	"""DBAPI2.0 adapter interface for SQL databases

	This is the base class for DBAPI 2.0 adapters
	it provides only the most basic insert, update and
	property support (with no data type information
	available, and hence no specialized editors).

	The values edited by a DBAPI adapter are "DBTables",
	which are specialized collections providing
	sequence semantics for a query-result set
	(though at the moment, this must be an actual table).
	"""
	def CalculateProperties(self, value = None):
		"""Return property set for the given or current value

		value -- if not None, a value other than the current value
			for which properties should be retrieved.

		This implementation uses the propertyset module to
		create a set of property definitions for the value.
		"""
		if value is None:
			value = self.GetValue()
		if value and value.properties:
			return value.properties
		else:
			return []
		
