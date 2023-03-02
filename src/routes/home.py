from flask import render_template

def homeRoute (app):
    @app.route('/', methods = ['GET'])
    def home():
        return render_template('home.html', isHome=True)