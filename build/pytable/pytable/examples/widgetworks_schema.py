from pytable.schemabuilder import *

schema = database(
	name = "widgetworks",
	comment = """A Widget-seller's database""",
	tables = [
		table(
			"customer",
			fields = [
				field( 
					"customer_id", "serial", 0, """Unique id for the customer""",
					constraints = [ primary(), notNull() ],
				),
				field(
					"customer_name", "varchar", 0, """Human-friendly name of the customer""",
					constraints = [ notNull() ],
				),
			],
			defaultRecords = [
				{ 'customer_name': "Ricky's Dept. Store" },
				{ 'customer_name': "Vicky Valencourt Inc." },
				{ 'customer_name': "James Joyce Bars" },
				{ 'customer_name': "Regal Regalia" },
				{ 'customer_name': "Bitter Biters" },
			],
		),
		table(
			"widget",
			comment ="""Base table for a saleable product""",
			fields = [
				field(
					"widget_id", "serial", 0, """Unique id for the widget""",
					constraints = [ primary(), notNull() ],
				),
				field(
					"widget_name", "varchar", 0, """Human-friendly name for the widget""",
					constraints = [ notNull() ],
				),
				field(
					"widget_cost", "number", 0, """Decimal description of a widget's base cost""",
					constraints = [ notNull() ],
				),
				field(
					"product_id", "varchar", 8, """8-Character product ID for external reference""",
					constraints = [ notNull() ],
				),
			],
			indices = [
				index( unique=1, primary=0, fields=('product_id',)),
			],
			defaultRecords = [
				{ 'widget_name': 'Vipo Vapour Grommit', "widget_cost": 32.33, "product_id": "AABBCCDD"},
				{ 'widget_name': 'Vegan Verdana',"widget_cost": 59.99, "product_id": "AABBCCDE"},
				{ 'widget_name': 'Wisconsin Whippet',"widget_cost": 34.00, "product_id": "AABBCCDF"},
				{ 'widget_name': 'Magic Merdana',"widget_cost": 55.98, "product_id": "AABBCCDG"},
				{ 'widget_name': 'Loputuk Latkes',"widget_cost": 29.32, "product_id": "AABBCCDH"},
				{ 'widget_name': 'Galaxy Ginseng Garter',"widget_cost": 55.30, "product_id": "AABBCCDI"},
			],
		),
		table(
			"order",
			comment = """Overall order from a customer from some set of widgets""",
			fields = [
				field(
					"order_id", "serial", 0, """Unique id for the order""",
					constraints = [ primary(), notNull() ],
				),
				field(
					"order_date", "timestamp", 0, """Date the order was submitted""",
					defaultValue = 'CURRENT_TIMESTAMP',
				),
				field(
					"delivery_date", "timestamp", 0, """Date the order is to be delivered""",
				),
				field(
					"customer_id", "integer", 0, """The customer that placed the order""",
					constraints = [
						foreignKey(
							"customer", # uses primary key by default...
							onDelete = "CASCADE",
							onUpdate = "CASCADE",
						),
						notNull(),
					],
				),
			],
		),
		table(
			"order_widgets",
			comment = """Widgets expected for a given order""",
			fields = [
				field(
					"order_id", "integer", 0, """The order being described""",
					constraints = [
						foreignKey(
							"order", # uses primary key by default...
							onDelete = "CASCADE",
							onUpdate = "CASCADE",
						),
						notNull(),
					],
				),
				field(
					"widget_id", "integer", 0, """The widgets being ordered""",
					constraints = [
						foreignKey(
							"widget", # uses primary key by default...
							onDelete = "CASCADE",
							onUpdate = "CASCADE",
						),
						notNull(),
					],
				),
				field(
					"widgets_ordered", "integer", 0, """Number of widgets ordered""",
					defaultValue = 0,
					constraints = [
						notNull(),
					],
				),
				field(
					"widgets_reserved", "integer", 0, """Number of widgets already reserved from inventory""",
					defaultValue = 0,
					constraints = [
						notNull(),
					],
				),
			],
			indices = [
				index( unique=1, primary=0, fields=('order_id','widget_id'), ),
			],
		),
		table(
			"inventory",
			comment = """Widgets currently on hand""",
			fields = [
				field(
					"widget_id", "integer", 0, """The widgets being stored""",
					constraints = [
						foreignKey(
							"widget", # uses primary key by default...
							onDelete = "CASCADE",
							onUpdate = "CASCADE",
						),
						notNull(),
					],
				),
				field(
					"widgets_onhand", "integer", 0, """Number of widgets currently on-hand""",
					defaultValue = 0,
					constraints = [
						notNull(),
					],
				),
				field(
					"widgets_reserved", "integer", 0, """Number of widgets currently reserved (already allocated to orders)""",
					defaultValue = 0,
					constraints = [
						notNull(),
					],
				),
			],
		),
	],
)
