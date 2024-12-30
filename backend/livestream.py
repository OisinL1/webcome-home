from flask import Flask, Response
from picamera2 import Picamera2
from time import sleep
import cv2

# Initialize Flask app
app = Flask(__name__)

# Initialize the camera
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()
sleep(2)  # Let the camera warm up

def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame in HTTP response format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Home route."""
    return "<h1>Raspberry Pi Camera Livestream</h1><img src='/video_feed' width='640' height='480'>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
