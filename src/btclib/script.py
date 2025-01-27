'''

Coding operations codes; opcodes, and operations.

let x = [1,2,3,5,6] be considered a stack then 

the TOP of the stack is the right-hand-side, the last, element in the list 6
and BOTTOM of the stack is the left-most-side, the first, element in the list 1

'''
from .utils import hash256, hash160, Varint
class Script:

    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds
    

    
    def raw_serialize(self):
        # initialize what we'll send back
        result = b''
        # go through each cmd
        for cmd in self.cmds:
            # if the cmd is an integer, it's an opcode
            if type(cmd) == int:
                # turn the cmd into a single byte integer using int_to_little_endian
                result += cmd.to_bytes(1, 'little')
                # print(f"raw_serialize: {result}")
            else:
                # otherwise, this is an element
                # get the length in bytes
                length = len(cmd)
                # for large lengths, we have to use a pushdata opcode
                if length < 75:
                    # turn the length into a single byte integer
                    result += length.to_bytes(1, 'little')
                elif length > 75 and length < 0x100:
                    # 76 is pushdata1
                    result += int(76).to_bytes(1, 'little')
                    result += length.to_bytes(1, 'little')
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += int(77).to_bytes(1, 'little')
                    result += length.to_bytes(2, 'little')
                else:
                    raise ValueError('too long an cmd')
                result += cmd
        return result



    def serialize(self):
        # get the raw serialization (no prepended length)
        result = self.raw_serialize()
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return Varint.encode(total) + result
        return  result

    @classmethod
    def parse(cls, s):
        # get the length of the entire field
        length = Varint.decode(s)
        # print(f"length: {length}")
        # initialize the cmds array
        cmds = []
        # initialize the number of bytes we've read to 0
        count = 0
        # loop until we've read length bytes
        while count < length:
            # get the current byte
            current = s.read(1)
            # increment the bytes we've read
            count += 1
            # convert the current byte to an integer
            current_byte = current[0]
            # if the current byte is between 1 and 75 inclusive
            if current_byte >= 1 and current_byte <= 75:
                # we have an cmd set n to be the current byte
                n = current_byte
                # add the next n bytes as an cmd
                cmds.append(s.read(n))
                # increase the count by n
                count += n
            elif current_byte == 76:
                # op_pushdata1
                data_length = int.from_bytes(s.read(1), 'little')
                cmds.append(s.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                # op_pushdata2
                data_length = int.from_bytes(s.read(2), 'little')
                cmds.append(s.read(data_length))
                count += data_length + 2
            else:
                # we have an opcode. set the current byte to op_code
                op_code = current_byte
                # add the op_code to the list of cmds
                cmds.append(op_code)
        if count != length:
            raise SyntaxError('parsing script failed')
        return cls(cmds)



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



def op_0(s):
    pass 

def op_1(s):
    pass 

def op_16(s):
    pass 

def op_add(s):
    pass 

def op_checksig(s):
    pass 


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



