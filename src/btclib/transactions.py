from btclib.utils import hash256
import requests
from io import BytesIO

# from .script import Script 
from typing import BinaryIO

class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return "https://testnet.programmingbitcoin.com"
        else:
            return "https://mainnet.programmingbitcoin.com"

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = f"{cls.get_url(testnet)}/tx/{tx_id}.hex"
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


class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ""
        for tx_in in self.tx_ins:
            txt_ins += tx_in.__repr__() + "\n"
        tx_outs = ""
        for tx_out in self.tx_outs:
            txt_outs += tx_out.__repr__() + "\n"
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
    def parse(cls, s:BinaryIO):
        version = s.read(4)
        int.from_bytes(version, 'little')
        pass


class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        
        
        # if script_sig is None:
        #     self.script_sig = Script()
        # else:
        #     self.script_sig = script_sig
        
        
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
        result = self.prev_tx[::-1]
        result += self.prev_index.to_bytes(4, "little")
        result += self.script_sig.serialize()
        result += self.sequence.to_bytes(4, "little")
        return result


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
