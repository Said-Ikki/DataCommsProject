from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from cryptography.fernet import Fernet
'''
private_key = RSA.generate(4096)
public_key = private_key.publickey()
f = open('privatekey.pem', 'wb')
f.write(private_key.exportKey('PEM'))
f.close()
f = open('publickey.pem', 'wb')
f.write(public_key.exportKey('PEM'))
f.close()
'''

key = Fernet.generate_key()

# string the key in a file
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)