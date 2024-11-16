from math import isclose
# elliptic curve point defintion

# want to define properties for points A, B and C to allow for point addition:
	
# 1) indentity -> I + A = A 
# I is a zero-like point. we consider it (inf,inf)
# 2) commutativity -> A + B = B + A
# 3) associativity -> (A + B) + C = A + ( B + C)
# 4) invertibility -> A + (- A) = I

# from finite_field import FiniteElement
class Point:
	
 def __init__(self, x,y,a,b):
  '''curve y^2 = x^3 + a*x + b
  curve parameterised by a & b'''
  
  # infinity point
  if x is None and y is None:
   self.x = None
   self.y = None
   self.a = a
   self.b = b 
   return
   
  try:
   # testing over real numbers
   if not isclose( y**2, x**3 + a*x + b):
    err_msg = f'({x},{y}) does not lie on curve y^2 = x^3 + {a}*x + {b}'
    raise ValueError(err_msg)
  except TypeError:
   # testing over finite field elements
   if y**2 != x**3 + a*x + b:
    err_msg = f'({x},{y}) does not lie on curve y^2 = x^3 + {a}*x + {b}'
    raise ValueError(err_msg)
   
  
  self.x=x
  self.y=y
  self.a=a
  self.b=b
	
 def __repr__(self):
  return f'({self.x},{self.y})_{self.a}_{self.b}'
   
 def __eq__(self, other):
  return self.x==other.x and self.y==other.y and self.a==other.a and self.b==other.b
	
 def __neq__(self, other):
  return self.x!=other.x and self.y!=other.y and self.a!=other.a and self.b!=other.b
	
	
 def __add__(self,other):
  if self.a != other.a or self.b != other.b:
   err_msg = f'{self} and {other} are not on the same curve'
   raise TypeError(err_msg)
  # self Point is infinite return Point other 
  if self.x is None or self.y is None:
   return other
  # other Point is infinite return Point self 
  if other.x is None or other.y is None:
   return self
  # point self and point other produce zero-like point; P + (-P) = I 
  if self.x == other.x and self.y != other.y:
   return self.__class__(None,None,self.a,self.b)
  # self addition with Point at x axis intersect
  if self == other and self.y == 0 * self.x:
   return self.__class__(None,None,self.a,self.b)
  if self.x != other.x:
      # 2 points with different x coordinates
      s = (other.y-self.y)/(other.x -self.x)
      x_new = s**2 - self.x - other.x
      y_new = s*(self.x -x_new) - self.y
      return self.__class__(x_new,y_new,self.a,self.b)
  if self.x == other.x and self.y == other.y:
   # 2 * point; tagent line to curve
   s = (3*self.x**2 +self.a)/(2*self.y)
   x_new = s**2 - 2*self.x
   y_new = s*(self.x -x_new)-self.y
   return self.__class__(x_new,y_new,self.a,self.b)
   
 def __rmul__(self, value):
  # time-complexity(value)
  # value * self.Point
  # zero-like Point to aggregate result in
  result = self.__class__(None,None,self.a,self.b)
  for _ in range(value):
   result += self
  return result
  
 def __rmul__(self,value):
  # time-complexity(log_2(value))
  v = value 
  p = self 
  result = self.__class__(None,None,self.a,self.b)
  # until v is zero
  while v:
   if v & 1:
    # if least sig bit-position 1, add to result
    result += p
   # double point value to correspond bit-positional value
   p += p
   #bit-wise right shift
   #e.g little-edian v = 10110
   # then v >>=1 -> 1011
   # apply again
   # v >>=1 -> 101
   v >>= 1
  return result 
  
  
  
   
   
if __name__ == '__main__':
   
 # test cases
 fmt = 8
 print('#'*fmt,'represent point', '#'*fmt)
 p1 = Point(18,77,5,7)
 print(p1)
 p2 = Point(-1,-1,5,7)
 print(p2)
 print('#'*fmt,'comparison', '#'*fmt)
 print(f'are {p1} and {p1} the same?', p1 == p1)
 print(f'are {p1} and {p2} the same?',p1 == p2)
	
 p_inf = Point(None,None,5,7)
	
 print('#'*fmt,'addition', '#'*fmt)
 print( f'{p1}+{p_inf}={p1+ p_inf}')
 print( f'{p1}+{p2}={p1+p2}')
 print( f'{p2}+{p2}={p2+p2}')
	
 # NOTICE: we have defined
 # P = I + P 
 # where I is the additive identity (zero-like element - infinite point)
 # we however have NOT defined 
 # subtraction on the Point  
 # P + (-P) = I 
	
 # print('#'*fmt,'subtraction', '#'*fmt)
 # print( f'{p2}-{p2}={p2-p2}')
 print('#'*fmt,'multiplication', '#'*fmt)
 coefs =[1, 100, 100000]
	
 for coef in coefs:
  print( f'{coef}*{p1}={coef*p1}')
	
	
 # special case for y = 0 coordinate -> x axis intersection point
 # TO DO: find x coordinate of intersection point
 # test addition of point(x,0,5,7) should be infinity
	
	
