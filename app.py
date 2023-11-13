from flask import Flask, request, render_template_string
import base64
from PIL import Image
from io import BytesIO
from time import time
from ultralytics import YOLO
import pandas
app = Flask(__name__)
model = YOLO('yolov8n.onnx')
latest_frame = None
latest_frame_timestamp = 0  # Timestamp to track the latest frame update
@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame, latest_frame_timestamp
    frame = request.files['frame']
    # Process the frame with YOLO model
    try:
        with Image.open(frame.stream) as img:
            results = model.predict(img)
                        # Accessing names of detected objects
            detected_names = results.names  # This is typically how you access names

            # Convert to list if necessary
            detected_names_list = [name for name in detected_names]
             # Convert list to a JSON-serializable response
            return {'detected_objects': detected_names_list}
            
            # Process results here as needed, e.g., store them, send them elsewhere, etc.
    except Exception as e:
        # print(f"Error processing the image with YOLO: {e}")
        return {"error": str(e)}

    # Resize and compress the image to reduce the size
    # with Image.open(frame.stream) as img:
    #     buffer = BytesIO()
    #     img.save(buffer, format="JPEG", quality=70)  # Compress image
    #     latest_frame = base64.b64encode(buffer.getvalue()).decode()

    # latest_frame_timestamp = int(time())  # Update the timestamp
    # return {'status': 'Latest frame received'}



@app.route('/get_latest_frame')
def get_latest_frame():
    return {'frame': latest_frame, 'timestamp': latest_frame_timestamp}

@app.route('/view_frames')
def view_frames():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Latest Frame</title>
            <script>
                let lastTimestamp = 0;

                function checkForNewFrame() {
                    fetch('/get_latest_frame')
                        .then(response => response.json())
                        .then(data => {
                            if (data.timestamp > lastTimestamp) {
                                document.getElementById('latestFrame').src = 'data:image/jpeg;base64,' + data.frame;
                                lastTimestamp = data.timestamp;
                            }
                        })
                        .catch(error => console.error('Error:', error));
                }

                setInterval(checkForNewFrame, 1000);  // Check for new frame more frequently
            </script>
        </head>
        <body>
            <h1>Latest Frame</h1>
            <img id="latestFrame" alt="Latest Frame" style="max-width: 100%; height: auto;">
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(port=8080)