from pytable import dbrow
from basicproperty import common, propertied, basic

class X( dbrow.DBRow ):
	value = common.StringProperty(
		'value', '''Testing value''',
		defaultValue = 'this',
	)

if __name__ == "__main__":
	x = X()
	assert x.value == 'this', x.value
	print x.value
