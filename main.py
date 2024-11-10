import requests
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import pickle
import numpy as np

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from cryptography.fernet import Fernet

import recording_and_decoding

# Sampling frequency
freq = 44100
# Recording duration
duration = 5
# Start recorder with the given values
# of duration and sample frequency
print("start talking!")
recording = sd.rec(int(duration * freq),
                   samplerate=freq, channels=2)
# Record audio for the given number of seconds
sd.wait()
print("OK, we're done!")

# This will convert the NumPy array to an audio
# file with the given sampling frequency

# turn to bytes
x = recording
x_as_bytes = pickle.dumps(x)

# encryption
# this method apparently has file sizes too large
'''
public_key = RSA.importKey(open('publickey.pem').read())
cipher = PKCS1_OAEP.new(public_key)
enc_x_as_bytes = cipher.encrypt(x_as_bytes)

# decryption
private_key = RSA.importKey(open('privatekey.pem').read())
cipher = PKCS1_OAEP.new(private_key)
x_as_bytes = cipher.decrypt(enc_x_as_bytes)
'''

# turn back from bytes
y = pickle.loads(x_as_bytes)
write("recording0.wav", freq, y)

# Convert the NumPy array to audio file
#wv.write("recording1.wav", recording, freq, sampwidth=2)

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

# using the generated key
fernet = Fernet(key)

# opening the original file to encrypt
with open('recording0.wav', 'rb') as file:
    original = file.read()

# encrypting the file
encrypted = fernet.encrypt(original)

# opening the file in write mode and
# writing the encrypted data
with open('encrypted.wav', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

fernet = Fernet(key)

# opening the encrypted file
with open('encrypted.wav', 'rb') as enc_file:
    encrypted = enc_file.read()

# decrypting the file
decrypted = fernet.decrypt(encrypted)

# opening the file in write mode and
# writing the decrypted data
with open('recording1.wav', 'wb') as dec_file:
    dec_file.write(decrypted)

response = requests.post(url="http://192.168.250.68:2000/", data=encrypted)
#print()

recording_and_decoding.decrypt_and_save(response.content)