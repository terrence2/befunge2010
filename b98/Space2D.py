from Cell import Cell

class Space2D(object):
	def __init__( self, program ):
		'''Accepts a program encoded in utf-8 and builds a 2-funge cell space.'''
		self.raw = program.split('\n')

		# grid position
		self.least = (0,0)

		# find dimensions
		self.w = 0
		for ln in self.raw:
			if len(ln) > self.w: self.w = len(ln)
		self.h = len(self.raw)

		# rebuild with normalized widths and char reprs
		self.grid = []
		for i in xrange(self.h):
			self.grid.append( [] )
			for j in xrange(self.w):
				self.grid[i].append( Cell(ord(' ')) )
				if j < len(self.raw[i]):
					self.grid[i][j] = Cell(ord(self.raw[i][j]))

	def _grow( self, w, h ):
		'''Make the space larger, to w h'''
		grid = []
		for i in xrange(h):
			grid.append( [] )
			for j in xrange(w):
				grid[i].append( Cell(ord(' ')) )
				if i < self.h and j < self.w:
					grid[i][j] = self.grid[i][j]
		self.w = w
		self.h = h

	def inside( self, x, y ):
		'''Return true if the given coordinates are inside the currently allocated space.'''
		return x < self.w and x >= 0 and y < self.h and y >= 0

	def get( self, x, y ):
		if self.inside(x,y):
			return self.grid[y][x]
		return Cell(ord(' '))
	
	def put( self, x, y, val ):
		assert isinstance(val,Cell)
		if x >= self.w or y >= self.h:
			self._grow( max(x,self.w), max(y,self.h) )
		#print "PUT: %s,%s in %s" % (x,y,self.grid)
		self.grid[y][x] = val
	
	def __str__( self ):
		out = ""
		for row in self.grid:
			for r in row:
				c = '.'
				try: c = r.as_int()
				except: out += '.'
				if c < 10: c = str(c)
				try: c = chr(c)
				except: out += '.'
				out += c
			out += "\n"
		return out