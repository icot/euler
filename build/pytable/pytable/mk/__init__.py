"""Metakit database driver
"""
from pytable import dbdriver
name = dbdriver.DriverNameSet.new(
	name = 'MkSQL',
	friendlyName = 'Metakit via MkSQL',
	value = 'pytable.mk.mkdriver.MkDriver',
)

