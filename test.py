from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
from PIL import Image
import io
import base64
model = YOLO('yolov8n.pt')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('drafts.html')  # Make sure 'index.html' exists in your templates folder

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_frame')
def handle_frame(data):
    print("video recived")
    print(type(data))

    # Predict using YOLO
    # results = model.predict(image)
    # print(results)

    # Process the frame as needed
    emit('response_event', 'coming from flask i got your frame ')



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000
    )

















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

# from flask import Flask
# from flask_socketio import SocketIO
# import base64
# import os
# import asyncio
# from ultralytics import YOLO
# model = YOLO('yolov8n.pt')
# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# @app.route('/')
# def index():
#     return "WebSocket Server"

# @socketio.on('upload_frame')
# def handle_upload_frame(data):
#     # Convert ArrayBuffer to bytes
#     image_data = base64.b64decode(data)
#     print(image_data)
#     print(model.predict(image_data))
#     # Process the image data (e.g., save to file, run ML model, etc.)
#     # You can use a similar approach as before for processing

#     # Send response back to client if needed
#     socketio.emit('response', {'message': 'Frame received'})

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=8080)
