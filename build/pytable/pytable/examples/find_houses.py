from pytable import sqlquery

class FindHouses( sqlquery.SQLQuery ):
	"""Queries database for houses by pet_name or pet
	"""
	sql = """SELECT h.*
	FROM
		houses h, house_pets hp
	WHERE
		hp.pet_name = %%(pet)s
	AND
		h.house_id = hp.house_id
	;"""
	def __call__( self, cursor, pet, **named ):
		"""Coerce pet to pet_name and then execute query"""
		if not isinstance( pet, (str,unicode)):
			name = getattr( pet, 'pet_name', None )
			if name is None or not isinstance( name, (str,unicode)):
				raise TypeError( """%r instance %s could not be coerced to a pet_name"""%(
					pet.__class__, pet,
				))
			pet = name
		return super( FindHouses, self ).__call__(
			cursor,
			pet = pet,
			**named
		)
if __name__ == "__main__":
	import build
	name = raw_input( """pet name? """ )
	print 'Houses:'
	for row in FindHouses()(  build.connection, pet = name ):
		print '\t',row.type
	print 'Finished'
	