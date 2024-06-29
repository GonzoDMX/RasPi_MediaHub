import cv2
import vlc
import time
import os
import numpy as np



# Constants
SCREEN_SIZE = (1920, 1080)  # Replace with your target monitor resolution
FADE_TIME = 1  # in seconds

# Initialize VLC instance
instance = vlc.Instance([
    '--fullscreen',
    '--no-video-title-show',
    '--vout', 'gl',
])
player = instance.media_player_new()

# Initialize OpenCV window for fullscreen display
cv2.namedWindow("Display", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Display", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("Display", 0, 0)


def resize_with_aspect_ratio(image, target_size):
    h, w = image.shape[:2]
    target_w, target_h = target_size
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized_image = cv2.resize(image, (new_w, new_h))
    
    top = (target_h - new_h) // 2
    bottom = target_h - new_h - top
    left = (target_w - new_w) // 2
    right = target_w - new_w - left
    
    color = [0, 0, 0]  # Black borders
    return cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

def fade_screen(image, target_color, duration):
    start_time = time.time()
    end_time = start_time + duration
    alpha = 0.0
    
    image_resized = resize_with_aspect_ratio(image, SCREEN_SIZE)
    target_color_image = np.full((SCREEN_SIZE[1], SCREEN_SIZE[0], 3), target_color, dtype=np.uint8)
    
    while time.time() < end_time:
        alpha = (time.time() - start_time) / duration
        blended = cv2.addWeighted(image_resized, 1-alpha, target_color_image, alpha, 0)
        cv2.imshow("Display", blended)
        cv2.waitKey(10)
    
    cv2.imshow("Display", target_color_image)
    cv2.waitKey(10)

def play_video(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Video file '{file_path}' not found.")
        return

    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()
    player.set_fullscreen(True)
    time.sleep(1)  # Wait for the video to start playing
    
    if player.is_playing():
        while player.is_playing():
            if cv2.waitKey(10) == ord('q'):  # Press 'q' to stop video
                break
    else:
        print("Error: Unable to play video. Check file format and codecs.")
    
    player.stop()


def main():
    splash_screen = cv2.imread('splash/sogeti_splash.jpg')
    video_playing = False
    fade_queue = []

    while True:
        if len(fade_queue) > 0:
            command = fade_queue.pop(0)
            command()

        key = cv2.waitKey(100)
        # Press 'q' to quit
        if key == ord('q'):
            break

        # Stop current video
        elif key == ord('s'):
            if player.is_playing():
                fade_screen(splash_screen, (0, 0, 0), FADE_TIME)
                player.stop()
                cv2.imshow("Display", splash_screen)

        # 'p' to start video
        elif key == ord('p'):
            fade_queue.append(lambda: fade_screen(splash_resized, (0, 0, 0), FADE_TIME))
            fade_queue.append(lambda: play_video('media/hololens/HololensDemo_1.mp4'))
            video_playing = True

        # Play video logic
        if not video_playing and len(fade_queue) == 0:
            if splash_screen is not None:
                splash_resized = resize_with_aspect_ratio(splash_screen, SCREEN_SIZE)
                cv2.imshow("Display", splash_resized)
                key = cv2.waitKey(10)


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()

