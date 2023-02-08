from flask import Flask

from routes.home import homeRoute
from routes.facefinder import faceFinderRoute
from routes.translator import translatorRoute
from routes.chatbot import chatBotRoute
from routes.whatisthis import whatIsThisRoute
from routes.detectnumber import detectNumberRoute
#from routes.animals import animalsRoute
from routes.twittersentimental import twitterSentimentalRoute
from routes.voices import voicesRoute

def create_app ():
    app = Flask(__name__)

    homeRoute(app)
    faceFinderRoute(app)
    translatorRoute(app)
    chatBotRoute(app)
    whatIsThisRoute(app)
    detectNumberRoute(app)
    #animalsRoute(app)
    twitterSentimentalRoute(app)
    voicesRoute(app)

    return app;