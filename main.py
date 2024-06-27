import os
import sys
import pygame
from pygame.locals import *
from splash_screen import display_splash_screen, fade_to_black
from media_handler import play_media, stop_media_playback
from server import start_server_thread
from utils import get_splash_image_path
from queue import Queue, Empty

# Initialize pygame
pygame.init()

# Constants
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Media Player")

# Load splash screen image
splash_path = get_splash_image_path('splash')
splash_image = None
if splash_path:
    splash_image = pygame.image.load(splash_path)
    splash_image = pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a queue to communicate with the main loop
command_queue = Queue()

if __name__ == "__main__":
    # Start the server in a separate thread and pass the queue
    start_server_thread(command_queue)

    # Display the splash screen initially
    display_splash_screen(screen, splash_image)

    current_state = 'splash'
    media_directory = None

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Process commands from the queue
        try:
            command = command_queue.get_nowait()
            state = command.get('state')
            obj = command.get('object')

            if state == 'true':
                if current_state != 'playing':
                    fade_to_black()
                    media_directory = os.path.join('media', obj)
                    if os.path.isdir(media_directory):
                        current_state = 'playing'
            elif state == 'false':
                if current_state == 'playing':
                    stop_media_playback()
                    fade_to_black()
                    display_splash_screen(screen, splash_image)
                    current_state = 'splash'
        except Empty:
            pass

        if current_state == 'playing' and media_directory:
            play_media(media_directory)

        pygame.time.wait(100)  # Adjust the wait time as needed
