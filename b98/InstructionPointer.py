class InstructionPointer(object):
	def __init__( self, space ):
		self.position = [0,0]
		self.delta = (1,0)
		self.space = space
		self.storage_offset = (0,0)
	
	def instr( self ):
		'''Return the instruction under the instruction pointer.'''
		return self.space.get( self.position[0], self.position[1] ).as_int()
	
	def next( self ):
		'''Move the instruction pointer forward by delta.'''
		assert not self.is_dead()
		
		self.position[0] += self.delta[0]
		self.position[1] += self.delta[1]

		# use befunge's special backtracking wrapping method
		if not self.space.inside(self.position[0],self.position[1]):
			# reverse
			dx = -self.delta[0]
			dy = -self.delta[1]
			# prior backward (inside space)
			px = self.position[0] + dx
			py = self.position[1] + dy
			# backtrack
			while self.space.inside( px, py ):
				px += dx
				py += dy
			# prior forward (back inside space)
			self.position[0] = px - dx
			self.position[1] = py - dy
			
			# if the delta is larger than the board... 
			assert self.space.inside(self.position[0],self.position[1])			

	def prev( self ):
		'''Move the instruction pointer backward by -delta.'''
		self.reverse()
		self.next()
		self.reverse()
		
	def is_dead( self ):
		'''Return true if the instruction pointer has no delta.'''
		return self.delta[0] == 0 and self.delta[1] == 0
	
	def reverse( self ):
		'''Flip the direction of the instruction pointer delta.'''
		self.delta = (-self.delta[0],-self.delta[1])
	
	def rotate( self, angle ):
		'''Rotate the angle of our instruction pointer's delta by angle degrees.'''
		# this should be a lut for cardinal cases plus a real vector rotation, either matrix or hacked 2D
		# this is only used for [ and ], but the ip can be in 'absolute vector' or 'flying' mode
		#	when it hits one of these, so we do really need a full rotation implementation.
		# FIXME: this is probably the worst of all possible implementations
		assert abs(angle) == 90.0, "IP Rotation must currently be 90 degrees"
		if angle > 0.0:
			if self.delta == (1,0): self.delta = (0,1)
			elif self.delta == (0,1): self.delta = (-1,0)
			elif self.delta == (-1,0): self.delta = (0,-1)
			elif self.delta == (0,-1): self.delta = (1,0)
			else:
				raise NotImplementedError, "IP Rotation about non cardinal axis is not implemented"
		elif angle < 0.0:
			if self.delta == (1,0): self.delta = (0,-1)
			elif self.delta == (0,1): self.delta = (1,0)
			elif self.delta == (-1,0): self.delta = (0,1)
			elif self.delta == (0,-1): self.delta = (-1,0)
			else:
				raise NotImplementedError, "IP Rotation about non cardinal axis is not implemented"
		else:
			pass
