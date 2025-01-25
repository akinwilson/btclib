import pytest 
from btclib.ec import S256Point
from btclib.ecds import Signature
from btclib.constants import Gx,Gy
# public point:
# uncompressed format
# ---> prefix \x04
# ---> x coord 32 bytes big-endian order
# ---> y coord 32 bytes as big-endian order


test_cases = [(True, 33),(False, 65)]
@pytest.mark.parametrize('compressed,sec_length', test_cases)
def test_standards_for_efficient_cryptography_public_key_serialisation( compressed, sec_length):
    sk = int.from_bytes(b"seed phrased wallet", "big") 
    pk = sk * S256Point(Gx,Gy)
    assert pk.sec(compressed=compressed).__len__() == sec_length



# Distinguished encoding rules; DER 
# signature encoding scheme 
# start prefix byte 0x30
# encoding length of rest of signature; usual 0x44 or 0x45 
# append market 0x02
# encode x coordinate of random public point used to create signature validity, r_x, as big-endian BUT if the first byte is > 0x80 prepend 0x00 prepend the resulting length of r_x
# append bytw 0x02 
# Encode signature value s as big-endian BUT prepend with 0x00 if the first byte > 0x80 preprend the resulting length to s 




# if __name__ == "__main__":
#     print(pk.sec(compressed=True).__len__())

#     print(pk.sec(compressed=False).__len__())

    # pk.sec(compressed=False, display=True)



