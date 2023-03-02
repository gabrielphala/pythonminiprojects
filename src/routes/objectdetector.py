from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from src.utils import allowed_file

from torchvision import transforms, models
from PIL import Image
import torch

import json

def objectDetectorRoute (app):
    UPLOAD_FOLDER = 'static/uploads'

    app.secret_key = 'scerey';
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTEBT_LENGTH'] = 16 * 1024 * 1024

    @app.route('/objectdetector', methods = ['GET'])
    def renderObjectDetector():
        return render_template('objectdetector.html')
    
    @app.route('/objectdetector/detect', methods = ['POST'])
    def detectOject ():
        if ('file' not in request.files) or (request.files['file'] and request.files['file'].filename == ''):
            return json.dumps({ 'error': 'Please select a file', 'successful': False })

        file = request.files['file']

        if (not(allowed_file(file.filename))):
            return json.dumps({ 'error': 'File type not allowed', 'successful': False })

        filename = secure_filename(file.filename) 
        filelocation = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + filename) # get file location
        
        file.save(filelocation)
        
        resnet = models.resnet101(pretrained=True)

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        try:
            img = Image.open(filelocation)

            img_t = preprocess(img)

            batch_t = torch.unsqueeze(img_t, 0)
            resnet.eval()
            out = resnet(batch_t)

            with open(os.path.normpath(os.path.dirname(__file__) + '/../static/data/imagenet_classes.txt')) as f:
                labels = [line.strip() for line in f.readlines()]

            _, index = torch.max(out, 1)

            percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
            w,x = labels[index[0]], percentage[index[0]].item()

            return json.dumps({
                'successful': True,
                "filename": filename,
                "item": w,
                "accuracy": x
            })
        except:
            return json.dumps({ 'error': 'File could not be read', 'successful': False })

