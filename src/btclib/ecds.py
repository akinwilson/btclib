# elliptic curve signature algorithm
import hashlib


# ansi escape codes ; https://en.wikipedia.org/wiki/ANSI_escape_code
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
# private_key                    x       private 
# random_target                  b       private 
# generator_point                g       public
# public_key                     y       public 
# x_coord_random_point           r_x     public
# signature_value                s       public
# hashed_document                z       public 

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
	def __init__(self, r_x, value):
		self.r_x = r_x
		self.value = value
	def __repr__(self):
		return f'Signature({self.r_x},{self.value})'


	def __format__(self, x):
		return f'Signature({self.r_x:x},{self.value:x})'
		 
		
	def der(self, display=False):
		if not display:
			rxbin = self.r_x.to_bytes(32, 'big')
			# removing all null bytes
			rxbin = rxbin.lstrip(b"\x00")
			# if rxbin has high bit add \x00
			if rxbin[0] & 0x80:
				rxbin = b'\x00' + rxbin
			result = bytes([2, len(rxbin)]) + rxbin
			
			sigbin = self.value.to_bytes(32, 'big')
			sigbin = sigbin.lstrip(b"\x00")
			if sigbin[0] & 0x80:
				sigbin = b'\x00' + sigbin
			result += bytes([2, len(sigbin)]) + sigbin
			return bytes([0x30, len(result)]) + result 

		else:
			rxbin = self.r_x.to_bytes(32, 'big') # 
			# removing all null bytes
			rxbin = rxbin.lstrip(b"\x00") # 
			# if rxbin has high bit add \x00
			prepend  = False
			if rxbin[0] & 0x80:
				prepend = True 
				rxbin = b'\x00' + rxbin

			if prepend:
				r_x_value = lp + '00' + f"{int.from_bytes(rxbin, 'big'):x}" + r
			else: 
				r_x_value = lp + f"{int.from_bytes(rxbin, 'big'):x}" + r

			print("r_x value (base 16)",  r_x_value)
			r_x_length =  lc  + f"{len(rxbin):x}" + r
			print("length of r_x (base 16): ", r_x_length)
			r_prefxbyte = re + "02" + r
			print("r_prefix byte (base 16) byte container", r_prefxbyte)
		 	
			r_x_part = r_prefxbyte + r_x_length + r_x_value
			print(f"r_x EXPECT:{r_x_part}\n\n")
			result = bytes([2, len(rxbin)]) + rxbin

			sigbin = self.value.to_bytes(32, 'big')
			# print("sigbin[0] before strip", sigbin[0])
			sigbin = sigbin.lstrip(b"\x00")
			# print("sigbin[0]", sigbin[0])
			prepend = False 
			if sigbin[0] & 0x80:
				prepend = True 
				sigbin = b'\x00' + sigbin	
			if prepend:
				sig_value =  y + '00' + f"{int.from_bytes(sigbin, 'big'):x}" + r
			else: 
				sig_value =  y +  f"{int.from_bytes(sigbin, 'big'):x}" + r
				
			sig_length = gr  +  f"{len(sigbin):x}" + r
			print("sig length (base 16):", sig_length)
			

			## manually prepending the 
	
			print("sig value (base 16): ", sig_value)
			sig_prefxbyte =  bb + '02' + r
			print("sig prefix byte (base 16) byte container:", sig_prefxbyte)
			sig_part = sig_prefxbyte + sig_length + sig_value
			print(f"sig EXPECT: ", sig_part )

			result += bytes([2, len(sigbin)]) + sigbin
			
			# print("int.from_bytes(sigbin, 'big'):x}.lstrip('0x')", f"{int.from_bytes(sigbin, 'big'):x}".lstrip("0x").zfill(64))
			# print("siglen",f"{int.from_bytes(sigbin, 'big'):x}".lstrip("0x").__len__())

			sig_value =  y + f"{int.from_bytes(sigbin, 'big'):x}".lstrip("0x") + r
			sig_length = gr  + f"{len(sigbin)}".lstrip('0x') + r
			sig_prefxbyte =  bb + '02' + r
			
			marker_byte =  g + '30' + r
			
			print("\n\nPrefix byte (base 16): ", marker_byte)
			total_serial_len = w + f"{len(result):x}" + r
			print("total sig length (base16): ", total_serial_len)

			print()
			print("Distinguished encoding representation for signatures in hex base. der signature serialization:")
			print()
			print(marker_byte + total_serial_len + r_x_part + sig_part)
			print()
			print("key:")
			print(g + "Signature prefix "+ r )
			print(w+ "Length of complete signature" + r)
			print(re + "r_x prefix " + r )
			print(lc + "r_x length " + r )
			print(lp + "r_x value " + r )
			print(bb + "signature prefix " + r )
			print(gr + "signature length " + r )
			print(y + "signature value " + r )
			print()
			return bytes([0x30, len(result)]) + result 

			






