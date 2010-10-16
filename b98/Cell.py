class IntCell(object):
	def __init__( self, value ):
		self.value = int(value)
	
	def iadd( self, other ):
		return Cell( self.value + other.value )
	
	def imul( self, other ):
		return Cell( self.value * other.value )
	
	def isub( self, other ): 
		return Cell( self.value - other.value )
	
	def idiv( self, other ):
		if other.value == 0: return Cell(0)
		return Cell( self.value / other.value )
	
	def imod( self, other ):
		return Cell( self.value % other.value )
	
	def is_true( self ):
		return bool(self.value)
	
	def cmp_( self, other ):
		return self.value - other.value
	
	def dup( self ):
		return IntCell( self.value )
	
	def as_int( self ):
		return self.value
	
	def str( self ):
		return str(self.value)


from pypy.rlib.rbigint import rbigint
ZERO = rbigint.fromint(0)

class BigIntCell(object):
	def __init__( self, ivalue, bvalue=None ):
		if bvalue:
			self.value = bvalue
		else:
			self.value = rbigint.fromint(ivalue)
	
	def iadd( self, other ):
		v = self.value.add( other.value )
		return BigIntCell(0,v)
	
	def imul( self, other ):
		v = self.value.mul( other.value )
		return BigIntCell(0,v)
	
	def isub( self, other ):
		v = self.value.sub( other.value )
		return BigIntCell(0,v)
	
	def idiv( self, other ):
		if not other.value.tobool(): return BigIntCell(0)
		v = self.value.floordiv( other.value )
		return BigIntCell(0,v)
	
	def imod( self, other ):
		v = self.value.mod( other.value )
		return BigIntCell(0,v)
	
	def is_true( self ):
		return not self.value.eq(ZERO)
	
	def cmp_( self, other ):
		diff = self.value.sub( other.value )
		if diff.lt( ZERO ): return -1
		elif diff.eq(ZERO): return 0
		else: return 1
	
	def dup( self ):
		v = self.value.add( ZERO )
		return BigIntCell(0,v)
	
	def as_int( self ):
		return self.value.toint()

	def str( self ):
		return self.value.str()

from pypy.rlib.rarithmetic import ovfcheck

class HybridCell(object):
	'''~6min on pidigits 10k'''
	def __init__( self, ivalue, bvalue=None ):
		self.ivalue = int(ivalue)
		self.bvalue = bvalue
	
	def iadd( self, other ):
		if self.bvalue:
			if other.bvalue:
				return HybridCell( 0, self.bvalue.add( other.bvalue ) )
			else:
				o = rbigint.fromint(other.ivalue)
				v = self.bvalue.add( o )
				return HybridCell( 0, v )
		else:
			if other.bvalue:
				s = rbigint.fromint(self.ivalue)
				v = s.add( other.bvalue )
				return HybridCell( 0, v )
			else:
				try:
					v = ovfcheck(self.ivalue + other.ivalue)
					return HybridCell( v )
				except OverflowError:
					v = rbigint.fromint(self.ivalue).add( rbigint.fromint(other.ivalue) )
					return HybridCell( 0, v )

	def imul( self, other ):
		if self.bvalue:
			if other.bvalue:
				return HybridCell( 0, self.bvalue.mul( other.bvalue ) )
			else:
				o = rbigint.fromint(other.ivalue)
				v = self.bvalue.mul( o )
				return HybridCell( 0, v )
		else:
			if other.bvalue:
				s = rbigint.fromint(self.ivalue)
				v = s.mul( other.bvalue )
				return HybridCell( 0, v )
			else:
				try:
					v = ovfcheck(self.ivalue * other.ivalue)
					return HybridCell( v )
				except OverflowError:
					v = rbigint.fromint(self.ivalue).mul( rbigint.fromint(other.ivalue) )
					return HybridCell( 0, v )
		
	def isub( self, other ):
		if self.bvalue:
			if other.bvalue:
				return HybridCell( 0, self.bvalue.sub( other.bvalue ) )
			else:
				o = rbigint.fromint(other.ivalue)
				v = self.bvalue.sub( o )
				return HybridCell( 0, v )
		else:
			if other.bvalue:
				s = rbigint.fromint(self.ivalue)
				v = s.sub( other.bvalue )
				return HybridCell( 0, v )
			else:
				v = self.ivalue - other.ivalue
				return HybridCell( v )
	
	def idiv( self, other ):
		if other.bvalue:
			if other.bvalue.eq( ZERO ):
				return HybridCell(0)
		else:
			if 0 == other.ivalue:
				return HybridCell(0)
		
		if self.bvalue:
			if other.bvalue:
				return HybridCell( 0, self.bvalue.div( other.bvalue ) )
			else:
				o = rbigint.fromint(other.ivalue)
				v = self.bvalue.div( o )
				return HybridCell( 0, v )
		else:
			if other.bvalue:
				s = rbigint.fromint(self.ivalue)
				v = s.div( other.bvalue )
				return HybridCell( 0, v )
			else:
				v = self.ivalue / other.ivalue
				return HybridCell( v )

	def imod( self, other ):
		if self.bvalue:
			if other.bvalue:
				return HybridCell( 0, self.bvalue.mod( other.bvalue ) )
			else:
				o = rbigint.fromint(other.ivalue)
				v = self.bvalue.mod( o )
				return HybridCell( 0, v )
		else:
			if other.bvalue:
				s = rbigint.fromint(self.ivalue)
				v = s.mod( other.bvalue )
				return HybridCell( 0, v )
			else:
				v = self.ivalue % other.ivalue
				return HybridCell( v )
	
	def is_true( self ):
		if self.bvalue:
			return not self.bvalue.eq(ZERO)
		return bool(self.ivalue)
	
	def cmp_( self, other ):
		if self.bvalue:
			if other.bvalue: o = other.bvalue
			else: o = rbigint.fromint( other.ivalue )
			diff = self.bvalue.sub( o )
			if diff.lt( ZERO ): return -1
			elif diff.eq(ZERO): return 0
			else: return 1
		return self.ivalue - other.ivalue
	
	def dup( self ):
		if self.bvalue:
			v = self.bvalue.add( ZERO )
			return HybridCell(0,v)
		return HybridCell( self.ivalue )
	
	def as_int( self ):
		if self.bvalue:
			return self.bvalue.toint()
		return self.ivalue
	
	def str( self ):
		if self.bvalue: return self.bvalue.str()
		return str(self.ivalue)


class HybridPromotingCell(object):
	'''~5.5min on pidigits 10k'''
	def __init__( self, ivalue, bvalue=None ):
		self.ivalue = int(ivalue)
		self.bvalue = bvalue
	
	def promote( self ):
		if self.bvalue: return
		self.bvalue = rbigint.fromint( self.ivalue )
	
	def iadd( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()
		
		if self.bvalue:
			return HybridPromotingCell( 0, self.bvalue.add( other.bvalue ) )
		else:
			try:
				v = ovfcheck(self.ivalue + other.ivalue)
				return HybridPromotingCell( v )
			except OverflowError:
				self.promote()
				other.promote()
				return HybridPromotingCell( 0, self.bvalue.add( other.bvalue ) )

	def imul( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()

		if self.bvalue:
			return HybridPromotingCell( 0, self.bvalue.mul( other.bvalue ) )
		else:
			try:
				v = ovfcheck(self.ivalue * other.ivalue)
				return HybridPromotingCell( v )
			except OverflowError:
				self.promote()
				other.promote()
				return HybridPromotingCell( 0, self.bvalue.mul( other.bvalue ) )

		
	def isub( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()

		if self.bvalue:
			return HybridPromotingCell( 0, self.bvalue.sub( other.bvalue ) )
		else:
			return HybridPromotingCell( self.ivalue - other.ivalue )
	

	def idiv( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()

		if self.bvalue:
			return HybridPromotingCell( 0, self.bvalue.floordiv( other.bvalue ) )
		else:
			return HybridPromotingCell( self.ivalue / other.ivalue )


	def imod( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()

		if self.bvalue:
			return HybridPromotingCell( 0, self.bvalue.mod( other.bvalue ) )
		else:
			return HybridPromotingCell( self.ivalue % other.ivalue )
	
	def is_true( self ):
		if self.bvalue:
			return not self.bvalue.eq(ZERO)
		return bool(self.ivalue)
	
	def cmp_( self, other ):
		if self.bvalue: other.promote()
		if other.bvalue: self.promote()

		if self.bvalue:
			diff = self.bvalue.sub( other.bvalue )
			if diff.lt( ZERO ): return -1
			elif diff.eq(ZERO): return 0
			else: return 1
		return self.ivalue - other.ivalue
	
	def dup( self ):
		if self.bvalue:
			v = self.bvalue.add( ZERO )
			return HybridPromotingCell(0,v)
		return HybridPromotingCell( self.ivalue )
	
	def as_int( self ):
		if self.bvalue:
			return self.bvalue.toint()
		return self.ivalue
	
	def str( self ):
		if self.bvalue: return self.bvalue.str()
		return str(self.ivalue)

	def __str__( self ):
		if self.bvalue: return self.bvalue.str()
		return str(self.ivalue)

Cell = HybridPromotingCell
