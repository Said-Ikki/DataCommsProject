from cryptography.fernet import Fernet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import pyautogui

import recording_and_decoding
import AES

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
        decrypted = AES.decrypt(encrypted)
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
        AES.record('server_recording.wav')

        # open sound file and encrypt it using AES
        with open('server_recording1.wav', 'rb') as file:
            encrypted = AES.encrypt(file.read())

        return encrypted
        pass
    else:
        return request.data


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)