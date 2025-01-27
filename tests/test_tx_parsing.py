from btclib.transaction import Tx
from io import BytesIO
from helpers import TxParseVerification



GREEN='\033[0;32m'
RESET='\033[0m'

raw_tx = (
 '0100000001813f79011acb80925dfe69b3def355fe914bd1d9'
 '6a3f5f71bf8303c6a989c7d1000000006b483045022100ed'
 '81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf213'
 '20b0277457c98f02207a986d955c6e0cb35d446a89d3f5610'
 '0f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3'
 '624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b27'
 '8afeffffff02a135ef01000000001976a914bc3b654dca7e56b'
 '04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141'
 'c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')

# testing via
# https://www.blockchain.com/explorer/assets/btc/decode-transaction
# with selenium if available
url = 'https://www.blockchain.com/explorer/assets/btc/decode-transaction'
NETWORK_CONNECTED = False 
try: 
    result = TxParseVerification(raw_tx, url)()
    NETWORK_CONNECTED =True 
    print("\n\nUsing network connectivity to verify parsing TXs works as expected\n\n")
    print(f"Using {GREEN + url + RESET} with selenium to acquire tx information\n\n")

except: 
    pass 



def test_parsing_version_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(raw_tx))
    tx =  Tx.parse(s)
    assert tx.version == result['version'] if NETWORK_CONNECTED else  1 


def test_parsing_number_of_inputs_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(raw_tx))
    tx =  Tx.parse(s)
    assert tx.tx_ins.__len__() == result['ins'].__len__() if NETWORK_CONNECTED else 1 


def test_parsing_previous_index_from_transaction_hex_dump():
    s = BytesIO(bytes.fromhex(raw_tx))
    tx =  Tx.parse(s)   
    assert tx.tx_ins[0].prev_index == 0 

def test_parsing_outputs_of_transaction():
    s = BytesIO(bytes.fromhex(raw_tx))
    tx =  Tx.parse(s)
    assert tx.tx_outs.__len__() == result['outs'].__len__() if NETWORK_CONNECTED else 2 
    expect = 32454049
    assert tx.tx_outs[0].amount == result['outs'][0]['value'] if NETWORK_CONNECTED else expect 
    expect = 10011545
    assert tx.tx_outs[1].amount == result['outs'][1]['value'] if NETWORK_CONNECTED else expect
    
    ## inside of Script.serialize(), we preprend the length of the pubkey script to the serialisation of it
    # the problem is, this a a Varint, hence, to parameterised this, we need to know the length of the pubkey script for every output tx 
    assert tx.tx_outs[1].script_pubkey.serialize().hex()[2:] == result['outs'][1]['script']['hex'] if NETWORK_CONNECTED else '76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac', f"{tx.tx_outs[1].script_pubkey.serialize().hex()} versus 76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac"
    assert tx.tx_outs[0].script_pubkey.serialize().hex()[2:] == result['outs'][0]['script']['hex'] if NETWORK_CONNECTED else '76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac', f"{tx.tx_outs[0].script_pubkey.serialize().hex()} versus 76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac"
 