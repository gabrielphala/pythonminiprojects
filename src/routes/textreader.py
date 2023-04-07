import os

from flask import render_template , request
from werkzeug.utils import secure_filename
from PIL import Image

from src.utils import allowed_file

import json
import pytesseract
import cv2

def textReaderRoute (app):
    if os.environ.get('server_mode') == 'development' or os.environ.get('server_mode') == None:
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    UPLOAD_FOLDER = 'static/uploads'

    app.secret_key = 'scerey';
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTEBT_LENGTH'] = 16 * 1024 * 1024 

    @app.route('/textreader' , methods = ['GET'])
    def renderTextReader ():
        return render_template("textreader.html")

    @app.route('/textreader/read' , methods = ['POST'])
    def readText ():
        
        try:
            if ('file' not in request.files) or (request.files['file'] and request.files['file'].filename == ''):
                return json.dumps({ 'error': 'Please select a file', 'successful': False })

            file = request.files['file']

            if not allowed_file(file.filename):
                return json.dumps({ 'error': 'File type not allowed', 'successful': False })

            filename = secure_filename(file.filename)
            filelocation = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + filename)

            file.save(filelocation)
            
            img = cv2.cvtColor(cv2.imread(filelocation), cv2.COLOR_BGR2GRAY)
            
            cv2.threshold(img, 0, 255, cv2.THRESH_BINARY| cv2.THRESH_OTSU)[1]
                
            filename = "{}.jpg".format(os.getpid())

            cv2.imwrite(filename, img)

            text = pytesseract.image_to_string(Image.open(filename))

            os.remove(filename)

            return json.dumps({ 'successful': True, 'text': text })
        except Exception as e:
            print(e);

            return json.dumps({ 'error': 'Could not read file', 'successful': False })