from flask import render_template, request
import json
from googletrans import Translator

# initiate Google Translate

def translatorRoute (app):
    # define REST API route where traslation will take place
    @app.route('/translator/translate', methods=['POST'])
    def translate ():
        # if text to translate is empty quit
        if not (request.json['text']): return str(json.dumps({'error': 'Text is empty'}))

        translator = Translator()

        # now translate text
        res = translator.translate(request.json['text'], dest = request.json['dest'])

        # return translated text
        return str(json.dumps({ 'detected': res.src, 'text': res.text }))

    # define home REST API route
    @app.route('/translator')
    def translator ():
        # render home page
        return render_template('translator.html')

