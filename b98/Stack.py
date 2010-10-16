
class Stack(object):
	def __init__( self ):
		self.inner = []

	def push( self, value ):
		self.inner.append( value )
	
	def pop( self ):
		if len(self.inner): return self.inner.pop()
		return 0

	def length( self ):
		return len(self.inner)