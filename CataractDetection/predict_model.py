
from tensorflow import keras
import cv2


class CataractDetector:

    def __init__(self, model_weights_path, img_size=(160, 160)):
        self.model_weights_path = model_weights_path
        self.model = keras.models.load_model(self.model_weights_path)
        self.img_size = img_size

    def predict(self, img):

        resized_img = cv2.resize(img, self.img_size)
        resized_img = resized_img.reshape((1,)+resized_img.shape)
        output = self.model.predict(resized_img/255.0)

        return "Cataract" if output >= 0.5 else "Normal"
