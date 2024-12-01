import base64
import os
import sys
import zlib

import sounddevice as sd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from scipy.io.wavfile import write


# AES encryption and decryption functions
def encrypt(data):
    with open('Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_data = iv + cipher_text
    encoded_cipher_text = base64.b64encode(encrypted_data)

    return encoded_cipher_text


def decrypt(data):
    with open('Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    encrypted_data = base64.b64decode(data)

    iv = encrypted_data[:16]
    cipher_text = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data


def record(name):
    # Sampling frequency
    #freq = 44100 # hi quality
    #freq = 1638 $ hella bad
    freq = 4000
    # Recording duration
    duration = 5
    # Start recorder with the given values
    # of duration and sample frequency
    print("start talking!")
    recording = sd.rec(int(duration * freq),
                       samplerate=freq, channels=1)
    # Record audio for the given number of seconds
    sd.wait()
    print("OK, we're done!")

    # This will convert the NumPy array to an audio file
    write(name, freq, recording)


def compress(filename_in, filename_out):
    with open(filename_in, mode="rb") as fin, open(filename_out, mode="wb") as fout:
        data = fin.read()
        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        print(f"Original size: {sys.getsizeof(data)}")
        # Original size: 1000033
        print(f"Compressed size: {sys.getsizeof(compressed_data)}")
        # Compressed size: 1024

        fout.write(compressed_data)

def decompress(filename_in, filename_out):
    with open(filename_in, mode="rb") as fin, open(filename_out, mode="wb") as fout:
        data = fin.read()
        compressed_data = zlib.decompress(data)
        print(f"Compressed size: {sys.getsizeof(data)}")
        # Compressed size: 1024
        print(f"Decompressed size: {sys.getsizeof(compressed_data)}")
        # Decompressed size: 1000033
        fout.write(compressed_data)