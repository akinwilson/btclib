from btclib.ec import S256Point, SecretKey
from btclib.ecds import Signature
from btclib.constants import Gx, Gy, SECP256K1_A,SECP256K1_B
from btclib.transaction import Tx
from io import BytesIO
import pytest 




tx_serialized = (
 '0100000001813f79011acb80925dfe69b3def355fe914bd1d9'
 '6a3f5f71bf8303c6a989c7d1000000006b483045022100ed'
 '81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf213'
 '20b0277457c98f02207a986d955c6e0cb35d446a89d3f5610'
 '0f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3'
 '624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b27'
 '8afeffffff02a135ef01000000001976a914bc3b654dca7e56b'
 '04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141'
 'c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')


def test_parsing_version_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(tx_serialized))
    tx =  Tx.parse(s)
    assert tx.version == 1 


def test_parsing_number_of_inputs_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(tx_serialized))
    tx =  Tx.parse(s)
    assert tx.tx_ins.__len__() == 1 


def test_parsing_previous_index_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(tx_serialized))
    tx =  Tx.parse(s)   
    assert tx.tx_ins[0].prev_index == 0 




test_cases = [(5003, True, True, 'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK'),
              (2021**5, False, True, '91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic'),
              (0x54321deadbeef, True, False, 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a')] 
@pytest.mark.parametrize("sk, compressed, testnet, expected", test_cases)
def test_wallet_import_format_serialization_wif(sk, compressed, testnet, expected):
    sk =  SecretKey(sk)
    wif = sk.wif(compressed, testnet)
    assert wif == expected




test_cases = [(True, 33),(False, 65)]
@pytest.mark.parametrize('compressed,sec_length', test_cases)
def test_standards_for_efficient_cryptography_public_key_serialisation_length( compressed, sec_length):
    sk = int.from_bytes(b"seed phrased wallet", "big") 
    pk = sk * S256Point(Gx,Gy)
    assert pk.sec(compressed=compressed).__len__() == sec_length



def test_compressed_public_point_serialization_for_even_y_coordinate():

    pk = 668868866 * S256Point(Gx, Gy, SECP256K1_A, SECP256K1_B) # even 
    b = pk.sec(display=True)
    assert b[0] == 2, "Expected prefix byte to be of value 2 for even y coordinate"
    assert int.from_bytes(b[1:], 'big') == int('644e7bcaf03fc16b300b5b1645e0fa73b7f5ac9fff270e0613999dbec305ac59',16)


def test_compressed_public_point_serialization_for_odd_y_coordinate():

    pk = 666* S256Point(Gx, Gy, SECP256K1_A, SECP256K1_B) # odd 
    b = pk.sec(display=True)
    assert b[0] == 3
    assert int.from_bytes(b[1:], 'big') == int('7f75c66c45a52c35ead5970bbfaafdfba626a6ddceabc14e0f8a8c7d88a5772b',16)


def test_uncompressed_public_point_serialzation():
    pk = 1066 * S256Point(Gx, Gy, SECP256K1_A, SECP256K1_B) # even 
    b = pk.sec(compressed=False, display=True)
    assert b[0] == 4
    xr = f"{int.from_bytes(b[1:33], 'big'):x}"
    yr = f"{int.from_bytes(b[33:], 'big'):x}"
    x =  '6fe50b285af96708ad084423dc791fe8c1e3a060437aada0f1eb001643215e80'
    y = '71769872680384f8b4f6d9191813857b01c3b5d671a7be8eaa65e919652f92ce'
    assert xr == x
    assert yr == y 


def test_signature_serialization_for_display_option():
    r_x = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
    s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

    # print(sys.getsizeof(Signature(r_x, s).der().hex()))
    x1 = Signature(r_x, s).der().hex()
    x2 = Signature(r_x, s).der(display=True).hex()
    assert x1 == x2


def test_signature_parsing():
    r_x = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
    s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

    # print(sys.getsizeof(Signature(r_x, s).der().hex()))
    x = Signature(r_x, s).der().hex()
    tot_sig_prefix = x[:2]
    assert tot_sig_prefix == '30'
    tot_len = x[2:4] 
    assert tot_len == '45'
    r_x_prefix = x[4:6]
    assert r_x_prefix == '02'

    #  NOTE 
    # Why to I have to multiple by 2 get the right answer? for the length?
    r_x_len16 = x[6:8] # base 16 
    r_x_len10 = int(r_x_len16,16) *2  # how chars, one char = 1 bytes in base 2 has len 8, in base 16, len 2. i.r two hex digit represent one byte 
    r_x_val = x[8:8+r_x_len10]

    assert r_x_val == '37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6' 

    sig_prefix = x[8+r_x_len10:8+r_x_len10 +2]
    assert sig_prefix == '02'

    sig_len16 = x[8+r_x_len10 +2:8+r_x_len10 +2 + 2]
    sig_len10 = int(sig_len16, 16) * 2

    sig_val = x[8+r_x_len10 +2 + 2 : 8+r_x_len10 +2 + 2 + sig_len10]
    assert sig_val == '008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec'
    
