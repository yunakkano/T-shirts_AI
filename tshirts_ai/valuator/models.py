from django.db import models
from django.contrib.auth.models import User
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, model_from_json
from PIL import Image
from tshirts_ai.settings import BASE_DIR
import os
import io
import base64

graph = tf.compat.v1.get_default_graph()

class Tshirt(models.Model):
    image = models.ImageField(upload_to='Photos/')
    price_range = models.CharField(max_length=50)
    comment = models.TextField()
    saved_at = models.DateTimeField()
    confidence = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    IMAGE_SIZE = 224  # 画像サイズ
    MODEL_FILE_PATH = os.path.join(BASE_DIR, 'valuator/my_model')
    classes = [
        "300円〜800円", "800円〜1300円", "1300円〜1800円", "1800円〜2500円",
        "2500円〜3200円", "3200円〜4000円", "4000円〜5000円", "5000円以上"
    ]
    num_classes = len(classes)

    def valuate(self):
        model = None
        global graph  # graph is called every time to use the same VGG16 model
        with graph.as_default():
            # model = keras.models.load_model(self.MODEL_FILE_PATH)  # 2. This is 2nd try
            # model = load_model(self.MODEL_FILE_PATH)                # 1. This is original
            json_string = open(os.path.join('valuator/my_model', 'vgg16_Tshirts.json')).read()
            model = model_from_json(json_string)
            model.load_weights(os.path.join('valuator/my_model', 'vgg16_Tshirts.hdf5'))
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
            return self.classes[predicted], percentage

    def image_source(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()
            return 'data:' + img.file.content_type + ';base64,' + base64_img

    def __str__(self):
        return self.comment

    def summary(self):
        dots = '...' if len(self.comment) > 20 else ''
        return self.comment[:20] + dots
