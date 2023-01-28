from flask import Flask, render_template, request, redirect #for creating server
import os
from werkzeug.utils import secure_filename
from .facefinder import allowed_file

from torchvision import transforms, models
from PIL import Image # for uploding images
import torch

def whatIsThisRoute (app):
    UPLOAD_FOLDER = 'static/uploads' #where images will be 

    app.secret_key = 'scerey';
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #the upload folder
    app.config['MAX_CONTEBT_LENGTH'] = 16 * 1024 * 1024 #the maximum size of any size that we upload

    @app.route('/whatisthis', methods = ['POST', 'GET'])
    def whatisthis():
        if (request.method == 'GET'):
            return render_template('whatisthis.html')

        if 'file' not in request.files: # if no file is being uploaded, reload page
            return redirect('/whatisthis')

        file = request.files['file']

        if (file.filename == ''): # if no file is being uploaded, reload page
            return redirect('/whatisthis')

        elif file and allowed_file(file.filename): # if file being uploaded is allowed
            filename = secure_filename(file.filename) # rename the file
            filelocation = os.path.normpath(os.path.dirname(__file__) + '/../static/uploads/' + filename) # get file location
            
            file.save(filelocation) # save the file
            
            # alexnet = models.AlexNet()

            # model we are using
            resnet = models.resnet101(pretrained=True)

            # define preprocessing method
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])

            img = Image.open(filelocation)

            # preprocess the uploadede image
            img_t = preprocess(img)

            batch_t = torch.unsqueeze(img_t, 0)
            resnet.eval()
            out = resnet(batch_t)

            # loading names of objects, into an array
            with open(os.path.normpath(os.path.dirname(__file__) + '/../static/data/imagenet_classes.txt')) as f:
                labels = [line.strip() for line in f.readlines()]

            # getting the prediction
            _, index = torch.max(out, 1)

            percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
            w,x = labels[index[0]], percentage[index[0]].item()

            # print(w, filename, x)

            # render to
            return render_template('whatisthis.html', data={
                "filename": filename,
                "item": w,
                "accuracy": x
            });
        
        else:
            return redirect('/whatisthis')

