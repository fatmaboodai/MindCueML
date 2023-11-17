import os
import signal
from flask import Flask, request
from PIL import Image
from flask_socketio import SocketIO
import numpy as np
from roboflow import Roboflow
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tempfile

rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
project = rf.workspace("mindcue").project("combo-dataset")
model = project.version(3).model

temp_image_paths = []
app = Flask(__name__)
socketio = SocketIO(app)

def async_predict(model, img_path):
    p = model.predict(img_path)
    return p


@app.route('/upload_frame', methods=['POST'])
async def upload_frame():
    frame = request.files['frame']
    image_data = frame.read()
    print(frame)
    # Create a temporary in-memory file-like object
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(image_data)
        temp_file.seek(0)
        image_path = temp_file.name
        temp_image_paths.append(image_path)
    try:
        # Execute the prediction in an asynchronous manner
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            predictions = await loop.run_in_executor(pool, async_predict, model, image_path)
            p = predictions.json()

        if p['predictions'] != []:
            print(p['predictions'][0])

        return {'detected_objects': predictions.json()}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": str(e)}


# Register a function to clean up temporary files when the application context is popped (server stopped)
import time

@app.teardown_appcontext
def cleanup_temp_files(error=None):
    # Check if the context is being popped due to an error (exception)
    for temp_image_path in temp_image_paths:
        t = temp_image_path.replace('\\\\', '\\')
        for _ in range(10):  # Attempt to delete the file up to 10 times
            if os.path.exists(t):
                # Wait for a timeout before attempting to delete
                time.sleep(0.1)  # Adjust the timeout value as needed
                try:
                    os.remove(t)
                    break  # File deleted, exit the loop
                except Exception as e:
                    print(f"Error removing file {t}: {e}")

            else:
                break  # File does not exist, no need to retry
        else:
            print(f"Failed to delete file {t} after 10 attempts")


if __name__ == '__main__':
    import gunicorn.app.base

    class FlaskApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key, value)

        def load(self):
            return self.application

    from gunicorn_config import bind, workers, app_module

    options = {
        'bind': bind,
        'workers': workers,
    }

    FlaskApplication(app, options).run()





















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
