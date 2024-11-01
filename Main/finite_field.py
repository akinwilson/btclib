# element of finite set with properties:
# 1) additive identity
# 2) additive inverse
# 3) multiplicative identity
# 4) multiplicative inverse
# defined upon primitive FiniteElement.

# any exercise of properties returns element in finite set.

# elements of finite set also belong to the positive integers (include the additive identity element 0) i.e FiniteSet_order = { 0,1,...,order-2,order-1} which are all integers and FiniteElement belongs to aformentioned set. 

# order **MUST** be prime such that all elements are co-prime to order of set. otherwise divsion is not defined correctly for values not co-prime to order

# **fermats little theorem** allows for definition of inverse 

# a / b mod (order) => a * ( 1/b) mod (order) => a * b^(-1) mod (order), since b^(order -1) mod( order) = 1 mod (order) **IFF** order is prime therefore indroducing a 1 and substituting it leafs to: 

# a * b^(-1) * 1 mod (order) => a * b^(-1) * b^(order-1) mod (order) => a * b^(order - 2) mod(order) is equivalent to a/b mod (order)


class FiniteElement:
 def __init__(self,element,order):
  if element < 0 or element >= order:
   err_msg = f'Element {element} is not within finite set of order {order}. Element {element} required to be >=0 and < order of {order} ' 
   raise ValueError(err_msg)
  self.order = order
  self.element = element
  
 def __repr__(self):
  return f'FE_Ord{self.order}_({self.element})'
  
 def __eq__(self,other):
  if other is None:
   return False 
  return self.element == other.element and self.order == other.order
  
 def __add__(self, other):
  if self.order != other.order:
   err_msg = f'Cannot add elements from different finite sets. I.e Order of sets must be equal and supplied elements, {self.element} and {other.elemen} belong to sets of order {self.order} and {other.order} respectively.'
   raise TypeError(err_msg)
  new_element = (self.element + other.element) % self.order
  return self.__class__(new_element, self.order)
	
 def __sub__(self, other):
  if self.order != other.order:
   err_msg = f'Cannot subtract elements from different finite sets. I.e Order of sets must be equal and supplied elements, {self.element} and {other.elemen} belong to sets of order {self.order} and {other.order} respectively.'
   raise TypeError(err_msg)
  new_element = (self.element - other.element) % self.order 
  return self.__class__(new_element, self.order )
  
 def __rsub__(self, other):
  if self.order != other.order:
   err_msg = f'Cannot subtract elements from different finite sets. I.e Order of sets must be equal and supplied elements, {self.element} and {other.elemen} belong to sets of order {self.order} and {other.order} respectively.'
   raise TypeError(err_msg)
  new_element = (other.element - self.element) % self.order 
  return self.__class__(new_element, self.order )
 def __neg__(self):
  new_element = (- self.element)% self.order
  return self.__class__(new_element, self.order)
	
 def __mul__(self, other):
  if self.order != other.order:
   err_msg = f'Cannot multiple elements from different finite sets. I.e Order of sets must be equal and supplied elements, {self.element} and {other.elemen} belong to sets of order {self.order} and {other.order} respectively.'
   raise TypeError(err_msg)
  new_element = (self.element*other.element) % self.order
  return self.__class__(new_element, self.order)
  
 def __rmul__(self, value):
  new_element = (self.element*value) % self.order
  return self.__class__(new_element, self.order)
	
 def __pow__(self, exponent):
  if type(exponent) != int:
   err_msg = f'Exponent should integer value to avoid rooting of finite element which would return none integer value. Received exponent {exponent}'
   raise ValueError(err_msg)
  n = exponent
  while n < 0:
   n += self.order -1
   
  new_element = pow(self.element, n, self.order)
  return self.__class__(new_element, self.order)
	
 def __truediv__(self, other):
  if self.order != other.order:
   err_msg = f'Cannot divide elements from different finite sets. I.e Order of sets must be equal and supplied elements, {self.element} and {other.elemen}, belong to sets of order {self.order} and {other.order} respectively.'
   raise TypeError(err_msg)
  if other.element == 0:
   err_msg = f'Division by {other} is not allowed. I.e. Division by 0 undefined'
   raise ValueError(err_msg)
   
  new_element = self.element * pow(other.element, self.order - 2, self.order) % self.order
  return self.__class__(new_element, self.order) 
  
class S256FieldElement(FieldElement):
  
  def __init__(self,element,order=None):
   super().__init__(element,order=)

  

  
if __name__ == '__main__':
	
 # test cases
 fmt = 12
 print('#'*fmt,'represent finite element', '#'*fmt)
 fe_o13_e7 = FiniteElement(7,13)
 print(fe_o13_e7)
 print('#'*fmt,'equality','#'*fmt)
 print(f'Is {fe_o13_e7} = {fe_o13_e7}? {fe_o13_e7 == fe_o13_e7}') 
 fe_o13_e5 = FiniteElement(5,13)
 print(f'Is {fe_o13_e7} = {fe_o13_e5}? {fe_o13_e7 == fe_o13_e5}')
 print('#'*fmt,'subtraction','#'*fmt)
 fe_o27_e2 = FiniteElement(2,27)
 fe_o27_e13 = FiniteElement(13,27)
 print(f'{fe_o27_e2}-{fe_o27_e13} = {fe_o27_e2 - fe_o27_e13}')
 print(f'{fe_o27_e13}-{fe_o27_e2} = {fe_o27_e13 - fe_o27_e2}')
 print('#'*fmt,'addition','#'*fmt)
 print(f'{fe_o27_e2}+{fe_o27_e13} = {fe_o27_e2+fe_o27_e13}')
 print(f'-{fe_o27_e13}+{fe_o27_e2} = {-fe_o27_e13 + fe_o27_e2}' )
 print('#'*fmt,'negation','#'*fmt )
 print(f'-{fe_o27_e13}={-fe_o27_e13}')
 print('#'*fmt, 'addiditive identity', '#'*fmt)
 print(f'{fe_o27_e13}+{FiniteElement(0,27)}={fe_o27_e13+FiniteElement(0,27)}')
 print('#'*fmt,'additive inverse','#'*fmt)
 print(f'{fe_o27_e13}-{fe_o27_e13}={fe_o27_e13- fe_o27_e13}')
 print('#'*fmt, 'multiplication','#'*fmt )
 print(f'{fe_o27_e2}*{fe_o27_e2}={fe_o27_e2 * fe_o27_e2}')
 print('#'*fmt, 'multiplicative identity', '#'*fmt)
 print(f'{fe_o27_e2}*{FiniteElement(1,27)}={fe_o27_e2 * FiniteElement(1,27)}')
 print('#'*fmt, 'exponentiation', '#'*fmt)
 print(f'{FiniteElement(7,31)}^2={FiniteElement(7,31)**2}')
 print(f'{FiniteElement(7,31)}^(-1)={FiniteElement(7,31)**(-1)}')
 print(f'{FiniteElement(7,31)}^0={FiniteElement(7,31)**(0)}')
 print('#'*fmt, 'Division','#'*fmt)
 a = FiniteElement(18,31)
 b = FiniteElement(9,31)
 a_div_b = a / b
 print(f'{a} / {b} = {a_div_b}')
 b_times_a_div_b = b * a_div_b
 print(f'does ({a}/{b}) * {b} = {a} {b_times_a_div_b == a}')
 a = FiniteElement(30,31)
 b = FiniteElement(17,31)
 a_div_b = a / b
 print(f'{a} / {b} = {a_div_b}')
 b_times_a_div_b = b * a_div_b
 print(f'does ({a}/{b}) * {b} = {a} {b_times_a_div_b == a}')
 print('#'*fmt, 'multiplicate inverse', '#'*fmt)
 # want a * a^(-1) = 1
 a = FiniteElement(21,31)
 a_inv = a**(-1)
 print(f'{FiniteElement(21,31)}^(-1) = {a_inv}')
 print(f'{a} * {a}^(-1) = {a*a_inv}')
	
	
 # divison by 0 element not allowed
 # a = FiniteElement(30,31)
 # b = FiniteElement(0,31)
 # a_div_b = a / b
 # print(f'{a} / {b} = {a_div_b}')
 # b_times_a_div_b = b * a_div_b
 # print(f'does ({a}/{b}) * {b} = {a} {b_times_a_div_b == a}')

 # print(FiniteElement(-2,13))
