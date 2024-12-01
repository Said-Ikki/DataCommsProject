
from flask_socketio import SocketIO
import pyautogui
import AES

from flask import Flask, request

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA384
import pygame
import random


# import keys
private_key = RSA.importKey(open('Keys/private_key_validate.pem').read())
public_key = RSA.importKey(open('Keys/public_key_validate.pem').read())

client_key = RSA.importKey(open('Keys/public_key_client.pem').read())

print("Setting Up Web Server")

app = Flask(__name__)
to_verify = []
valid_IPs = []
socketio = SocketIO(app, cors_allowed_origins="*")
chat_histories = {}


@app.route("/validate", methods=['GET', 'POST'])
def validate():
    data = request.json
    if data["admin"] == "val_start":
        print("starting validation")
        random_number = random.randint(1, 100)
        hash = SHA384.new(data=str(random_number).encode())
        to_verify.append(hash)
        return str(random_number)
    if data["admin"] == "val_verify":
        print("validating")
        signature = bytes.fromhex( data["signature"] )
        try:
            isSigned = pkcs1_15.new(client_key).verify(to_verify[0], signature)
            print(isSigned)
            to_verify.clear()
            valid_IPs.append(request.remote_addr)
            print("valid signature")
            return "validated"
        except ValueError:
            print("invalid signature")
            return "invalid signature"
    if data["admin"] == "val_yourself":
        print("validating myself")
        code = data["code"]
        signer = pkcs1_15.new(private_key)
        hash = SHA384.new(data=code.encode())
        signature = signer.sign(hash)
        print(signature)
        return signature
    pass


@app.route("/", methods=['GET', 'POST'])
def index():

    ip = request.remote_addr

    if ip not in valid_IPs:
        return "You are not authorized to access this server"

    # return render_template("index.html")
    # return render_template("gpt-clone.html")
    isListen = pyautogui.confirm('Would you like to listen to the message?',
                                buttons=["Yes", "No"])
    if isListen == "Yes":

        # get sent data
        encrypted = request.data

        # decrypt the data
        decrypted = AES.decrypt(encrypted)

        # save the decrypted data to a file
        with open('Audio/from_client_aftermath_compressed.wav', 'wb') as dec_file:
            dec_file.write(decrypted)

        AES.decompress('Audio/from_client_aftermath_compressed.wav','Audio/from_client_aftermath_decompressed.wav' )

        pygame.mixer.init()
        pygame.mixer.music.load("Audio/from_client_aftermath_decompressed.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.quit()

    isReply = pyautogui.confirm('Would you like to send a message back?',
                                            buttons=["Yes", "No"])

    if isReply == "Yes":
        AES.record('Audio/from_server_original.wav')
        AES.compress('Audio/from_server_original.wav', 'Audio/from_server_original_compressed.wav')
        # open sound file and encrypt it using AES
        with open('Audio/from_server_original_compressed.wav', 'rb') as file:
            encrypted = AES.encrypt(file.read())

        return encrypted
        pass
    else:
        return request.data


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)