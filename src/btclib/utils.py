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
