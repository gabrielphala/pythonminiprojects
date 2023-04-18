from flask import Flask

from .routes.home import homeRoute
from .routes.facedetector import faceDetectorRoute
from .routes.translator import translatorRoute
from .routes.chatbot import chatBotRoute
from .routes.objectdetector import objectDetectorRoute
from .routes.numberdetector import numberDetectorRoute
#from .routes.animals import animalsRoute
from .routes.twittersentimental import twitterSentimentalRoute
from .routes.voices import voicesRoute
from .routes.textreader import textReaderRoute
from .routes.facerestore import faceRestoreRoute


def create_app ():
    app = Flask(__name__)

    homeRoute(app)
    faceDetectorRoute(app)
    translatorRoute(app)
    chatBotRoute(app)
    objectDetectorRoute(app)
    numberDetectorRoute(app)
    #animalsRoute(app)
    twitterSentimentalRoute(app)
    voicesRoute(app)
    textReaderRoute(app)
    faceRestoreRoute(app)


    return app;