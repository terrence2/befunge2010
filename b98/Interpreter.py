#import random
import pypy.rlib.rrandom
from pypy.rlib.streamio import open_file_as_stream
import os
import sys
from Cell import Cell
from Space2D import Space2D
from StackStack import StackStack
from InstructionPointer import InstructionPointer


class UnsupportedOperator(Exception):
	def __init__( self, msg ):
		self.message = msg

class Interpreter(object):
	MODE_INTERP = 0
	MODE_STRING = 1
	
	def __init__( self, program=None, filename=None, argv=[] ):
		self.program = program
		if filename:
			f = open_file_as_stream(filename)
			self.program = f.readall()
			f.close()

		self.space = Space2D( self.program )
		self.stacks = StackStack()
		self.argv = argv

	def run( self ):
		icnt = 0
		ip = InstructionPointer(self.space)
		mode = self.MODE_INTERP
		rng = pypy.rlib.rrandom.Random()
		
		while True:
			icnt += 1
			instr = ip.instr()
			#print "%s: %s" % (icnt,chr(instr))
			#print "%s(%s): %s" % (icnt,chr(instr),str(self.stacks))
			
			if mode == self.MODE_STRING:
				# Unlike when we collapse spaces and comments, when we are
				#	in string mode the chars we push are still logically operators,
				#	so we need to allow icnt to increment as we read
				#while op
				if instr == ord('"'):
					mode = self.MODE_INTERP
				else:
					self.stacks.push( Cell(instr) )
				ip.next()
				
			else:
				if instr == ord('"'):
					mode = self.MODE_STRING

				# direction controls
				elif instr == ord('>'):
					ip.delta = (1,0)
				elif instr == ord('<'):
					ip.delta = (-1,0)
				elif instr == ord('v'):
					ip.delta = (0,1)
				elif instr == ord('^'):
					ip.delta = (0,-1)
				elif instr == ord('h'):
					raise UnsupportedOperator, "Go High is only for 3D funges."
				elif instr == ord('l'):
					raise UnsupportedOperator, "Go Low is only for 3D funges."
				elif instr == ord(']'):
					ip.rotate( 90.0 )
				elif instr == ord('['):
					ip.rotate( -90.0 )
				elif instr == ord('r'):
					ip.reverse()
				elif instr == ord('?'):
					val = rng.genrand32()
					if val < 1 * (2**31): ip.delta = (1,0)
					elif val < 2 * (2**31): ip.delta = (-1,0)
					elif val < 3 * (2**31): ip.delta = (0,1)
					else: #val < 1 * (2**31)
						ip.delta = (0,-1)

				# Cell Crunching
				elif instr >= ord('0') and instr <= ord('9'):
					self.stacks.push( Cell( instr - ord('0') ) )
				elif instr == ord('+'):
					b = self.stacks.pop()
					a = self.stacks.pop()
					self.stacks.push( a.iadd(b) )
				elif instr == ord('*'):
					b = self.stacks.pop()
					a = self.stacks.pop()
					self.stacks.push( a.imul(b) )
				elif instr == ord('-'):
					b = self.stacks.pop()
					a = self.stacks.pop()
					self.stacks.push( a.isub(b) )
				elif instr == ord('/'):
					b = self.stacks.pop()
					a = self.stacks.pop()
					self.stacks.push( a.idiv(b) )
				elif instr == ord('%'):
					b = self.stacks.pop()
					a = self.stacks.pop()
					self.stacks.push( a.imod(b) )

				# Strings
				elif instr == ord('\''): # Fetch Char
					ip.next()
					val = self.space.get( ip.position[0], ip.position[1] )
					self.stacks.push( val )
				elif instr == ord('s'): # Store Char
					val = self.stacks.pop()
					ip.next()
					self.space.put( ip.position[0], ip.position[1], val )
					ip.prev()

				# Stack
				elif instr == ord('$'): # Pop
					self.stacks.pop()
				elif instr == ord(':'): # Dup
					a = self.stacks.pop()
					b = a.dup()
					self.stacks.push( a )
					self.stacks.push( b )
				elif instr == ord('\\' ): # Swap
					a = self.stacks.pop()
					b = self.stacks.pop()
					self.stacks.push(a)
					self.stacks.push(b)
				elif instr == ord('n'): # Clear
					while len(self.stacks.toss()):
						self.stacks.pop()
				
				# Funge Space
				elif instr == ord('g'): # Get
					y = self.stacks.pop()
					x = self.stacks.pop()
					v = self.space.get( x.as_int()+ip.storage_offset[0], y.as_int()+ip.storage_offset[1] )
					self.stacks.push( v )
				elif instr == ord('p'): # Put
					y = self.stacks.pop()
					x = self.stacks.pop()
					v = self.stacks.pop()
					self.space.put( x.as_int()+ip.storage_offset[0], y.as_int()+ip.storage_offset[1], v )
				
				# Stack-Stack
				elif instr == ord('{'): # Begin Block
					n = self.stacks.pop()
					self.stacks.begin( n )
					self.stacks.soss().append( Cell(ip.storage_offset[0]) )
					self.stacks.soss().append( Cell(ip.storage_offset[1]) )
					ip.storage_offset = (ip.position[0]+ip.delta[0],ip.position[1]+ip.delta[1])
				elif instr == ord('}'): # End Block
					if not self.stacks.soss(): # act like r
						ip.reverse()
					else:
						n = self.stacks.pop()
						y = self.stacks.soss().pop()
						x = self.stacks.soss().pop()
						ip.storage_offset = (x.as_int(),y.as_int())
						self.stacks.end( n )
				elif instr == ord('u'): # Stack-Under-Stack
					raise UnsupportedOperator, "Stack-Under-Stack not yet supported."
				
				# i/o
				elif instr == ord(','):
					val = self.stacks.pop()
					os.write( 1, chr(val.as_int()) )
				elif instr == ord('.'):
					val = self.stacks.pop()
					os.write( 1, val.str() )
				elif instr == ord('&'):
					val = os.read( 0, 1 )
					self.stacks.push( Cell( int(val[0]) ) )
				elif instr == ord('~'):
					val = os.read( 0, 1 )
					self.stacks.push( Cell( int(ord(val[0])) ) )

				# flow control
				elif instr == ord('#'):
					ip.next()
					ip.next()
					continue
				elif instr == ord(';'):
					ip.next()
					i = ip.instr()
					while i != ord(';'):
						ip.next()
						i = ip.instr()
					ip.next()
					continue
				elif instr == ord(' '):
					ip.next()
					i = ip.instr()
					while i == ord(' '):
						ip.next()
						i = ip.instr()
					continue
				elif instr == ord('j'): # Jump Forward
					cnt = self.stacks.pop()
					for i in xrange(cnt.as_int()):
						ip.next()
						instr = ip.instr()
					continue
				elif instr == ord('k'): # Iterate
					raise UnsupportedOperator, "Iterate not yet supported."
				elif instr == ord('@'):
					return 0
				elif instr == ord('q'):
					#print "\n%s" % str(self.stacks)
					#print "\n%s" % str(self.space)
					return self.stacks.pop().as_int()
				
				# Decision Making
				elif instr == ord('!'): # Not
					val = self.stacks.pop()
					if val.is_true(): self.stacks.push(Cell(0))
					else: self.stacks.push(Cell(1))
				elif instr == ord('`'): # Greater Than
					b = self.stacks.pop()
					a = self.stacks.pop()
					if a.cmp_(b) > 0: self.stacks.push( Cell(1) )
					else: self.stacks.push( Cell(0) )
				elif instr == ord('_'): # E-W If
					val = self.stacks.pop()
					if val.is_true(): ip.delta = (-1,0)
					else: ip.delta = (1,0)
				elif instr == ord('|'): # N-S If
					val = self.stacks.pop()
					if val.is_true(): ip.delta = (0,-1)
					else: ip.delta = (0,1)
				elif instr == ord('m'): # High-Low If
					raise UnsupportedOperator, "High-Low If is not supported on 2D funges."
				elif instr == ord('w'): # Compare (rho-tate)
					b = self.stacks.pop()
					a = self.stacks.pop()
					if b.cmp_(a) > 0: ip.rotate( -90.0 )
					else: ip.rotate( 90.0 )
				
				# Get System Info
				elif instr == ord('y'): # (y not?)
					# env
					self.stacks.push( Cell(0) )
					self.stacks.push( Cell(0) )
					# command line
					#print self.argv
					self.stacks.push( Cell(0) )
					for i in xrange(len(self.argv)-1,-1,-1):
						self.stacks.push( Cell(0) )
						for j in xrange(len(self.argv[i])-1,-1,-1):
							#print "at: %s" % self.argv[i][j]
							self.stacks.push( Cell(ord(self.argv[i][j])) )
					for s in self.stacks.stacks: # length of all stacks
						self.stacks.push( Cell(len(s)) )
					self.stacks.push( Cell(len(self.stacks.stacks)) ) # stack count
					#import datetime
					#_td = datetime.date.today() # pypy does not like
					#self.stacks.push( (today.hour * 256 * 256) + (today.minute * 256) + (today.second) ) # time
					#self.stacks.push( ((today.year - 1900) * 256 * 256) + (today.month * 256) + (today.day) ) # day
					self.stacks.push(Cell(0)); self.stacks.push(Cell(0))
					self.stacks.push( Cell(self.space.w) ); self.stacks.push( Cell(self.space.h) ); # space size
					self.stacks.push( Cell(self.space.least[0]) ); self.stacks.push( Cell(self.space.least[1]) ); # space lower bound
					self.stacks.push( Cell(ip.storage_offset[0]) ); self.stacks.push( Cell(ip.storage_offset[1]) ); # ip storage offset
					self.stacks.push( Cell(ip.delta[0]) ); self.stacks.push( Cell(ip.delta[1]) ); # ip delta
					self.stacks.push( Cell(ip.position[0]) ); self.stacks.push( Cell(ip.position[1]) ); # ip position
					self.stacks.push( Cell(0) ) # team number?
					self.stacks.push( Cell(0) ) # thread id
					self.stacks.push( Cell(2) ) # funge dimension
					self.stacks.push( Cell(ord(os.sep)) ) # path sep char
					self.stacks.push( Cell(0) ) # subprocess type
					self.stacks.push( Cell(000) ) # version
					self.stacks.push( Cell(0x00000000) ) # handprint
					self.stacks.push( Cell(8) ) # bytes per cell
					self.stacks.push( Cell(0) ) # env flags

				ip.next()
		return 0
			
