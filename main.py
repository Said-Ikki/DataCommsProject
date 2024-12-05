import os

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA384
import requests
import random

import AES

# import keys
private_key = RSA.importKey(open('Keys/private_key_client.pem').read())
public_key = RSA.importKey(open('Keys/public_key_client.pem').read())

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
code = str(random.randint(1, 100))
yours_mael = {
    "admin": "val_yourself",
    "code": code
}

hash = SHA384.new(data=code.encode())
signature = requests.post(ip, json=yours_mael).content
try:
    isSigned = pkcs1_15.new(server_key).verify(hash, signature)
    print(isSigned)
    print("server authed")
except:
    print("invalid signature")

# start communication with server

# record and save sound file
AES.record('Audio/from_client_original_uncompressed.wav')

# generate random 32 byte key and save it to file
# with open('Keys/filekey.key', 'wb') as filekey:
#    filekey.write(os.urandom(32))

AES.compress('Audio/from_client_original_uncompressed.wav', 'Audio/from_client_original_compressed.wav')

# open sound file and encrypt it using AES
with open('Audio/from_client_original_compressed.wav', 'rb') as file:
    encrypted = AES.encrypt(file.read())

response = requests.post(url="http://127.0.0.1:2000/", data=encrypted)

# decrypt the response from the server
d = AES.decrypt(response.content)

with open('Audio/from_server_aftermath.mp3', 'wb') as dec_file:
    dec_file.write(d)

AES.decompress('Audio/from_server_aftermath.mp3', 'Audio/from_server_aftermath_uncompressed.mp3')
