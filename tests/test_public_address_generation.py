import pytest 
from btclib.ec import  SecretKey

testcases = [(5002,'mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA', True, False),
             (2020**5, 'mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH', True, True),
             (0x12345deadbeef,'1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1', False, True )]

@pytest.mark.parametrize('secret_key, address, net, compressed', testcases)
def test_public_address_generation(secret_key,address, net, compressed):
    addr = SecretKey(secret_key).pk.address(compressed=compressed,testnet=net)
    assert addr == address 

