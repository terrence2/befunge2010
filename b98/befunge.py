#!/usr/bin/python
# encoding: utf-8
#import autopath
import sys
import getopt

from pypy.rlib.streamio import open_file_as_stream

from Interpreter import Interpreter

f = open_file_as_stream(sys.argv[1])
program = f.readall()
f.close()

interp = Interpreter( program=program, argv=sys.argv[1:] )
rv = interp.run()

print interp.stacks

sys.exit( rv )
