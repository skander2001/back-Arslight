from PIL import ImageOps, Image
import cv2
import base64
import numpy as np
from django.http import JsonResponse
from keras.models import load_model
from rest_framework.views import APIView
from tensorflow.keras.optimizers import legacy


classes = {i: chr(i + 65) for i in range(26)}
characters = ['alef', 'beh', 'teh', 'theh', 'jeem', 'hah', 'khah', 'dal', 'thal',
              'reh', 'zain', 'seen', 'sheen', 'sad', 'dad', 'tah', 'zah', 'ain',
              'ghain', 'feh', 'qaf', 'kaf', 'lam', 'meem', 'noon', 'heh', 'waw', 'yeh']
arabic_chars = dict(zip(np.arange(0, len(characters)), characters))

def resize_image(image_path, target_size=(28, 28)):
    # Charger l'image
    image = Image.open(image_path)
    # Redimensionner l'image
    resized_image = image.resize(target_size)
    return resized_image

def preprocess_image(image, target_size=(28, 28)):
    # Charger l'image en niveaux de gris
    grayscale_image = image.convert("L")
    # Inverser les couleurs noir et blanc
    inverted_image = ImageOps.invert(grayscale_image)
    # Redimensionner l'image
    resized_image = inverted_image.resize(target_size)
    # Convertir l'image en tableau numpy
    image_array = np.array(resized_image)
    # Normaliser les valeurs des pixels
    normalized_image = image_array / 255.0
    # Ajouter une dimension pour correspondre aux attentes du modèle
    preprocessed_image = normalized_image.reshape(1, target_size[0], target_size[1], 1)
    return preprocessed_image, resized_image


class predictFr(APIView):
    def post(self,request):
        print(request)
        print(request.FILES['image'])
        if request.method == 'POST':

            model = load_model("/Users/skander/Desktop/pi/back/models/frFinal.h5",compile=False)
            model.compile(optimizer=legacy.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
            image = request.FILES['image']

            resized_image = resize_image(image)
            # Prétraiter l'image
            preprocessed_image, _ = preprocess_image(resized_image)
            # Faire une prédiction
            prediction = model.predict(preprocessed_image)
            # Récupérer la classe prédite
            predicted_class_index = np.argmax(prediction)
            predicted_class=classes[predicted_class_index]
            print(predicted_class)
            return JsonResponse({"predicted_class": predicted_class})

class predictDigits(APIView):
    def post(self,request):
        print(request)
        print(request.FILES['image'])
        if request.method == 'POST':
            model = load_model("/Users/skander/Desktop/pi/back/models/digits_recognition_cnn3.h5",compile=False)
            model.compile(optimizer=legacy.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
            image = request.FILES['image']
            # Redimensionner l'image
            resized_image = resize_image(image)
            # Prétraiter l'image
            preprocessed_image, _ = preprocess_image(resized_image)
            prediction = model.predict(preprocessed_image)
            # Récupérer la classe prédite
            predicted_class_index = np.argmax(prediction)
            predicted_class=str(predicted_class_index)
            print(predicted_class)
            return JsonResponse({"predicted_class": predicted_class})


class predictAr(APIView):

    def post(self,request):
        print(request)
        print(request.FILES['image'])
        if request.method == 'POST':
            model = load_model("/Users/skander/Desktop/pi/back/models/modelAr.h5",compile=False)
            model.compile(optimizer=legacy.Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
            image = request.FILES['image']
            resized_image = resize_image(image, target_size=(32, 32))
            # Prétraiter l'image
            preprocessed_image, _ = preprocess_image(resized_image, target_size=(32, 32))
            # Faire une prédiction
            prediction = model.predict(preprocessed_image)
            # Récupérer la classe prédite
            predicted_class_index = np.argmax(prediction)
            predicted_class=arabic_chars[predicted_class_index] #Maj
            print(predicted_class)
            return JsonResponse({"predicted_class": predicted_class})
