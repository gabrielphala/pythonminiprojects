from flask import render_template , request

import os , csv , re

import twitter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from string import punctuation

from numpy import array2string
import numpy as np
import tensorflow as tf

def twitterSentimentalRoute (app):
    twitter_api = twitter.Api(
        consumer_key="juajwWb814cGSpEYQyI9WNz2T",
        consumer_secret="c6kAI9ki3G1d8kKdp1T7PRcBv6ruw83YtMsuLf43dyvCGfdk96",
        access_token_key="1612739396121272320-b7jG8KHb85eQ7EFhbxWnyVuZh0P72V",
        access_token_secret="3yAZXuOE7MpXMrYuvZU0v1x5zTK4EjLh41hgPOSl0JNru"
    )

    @app.route('/twitter' , methods = ['GET'])
    def renderTwitter():
        return render_template("twitter.html")
        
    @app.route('/twitter' , methods = ['POST'])
    def postTwitter():
        topic = request.form["inputTopic"]

        def build_test_set(search_keyword):
            try:
                tweets_fetched = twitter_api.GetSearch(search_keyword, count=100)

                return [{"text": status.text, "label": None} for status in tweets_fetched]
            except:
                return None

        test_data_set = build_test_set(topic)

        training_data_set = []
        with open(os.path.normpath(os.path.dirname(__file__) + '/../static/data/tweetDataFile.csv'), 'rt',  encoding='utf-8') as csvfile:
            lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
            for row in lineReader:
                training_data_set.append({"tweet_id": row[0], "text": row[1], "label": row[2], "topic": row[3]})

        #preprocessing
        class PreprocessTweets:
            def __init__(self):
                self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

            def process_tweets(self, list_of_tweets):
                processed_tweets = []
                for tweet in list_of_tweets:
                    if tweet["label"] is not None:
                        if tweet["label"] == "positive" or tweet["label"] == "negative":
                            processed_tweets.append((self._process_tweet(tweet["text"]), tweet["label"]))
                    else:
                        processed_tweets.append((self._process_tweet(tweet["text"]), None))

                return processed_tweets

            def _process_tweet(self, tweet):
                tweet = tweet.lower()  # convert text to lower-case
                tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
                tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
                tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
                tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)

                words = []
                for word in tweet:
                    if word not in self._stopwords:
                        words.append(word)
                return words

        tweet_processor = PreprocessTweets()
        preprocessed_training_set = tweet_processor.process_tweets(training_data_set)
        preprocessed_test_set = tweet_processor.process_tweets(test_data_set)

        def build_vocabulary(preprocessed_training_data):
            all_words = []

            for (words, sentiment) in preprocessed_training_data:
                all_words.extend(words)

            wordlist = nltk.FreqDist(all_words)
            word_features = wordlist.keys()

            return word_features

        training_data_features = build_vocabulary(preprocessed_training_set)

        def extract_features(tweet):
            tweet_words = set(tweet)
            features = {}
            for word in training_data_features:
                is_feature_in_words = word in tweet_words
                features[word] = is_feature_in_words
            return features

        training_features = nltk.classify.apply_features(extract_features, preprocessed_training_set)

        NBayesClassifier = nltk.NaiveBayesClassifier.train(training_features)

        label = NBayesClassifier.classify(extract_features("I am happy"))

        classified_result_labels = []
        for tweet in preprocessed_test_set:
            classified_result_labels.append(NBayesClassifier.classify(extract_features(tweet[0])))

        if classified_result_labels.count('positive') > classified_result_labels.count('negative'):
            perc = 100 * classified_result_labels.count('positive') / len(classified_result_labels)
            return render_template("twitter.html", senti = "positively" ,  perc = perc , topic =topic)

        else:
            perc = 100 * classified_result_labels.count('positive') / len(classified_result_labels)
            return render_template("twitter.html", senti = "negatively" ,  perc = perc , topic =topic)

        return render_template("twitter.html")
