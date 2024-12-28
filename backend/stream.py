import cv2
import zmq
import base64
import time
import threading
from flask import Flask, Response

# Set up ZeroMQ PUB socket
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5559")  # Change the address and port as needed

# Initialize Flask app
app = Flask(__name__)

# OpenCV for capturing video
cap = cv2.VideoCapture(0)  # Open the default camera (0)

def stream_video():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Perform ML processing here (optional)
        
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        
        # Send the frame over the socket
        socket.send(jpg_as_text)
        time.sleep(0.03)  # Sleep for ~30fps (Adjust as necessary)

# Start video capture and ZeroMQ socket streaming in a separate thread
stream_thread = threading.Thread(target=stream_video)
stream_thread.daemon = True
stream_thread.start()

# Function to serve MJPEG stream to the browser
def generate_video_stream():
    # Connect to ZeroMQ socket to receive frames
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    while True:
        # Receive frame from ZeroMQ
        jpg_as_text = socket.recv()
        
        # Decode the JPEG image
        jpg_data = base64.b64decode(jpg_as_text)
        
        # Yield it as MJPEG stream for Flask
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_data + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "Video Streaming Started! Go to /video_feed for video stream."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
