from Space2D import Space2D
from StackStack import StackStack
from Interpreter import Interpreter
from pypy.rlib.streamio import open_file_as_stream

def entry_point(argv):
	filename = argv[1]
	args = []
	args.append( filename )
	for i in xrange(len(argv)):
		if i > 1:
			args.append( argv[i] )

	interp = Interpreter( filename=filename, argv=args )
	rv = interp.run()

	return rv
	
def target(driver, args):
	driver.exe_name = 'befunge-%(backend)s'
	return entry_point, None
