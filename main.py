import os
import time
import cv2
import numpy as np
from queue import Queue, Empty
from media_player import MediaPlayer
from utility import get_splash_screen, get_video_path
from config import SCREEN_SIZE, BLANK_SCREEN
from server import start_server_thread

def main(player, queue):
    player.display_splash()
    while True:
        # Process commands from the queue
        try:
            command = command_queue.get_nowait()
            state = command.get('state')
            obj = command.get('object')

            if state == 'true':
                file_path = get_video_path(obj)
                if file_path is not None:
                    if player.is_playing():
                        player.stop_video_loop()
                    # Queue up the video
                    player.load_video(file_path)
                    player.start_video_loop()
            else:
                player.end_video_loop()
        except Empty:
            pass


if __name__ == '__main__':
    # Create a queue to communicate with the main loop
    command_queue = Queue()
    start_server_thread(command_queue)
    splash_screen = get_splash_screen()
    media_player = MediaPlayer(splash_screen)
    main(media_player, command_queue)
    media_player.close_player()
    cv2.destroyAllWindows()

