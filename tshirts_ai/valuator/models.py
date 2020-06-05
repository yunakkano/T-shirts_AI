from django.db import models

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from PIL import Image
import io
import base64

# Initialize graph variable to load Prediction model.
graph = tf.compat.v1.get_default_graph()

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Tshirt(models.Model):
    image = models.ImageField(upload_to='photos')

    comment = models.CharField(max_length=100)
    up_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    IMAGE_SIZE = 224  # 画像サイズ
    MODEL_FILE_PATH = './valuator/ml_models/vgg16_Tshirts.h5'  # Model file
    classes = [
        "0300-0800", "0800-1300", "1300-1800", "1800-2500",
        "2500-3200", "3200-4000", "4000-5000", "5000-"
    ]
    num_classes = len(classes)

    def predict(self):
        model = None
        global graph  # graph is called every time to use the same VGG16 model
        with graph.as_default():
            model = load_model(self.MODEL_FILE_PATH)

            img_data = self.image.read()
            # For Pillow to open the image file, convert data to BytesIO
            img_bin = io.BytesIO(img_data)
            image = Image.open(img_bin)
            image = image.convert("RGB")
            image = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
            data = np.asarray(image) / 255.0
            X = []

            X.append(data)
            X = np.array(X)
            result = model.predict([X])[0]  # Obtain the first result
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)
            # print(self.classes[predicted], percentage)
            return self.classes[predicted], percentage

    def image_source(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img
