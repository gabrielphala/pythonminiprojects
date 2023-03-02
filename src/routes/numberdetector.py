from flask import render_template , request
import os
import numpy as np
import tensorflow as tf

from src.utils import allowed_file

import json

def numberDetectorRoute (app):
    allowed = ['jpg' , "jpeg" , 'png', 'webp', 'jfif', "tif" , "bmp"]

    @app.route('/numberdetector' , methods = ['GET'])
    def renderNumberDetector():
        return render_template("numberDetector.html");
        
    @app.route('/numberdetector/detect' , methods = ['POST'])
    def detectNumber():
        if ('file' not in request.files) or (request.files['file'] and request.files['file'].filename == ''):
            return json.dumps({ 'error': 'Please select a file', 'successful': False })

        file = request.files['file']

        ext = file.filename.split('.')[-1]

        if not(allowed_file(file.filename, 1)):
            return json.dumps({ 'error': 'File extention now allowed', 'succesful': False }); 

        image_path = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + file.filename)
        file.save(image_path)
        
        image = tf.keras.utils.load_img(image_path,  grayscale=True,  color_mode='grayscale' ,target_size=(28,28))
        image = tf.keras.utils.img_to_array(image)

        image = image.reshape((1, image.shape[0], image.shape[1],image.shape[2]))

        model = tf.keras.models.load_model(os.path.normpath(os.path.dirname(__file__) + '/../static/model/number'))
        
        results = model.predict(image)
        highest = np.argmax(results)
        
        results = results.flatten()

        return json.dumps({ 'successful': True, 'number': int(highest) })
