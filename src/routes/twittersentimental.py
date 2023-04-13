from flask import render_template , request

import csv , sys
import twitter

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import urllib.request


def twitterSentimentalRoute (app):

    
    twitter_api = twitter.Api(
        consumer_key="skzTUzRzNHVS2YoUOoq1HEsOd",
        consumer_secret="m7ZGlU2IB2b57WULWjMXlIrw2SlTQNH7wwY41sLjZT4OT5NjBg",
        access_token_key="1612739396121272320-Z4VSu8wfbucXjBOviKOyajSyY60WtZ",
        access_token_secret="f4inHTTQ9MmXE0ot4wgTECuqSjusIG8X6wBLTZonvO6Il"
    )



    @app.route('/twitter' , methods = ['GET'])
    def renderTwitter():
        return render_template("twitter.html")
        

    @app.route('/twitter' , methods = ['POST'])
    def postTwitter():

        topic = request.form["inputTopic"]

        # Get 100 tweets from twitter
        def build_test_set(search_keyword):
            try:
                tweets_fetched = twitter_api.GetSearch(search_keyword, count = 10)

                tws = ""
                for status in tweets_fetched:
                    tws += status.text
                    
                return tws
            except:
                return None


        # Clean the text
        def preprocess(text):
            new_text = []
            for t in text.split(" "):
                t = '@user' if t.startswith('@') and len(t) > 1 else t
                t = 'http' if t.startswith('http') else t
                new_text.append(t)
            return " ".join(new_text)


        test_data_set = build_test_set(topic)
        
        if  len(test_data_set) > 1300:
            test_data_set = test_data_set[:1300]


        task='emotion'
        MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

        tokenizer = AutoTokenizer.from_pretrained(MODEL)

        # download label mapping
        mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        labels = [row[1] for row in csvreader if len(row) > 1]


        model = AutoModelForSequenceClassification.from_pretrained(MODEL)

        text =  test_data_set
        text = preprocess(text)
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        
        outcome = []

        for i in range(scores.shape[0]):
            l = labels[ranking[i]]
            s = scores[ranking[i]]
            outcome.append( str(i+1) + " " + l + " " + str(np.round(float(s * 100), 4)) )
               
        
        print('=======================================I did something i think=========================', file=sys.stderr)
        print( outcome , file=sys.stderr)

        return render_template("twitter.html", senti =  outcome , topic = topic)