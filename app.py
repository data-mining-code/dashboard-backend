from flask import Flask, request
import json
import numpy as np # linear algebr
import os
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pyrebase
from random import randint
import socket
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

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
  def __init__(self, id, request, analyzed=False, sentiment="", type=""):
    self.id = id
    self.sentiment = sentiment
    self.request = request
    self.analyzed = analyzed
    self.type = type

  def get_sentiment(self):
    
    return self.sentiment

  def get_type(self):
    if self.sentiment > 0:
      self.type = "positive"
    elif self.sentiment < 0:
      self.type = "negative"
    else:
      self.type = "neutral"
    return self.type
      
  def __repr__(self):
    return ('Id: ', self.id, 'Anzahl Requests: ', len(self.request))
  # attr ID, Sentiment, all request, analyzed=true/false
  # method sentiment, positive and complaints


user1 = User(11,0,['hallo', 'moin', 'test'])


class Request(object):
  def __init__(self, log):
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
    self.sentiment_type = log['request']['sentiment_type']
    self.text = log['request']['text']
    self.response = log['response']['text']



  def get_sentiment(self):
    string = self.text

    objectivity = TextBlob(string)
    obj = objectivity.sentiment

    if obj[1] == 0:
        self.sentiment = ['neu', 0, 0]
        return (self.sentiment)
    else:
        sentiment = TextBlob(string, analyzer=NaiveBayesAnalyzer())
        sen = sentiment.sentiment
        return ([sen[0], sen[1], sen[2]])
  # attr id, sentiment, timestamp, intents, input string, 
  # method sentiment



def get_chatlog(db):
  # iterate through database and process it to make it available for later actions
  # listen to db and update if sth has changed
  pass

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

