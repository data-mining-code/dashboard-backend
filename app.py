import json
import numpy as np # linear algebr
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from flask import Flask, request
from functools import reduce
import os
import pyrebase
from random import randint
import socket
from textblob import TextBlob

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyD5BJ2gNDZUP9n7m1E7sYD2NjyKBLQgenU",
  "authDomain": "metro-data-mining-chatlog.firebaseapp.com",
  "databaseURL": "https://metro-data-mining-chatlog.firebaseio.com",
  "storageBucket": "metro-data-mining-chatlog.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password('metrodatamining@code.berlin', 'test123')

def start():
  pass
  # get_chatlog
  # get_usertypes
  # get_userneeds
  # save_with_analyzed=True

class User(object):
    """ classifies the attributes of the user and gets the overall sentiment of the users requests """
    def __init__(self, session, timestamp):

        self.log_list = [Request(session['chat'][log]) for log in session['chat']]
        print(self.log_list)
        self.sessionid = timestamp
        self.session = session

    def get_sentiment_overall(self):
        request = [req.get_sentiment() for req in self.log_list]
        sen_array = []
        for sen in request:
            sen_array.append(sen[1])

        if len(sen_array) > 1:
            mean_sen = reduce((lambda x,y: x + y), sen_array) / len(sen_array)
            return mean_sen
        else:
            return sen_array
        pass


class Request(object):

    def __init__(self, log):
        #print(log['request'])
        self.id = id
        self.query = log['request']['query']
        self.client = log['request']['query']['client']
        self.location = log['request']['query']['location']
        self.notmatched = log['request']['query']['notmatched']
        self.productid = log['request']['query']['productid']
        self.product_key_words = log['request']['query']['product_key_words']
        self.question_key_words = log['request']['query']['question_key_words']
        self.question_words = log['request']['query']['question_words']
        self.verb = log['request']['query']['verb']
        self.sentiment = log['request']['sentiment']
        self.sentiment_type = log['request']['type']
        self.text = log['request']['text']
        self.response = log['response']['text']

    def get_sentiment(self):
        string = self.text
        polarity = TextBlob(string)
        pol = polarity.sentiment

        if pol[0] > 0:
            self.sentiment = pol[0]
            self.sentiment_type = 'pos'
        elif pol[0] == 0:
            self.sentiment = pol[0]
            self.sentiment_type = 'neu'
        else:
            self.sentiment = pol[0]
            self.sentiment_type = 'neg'

        return (self.sentiment_type, self.sentiment)



def get_chatlog(logs):
    users = {}
    for session in logs:
        users[session] = (User(logs[session], session))
    return users


def  get_usertypes():
  # classify each user into one of the three user types
  # and create a list out of them
  pass

def get_userneeds():
  # classify each request's intent
  # and also create a list out of them
  pass

def get_all_():
  pass


@app.route("/")
def hello():
  input = {}
  return input

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
