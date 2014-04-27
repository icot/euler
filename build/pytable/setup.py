#!/usr/bin/env python
"""Installs properties using distutils

Run:
	python setup.py install
to install the packages from the source archive.
"""
import os, sys
from setuptools import setup, find_packages, Extension

if __name__ == "__main__":
	if sys.hexversion >= 0x2030000:
		# work around distutils complaints under Python 2.2.x
		extraArguments = {
			'classifiers': [
				"""License :: OSI Approved :: BSD License""",
				"""Programming Language :: Python""",
				"""Topic :: Software Development :: Libraries :: Python Modules""",
				"""Intended Audience :: Developers""",
				"""Operating System :: OS Independent""",
				"""Topic :: Database""",
			],
			'download_url': "https://sourceforge.net/project/showfiles.php?group_id=87033",
			'keywords': 'database,postgresql,mysql,db-api,object-relational mapper,basicproperty,property,descriptor,schema,query,sql',
			'long_description' : """BasicProperty-based RDBMS Wrapper

PyTable provides a schema-based mechanism for constructing
database-based applications.  Included is a fairly elegant
SQLQuery object which makes creation of complex SQL in response
to application requirements somewhat easier, as well as
classes allowing the modelling of database schemas.

Can read MySQL and PostgreSQL schemas from live databases.
Can build databases from schemas.
Does not attempt to abstract away differences in SQL syntax.
Provides optional object-oriented row-wrappers with
BasicProperty properties defining fields.
""",
			'platforms': ['Any'],
		}
	else:
		extraArguments = {
		}

	setup (
		name = "pytable",
		version = "0.8.23a",
		description = "BasicProperty-based RDBMS Wrapper",
		author = "Mike C. Fletcher",
		author_email = "mcfletch@users.sourceforge.net",
		url = "http://pytable.sourceforge.net/",
		license = "BSD-style, see license.txt for details",
		
		install_requires = """basicproperty >= 0.6.9a""",
		
		packages = find_packages(),
		include_package_data = True,
		zip_safe = False,
		**extraArguments
	)
