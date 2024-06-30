import os
import cv2
import glob
from config import SCREEN_SIZE, BLACK_OUT, BLANK_SCREEN


# Fit image to Screen Size
def fit_aspect_ratio(image):
    h, w = image.shape[:2]
    target_w, target_h = SCREEN_SIZE
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized_image = cv2.resize(image, (new_w, new_h))
    
    top = (target_h - new_h) // 2
    bottom = target_h - new_h - top
    left = (target_w - new_w) // 2
    right = target_w - new_w - left
    
    return cv2.copyMakeBorder(
        resized_image,
        top, bottom, left, right,
        cv2.BORDER_CONSTANT,
        value=BLACK_OUT
    )

# Fetch personalized splash image
def get_splash_screen():
    splash_dir = os.path.join(os.path.dirname(__file__), 'splash')
    image_exts = ['.png', '.jpg', '.jpeg']
    
    # Create a list to store the image files
    image_files = []

    # Iterate through the files in the splash directory
    for file in glob.glob(os.path.join(splash_dir, '*')):
        if os.path.isfile(file):
            extension = os.path.splitext(file)[1].lower()
            if extension in image_exts:
                image_files.append(file)

    # If no image is found, return Black Screen
    if not image_files:
        print("No Splash Image Found.")
        return BLANK_SCREEN

    # Get the most recently added image file
    latest_image = max(image_files, key=os.path.getctime)
    
    print(f"Loading Splash Image: {latest_image}")

    splash_img = cv2.imread(latest_image)
    splash_screen = fit_aspect_ratio(splash_img)

    return splash_screen


# Fetch a video path from object name
def get_video_path(obj_name):
    try:
        obj_dir = os.path.join('media', obj_name)
        video_exts = ('.mp4', '.avi', '.mov')

        files = sorted(os.listdir(obj_dir))
        video_files = [os.path.join(obj_dir, f) for f in files if f.lower().endswith(video_exts)]
        if not video_files:
            print(f"No compatible video files found for: {obj_name}")
            return None

        latest_video = max(video_files, key=os.path.getctime)
        print(f"Loading Video: {latest_video}")
        return latest_video

    except Exception as e:
        print(f"Error: Unable to access {obj_name}")
        return None
