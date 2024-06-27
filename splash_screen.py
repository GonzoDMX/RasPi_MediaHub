import pygame
import logging

# Constants
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def display_splash_screen(screen, splash_image):
    try:
        if splash_image:
            screen.blit(splash_image, (0, 0))
        else:
            screen.fill((0, 0, 0))
        pygame.display.flip()
    except Exception as e:
        logger.error(f"Error displaying splash screen: {e}")

def fade_to_black(duration=1.0):
    try:
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))
        screen = pygame.display.get_surface()
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(int(duration * 10))
    except Exception as e:
        logger.error(f"Error during fade to black: {e}")

