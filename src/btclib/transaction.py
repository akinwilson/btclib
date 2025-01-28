from btclib.utils import hash256
import requests
from io import BytesIO
import json 

from .script import Script 
from .utils import Varint
from typing import BinaryIO, List


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
            print(f"{response.text=}")
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError(f"Unexpected response: {response.text}")
            if raw[4] == 0:
                # print("Hit")
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = int.from_bytes(raw[-4:], "little")
            else:
                # print("Hit else")
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





class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF, testnet=False):
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
        tx = self.fetch_tx(self.prev_index, testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

    def serialize(self):
        '''
        result is a byte string 
        '''
        result = self.prev_tx[::-1]
        # self.prev_index is already bytes? why to bytes?
        result += self.prev_index.to_bytes(4, "little")
        result += self.script_sig.serialize()
        result += self.sequence.to_bytes(4, "little")
        return result

    @classmethod
    def parse(cls, s:BinaryIO):
        '''
        the stream has already had the:
         - verions: 4 bytes 
         - number of inputs: varint; {2|4|8} bytes
         consumed.  

         next, for the input object, we parse:
         - previous transaction hash: 32 bytes
         - previous transaction index: 4 bytes 

        '''
        prev_tx_hash = s.read(32)[::-1]
        
        # print('txin: prev_tx_hash', prev_tx_hash.hex())
        # prev_tx_hash = int.from_bytes(prev_tx_hash_bytes, 'little')
        prev_tx_idx = int.from_bytes(s.read(4), 'little')

        # print("txin: previous tx id :", prev_tx_idx)
        script_sig = Script.parse(s)
        sequence = int.from_bytes(s.read(4), 'little')
        return TxIn(prev_tx=prev_tx_hash, script_sig=script_sig, sequence=sequence, prev_index=prev_tx_idx)



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
        # print(f"txout: {amount=}")      
        # print(f"{amount=}")
        # script_pub_key_len = Varint.decode(s)
        # print(s.read(8).hex())

        script_pubkey = Script.parse(s)
        return TxOut(amount=amount, script_pubkey=script_pubkey)
  



class Tx:

    def __init__(self,locktime: int, version:int, tx_ins:List[TxIn]=[], tx_outs : List[TxOut]=[] , testnet: bool =False):
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
    

    def fee(self):
        fee = sum([tx_in.value(self.testnet) for tx_in in self.tx_ins]) - sum([tx_out.amount for tx_out in self.tx_outs])
        assert fee > 0, "The fee somehow came out as negative, i.e. fee={fee}"
        return fee 
    

    def id(self):
        return self.hash().hex()

    def hash(self):
        return hash256(self.serialize())[::-1]

    def serialize(self) -> bytes:
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

        v_bytes = s.read(4) # first 4 bytes are version bytes 
        version = int.from_bytes(v_bytes, 'little')
        # print(f"tx: {version=}")
        num_inputs = Varint.decode(s)
        # print("tx: num inputs", num_inputs)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s)) #  for _ in range(num_inputs)]

        # sequence = int.from_bytes(s.read(4), 'little')
        # print(f"{sequence=}") 
        # print('tx: supposed to be: ', 4294967295) # 

        # for i in range(len(inputs)):
        #     inputs[i].sequence = sequence

        num_outputs = Varint.decode(s)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(s)) #   for _ in range(num_outputs)]
        locktime = int.from_bytes(s.read(4), 'little')


        return Tx(version=version, tx_outs=outputs, locktime=locktime, tx_ins=inputs, testnet=testnet)
    

