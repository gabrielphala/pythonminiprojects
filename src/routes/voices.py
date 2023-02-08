import os
import uuid
import time
import sys
from pathlib import Path
import whisper
from flask import flash, request, redirect, render_template

def voicesRoute (app):
    @app.route('/voices')
    def render_voices():
        return render_template('voices.html')

    @app.route('/voices/record', methods=['POST'])
    def save_record():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/voices')

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/voices')

        file_name = str(uuid.uuid4()) + ".mp3"
        file_path = os.path.normpath(os.path.dirname(__file__) + "/../static/audio/" + file_name )
        file.save(file_path)

        newModel = whisper.load_model(
            os.path.normpath(os.path.dirname(__file__) + "/../static/model/voices.base.en.pt")
        )

        result = newModel.transcribe(file_path)

        return result["text"]