import os
from picamera2 import Picamera2

# Initialize the camera once and configure it
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

def capture_image(path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        # Start the camera
        picam2.start()

        # Capture the image and save it
        picam2.capture_file(path)
        print(f"Image saved to {path}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Stop the camera after capturing the image
        picam2.stop()

# Example call to capture an image
capture_image("./week10-lab2/images/image.jpg")
