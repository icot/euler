# -*- coding: latin-1 -*-
"""Generate XML database schema from live DBSchema"""
from xml.sax import saxutils
from xml import sax
import locale
defaultEncoding = locale.getdefaultlocale()[-1]
from pytable import sqlquery, dbschema, sqlutils
from basicproperty import propertied, common, basic

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

class Generator( saxutils.XMLGenerator ):
	"""Friendly generator for XML code"""
	def __init__( self, out=None, encoding="utf-8"):
		"""Initialise the generator

		Just overrides the default encoding of the base-class
		"""
		saxutils.XMLGenerator.__init__( self, out, encoding )
	def startElement( self, name, attributes=None ):
		"""Start a new element with given attributes"""
		saxutils.XMLGenerator.startElement( self, name, self._fixAttributes(attributes) )
	def _fixAttributes( self, attributes=None ):
		"""Fix an attribute-set to be all unicode strings"""
		if attributes is None:
			attributes = {}
		for key,value in attributes.items():
			if not isinstance( value, (str,unicode)):
				attributes[key] = unicode( value )
			elif isinstance( value, str ):
				attributes[key] = value.decode( defaultEncoding )
		return attributes

class XMLGenerator( propertied.Propertied ):
	"""Base-class for XML-generating objects"""
	propertyTagName = 'p'
	def __init__( self, driver=None, **named ):
		"""Initialise the statement-generator

		Driver will be used to determine features for
		generation (when that's implemented).
		"""
		super( XMLGenerator, self).__init__(
			driver = driver,
			**named
		)
	def __call__( self, schema, *arguments, **named ):
		"""Create XML document for given schema"""
		file = StringIO()
		self._generator = Generator(file)
		self._generator.startDocument()
		self.node( schema, *arguments, **named )
		self._generator.endDocument()
		return file.getvalue()
	def node( self, schema, *arguments, **named ):
		"""Generate XML for a single schema node"""
		properties = type(schema).getProperties()
		if hasattr( schema, 'dbObjectType'):
			tagName = schema.dbObjectType.lower()
		else:
			tagName = '%s.%s'%( schema.__class__.__module, schema.__class__.__name__ )
			print 'Warning: schema %s has no dbObjectType attribute, exporting as class-name'%(schema,)
		propertySet = {}
		propertyTags = []
		for property in properties:
			if not property.name.startswith( '_Schema__' ):
				if hasattr( property, 'getState' ):
					try:
						value = property.getState( schema )
					except (AttributeError,KeyError):
						# no non-default value set, so ignore...
						print 'skipping', property.name
					else:
						propertyTags.append( (property, value ) )
##						if self.simpleDataType( property, schema, value ):
##							propertySet[ property.name ] = unicode( value )
##						else:
				else:
					print """Warning: don't know how to linearise property %r, skipping"""%( property, )
		self._generator.startElement( tagName, propertySet )
		for property, value in propertyTags:
			self._generator.startElement( self.propertyTagName )
			self._generator.startElement( 'pn' )
			self._generator.characters( property.name )
			self._generator.endElement( 'pn' )
			self.valueAsContent( value )
			self._generator.endElement( self.propertyTagName )
		self._generator.endElement( tagName )
	def valueAsContent( self, value ):
		"""Export given value as a piece of content"""
		if isinstance( value, dbschema.Schema):
			self.node( value )
		elif isinstance( value, (str,unicode,int,float,long)):
			self._generator.characters( unicode(value) )
		elif isinstance( value, (list,tuple)):
			self._generator.startElement( 'list')
			for item in value:
				self._generator.startElement( 'li')
				self.valueAsContent( item )
				self._generator.endElement( 'li')
			self._generator.endElement( 'list')
		elif isinstance( value, dict ):
			self._generator.startElement( 'dict')
			for key,item in value.items():
				self._generator.startElement( 'li', name=unicode(key))
				self.valueAsContent( item )
				self._generator.endElement( 'li')
			self._generator.endElement( 'dict')
		else:
			print """Warning: don't know how to linearise %r object"""%( value, )
			
			
	def simpleDataType( self, property, client=None, value=None ):
		"""Is this property a simple data-type (can be included in an attr)?"""
		dataType = property.getDataType().split( '.' )
		if dataType:
			if dataType[:2] == ['str','long']:
				return 0
			elif dataType[0] in ('str', 'int','float','id', 'long','bool'):
				return 1
			else:
				return 0
		else:
			return 0
		

class XMLReader( propertied.Propertied ):
	"""Class to read in a database description"""
	def __init__( self ):
		self.stack = []
	def startElement( self, name, properties ):
		"""Deal with the start of any element"""
		node = self.node( name, properties )
		if self.stack and self.stack[-1]:
			self.stack[-1].append( node )
		elif not self.stack:
			self.root = node
		self.stack.append( node )
		if not node:
			print 'Warning: %r tag not recognised: %s'%(name,properties.items())
	def endElement( self, name ):
		try:
			method = self.dispatchEndMapping.get( name )
			if method:
				method( self, name, properties )
		finally:
			self.stack.pop()
	def processingInstruction( self, *args, **named ):
		print 'processingInstruction', args, named
	def characters( self, *args, **named ):
		print 'characters', args, named
	def setDocumentLocator( self, *args, **named ):
		print 'setDocumentLocator', args, named
	def startDocument( self, *args,**named ):
		print 'startDocument', args, named
	def endDocument( self, *args,**named ):
		print 'endDocument', args, named
	dispatchEndMapping = {}
	nodeMapping = {
		"database": dbschema.DatabaseSchema,
	}
	def node( self, name, properties ):
		"""Create a new node given familiar name "name" and property-set"""
		cls = self.nodeMapping.get( name )
		if cls:
			properties = dict([(str(x),y) for (x,y) in properties.items()])
			print 'properties', properties
			node = cls( **properties )
			return node
		return None

if __name__ == "__main__":
	from pytable import schemabuilder
	db = schemabuilder.database(
		unicode("testá", 'latin-1'),
		[
			schemabuilder.table(
				"sometable",
				[
					schemabuilder.field(
						"somefield",
						"integer",
						0,
						"""Some comment for a field""",
					),
				],
			),
		],
	)
	print repr(db), repr(db.name)
	result = XMLGenerator()( db )
	reader = XMLReader()
	print result
	
##	sax.parseString( result, reader)
##	print repr(reader.root), repr(reader.root.name)
	