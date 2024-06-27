import os
import sys
import pygame
from pygame.locals import *
from splash_screen import display_splash_screen, fade_to_black
from media_handler import play_media
from server import run_server, start_server_thread
from utils import get_splash_image_path

# Initialize pygame
pygame.init()


# Constants
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Media Player")

# Load splash screen image
splash_path = get_splash_image_path('splash')
splash_image = None
if splash_path:
    splash_image = pygame.image.load(splash_path)
    splash_image = pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

if __name__ == "__main__":
    # Start the server in a separate thread
    start_server_thread()

    # Display the splash screen initially
    display_splash_screen(screen, splash_image)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

