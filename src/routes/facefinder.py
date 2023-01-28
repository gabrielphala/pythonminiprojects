from flask import render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import cv2

ALLOWED_EXTENSIONS = ('png', 'jpg', 'gif', 'webp');

def allowed_file (filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS;

def faceFinderRoute (app):
    UPLOAD_FOLDER = 'static/uploads'

    app.secret_key = 'scerey';
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTEBT_LENGTH'] = 16 * 1024 * 1024

    @app.route('/facefinder', methods = ['POST', 'GET'])
    def faceFinder():
        if (request.method == 'GET'):
            return render_template('facefinder.html')

        if 'file' not in request.files:
            return redirect('/facefinder')

        file = request.files['file']

        if (file.filename == ''):
            return redirect('/facefinder')

        elif file and allowed_file(file.filename):
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
                face_arr.append([x, y, w, h])

            return render_template('facefinder.html', filename=filename, faces=face_arr)
        
        else:
            return redirect('/facefinder')