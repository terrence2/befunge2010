import os
import os.path
import subprocess
from pypy.rlib.streamio import open_file_as_stream

def runtest( filename ):
	print "File: %s -> " % os.path.basename(filename),
	
	# get program contents
	f = open_file_as_stream(filename)
	program = f.readall()
	f.close()
	
	# expect?
	expect_rv = 0
	
	# look for special tags in out
	for ln in program.split('\n'):
		if ln.startswith( 'Return:' ):
			expect_rv = int(ln.split(' ')[-1])
	
	# run the program
	rv = subprocess.call( ['../../../translator/goal/befunge-c',filename] )
	assert rv == expect_rv

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
