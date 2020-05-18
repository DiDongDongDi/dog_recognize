from keras.models import load_model
import os
import numpy as np
from keras.preprocessing import image
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

from dog_recognize.settings import BASE_DIR

model_path = os.path.join(BASE_DIR, 'resources/models/dogImages.augmentation.model.weights.best.1.hdf5')
model = load_model(model_path)
model.predict(np.zeros((1, 512, 512, 3)))

def recognize(pred_img_path):
    img = image.load_img(pred_img_path, target_size=(512, 512))
    x = image.img_to_array(img)
    x = x / 255.
    x = np.expand_dims(x, axis=0)

    pred = (model.predict(x))[0]
    pred_classes = []
    pred_percents = []
    for i in range(3):
        pred_classes.append(pred.argmax())
        pred_percents.append(pred.max()*100)
        pred[pred_classes[i]] = 0

    return pred_classes, pred_percents
