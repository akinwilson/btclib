from btclib.utils import hash256
import requests
from io import BytesIO
import json 

from .script import Script 
from typing import BinaryIO

# script_hex = ('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c50'
#               '31ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3'
#               'f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e'
#         '3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
SCRIPT_HEX = ('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c50'
            '31ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3'
            'f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e'
            '3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')

class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return "https://blockstream.info/testnet/api/"
        else:
            return "https://blockstream.info/api/"

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = f"{cls.get_url(testnet)}/tx/{tx_id}/hex"
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError(f"Unexpected response: {response.text}")
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = int.from_bytes(raw[-4:], "little")
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError(
                    f"Received non-matching tx ids: {tx.id()} versus {tx_id}"
                )

            cls.cache[tx_id] = tx

        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
    
    @classmethod
    def load_cache(cls, filepath):
        with open(filepath, 'r') as f:
            disk_cache = json.loads(f.read())
        
        for k, raw_hex in disk_cache.items():
            raw = bytes.fromhex(raw_hex)
            if raw[0] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw))
                tx.locktime = int.from_bytes(raw[-4:], 'little')
            else:
                tx = Tx.parse(BinaryIO(raw))
    

    @classmethod
    def dump_cache(cls, filepath):
        with open(filepath, 'w') as f:
            dump = {k: tx.serialize().hex() for k,tx in cls.cache.items()}
            f.write(json.dumps(dump, sort_keys=True, indent=4))



class Tx:

    def __init__(self, version, tx_ins=[], tx_outs="", locktime: int =10, testnet: bool =False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ""
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + "\n"
        tx_outs = ""
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + "\n"
        return f"Tx: {self.id()}\nverison: {self.version}\ntx_ins:\n{tx_ins}tx_outs:\n{tx_outs}locktime: {self.locktime}"

    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    def serialize(self):
        result = self.version.to_bytes(4, "little")
        result += Varint.encode(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += Varint.encode(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += self.locktime.to_bytes(4, "little")
        return result

    @classmethod
    def parse(cls, s:BinaryIO, testnet : bool = False):
        v_bytes = s.read(4)
        version = int.from_bytes(v_bytes, 'little')
        print("verison: ", version)
        num_inputs = Varint.decode(s)
        print("num inputs", num_inputs)
        inputs =[TxIn.parse(s) for _ in range(num_inputs)]
        # when pass the stream into the above class, its 
        # is not reading move the pointer along.


        # this will be produced by the soon-to-be-defined Script class
        # until then, hard-coding its value
        #######################################################################
        matched = False
        test_hex = ''
        while not matched:
            test_hex += s.read(1).hex()
            if test_hex == SCRIPT_HEX:
                break 
        ##########################################################################

        # sequences = [int.from_bytes(s.read(4), 'little') for _ in range(num_inputs)]
        # print("After extracting TX in info, ")
        # print(f"Look for sequence: feffffff")
        # print("The next 27*4 bytes in hex are:",s.read(27*4).hex() )
        sequence = int.from_bytes(s.read(4), 'little') 
                 
        for i in range(len(inputs)):
            inputs[i].sequence = sequence


        # print(f"What are the next 4 bytes?",sequences )
        # print(inputs)


        num_outputs = Varint.decode(s)
        outputs = [TxOut.parse(s) for _ in range(num_outputs)]
        locktime = int.from_bytes(s.read(4), 'little')
        # print(f"locktime {locktime}")
        # for (tx_in, seq) in zip(inputs, sequences):
        #     tx_in.sequence = seq

        # inputs = [tx_in.sequence = seq for (tx_in, seq) in zip(inputs, sequences)]
        # TxOut.parse(s)
        # num_outputs = Varint.decode(s)
        # outputs = TxOut.parse(s)
        # tx_in  = TxIn.parse(s)
        # print(f'{version=}')
        # print(f'{num_inputs=}')
        # outputs = TxOut.parse(s)


        return Tx(version=version, tx_outs=outputs, locktime=locktime, tx_ins=inputs, testnet=testnet)
    



class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        
        
        self.sequence = sequence

    def __repr__(self):
        return f"{self.prev_tx.hex()}:{self.prev_index}"

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        tx = self.fetch_tx(self.prev_index)
        return tx.tx_outs[self.prev_index].script_pubkey

    def serialize(self):
        '''
        result is a byte string 
        '''
        result = self.prev_tx[::-1]

        # self.prev_index is already bytes? why to bytes?

        result += self.prev_index.to_bytes(4, "little")
        
        # result += self.script_sig.serialize()
        result += self.sequence.to_bytes(4, "little")
        return result

    @classmethod
    def parse(cls, s:BinaryIO):
        prev_tx_hash_bytes = s.read(32)[::-1]
        print('prev_tx_hash_bytes', prev_tx_hash_bytes.hex())
        # prev_tx_hash = int.from_bytes(prev_tx_hash_bytes, 'little')
        prev_tx_idx = int.from_bytes(s.read(4), 'little')

        print("previous tx id :", prev_tx_idx)
        
        # print("Byte stream left: ", len(s.read()))
        # script_sig = Script.parse(s)cr
        # prev_tx_idx = int.from_bytes(prev_tx_idx_bytes, 'little')
        return TxIn(prev_tx=prev_tx_hash_bytes, prev_index=prev_tx_idx)



class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return f"{self.amount}:{self.script_pubkey}"

    def serialize(self):

        result = self.amount.to_bytes(8, "little")
        result += self.script_pubkey.serialize()
        return result
    
    @classmethod
    def parse(cls, s:BinaryIO):
        # num_outputs = Varint.decode(s)
        # print(f"{num_outputs=}") #this is correct 
        # TxOut()
        # trying to extract he amount is near imposssible 
        # print("s.read(8) to little int", int.from_bytes(s.read(8), 'little'))
        amount = int.from_bytes(s.read(8), 'little')        
        # print(f"{amount=}")
        script_pub_key_len = Varint.decode(s)
        # print(s.read(8).hex())
        script_pub_key = s.read(script_pub_key_len).hex() # , 'little')
        # print(f"{script_pub_key_len=}")
        # print(f"{script_pub_key=}")
        # amount = int.from_bytes(s.read(8), 'little')
        return TxOut(amount=amount, script_pubkey=script_pub_key)
        # num_outputs = Varint.decode(s) # .read(4), 'little')
        # print(f"{num_outputs=}")
        # outputs = [TxOut.parse(s) for _ in range(num_outputs)]
        # print(f"{num_outputs=}")
        # print(f"{outputs=}")
        # return outputs



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
