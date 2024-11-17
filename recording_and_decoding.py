import requests
import sounddevice as sd
from scipy.io.wavfile import write
# import wavio as wv
import pickle
# import numpy as np

# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP

from cryptography.fernet import Fernet

import AES

from scipy.io.wavfile import read
import numpy

def record_and_encrypt():
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
    # wv.write("recording1.wav", recording, freq, sampwidth=2)

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open('recording0.wav', 'rb') as file:
        original = file.read()

    # encrypting the file
    #encrypted = fernet.encrypt(original)

    encrypted = AES.encrypt('recording0.wav')

    return encrypted



def decrypt_and_save(encrypted):

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    with open('encrypted.wav', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    fernet = Fernet(key)
    # opening the encrypted file
    with open('encrypted.wav', 'rb') as enc_file:
        encrypted = enc_file.read()
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    with open('server_recording1.wav', 'wb') as dec_file:
        dec_file.write(decrypted)


def snr_calc():
    a = read("from_client_original.wav")
    b = read("from_client_aftermath.wav")
    before_transmit = numpy.mean( numpy.array(a[1], dtype=float) + numpy.array(a[0], dtype=float) )
    after_transmit =  numpy.mean( numpy.array(b[1], dtype=float) + numpy.array(b[0], dtype=float)  )
    #before_transmit = numpy.mean(a, axis=1) #numpy.array(a[1], dtype=float) #
    #after_transmit = numpy.mean(b, axis=1) #numpy.array(b[1], dtype=float)

    #min_len = min(len(before_transmit), len(after_transmit))
    #before_transmit = before_transmit[:min_len]
    #after_transmit = after_transmit[:min_len]

    noise = before_transmit - after_transmit

    signal_power = numpy.mean(before_transmit ** 2)
    noise_power = numpy.mean(noise ** 2)

    if noise_power == 0:
        noise_power = 0.0001

    snr = 10 * numpy.log10(signal_power / noise_power)

    print("Signal Power:", signal_power)
    print("Noise Power:", noise_power)
    print("SNR from client to server: ", snr)

snr_calc()