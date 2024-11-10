from cryptography.fernet import Fernet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import pyautogui

import recording_and_decoding

import pygame

print("Setting Up Web Server")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
chat_histories = {}

@app.route("/", methods=['GET', 'POST'])
def index():
    # return render_template("index.html")
    # return render_template("gpt-clone.html")
    isListen = pyautogui.confirm('Would you like to listen to the message?',
                                buttons=["Yes", "No"])
    if isListen == "Yes":
        encrypted = request.data
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

        pygame.mixer.init()
        pygame.mixer.music.load("server_recording1.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        pygame.quit()

    isReply = pyautogui.confirm('Would you like to send a message back?',
                                            buttons=["Yes", "No"])

    if isReply == "Yes":
        encrypted = recording_and_decoding.record_and_encrypt()
        return encrypted
        pass
    else:
        return request.data

    #return "hello world"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)