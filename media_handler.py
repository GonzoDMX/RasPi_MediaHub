import os
import time
import pygame
import cv2
import logging
from pygame.locals import *

# Constants
from config import SCREEN_WIDTH, SCREEN_HEIGHT, IMAGE_DISPLAY_TIME

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def play_image(image_path):
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen = pygame.display.get_surface()
        screen.blit(image, (0, 0))
        pygame.display.flip()
        time.sleep(IMAGE_DISPLAY_TIME)
    except Exception as e:
        logger.error(f"Error playing image {image_path}: {e}")

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    screen = pygame.display.get_surface()
    try:
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
    except Exception as e:
        logger.error(f"Error playing video {video_path}: {e}")
    finally:
        cap.release()

def play_media(directory):
    try:
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
    except Exception as e:
        logger.error(f"Error playing media in directory {directory}: {e}")

