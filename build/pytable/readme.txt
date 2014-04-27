wxPython Properties Distribution

What Is It:

	An alternative to the wxWindows property editing
	classes for use with wxPython  2.3.3 (and above)
	and Python 2.2 (and above).  It allows property
	editing with python objects (as opposed to the
	wxWindows property editors, which manipulate primitive
	data types).

	There are 3 packages included in the distribution:

		wxprop -- the wxPython property editing package
			Includes "standard" property editors, and a
			framework for custom property editors.  Also
			includes property editing views for single objects
			and collections of objects.

		wxoo -- python-object-oriented wxPython controls and events.
			Includes object-oriented drag and drop mechanisms.

		basicproperty -- Python 2.2 property sub-classes
			Provide a framework for higher-level property classes
			which substantially automate the bookkeeping of
			type checking, type coercion, bounds checking,
			and storage of data values.

Installation:

	Note: this is early alpha software, expect that there will
		be bugs, and that the APIs will change over time.

	The homepage for the distribution is:

		http://sourceforge.net/projects/wxpypropdist/

	Generally speaking, you should get the latest released version
	available on this page.  If you have CVS available, a more
	appropriate option for contributing and/or keeping current
	is to use the SourceForge CVS repository.  You can find
	information on the CVS repository here:

		http://sourceforge.net/cvs/?group_id=50588

	You'll need to install the following dependencies before
	installing the wxPython properties distribution:

		Python 2.2(.1) or above
			http://www.python.org/

		wxPython 2.3.3
			http://www.wxpython.org/
			Note: as of this writing, only wxPython 2.3.3pre5
			is available, this version fixes a bug with
			wxPython 2.3.2.1, and is preferable for developers
			wishing to work on the wxPython properties distribution

		[optional]
		mx.DateTime (part of the mx.Base distribution)
			http://www.egenix.com/files/python/eGenix-mx-Extensions.html#Download-mxBASE
			Presently most of the date-specific code relies on
			the mx.DateTime extension library.  This is largely
			an artifact of the original project from which the
			properties distribution was derived.  Making this
			dependency non-critical is an open project.
			
		wxpycolors (new)
			http://sourceforge.net/projects/wxpycolors/
			
			An optional colour-editing control relies on this
			colour-space aware set of colour-editing controls.
			This package has just released the first readily
			downloadable version, so you can now install it
			with a simple "setup.py install" call.
			Note: requires Numeric Python
			If you do not install this, a control that launches
			the standard colour dialog will be used.

	To install the properties distribution from the source archive,
	you will use the standard python distutils approach.

		Unzip the source archive (for example, properties-0.1.7a.zip)
		into a temporary directory.  Be sure to maintain the internal
		directory structure of the zip file.

		Run:  python setup.py install
			Note: There is currently an error in the installer which
			causes the installation of the source graphics for the
			collection editors to fail.  As these are merely source
			files (the images are compiled into Python modules), the
			error is non-critical, and the message can be ignored.

	To install the properties distribution from CVS, the recommended
	approach is:

		check out the properties "module" (WinCVS term) from CVS into
		some directory on your hard disk (the location is unimportant)
		
			This will create a directory "properties" with subdirectories
			named wxprop, wxoo, and basicproperty.

		add the properties directory created in the previous step to
		your PythonPath.  The easiest way to do this is to add a file
		to your Python/Lib directory named properties.pth containing a
		single line specifying the properties directory.

	Alternately, for those not intending to help with the development
	of the properties distribution (though realistically, it is probably
	too early for such people to be working with the package), you could
	check out just the 3 packages directly into a directory on your
	PythonPath.


Testing/Demonstration:

	At present there is very little testing/demonstration code in the
	project.  A single file properties/wxprop/test.py serves
	as both test and demonstration for the package.  If this file runs
	without complaining, (and displays the multi-object property editor),
	then you have a functional installation.

	basicproperty/tests/test.py will run the basicproperty test suite
	(which is currently fairly spotty).

	wxprop/tests contains a few quick demo/tests, and should eventually
	house most of the demo/testing code when it's finished.
