from flask import render_template, request
from nltk.chat.util import Chat, reflections

def chatBotRoute (app):
    pairs = [
        [
            r"(.*)my name is (.*)",
            ["Hello %2, How are you today ?",]
        ],
        [
            r"(.*)help(.*) ",
            ["I can help you ",]
        ],
        [
            r"(.*) your name",
            ["My name is chatbot.",]
        ],
        [
            r"how are you (.*)",
            ["I'm doing very well", "i am great !"]
        ],
        [
            r"sorry (.*)",
            ["Its alright","Its OK, never mind that",]
        ],
        [
            r"i'm (.*) (good|well|okay|ok)",
            ["Nice to hear that","Alright, great !",]
        ],
        [
            r"(hi|hey|hello|hola|holla)(.*)",
            ["Hello", "Hey there",]
        ],
        [
            r"what (.*) want",
            ["Make me an offer I can't refuse",]
            
        ],
        [
            r"(.*)created(.*)",
            ["Aman Kharwal created me using Python's NLTK library ","top secret ;)",]
        ],
        [
            r"(.*) (location|city) ?",
            ['New Delhi, India',]
        ],
        [
            r"(.*)raining in (.*)",
            ["No rain in the past 4 days here in %2","In %2 there is a 50% chance of rain",]
        ],
        [
            r"how (.*) health (.*)",
            ["Health is very important, but I am a computer, so I don't need to worry about my health ",]
        ],
        [
            r"(.*)(sports|game|sport)(.*)",
            ["I'm a very big fan of Cricket",]
        ],
        [
            r"who (.*) (Cricketer|Batsman)?",
            ["Virat Kohli"]
        ],
        [
            r"quit",
            ["Bye for now. See you soon :) ","It was nice talking to you. See you soon :)"]
        ],
        [
            r"(.*)",
            ['That is nice to hear']
        ],
    ]

    chat = Chat(pairs, reflections)

    @app.route('/chatbot/message', methods = ['POST'])
    def message ():
        text = request.json['text']
        return str(chat.respond(text))

    @app.route('/chatbot')
    def chatbot ():
        return render_template('chatbot.html')
