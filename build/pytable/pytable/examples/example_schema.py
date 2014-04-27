"""Example of manually creating a database schema

There are two normal ways to create database schemas
for use with pytable.  This approach, (manually creating
the description using the schemabuilder module) is the
more common "application" development pattern, while the
reverse engineering mechanism is more commonly used for
"scripts" which need to deal with existing databases.
"""
from pytable.schemabuilder import *

schema = database(
	name = "test",
	comment = """A simple testing database""",
	tables = [
		table(
			"pets",
			comment ="""Storage for simple pets information""",
			fields = [
				field(
					"pet_name", "text", 0, """The name of the pet""",
					defaultValue = "'stringValue'", # note use of SQL syntax
					constraints = [ primary(), notNull() ],
				),
				field(
					"pet_age", "integer", 0, """The age of the pet""",
					constraints = [ notNull() ],
				),
			],
			defaultRecords = [
				{ 'pet_name': 'Fido', 'pet_age': 3 },
				{ 'pet_name': 'Fluffy', 'pet_age': 5 },
				{ 'pet_name': 'Jimminy', 'pet_age': 0 },
				{ 'pet_name': 'Vigo', 'pet_age': 2 },
			],
		),
		table(
			"houses",
			comment ="""Storage for simple house information""",
			fields = [
				field(
					"house_id", "serial", 0, """Unique house identifier""",
					constraints = [ primary(), notNull() ],
				),
				field(
					"type", "text", 0, """The type of the house""",
					constraints = [ notNull()],
				),
			],
			defaultRecords = [
				{ 'house_id':0, 'type': 'cage' },
				{ 'house_id':1, 'type': 'dog house' },
				{ 'house_id':2, 'type': 'dog basket' },
				{ 'house_id':3, 'type': 'cat basket' },
				{ 'house_id':4, 'type': 'bowl' },
				{ 'house_id':5, 'type': 'acquarium' },
			],
			indices = [
				index( unique=1, fields=('type', ) ),
			],
		),
		table(
			"house_pets",
			comment = """Stupid word-play mapping pet: house""",
			fields = [
				field(
					'house_id', 'integer', 0, """Reference to the house""",
					constraints = [
						foreignKey(
							"houses", # uses primary key by default...
							onDelete = "CASCADE",
							onUpdate = "CASCADE",
						),
						notNull(),
					],
				),
				field(
					'pet_name', 'text', 0, """Reference to the pet""",
					constraints = [
						notNull(),
					],
				),
			],
			constraints = [
				foreignKey(
					"pets", # foreign table which constrains
					("pet_name",), # foreign fields which constrain
					fields = ("pet_name",), # local fields constrained
					onDelete = "SET NULL",
					onUpdate = "CASCADE",
				),
			],
			defaultRecords = [
				{ 'house_id':1, 'pet_name':'Fido' },
			],
		),
	],
)
