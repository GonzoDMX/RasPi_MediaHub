import numpy as np

SCREEN_SIZE = (1920, 1080)      # Set target monitor resolution
FADE_TIME = 1                   # in seconds
BLACK_OUT = (0, 0, 0)
BLANK_SCREEN = np.full(
    (SCREEN_SIZE[1], SCREEN_SIZE[0], 3),
    BLACK_OUT, dtype=np.uint8
)
