from btclib.utils import Base58
import pytest

testcases = [('7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d','7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'), 
    ('eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c','eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c'),
    ('c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6','c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6')]

@pytest.mark.parametrize("base16, reconstructed_base16", testcases)
def test_base58_encoding_and_decoding(base16, reconstructed_base16):
    x = bytes.fromhex(base16)
    b58 = Base58.encode(x)
    rb16 = Base58.decode(b58)
    assert rb16 == reconstructed_base16, "Encoding and decoding from base 16 and base 58 failed"
