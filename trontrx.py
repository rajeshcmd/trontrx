from mnemonic import Mnemonic
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from bip32utils import BIP32Key, BIP32_HARDEN
import hashlib
import hmac
import binascii

# Function to generate private key from mnemonic
def generate_private_key(mnemonic_phrase: str, passphrase: str = ""):
    seed = Mnemonic.to_seed(mnemonic_phrase, passphrase)
    master_key = BIP32Key.fromEntropy(seed)
    
    # Following SLIP-0044 standard for TRON (coin type 195)
    purpose = master_key.ChildKey(44 + BIP32_HARDEN)
    coin_type = purpose.ChildKey(195 + BIP32_HARDEN)
    account = coin_type.ChildKey(0 + BIP32_HARDEN)
    change = account.ChildKey(0)
    address_index = change.ChildKey(0)
    
    return PrivateKey(address_index.PrivateKey())

# Function to get TRON address from private key
def get_tron_address(private_key: PrivateKey):
    return private_key.public_key.to_base58check_address()

# Function to check TRON wallet balance
def check_balance(address: str, api_key: str):
    client = Tron(provider=HTTPProvider(api_key=api_key))
    balance = client.get_account_balance(address)
    return balance

if __name__ == "__main__":
    #OKX Wallet Seed
    mnemonic_phrase = "tissue polar basket gold fly spirit close weasel coffee gesture myself light"
    trongrid_api_key = "9335bd23-e6c7-4f54-9e29-5071faa5c0e1"
    
    private_key = generate_private_key(mnemonic_phrase)
    tron_address = get_tron_address(private_key)
    balance = check_balance(tron_address, trongrid_api_key)
    
    print(f"TRON Address: {tron_address}")
    print(f"Balance: {balance} TRX")
