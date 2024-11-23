from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import pyautogui
import AES
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

        # get sent data
        encrypted = request.data

        # decrypt the data
        decrypted = AES.decrypt(encrypted)

        # save the decrypted data to a file
        with open('from_client_aftermath_compressed.wav', 'wb') as dec_file:
            dec_file.write(decrypted)

        recording_and_decoding.decompress('from_client_aftermath_compressed.wav','from_client_aftermath_decompressed.wav' )

        pygame.mixer.init()
        pygame.mixer.music.load("from_client_aftermath_decompressed.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.quit()

    isReply = pyautogui.confirm('Would you like to send a message back?',
                                            buttons=["Yes", "No"])

    if isReply == "Yes":
        AES.record('from_server_original.wav')
        recording_and_decoding.compress('from_server_original.wav', 'from_server_original_compressed.wav')
        # open sound file and encrypt it using AES
        with open('from_server_original_compressed.wav', 'rb') as file:
            encrypted = AES.encrypt(file.read())

        return encrypted
        pass
    else:
        return request.data


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=2000, allow_unsafe_werkzeug=True)