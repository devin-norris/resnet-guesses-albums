import requests
from collections import namedtuple
from PIL import Image
import numpy as np
from keras.applications.resnet import ResNet50

ModelResult = namedtuple("Prediction", "prediction confidence")

class Model:
    def __init__(self) -> None:
        self.model = ResNet50(input_shape=(224, 224, 3))
        self.classes = self.get_classes()

    def get_classes(self) -> np.ndarray:
        classes = (requests
           .get("https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json")
           .json())
        classes = np.array(classes)
        return classes

    def img_predict(self, img: Image.Image) -> ModelResult:
        x = np.array(img)[np.newaxis, :]
        y_hat = self.model(x).numpy().squeeze()
        I = y_hat.argsort()[::-1]

        prediction = self.classes[I[:1]][0]
        confidence = f"{str(y_hat[I[:1]][0]*100)[:5]}%"
        return ModelResult(prediction, confidence)
