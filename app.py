from flask import Flask, request, render_template_string
import base64
from PIL import Image
from io import BytesIO
from time import time
from flask_socketio import SocketIO
import numpy as np
from ultralytics import YOLO
from roboflow import Roboflow
import cv2 as cv
rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
project = rf.workspace("mindcue").project("combo-dataset")
model = project.version(3).model
model = YOLO('yolov8n.onnx')

app = Flask(__name__)
socketio = SocketIO(app)
latest_frame_timestamp = 0  # Timestamp to track the latest frame update
latest_frame = None

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    frame = request.files['frame']
    frame.save('image.png')
    print(frame)
    try:
        # Convert PIL Image to OpenCV format
        with Image.open("image.png") as img:
            predictions = model.predict(img)
            # Print predictions to the terminal
            print(predictions.json())
            return {'detected_objects': predictions.json()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    socketio.run(app, port=8080)











# from flask import Flask, request, render_template_string
# import base64
# from PIL import Image
# from io import BytesIO
# from time import time
# from flask_socketio import SocketIO
# from ultralytics import YOLO

# app = Flask(__name__)
# model = YOLO('yolov8n.onnx')
# socketio = SocketIO(app)
# latest_frame_timestamp = 0  # Timestamp to track the latest frame update
# latest_frame = None

# @app.route('/upload_frame', methods=['POST'])
# def upload_frame():
#     frame = request.files['frame']
#     try:
#         # Convert PIL Image to OpenCV format
#         with Image.open(frame.stream) as img:
#            results = model.predict(img)
           
#         return {'detected_objects':results.names}
#     except Exception as e:

#         return {"error": str(e)}

# if __name__ == '__main__':
#     socketio.run(app, port=8080)
