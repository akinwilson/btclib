import pytest 
from btclib.transaction import Varint
from io import BytesIO



def test_decoding_varints():
    '''
    integer possible range: [0, 18446744073709551615]
       ''     ''      ''  : [0, 2**64-1]
    '''
    t = bytes.fromhex( 'FD10')  # 16
    s = BytesIO(t)
    assert Varint.decode(s) == 16 

    t = bytes.fromhex('FE2b020000') # 555
    s = BytesIO(t)
    assert Varint.decode(s) == 555

    t = bytes.fromhex('FFcb10c7bab88d0600') #  1844674407370955
    s = BytesIO(t)
    assert Varint.decode(s) == 1844674407370955


test_cases= [16,555,1844674407370955]
@pytest.mark.parametrize('ints', test_cases)
def test_encoding_variants(ints):
    assert Varint.decode(BytesIO(bytes.fromhex(Varint.encode(ints).hex()))) == ints


def test_too_large_int_encoding_with_varint():
    with pytest.raises(ValueError):
        i = 2**66
        Varint.encode(i)