# import base64
# from io import BytesIO
# import os
# import tempfile
# from PIL import Image
# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit                
# from ultralytics import YOLO
# import signal
# from roboflow import Roboflow

# rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
# project = rf.workspace("mindcue").project("combo-dataset")
# model = project.version(3).model
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins="*")
# temp_image_paths=[]
# print(temp_image_paths)


# @app.route('/')
# def index():
#     return render_template('index.html')  # Make sure 'index.html' exists in your templates folder

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('send_frame')
# def handle_frame(data):
#     print("Frame received")
#     image_data = base64.b64decode(data.split(',')[1])

#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg') as temp_file:
#             temp_file.write(image_data)
#             temp_file.seek(0)
#             image_path = temp_file.name
#             temp_image_paths.append(image_path)
#             temp_file.close()
#             try:
#                 results = model.predict(image_path)
#                 p = results.json()

#                 if p['predictions']:
#                     emit('predictions',p['predictions'][0])
#                     print(p['predictions'][0])
#             except Exception as e:
#                 print(f"Error during prediction: {e}")

#     finally:
#         # Clean up the file immediately after processing
#         try:
#             os.remove(image_path)
#             print(f"Deleted: {image_path}")
#         except Exception as e:
#             print(f"Error deleting {image_path}: {e}")

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=9000)
















# from flask import Flask

# from flask_socketio import SocketIO
# from roboflow import Roboflow
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# import tempfile
# import os

# rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
# project = rf.workspace("mindcue").project("combo-dataset")
# model = project.version(3).model

# app = Flask(__name__)
# socketio = SocketIO(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

# executor = ThreadPoolExecutor()

# def async_predict(model, img_path):
#     return model.predict(img_path)

# @socketio.on('upload_frame')
# async def handle_upload_frame(json):
#     image_data = json['frame']
#     # Handle image data, save to temporary file and predict
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
#         temp_file.write(image_data)
#         image_path = temp_file.name

#     try:
#         loop = asyncio.get_running_loop()
#         predictions = await loop.run_in_executor(executor, async_predict, model, image_path)
#         p = predictions.json()

#         if p['predictions']:
#             print(p['predictions'][0])

#         socketio.emit('prediction_response', {'detected_objects': p})
#     except Exception as e:
#         print(f"Error during prediction: {e}")
#         socketio.emit('error', {'message': str(e)})
#     finally:
#         os.remove(image_path)

# if __name__ == '__main__':
#     socketio.run(app, host='127.0.0.1', port=5500)

from flask import Flask
from flask_socketio import SocketIO
import base64
import os
import asyncio
from ultralytics import YOLO
import base64
import numpy as np
from PIL import Image
from io import BytesIO


model = YOLO('yolov8n.onnx')
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "WebSocket Server"

@socketio.on('upload_frame')
def handle_upload_frame(data):
    # Convert ArrayBuffer to bytes
    image_data = base64.b64decode(data)
    image = Image.open(BytesIO(image_data))
    # print(image_data)
    print(model.predict(image))

    # Send response back to client if needed
    socketio.emit('predictions', {'message': 'Frame received'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
