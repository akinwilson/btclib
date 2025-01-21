from btclib.ec import S256Point, Signature, SecretKey
from btclib.utils import hash256
from btclib.constants import EC_ORDER, Gx, Gy
import pytest




def test_known_valid_signatue():
    # x and y coords of public point 
    x = 0x887387E452B8EACC4ACFDE10D9AAF7F6D9A0F975AABB10D006E4DA568744D06C
    y = 0x61DE6D95231CD89026E286DF3B6AE4A894A3378E393E93A0F45B666329A0AE34
    # hash of document signed 
    hashed_document = 0xEC208BAA0FC1C19F708A9CA96FDEFF3AC3F230BB4A7BA4AEDE4942AD003C0F60
    # x coord of random public point
    r_x = 0xAC8D1C87E51D0D441BE8B3DD5B05C8795B48875DFFE00B7FFCFAC23010D3A395
    # signature value 
    sig_value = 0x68342CEFF8935EDEDD102DD876FFD6BA72D6A427A3EDB13D26EB0781CB423C4

    sig = Signature(r_x, sig_value)
    public_key = S256Point(x, y)

    assert public_key.verify(hashed_document, sig), f"\n\nSignature value\n{sig}\nand x coordinate of randomly chosen point\n{r_x:x}\ndo not correspond to the signature required for hashed document\n{hashed_document:x}.\n\nThe signature is known to verify the signing of the hashed document\n"





test_params = [(b"rust is an amazing language", b"transfer 10 dollars to xi jinping", 24544566675677, True),
               (b"normally mnemonics are generated for you. you dont choose them", b"any message could be document.", 121212767577775, True),
                (b"sie konnten auch auf Deutsche schreiben", b"transformer models", 75, True) ]

@pytest.mark.parametrize("secret_mnemonic,document,random_k,expect", test_params)
def test_generating_signatures(secret_mnemonic, document, random_k, expect):
    '''
    generating sigs and verifying range of secrect mnemonics documents and random ks
    '''
    secret_key = int.from_bytes(hash256(secret_mnemonic), "big")
    hashed_document = int.from_bytes(hash256(document), "big")
    
    # random k <--- remember choosing this k, and not reusing an old one, is critial. You will expose your private key if you reuse 
    # the same k 
    secret_key = SecretKey(secret_key)
    r_x = (random_k * S256Point(Gx, Gy)).x.element
    k_inv = pow(random_k, EC_ORDER - 2, EC_ORDER)
    signature_value = (hashed_document + r_x * secret_key.sk) * k_inv % EC_ORDER
    # s256 curve generator point corresponding to bitcoin curve multipled by secret key gives public point 
    public_key = secret_key.sk * S256Point(Gx, Gy)
    assert public_key.verify(hashed_document, Signature(r_x, signature_value)) == expect

