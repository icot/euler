"""A few simple SQL-code manipulation functions"""

def characterType( dbDataType ):
	"""Is this a character data-type?"""
	likelyCharTypes = ('char','byte','text','inet','bool')
	dbDataType = dbDataType.lower()
	for typ in likelyCharTypes:
		if dbDataType.find( typ ) > -1:
			return typ
	return None

def sqlEscape( value, encoding='utf-8', dbDataType='' ):
	"""Perform SQL escaping on given (string) value"""
	if isinstance( value, unicode ):
		value = value.encode( encoding )
	if characterType( dbDataType ) or isinstance( value, str ):
		value = str(value)
		value = value.replace( "'", "''" ).replace( '\\','\\\\')
		return "'%s'"%(value)
	else:
		return repr(value)
	