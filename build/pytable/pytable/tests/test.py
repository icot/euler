#! /usr/bin/env python2.2
"""Test everything in one go"""
import unittest, types

def moduleSuite( module ):
	return unittest.TestLoader().loadTestsFromModule( module )

import test_basic
import test_dbdriver
import test_dbschema
import test_schemabuilder
import test_sqlgeneration
import test_lazyresultset
import test_datatypedetermination
import test_foreignkeyprop
import test_dbrow
import test_namespaces

suite = unittest.TestSuite( [
	moduleSuite( module )
	for module in [
		test_schemabuilder, # there's some interference if this isn't first :(
		test_basic,
		test_dbdriver,
		test_dbschema,
		test_sqlgeneration,
		test_lazyresultset,
		test_datatypedetermination,
		test_foreignkeyprop,
		test_dbrow,
		test_namespaces,
	]
])
if __name__ == "__main__":
	 unittest.TextTestRunner(verbosity=2).run( suite )

