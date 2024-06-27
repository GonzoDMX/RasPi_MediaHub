import os
from flask import Flask, request
from threading import Thread
from splash_screen import display_splash_screen, fade_to_black
from media_handler import play_media
import pygame

app = Flask(__name__)

@app.route('/mediahub', methods=['GET'])
def handle_media_request():
    state = request.args.get('state')
    obj = request.args.get('object')

    print(f"STATE: {state}")
    print(f"OBJ: {obj}")

    if obj is None:
        return '', 404

    if state == 'true':
        media_directory = os.path.join('media', obj)
        if os.path.isdir(media_directory):
            fade_to_black()
            play_media(media_directory)
            fade_to_black()
            screen = pygame.display.get_surface()
            display_splash_screen(screen, splash_image)
    elif state == 'false':
        fade_to_black()
        screen = pygame.display.get_surface()
        display_splash_screen(screen, splash_image)
    return '', 200

def run_server():
    app.run(host='0.0.0.0', port=5000)

def start_server_thread():
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

