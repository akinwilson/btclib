# btclib 貝
![Tests](https://github.com/akinwilson/btclib/actions/workflows/tests.yaml/badge.svg)

<img src="img/cowrie.jpg" alt="They used to be used as currency" title="Throughout the majority of the world, cowry shells have historically been used as a form of currency. This has been discovered to be the case in locations such as West Africa, the Americas, Asia, Australia and other parts of the world. Their value historically in China were so continually important that many characters relating to money or trade today in Mandarin contain the character for cowry: 貝."/>

To learn more about humanity's use throughout history of [cowry currency](https://en.wikipedia.org/wiki/Shell_money) click the link. 


## Overview 
Implementation of bitcoin library in python allowing for private and public key generation, transaction creation, signing, verification and broadcasting along with a wallet implementation. Project is accompanied with a CLI interface and desktop application. 

Wallets offered by companies like [Coinbase](https://www.coinbase.com/en-gb), do not embrace the  advantages taht decentralisation offer and still act like a [custodian bank](https://en.wikipedia.org/wiki/Custodian_bank); they fundamentally have the ability to control your wealth. The underlying technology blackchain is meant to elementate the need for such custodian entites acting as *caretakers* of your wealth. `btclib` allows you to store the information which controls your wealth [^1] locally on your desktop, or possibly, on a removable storage device. 

[^1]: Your funds/wealth with BTC, the ability to transfer it partially or fully, is controlled via accesing objects called your [secret/private](https://en.wikipedia.org/wiki/Public-key_cryptography) and mathematically connected [public](https://en.wikipedia.org/wiki/Public-key_cryptography) key(s) in crpytographic terminology; specifically the [public-private](https://en.wikipedia.org/wiki/Public-key_cryptography) cryptography system, and an associated [digital signature algorithm](https://en.wikipedia.org/wiki/Digital_signature) that secures all of the bitcoin blockchain. With acccess to these paired keys, it allows one to generate the authorising digital signature to move (partially or all of) your funds to different addresses, and broadcast this transaction to the rest of the network. These new destination addresses, are themselves paired keys, but, you would not have access to them, hence be unable to control them.  Hence keeping these objects stored locally (your public and private keys), rather than with custondian banks or companies which behave alike, is likely an option you would prefer if you would like full control over your wealth, knowing exactly where the essence of your wealth, and control of it, is actually stored; locally on your chosen storage location; accessible and managable with this library `btclib`. 

For information on other organsiations that offer services like fiat-to-crypto-currency exchanging (a service you may believe only companies like Coinbase can offer) **but** that do not act as a custodian entity throughout the exchange process, I recommend reviewing [kycnot.me](https://kycnot.me/about) for alternative options. 

## Usage 
For programmatic use 
```python 
from btclib.wallet import Wallet 

# reload a wallet 
wallet = Wallet.from_path()
# generate a new wallet 
wallet = Wallet.new()
# update transcation information 
wallet.update()
# transfer funds 
wallet.send()
```
for use via the CLI 
```bash 
btclib --new-wallet 'cold wallet'
btclib --wallet 'cold wallet' --balance 
```

And there will hopefully also be a desktop application to accompany this application for those that are not comfortable with either the CLI or `python`. 


## Running tests 
To run tests locally, install the developer requirements
```
pip install -r requirements.dev.txt
```
then, with
```
python -m pytest
```
you can run the tests locally. For more information on how these tests are performed run the following command instead:
```
python -m pytest -s 
```


## Further improvements 

As well as programmatically interacting with the wallet, it would be more user friendly and made accessible to a wider audience if a desktop application is developed to allow interfacing with the wallet through a graphical user interface. 

## TODO 12/12/2024
- [ ] finish defining `OP_CODES` and associated function test the scripting language.
- [ ] create the networking infrastructure to be able to broadcast and receive across both the `testnet` and `mainnet`
- [ ] develop user-friendly UI for personal use as desktop stand alone application
- [ ] Develop production-environment with a more stable storage solution for secret and public keys when the application is used in a production-setting handling multitenancy wallet ; e.g. for a [quasi](https://en.wikipedia.org/wiki/Quasiparticle)-decentralised e-commerce store, where the store operator acts as the [escrow](https://en.wikipedia.org/wiki/Escrow) provider (as well as the marketplace provider), ensuring transactions align with involving party's expectations before finalising payments. For this, [sqlite](https://www.sqlite.org/), [MySQL](https://www.mysql.com/) and [Postgres](https://www.postgresql.org/) (will need to be integrate [sqlalchemy](https://www.sqlalchemy.org/)  to defined interfaces for the most popular database [dialects](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) ), along with providing an interface to use the wallet ontop of a local bitcoin node, to allow verification of transcations faster rather than relying on external service providers to update UTXO information when using the `btclib` in a production setting. 
