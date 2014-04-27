from pytable import dbdriver
import metakit
from basicproperty import common

class MkDriver( dbdriver.DBDriver ):
	"""Metakit database driver
	"""
	defaultTableClass = common.ClassByNameProperty(
		'defaultTableClass', """Default DBTable sub-class to be used for this driver""",
		defaultValue = "pytable.mk.mktable.MkTable",
	)
	### Required customization points (abstract methods)
	def establishConnection(self, fullSpecifier):
		"""Connect using the fully specified specifier

		fullSpecifier -- a specifier with all arguments unified
			and ready to be connected.  This specifier should
			include everything required to do the actual
			connection (including passwords or the like).

		All sub-classes must override this method!
		"""
		filename = fullSpecifier.dsn
		return metakit.storage( filename, 1 )
