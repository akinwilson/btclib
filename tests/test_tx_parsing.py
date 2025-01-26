from btclib.transaction import Tx
from io import BytesIO

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

