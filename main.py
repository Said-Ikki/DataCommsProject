import requests
import os

import AES

# record and save sound file
AES.record('sound1.wav')

# generate random 32 byte key and save it to file
with open('filekey.key', 'wb') as filekey:
    filekey.write(os.urandom(32))

# open sound file and encrypt it using AES
with open('sound1.wav', 'rb') as file:
    encrypted = AES.encrypt(file.read())

response = requests.post(url="http://127.0.0.1:2000/", data=encrypted)

# decrypt the response from the server
d = AES.decrypt(response.content)

with open('server_recording22.mp3', 'wb') as dec_file:
    dec_file.write(d)
