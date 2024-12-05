import os

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA384
import requests
import random

import AES


# import keys
# wrong client keys means the server will know not to trust this imposter
# it also makes it impossible for a MITM to send messages pretending to be the client
private_key = RSA.importKey(open('Keys/bad_private.pem').read())
public_key = RSA.importKey(open('Keys/bad_public.pem').read())

server_key = RSA.importKey(open('Keys/public_key_validate.pem').read())

# generate signature
recieved_message = 'validate'

signer = pkcs1_15.new(private_key)
hash = SHA384.new(data=recieved_message.encode())
signature = signer.sign(hash)
print(signature)

new_hash = SHA384.new(data="grr".encode())
isSigned = pkcs1_15.new(public_key).verify(hash, signature)
print(isSigned)

# verify
ip = "http://127.0.0.1:2000/validate"
start_mael = {
    "admin": "val_start"
}

recieved_message = requests.post(ip, json=start_mael)

signer = pkcs1_15.new(private_key)
hash = SHA384.new(data=recieved_message.text.encode())
signature = signer.sign(hash)
print(signature)

validate_mael = {
    "admin": "val_verify",
    "signature": signature.hex(),
}

print(requests.post(ip, json=validate_mael).text)