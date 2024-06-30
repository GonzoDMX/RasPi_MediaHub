import os
import cv2
import vlc
import time
import threading
import numpy as np
from utility import fit_aspect_ratio
from config import SCREEN_SIZE, FADE_TIME, BLACK_OUT, BLANK_SCREEN


class MediaPlayer:
    def __init__(self, splash_screen):
        self.splash = splash_screen
        # Initialize VLC instance
        self.instance = vlc.Instance([
            '--fullscreen',
            '--no-video-title-show',
            '--vout', 'gl',
        ])
        self.player = self.instance.media_player_new()
        self.playing = threading.Event()
        self.video_loop_thread = None
        self.lock = threading.Lock() 

        self.display = "Display"

        self.stop_video = False

        self.target_video = None

        # Initialize OpenCV window for fullscreen display
        cv2.namedWindow(self.display, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.display, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.moveWindow(self.display, 0, 0)

    # Display the splash screen
    def display_splash(self):
        self.crossfade(BLANK_SCREEN, self.splash)

    # Fade from Splash to Black
    def fade_to_black(self):
        self.crossfade(self.splash, BLANK_SCREEN)

    # Fade from Screen A to Screen B
    def crossfade(self, screen_a, screen_b):
        start_time = time.time()
        end_time = start_time + FADE_TIME
        alpha = 0.0
        
        while time.time() < end_time:
            alpha = (time.time() - start_time) / FADE_TIME
            blended = cv2.addWeighted(screen_a, 1-alpha, screen_b, alpha, 0)
            cv2.imshow(self.display, blended)
            cv2.waitKey(10)
        
        cv2.imshow(self.display, screen_b)
        cv2.waitKey(10)


    def is_playing(self):
        return self.player.is_playing()

    def load_video(self, file_path):
        """Prepare the video for playing."""
        if not os.path.exists(file_path):
            print(f"Error: Video file '{file_path}' not found.")
            return
        self.fade_to_black()
        with self.lock:
            self.player.stop()  # Ensure any current video is stopped
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            self.player.play()
            self.player.set_fullscreen(True)
            time.sleep(1)  # Wait for the video to start playing

    def start_video_loop(self):
        """Starts the video loop in a separate thread."""
        self.playing.set()
        if self.video_loop_thread is None or not self.video_loop_thread.is_alive():
            self.video_loop_thread = threading.Thread(target=self.reset_video)
            self.video_loop_thread.start()

    def reset_video(self):
        """Loop the video while the playing event is set."""
        while self.playing.is_set():
            time.sleep(0.1)  # Frequent checks to remain responsive
            if self.player.get_state() == vlc.State.Ended:
                with self.lock:
                    self.player.set_position(0)  # Rewind
                    self.player.play()  # Restart
                    time.sleep(1)  # Wait for the video to start playing

    def stop_video_loop(self):
        """Stop the video and the looping thread."""
        self.playing.clear()
        with self.lock:
            self.player.stop()

    def end_video_loop(self):
        """Stop the video and the looping thread."""
        self.playing.clear()
        with self.lock:
            self.player.stop()
        self.display_splash()

    def close_player(self):
        """Properly release resources when done."""
        self.playing.clear()  # Ensure no threads attempt to continue looping
        with self.lock:
            if self.player.is_playing():
                self.player.stop()  # Explicitly stop any playing media
            self.player.release()
            self.instance.release()






