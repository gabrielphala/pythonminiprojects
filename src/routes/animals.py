# import tensorflow as tf
from flask import render_template , request
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16


import sys
import time
import math
 
from numpy import array2string
import numpy as np
import tensorflow as tf
import os

def animalsRoute (app):
    allowed = ['jpg' , "jpeg" , 'png', 'webp', 'jfif', "tif" , "bmp"]
    model = VGG16()

    @app.route('/animals' , methods = ['GET'])
    def imageRec ():
        return render_template("animals.html")
        
        
    @app.route('/animals' , methods = ['POST'])
    def predict ():
        imageInput = request.files["imageFile"]
        ext = imageInput.filename.split('.')[-1]

        if not(ext in allowed): return render_template("animals.html"); 

        image_path = os.path.normpath(os.path.dirname(__file__) + "/../static/uploads/" + imageInput.filename)
        imageInput.save(image_path)
        
        image = tf.keras.utils.load_img(image_path ,target_size=(224,224))
        image = tf.keras.utils.img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1],image.shape[2]))
        image = preprocess_input(image)
        
        yhat = model.predict(image)

        label = decode_predictions(yhat)
        label = label[0][0]

        name = label[1]
        perc = math.ceil( label[2]*100 ) 

        return render_template("animals.html" ,  name = name , perc = perc,  image_path = image_path)