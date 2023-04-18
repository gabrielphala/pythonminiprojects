from flask import Flask , render_template , request
from ..static.model.GFPGAN.inference_gfpgan import main
import sys , os
import subprocess

def faceRestoreRoute(app):
    allowed = ['jpg' , "jpeg" , 'png', 'webp', 'jfif', "tif" , "bmp"]

    # app = Flask(__name__)

    @app.route('/facerestore' , methods = ['GET'])
    def imageRec():
        print('Hello world!\n', file=sys.stderr)

        return render_template("facerestore.html")


    @app.route('/facerestore/restore' , methods = ['POST'])
    def predict():

        imageInput = request.files["imageFile"]
        ext = imageInput.filename.split('.')[-1]

        if not(ext in allowed): return render_template("facerestore.html");

        # image_path = "./inputs/upload/" + imageInput.filename
        image_path = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + imageInput.filename)
        imageInput.save(image_path)

        print('=====================================================', file=sys.stderr)

        print(imageInput.filename)

        print('=====================================================', file=sys.stderr)

        main(imageInput.filename)

        return render_template("facerestore.html" , img = imageInput.filename)