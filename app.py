from flask import Flask, request, render_template_string
import base64
from PIL import Image
from io import BytesIO
from time import time
from flask_socketio import SocketIO
from ultralytics import YOLO
app = Flask(__name__)
model = YOLO('yolov8n.onnx')
socketio = SocketIO(app)
latest_frame_timestamp = 0  # Timestamp to track the latest frame update
latest_frame = None



@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    frame = request.files['frame']

    try:
        with Image.open(frame.stream) as img:
            # Process the frame with YOLO model
            results = model.predict(img)
            detected_names = results.names
        
            return {'detected_objects': detected_names}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    socketio.run(app, port=8080)
