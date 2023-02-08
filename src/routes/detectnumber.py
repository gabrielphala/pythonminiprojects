from flask import render_template , request
import os
from numpy import array2string
import numpy as np
import tensorflow as tf

def detectNumberRoute (app):
    allowed = ['jpg' , "jpeg" , 'png', 'webp', 'jfif', "tif" , "bmp"]

    @app.route('/detectnumber' , methods = ['GET'])
    def show():
        return render_template("detectnumber.html");
        
    @app.route('/detectnumber' , methods = ['POST'])
    def detectNumber():
        imageInput = request.files["imageFile"]
        ext = imageInput.filename.split('.')[-1]

        if not(ext in allowed): return render_template("detectnumber.html"); 

        image_path = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + imageInput.filename)
        imageInput.save(image_path)
        
        image = tf.keras.utils.load_img(image_path,  grayscale=True,  color_mode='grayscale' ,target_size=(28,28))
        image = tf.keras.utils.img_to_array(image)

        image = image.reshape((1, image.shape[0], image.shape[1],image.shape[2]))

        model = tf.keras.models.load_model(os.path.normpath(os.path.dirname(__file__) + '/../static/model'))
        results = model.predict(image)
        highest = np.argmax(results)
        
        results = results.flatten()

        return render_template("detectnumber.html" ,  image_path = imageInput.filename , highest = highest  )
