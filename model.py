from roboflow import Roboflow

rf = Roboflow(api_key="7Hl9FLL5IgTbW6A70Nue")
project = rf.workspace("mindcue").project("combo-dataset")
model = project.version(3).model


img_url = "./test.jpeg"

predictions = model.predict(img_url)

print(predictions)