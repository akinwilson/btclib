import hashlib


def hash160(s):
    """sha256 followed by ripemd160"""
    return hashlib.new("ripemd160", hashlib.sha256(s).digest()).digest()


def hash256(s):
    """two rounds of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


class Base58:
    SYMBOLS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    ORDER = SYMBOLS.__len__()  # aka cardinality
    def encode(s: bytes):
        # Counting leading zeros 
        # 
        count = 0
        for c in s:
            if c == 0:
                count += 1
            else:
                break
        
        num = int.from_bytes(s, "big")
        # adding leading zeros in base58 representation (1s), back    
        prefix = Base58.SYMBOLS[0] * count
        result = ""
        while num > 0:
            num, mod = divmod(num, Base58.ORDER)
            result = Base58.SYMBOLS[mod] + result
        return prefix + result


    def decode(s):
        num = 0
        for c in s:
            num *= Base58.ORDER # increment the value each digit placeholder can hold
            num += Base58.SYMBOLS.index(c)
        # combined = num.to_bytes(25, byteorder="big")
        return f"{num:x}"
        # checksum = combined[-4:]
        # if hash256(combined[:-4])[:4] != checksum:
        #     raise ValueError(f"bad address: {checksum} {hash256(combined[:-4])[:4]}")
        # return combined[1:-4]


def encode_base58_checksum(b):
    return Base58.encode(b + hash256(b)[:4])



class Varint:
    '''
    For parsing the mount of inputs, where there may be more than 255 (a single byte) amount of inputs 
    if x < 253:
        encode as single byte 
        
    if 65535 > x >= 253:
        start with 253 byte [ fd ] then encode number in 2 bytes using little-endian 
        e.g 255 -> fd + int(255).to_bytes(2, 'little').hex() = fdxff00
        e.g 555 -> fd + int(555).to_bytes(2, 'little').hex() = fd2b02

    if 4294967295 > x >= 65535:
        start with 254 byte [ fe ] then encode the number in 4 bytes using little-endian 
        e.g. 70015 -> 0xfe + int(70015).to_bytes(4, 'little').hex() = fe7f110100

    if  18446744073709551615 > x >= 4294967295:
        strt with 255 byte [ ff ] then encode the number in 8 bytes using little-endian 
        e.g.  18005558675309 -> ff int(18005558675309).to_bytes(8, 'little').hex() = ff6dc7ed3e60100000
    '''
    def decode(s):
        i = s.read(1)[0]
        if i == 0xFD:
            return int.from_bytes(s.read(2), "little")
        elif i == 0xFE:
            return int.from_bytes(s.read(4), "little")
        elif i == 0xFF:
            return int.from_bytes(s.read(8), "little")
        else:
            return i


    def encode(i):
        if i < 0xFD:
            return bytes([i])
        elif i < 0x10000:
            return b"\xfd" + i.to_bytes(2, "little")
        elif i < 0x100000000:
            return b"\xfe" + i.to_bytes(4, "little")
        elif i < 0x10000000000000000:
            return b"\xff" + i.to_bytes(8, "little")
        else:
            raise ValueError(f"Integer {i} is too large")

