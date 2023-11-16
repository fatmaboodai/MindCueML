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
import asyncio
from concurrent.futures import ThreadPoolExecutor

rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
project = rf.workspace("mindcue").project("combo-dataset")
# model = YOLO('yolov8n.onnx')


app = Flask(__name__)
socketio = SocketIO(app)
latest_frame_timestamp = 0  # Timestamp to track the latest frame update
latest_frame = None
frame=[]
def async_predict(model, img):
    return model.predict(img)


@app.route('/upload_frame', methods=['POST'])
async def upload_frame():
    frame = request.files['frame']
    try:
        with Image.open(frame.stream) as img:
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                predictions = await loop.run_in_executor(pool, async_predict, model, img)
                print(predictions.json())
                return {'detected_objects': predictions.json()}
    except Exception as e:
        return {"error": str(e)}

# @app.route('/upload_frame', methods=['POST'])
# def upload_frame():
#     frame = request.files['frame']
#     try:
#         # Convert PIL Image to OpenCV format
#         with Image.open(frame.stream) as img:
#             predictions = model.predict(img
#             # Print predictions to the terminal
#             print(predictions.json())
#             return {'detected_objects': predictions.json()}
#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == '__main__':
#     socketio.run(app, port=8080)


if __name__ == '__main__':
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    asyncio.run(serve(app, config))







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
