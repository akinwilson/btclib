# elliptic curve signature algorithm
import hashlib
# want to 'sign' a 'document' s.t. it can be verified that the signature produced for document could only have been created by someone who knows the private/secret key, x, corresponding to a public key, y, where y is visible to all. 

 #  let g be the generator point 
 #  x * g = y
 
 # choose **RANDOM** 256-bit value, b
 # -> b * g = r    i.e a random point r
 # let x coordindate of r point be r_x
 
 # equivalent hardness to discrete logarithm problem:
 # finding u,v s.t 
 # u * g + v * y = b * g
 
 # u,v are none zero and are chosen by signer, whom knows x, (x * g = y; the public key) 
 
 # y = x * g  =( b  - u ) * v^(-1) * g
 # replace x*g = y leads to 
 # x = ( b  - u ) * v^(-1)
 
 # to a challenger (actor without access to x) finding the correct u & v would be equivalent to solving the discrete logarithm problem hence it can be assumed whomever produces u & v, knows x. 
 
 # to include document, z, in signature scheme with signature_value s, signer chooses u & v such that 
 
 # u = z * s^(-1)
 # v = r_x * s^(-1)
 
 # notice now we have included r_x, information about randomly generated point r using b (r = b * g)
 
# substituting u,v

# x = ( b * s - z  ) *  r_x^(-1)
# s = (x * r_x + z ) * b^(-1)

# i.e the signature_value s contains information about the randomly generated value b, the corresonding x coordinate of generated point r and the signed document z and our secret key x. 

# the signature is composed of  s and r_x

# NOTE: 
# private_key                        x      private 
# random_target                  b      private 
# generator_point                g      public
# public_key                         y       public 
# x_coord_random_point   r_x    public
# signature_value                s       public
# hashed_document           z       public 

# we DO NOT reveal b because:
# s = (x * r_x + z ) * b^(-1) rearranged leads to
# x = ( s * b - z ) * r_x^(-1) 

# i.e revealing b allows for the computing of x, our secret/private key. 

# Verification process
# given (r_x, s) as signature, z hashed document to be signed and y public key of signer 
# 1) calculate 
# u = z * s^(-1)
# v = r_x * s^(-1)
# 2) calculate 
# u * g + v * y = r
# 3) if r_x (x coord of r ) matches given in  (r_x, s) signature is valid 


class Signature:
	def __init__(self, r_x, value, display=False):
		self.r_x = r_x
		self.value = value
		self.display= display
	def __repr__(self):
		return f'Signature({self.r_x},{self.value})'


	def __format__(self, x):
		return f'Signature({self.r_x:x},{self.value:x})'
		 
		
	def der(self):
		if not self.display:
			rxbin = self.r_x.to_bytes(32, 'big')
			# removing all null bytes
			rxbin = rxbin.lstrip(b"\x00")
			# if rxbin has high bit add \x00
			if rxbin[0] & 0x80:
				rxbin = b'\00' + rxbin
			result = bytes([2, len(rxbin)]) + rxbin
			sigbin = self.value.to_bytes(32, 'big')
			sigbin = sigbin.lstrip(b"\x00")
			if sigbin[0] & 0x80:
				sigbin = b'\x00' + sigbin
			result += bytes([2, len(sigbin)]) + sigbin

			return bytes([0x30, len(result)]) + result 
		else:
			rxbin = self.r_x.to_bytes(32, 'big')
			# removing all null bytes
			rxbin = rxbin.lstrip(b"\x00")
			# if rxbin has high bit add \x00
			if rxbin[0] & 0x80:
				rxbin = b'\00' + rxbin
			


			r_x_value = lp + f"{hex(int.from_bytes(rxbin, 'big'))}".lstrip("0x") + r 
			r_x_length =  lc  + f"{hex(len(rxbin))}".lstrip('0x') + r 
			r_prefxbyte = re + f"{hex(2)}".lstrip('0x') + r
			 
			result = bytes([2, len(rxbin)]) + rxbin

			sigbin = self.value.to_bytes(32, 'big')
			sigbin = sigbin.lstrip(b"\x00")
			if sigbin[0] & 0x80:
				sigbin = b'\x00' + sigbin
			result += bytes([2, len(sigbin)]) + sigbin
			

			sig_value =  y + f"{hex(int.from_bytes(sigbin, 'big'))}".lstrip("0x") + r
			sig_length = gr  + f"{hex(len(sigbin))}".lstrip('0x') + r
			sig_prefxbyte =  bb + f"{hex(2)}".lstrip('0x') + r
			
			prefix = g + f"{hex(0x30)}".lstrip("0x") + r + w + f"{hex(len(result))}".lstrip("0x") + r

			print()
			print("Distinguished encoding representation for signatures in hex base")
			print()
			print(prefix + r_prefxbyte +r_x_length + r_x_value  + sig_prefxbyte + sig_length+ sig_value )
			print("key:")
			print(g + "Signature prefix "+ r )
			print(w+ "Length of complete signature" + r)
			print(y + "signature value " + r )
			print(gr + "signature length " + r )
			print(bb + "signature prefix " + r )
			
			print(lc + "r_x length " + r )
			print(lp + "r_x value " + r )
			print(re + "r_x prefix " + r )
			print()


			







g='\033[0;32m'
lp='\033[1;35m'
lc='\033[1;36m'
y='\033[1;33m'
r='\033[0m'
bb='\033[1;94m'
gr='\033[1;90m'
bc='\033[1;96m'
re='\033[1;31m'
rb='\033[1;91m'
w='\033[1;97m'