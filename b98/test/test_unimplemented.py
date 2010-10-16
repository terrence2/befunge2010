import sys
sys.path = ['..']+sys.path
from Interpreter import Interpreter, UnsupportedOperator

def test_high():
	try:
		Interpreter( program="h" ).run()
	except UnsupportedOperator, ex:
		return
	assert False

def test_low():
	try:
		Interpreter(program="l").run()
	except UnsupportedOperator, ex:
		return
	assert False

def test_iterate():
	try:
		Interpreter(program="k").run()
	except UnsupportedOperator, ex:
		return
	assert False

