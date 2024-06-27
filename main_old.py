import os
import glob
import sys
import time
import pygame
import cv2
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Adjust based on your screen resolution
BACKGROUND_COLOR = (0, 0, 0)
IMAGE_DISPLAY_TIME = 10  # seconds

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Media Player")

def get_splash_image_path(dir_name):
    splash_dir = os.path.join(os.path.dirname(__file__), dir_name)
    valid_image_extensions = ['.png', '.jpg', '.jpeg']
    
    # Create a list to store the image files
    image_files = []

    # Iterate through the files in the splash directory
    for file in glob.glob(os.path.join(splash_dir, '*')):
        if os.path.isfile(file):
            extension = os.path.splitext(file)[1].lower()
            if extension in valid_image_extensions:
                image_files.append(file)

    # If no valid image files are found, return None
    if not image_files:
        return None

    # Get the most recently added image file
    latest_image = max(image_files, key=os.path.getctime)

    return latest_image

def display_splash_screen(screen, splash_image):
    if splash_image:
        screen.blit(splash_image, (0, 0))
    else:
        screen.fill((0, 0, 0))
    pygame.display.flip()

def fade_to_black(duration=1.0):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(int(duration * 10))

def play_image(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    time.sleep(IMAGE_DISPLAY_TIME)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                cap.release()
                return
    cap.release()

def play_media(directory):
    files = sorted(os.listdir(directory))
    media_files = [os.path.join(directory, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi', '.mov'))]
    
    if len(media_files) == 1 and media_files[0].lower().endswith(('.png', '.jpg', '.jpeg')):
        play_image(media_files[0])
    else:
        while True:
            for media_file in media_files:
                if media_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    play_image(media_file)
                elif media_file.lower().endswith(('.mp4', '.avi', '.mov')):
                    play_video(media_file)

# Load splash screen image
splash_path = get_splash_image_path('splash')
splash_image = None
if splash_path:
    splash_image = pygame.image.load(splash_path)
    splash_image = pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    display_splash_screen(screen, splash_image)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    # Example: Hardcoded keyword detection
                    keyword = input("Enter keyword: ").strip()
                    if keyword == "end":
                        fade_to_black()
                        display_splash_screen()
                    else:
                        media_directory = os.path.join('media', keyword)
                        if os.path.isdir(media_directory):
                            fade_to_black()
                            play_media(media_directory)
                            fade_to_black()
                            display_splash_screen()

if __name__ == "__main__":
    main()

