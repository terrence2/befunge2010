from Cell import Cell

class StackStack(object):
	def __init__( self ):
		#self.stacks = [ Stack() ]
		self.stacks = [ [] ]

	def toss( self ): # top of stack stack
		return self.stacks[-1]

	def soss( self ): # second of stack stack
		if len(self.stacks) < 2: return []
		return self.stacks[-2]
	
	def begin( self, n ):
		'''Copy top n to new stack and push stack to new toss.
			Negative n backfills soss with 0's.
		'''
		s = []
		n = n.as_int()
		if n > 0:
			k = len(self.stacks[-1])
			for i in xrange(k):
				if i >= (k-n):
					s.append( self.stacks[-1][i] )
			if n > len(s):
				s = [Cell(0)]*(n-len(s)) + s
		elif n < 0:
			# put zeros on the soss (it's in the spec, but what good is it?)
			for i in xrange(abs(n)):
				self.push( Cell(0) )
		# add the new stack we just built
		self.stacks.append( s )

	def end( self, n ):
		assert len(self.stacks) > 1
		s = []
		n = n.as_int()
		if n > 0:
			k = len(self.stacks[-1])
			for i in xrange(k):
				if i >= (k-n):
					s.append( self.stacks[-1][i] )
			if n > len(s):
				s = [Cell(0)]*(n-len(s)) + s
		elif n < 0:
			# rip up the soss
			for i in xrange(abs(n)):
				self.stacks[-2].pop()
		for cell in s:
			self.soss().append( cell )
		self.stacks.pop()

	# passthrough to toss
	def push( self, value ):
		assert isinstance(value,Cell)
		self.stacks[-1].append( value )
	
	def pop( self ):
		if len(self.stacks[-1]):
			v = self.stacks[-1].pop()
		else:
			v = Cell(0)
		return v

	def __str__( self ):
		out = ""
		if len(self.stacks) > 0:
			out += "TOSS:\n"
			for i in self.stacks[-1]:
				out += "  %s\n" % str(i)
		if len(self.stacks) > 1:
			out += "SOSS:\n"
			for i in self.stacks[-2]:
				out += "  %s\n" % str(i)
		return out
	