import os
import glob

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

