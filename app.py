import os
import PIL
from flask import Flask, request, render_template_string
import base64
from PIL import Image
from io import BytesIO
import time
from flask_socketio import SocketIO
import numpy as np
from ultralytics import YOLO
from roboflow import Roboflow
import cv2 as cv
import asyncio
from concurrent.futures import ThreadPoolExecutor
import io
import tempfile
rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
project = rf.workspace("mindcue").project("combo-dataset")
model = project.version(3).model

temp_image_paths = []
app = Flask(__name__)
socketio = SocketIO(app)
latest_frame_timestamp = 0  # Timestamp to track the latest frame update
latest_frame = None
def async_predict(model, img_path):
    x = model.predict(img_path)
    # Assuming model.predict takes the path of the image and returns predictions
    return x
@app.route('/upload_frame', methods=['POST'])
async def upload_frame():
    frame = request.files['frame']
    image_data = frame.read()
    # Create a temporary in-memory file-like object
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(image_data)
        temp_file.seek(0)
        image_path = temp_file.name
        temp_image_paths.append(image_path)
    try:
        with Image.open(frame.stream) as img:
            # Close the image file explicitly
            img.close()
            # Execute the prediction in an asynchronous manner
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                predictions = await loop.run_in_executor(pool, async_predict, model, image_path)
                p = predictions.json()
                if p['predictions'] != []:
                    print(p['predictions'][0]['class'])
                return {'detected_objects': predictions.json()}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": str(e)}

# Register a function to clean up temporary files when the application context is popped (server stopped)
@app.teardown_appcontext
def cleanup_temp_files(error=None):
    for temp_image_path in temp_image_paths:
        t = temp_image_path.replace('\\\\', '\\')
        if os.path.exists(t):
            os.remove(t)
   
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
# import numpy as np
# from ultralytics import YOLO
# from roboflow import Roboflow
# import cv2 as cv
# rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
# project = rf.workspace("mindcue").project("combo-dataset")
# model = project.version(3).model
# model = YOLO('best.onnx')

# app = Flask(__name__)
# socketio = SocketIO(app)
# latest_frame_timestamp = 0  # Timestamp to track the latest frame update
# latest_frame = None

# @app.route('/upload_frame', methods=['POST'])
# def upload_frame():
#     frame = request.files['frame']
#     frame.save('image.png')
#     print(frame)
#     try:
#         # Convert PIL Image to OpenCV format
#         with Image.open("image.png") as img:
#             predictions = model.predict(img)
#             # Print predictions to the terminal
#             print(predictions.json())
#             return {'detected_objects': predictions.json()}
#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == '__main__':
#     socketio.run(app, port=8080)























# from flask import Flask, request, render_template_string
# import base64
# from PIL import Image
# from io import BytesIO
# from time import time
# from flask_socketio import SocketIO
# from ultralytics import YOLO

# app = Flask(__name__)
# model = YOLO('best.onnx')
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
