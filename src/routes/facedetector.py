from flask import render_template, request
import os
from werkzeug.utils import secure_filename
import cv2

from src.utils import allowed_file

import json

def faceDetectorRoute (app):
    UPLOAD_FOLDER = 'static/uploads'

    app.secret_key = 'scerey';
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTEBT_LENGTH'] = 16 * 1024 * 1024

    @app.route('/facedetector', methods = ['GET'])
    def renderFaceDetector():
        return render_template('facedetector.html')

    @app.route('/facedetector/detect', methods = ['POST'])
    def detectFace():
        try:
            if ('file' not in request.files) or (request.files['file'] and request.files['file'].filename == ''):
                return json.dumps({ 'error': 'Please select a file', 'successful': False })

            file = request.files['file']

            if (not(allowed_file(file.filename))):
                return json.dumps({ 'error': 'File type not allowed', 'successful': False })

            filename = secure_filename(file.filename)
            filelocation = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + filename)
            file.save(filelocation)

            cascadefile = os.path.normpath(os.path.dirname(__file__) + '/../static/cascade/face_cascade.xml')

            face_cascade = cv2.CascadeClassifier(cascadefile)
            img = cv2.imread(filelocation)

            newImage = cv2.resize(img, (400, 400), interpolation=cv2.INTER_AREA)

            faces = face_cascade.detectMultiScale(newImage, 1.1, 4)

            cv2.imwrite(filelocation, newImage);

            face_arr = []

            for (x, y, w, h) in faces:
                face_arr.append([int(x), int(y), int(w), int(h)])

            return json.dumps({ 'successful': True, 'filename': filename, 'faces': face_arr })
        except Exception as e:
            print(e)

            return json.dumps({ 'error': 'File could not be read', 'successful': False })