# from roboflow import Roboflow

# rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
# project = rf.workspace("mindcue").project("combo-dataset")
# # model = project.version(3).model
# from inference.models.utils import get_roboflow_model

# img_url = "./test.jpeg"

# # predictions = model.predict(img_url)
# model = get_roboflow_model(
#     api_key="rf_DM65bHNp6cbjPle0UTgOu1Aew442",
#     model_id="combo-dataset/3"
# )
# print(model.infer(image =img_url))


# from ultralytics import YOLO
# model = YOLO('yolov8n.pt')
# model.export(format = "onnx")


def normalize_path(path):
    # Replace double backslashes with single backslashes
    normalized_path = path.replace('\\\\', '\\')
    return normalized_path

# Example usage:
original_path = "C:\\Users\\mega\\AppData\\Local\\Temp\\tmpm98cuq4q.jpg"
normalized_path = normalize_path(original_path)
print(normalized_path)