import os
from Cryptodome.PublicKey import RSA
from cryptography.fernet import Fernet

private_key = RSA.generate(4096)
public_key = private_key.publickey()
f = open('Keys/bad_private.pem', 'wb')
f.write(private_key.exportKey('PEM'))
f.close()
f = open('Keys/bad_public.pem', 'wb')
f.write(public_key.exportKey('PEM'))
f.close()

with open('Keys/bad_filekey.key', 'wb') as filekey:
    filekey.write(os.urandom(32))

'''
key = Fernet.generate_key()

# string the key in a file
with open('Keys/filekey.key', 'wb') as filekey:
    filekey.write(key)
    '''