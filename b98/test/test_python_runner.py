#from pypy.lang.befunge.Interpreter import Interpreter, UnsupportedOperator
#from pypy.lang.befunge.Cell import Cell
import sys
sys.path = ['../python']+sys.path

from Interpreter import Interpreter, UnsupportedOperator
from Cell import Cell
from pypy.rlib.streamio import open_file_as_stream
import py
import os
import os.path

def runtest( filename ):
	print "File: %s -> " % os.path.basename(filename),

	# get program contents
	f = open_file_as_stream(filename)
	program = f.readall()
	f.close()
	
	# expect?
	expect_rv = 0
	expect_stack = []
	expect_space = []
	expect_stdout = ''
	
	# look for special tags in out
	for ln in program.split('\n'):
		if ln.startswith( 'Return:' ):
			expect_rv = int(ln.split(' ')[-1])
		elif ln.startswith( 'Stack:' ):
			expect_stack = [Cell(int(v)) for v in ln.split(' ')[1:]]
		elif ln.startswith( 'Space:' ):
			parts = ln.split(' ')[1:]
			expect_space.append( (int(parts[0]),int(parts[1]),Cell(int(parts[2]))) )
		elif ln.startswith( 'Stdout:' ):
			expect_stdout = ln[7:].strip()

	# run the interpreter on the file
	cap = py.io.StdCaptureFD()
	i = Interpreter( filename=filename, argv=['testrunner'] )
	rv = i.run()
	fds = cap.done()
	actual_stdout = fds[0].read().strip()
	
	# check results
	#print "E: %s" % str(expect_stack)
	#print "A: %s" % str(i.stacks.head().inner)
	try:
		assert rv == expect_rv
		for v in expect_stack:
			assert 0 == v.cmp_( i.stacks.pop() )
		for x,y,val in expect_space:
			assert 0 == val.cmp_( i.space.get( x, y ) )
		assert expect_stdout == actual_stdout
	except:
		print ""
		print "RV: %s" % rv
		print str(i.stacks)
		raise

def test_all():
	# find all tests under programs directory
	filenames = []
	subdirs = os.listdir( 'programs' )
	for name in subdirs:
		progs = os.listdir( os.path.join('programs',name) )
		for prog in progs:
			if not prog.startswith('_'):
				filename = os.path.realpath( os.path.join('programs',name,prog) )
				filenames.append( filename )

	# build a test for each file
	for filename in filenames:
		yield runtest, filename
		
