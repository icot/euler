"""Script to automatically generate PyTable documentation"""
import pydoc2
from wxoo import initimagehandlers

if __name__ == "__main__":
	try:
		import wx
	except ImportError:
		pass
	else:
		class MyApp(wx.App):
			def OnInit(self):
				wx.InitAllImageHandlers()
				return True
		app = MyApp(0)
		app.MainLoop()
	excludes = [
		"wxPython.wx",
		"Numeric",
		"_tkinter",
		"Tkinter",
		"math",
		"string",
	]
	stops = [
		"wxoo.demo.demo"
	]

	modules = [
		"basicproperty",
		"basictypes",
		'logging',
		'__builtin__',
		'pytable',
	]	
	pydoc2.PackageDocumentationGenerator(
		baseModules = modules,
		destinationDirectory = ".",
		exclusions = excludes,
		recursionStops = stops,
	).process ()
	