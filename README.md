# btclib
![Tests](https://github.com/akinwilson/btclib/actions/workflows/tests.yaml/badge.svg)

![]( img/cowrie.jpg )

## Overview 
Implementation of bitcoin library in python allowing for private and public key generation, transaction creation, signing, verification and broadcasting along with a wallet implementation. Project is accompanied with a CLI interface and desktop application. 

Wallets offered by companies like [coinbase](https://www.coinbase.com/en-gb) do not embrace the decentralisation principal that cryto-currencies and their underlying technologh promote since coinbase still act like a vanilla custodian bank; i.e they are in control of your funds. btclib promotes this principal of decentralisation by allow you to store the information which controls your coins (private or secret keys) locally on your desktop. 
 
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

And there will hopefully also be a desktop application to accompany this repositories for those that are not comfortable with either the CLI or `python`. 


## Running tests 
To run tests locally, install the developer requirements
```
pip install -r requirements.dev.txt
```
then, with
```
python -m pytest
```
you can run the tests locally.

## Further improvements 

As well as programmatically interacting with the wallet, it would be more user friendly and made accessible to a wider audience if a desktop application is developed to allow interfacing with the wallet through a graphical user interface. 