'''

Coding operations codes; opcodes, and operations.

let x = [1,2,3,5,6] be considered a stack then 

the TOP of the stack is the right-hand-side, the last, element in the list 6
and BOTTOM of the stack is the left-most-side, the first, element in the list 1

'''
from .utils import hash256, hash160

def op_dup(s):
    '''
    duplicate last element on stack 
    '''
    if len(s) < 1:
        return False 
    s.append(s[-1])
    return True 


def op_hash256(s):
    '''
    generates hash256 on element
    '''
    if len(s) < 1:
        return False 
    el = s.pop() # last element in list 
    s.append(hash256(el))
    return True 
    
def op_hash160(s):
    if  len(s) < 1:
        return False 
    el = s.pop()
    s.append(hash160(el))





# of byte beweem 0x01 and 75 - a value of n say -  we consider the next n bytes as elements 
# and not functions 
OP_CODES_FUNCS = {
        0x00: op_0,
        0x51: op_1,
        0x60: op_16,
        0x76: op_dup,
        0x93: op_add, 
        170: op_hash256,
        0xa9: op_hash160,
        0xac: op_checksig, 
        }



