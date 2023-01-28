from flask import Flask

from routes.home import homeRoute
from routes.facefinder import faceFinderRoute
from routes.translator import translatorRoute
from routes.chatbot import chatBotRoute
from routes.whatisthis import whatIsThisRoute
from routes.detectnumber import detectNumberRoute
#from routes.animals import animalsRoute
from routes.twittersentimental import twitterSentimentalRoute

app = Flask(__name__)

homeRoute(app)
faceFinderRoute(app)
translatorRoute(app)
chatBotRoute(app)
whatIsThisRoute(app)
detectNumberRoute(app)
#animalsRoute(app)
twitterSentimentalRoute(app)

if  (__name__ == '__main__'):
    app.run(port=80, debug=True)