import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import numpy as np
from scipy.io import wavfile
import scipy.signal as sps


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
    freq = 44100 # hi quality
    #freq = 1638
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


def quantize(name):
    # Your new sampling rate
    new_rate = 8000

    # Read file
    sampling_rate, data = wavfile.read(name)

    # Resample data
    number_of_samples = round(len(data) * float(new_rate) / sampling_rate)
    data = sps.resample(data, number_of_samples)
    sf.write('quantized_sound.wav', data, new_rate)


def snr_calc(n1,n2):
    import numpy as np
    import soundfile as sf

    # Load original and quantized audiothe
    original_audio, sample_rate = sf.read(n1)
    quantized_audio, _ = sf.read(n2)

    # Ensure both audio arrays are the same size
    min_length = min(len(original_audio), len(quantized_audio))
    original_audio = original_audio[:min_length]
    quantized_audio = quantized_audio[:min_length]

    # Recheck normalization in case there's any mismatch
    max_amplitude_original = np.max(np.abs(original_audio))
    max_amplitude_quantized = np.max(np.abs(quantized_audio))

    # Ensure both signals are normalized the same way
    original_audio = original_audio / max_amplitude_original
    quantized_audio = quantized_audio / max_amplitude_quantized

    # Calculate signal power (mean squared value of the original signal)
    P_signal = np.mean(original_audio ** 2)

    # Calculate noise power (mean squared value of the difference between original and quantized signals)
    noise = original_audio - quantized_audio
    P_noise = np.mean(noise ** 2)

    # Calculate SNR
    if P_noise == 0:
        print("No noise detected; the SNR is infinite.")
    else:
        snr = 10 * np.log10(P_signal / P_noise)
        print(f"SNR of the quantized audio: {snr:.2f} dB")
        print(f"Signal Power: {P_signal}")
        print(f"Noise Power: {P_noise}")
