from basicproperty import propertied, common
import re

sqlString = re.compile( r"""'([^']|'')*'""" )
pyformat = re.compile( r"%\(([^)]+)\)s" )

class PyFormatSupport( propertied.Propertied ):
	"""Support pyformat-style argument for non-pyformat DBs

	This version of PyFormatSupport actually tokenises the
	SQL query string to exclude string-embedded % tokens, and
	to only replace %(name)s formats.  However, there are still
	potential problems if there is a database operator % and it
	is used with a bracketed value.
	"""
	formatStrings = common.DictionaryProperty(
		"formatStrings", """paramstyle-indexed set of formatting codes""",
		defaultValue = {
			'qmark':'?',
			'numeric':':%(index)s', # should this start at 1, or 0?
			'named':':%(key)s',
			'format':'%%s',
			'pyformat':'%%(key)s', # should never get used, but oh well...
		}
	)
	multiple = common.BooleanProperty(
		"multiple", """Whether we are preparing a multiple-value query""",
		defaultValue = False,
	)
	sequential = common.ListProperty(
		"sequential", """Sequential ordering of values for numeric, qmark and format""",
	)
	sequentialNames = common.ListProperty(
		"sequentialNames", """Sequential mapping of field-names for sequential multiple queries""",
	)
	
	def __init__( self, format='qmark', **named ):
		"""Store values and set up internal sequence"""
		self.format = format
		super( PyFormatSupport, self ).__init__( **named )
	def convertQuery( self, queryString ):
		"""Given a query string, find all pyformat subs and replace

		Record the appropriate metadata to return correct result
		for substituting into the new query...
		"""
		result = []
		sequentialNames = []
		def convertNonString( nonString ):
			"""Convert non-string fragment of query's pyformat operators"""
			start = 0
			for pyformatMatch in pyformat.finditer(nonString):
				end,newStart = pyformatMatch.span()
				result.append( nonString[start:end] )
				index = len( sequentialNames )
				key = pyformatMatch.group(1)
				sequentialNames.append( key )
				result.append( self.formatStrings.get( self.format ) %locals())
				start = newStart
			result.append( nonString[start:])
		start = 0
		for stringMatch in sqlString.finditer(queryString):
			end,newStart = stringMatch.span()
			convertNonString( queryString[start:end] )
			result.append( queryString[end:newStart] )
			start = newStart
		convertNonString( queryString[start:] )
		self.sequentialNames = sequentialNames
		result = "".join(result)
		return result
		
	def retrieveValues( self, valueSet ):
		"""Return tuple of ordered values from valueSet

		This should only be called for multiple-query
		ordered queries.
		"""
		if self.format in ('qmark','numeric','format'):
			return [ valueSet[key] for key in self.sequentialNames ]
		return valueSet
	
