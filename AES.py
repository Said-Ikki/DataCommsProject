import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64
import sounddevice as sd
from scipy.io.wavfile import write


# AES encryption and decryption functions
def encrypt(data):
    with open('filekey.key', 'rb') as filekey:
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
    with open('filekey.key', 'rb') as filekey:
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
    freq = 44100
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
