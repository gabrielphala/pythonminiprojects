from flask import render_template, request
import json
from googletrans import Translator

def translatorRoute (app):
    @app.route('/translator')
    def renderTranslator ():
        return render_template('translator.html')

    @app.route('/translator/translate', methods=['POST'])
    def translateText ():
        if not (request.json['text']): return json.dumps({'error': 'Text is empty', 'successful': False})

        try:
            translator = Translator()

            res = translator.translate(request.json['text'], dest = request.json['dest'])

            return json.dumps({ 'detected': res.src, 'text': res.text, 'successful': True })
        except Exception as e:
            print(e)

            return json.dumps({'error': 'Could not translate text', 'successful': False})

