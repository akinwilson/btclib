from finite_field import FiniteElement
from elliptic_curve import Point 


PRIME = 223
secp256k1_curve ={'a': 0,'b':7}
gen_point = {'x': 192,'y':105} 

a = FiniteElement(secp256k1_curve['a'],PRIME)
b = FiniteElement(secp256k1_curve['b'],PRIME)
x = FiniteElement(gen_point['x'],PRIME)
y = FiniteElement(gen_point['y'],PRIME)

order = 1
while True:
	if order * Point(x,y,a,b) == Point(None,None,a,b):
		print(f'Order found: {order}')
		print(f'Does {order} +1 return us back to generator point {Point(x,y,a,b)}', Point(x,y,a,b)  == (order +1 )* Point(x,y,a,b))
		break
	else:
		order +=1


# finding order of  


# bitcoin curve and generator Point
Gx= 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
ORDER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


PRIME = 2**256 - 2**32 - 977
BTC_GEN_POINT = {'x': Gx,'y':Gy}


a = FiniteElement(secp256k1_curve['a'],PRIME)
b = FiniteElement(secp256k1_curve['b'],PRIME)
x = FiniteElement(BTC_GEN_POINT['x'],PRIME)
y = FiniteElement(BTC_GEN_POINT['y'],PRIME)

print(f'Does the order \n\n{ORDER:x}\n\nBitcoin generator point form a cyclical group? ', ORDER * Point(x,y,a,b) == Point(None,None,a,b))
