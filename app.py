import json
import numpy as np # linear algebr
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pyrebase
import socket
from flask import Flask, request
from random import randint
from UserClass import User, Request


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


## Get new Chatlogs, update the local dic and aggregate the new ones
def get_chatlog_stream(message):
    if message['path'] == '/':
        dataobject = message['data'] 
        for sess in dataobject:
            session_dic[sess] = User(dataobject[sess], sess)
            if session_dic[sess].usertype == "":
                aggregateData(session_dic[sess])
    else:
        sessid = message['path'].split('/')[1]
        new_log = dict(db.child("logs").child(sessid).get().val())
        session_dic[sessid] = User(new_log,sessid)
        aggregateData(session_dic[sessid])

def aggregateData(UserObj):
    UserObj.get_sentiment_overall()
    UserObj.get_questions_asked()
    UserObj.get_shops_asked()
    UserObj.get_products_asked()

## These Methods are called when the Call from Frontend comes        
def  get_usertypes():
    # classify each user into one of the three user types
    # and create a list out of them
    pass

def get_userneeds():
    # classify each request's intent
    # and also create a list out of them
    pass

def top_questions_asked():
    # Get the questions that were most often asked
    pass

def top_shops_asked():
    # Get the shops that were most often asked
    pass

def top_products_asked():
    # Get the products that were most often asked
    product_resp = {}
    # Get the products that were most often asked
    all_products_asked_for = []
    for sess in sessdic:
        for prdct in sessdic[sess].products_asked:
            all_products_asked_for.append(prdct)
    counted = Counter(all_products_asked_for)
    for counted_p in counted:
        product_resp[counted_p] = {'times': counted[counted_p], 'percent': counted[counted_p] / len(all_products_asked_for)}
    return product_resp


## MAIN ##
session_dic = {}
dataobject = ""        
my_stream = db.child("logs").stream(get_chatlog_stream)


@app.route("/")
def hello():
  input = {}
  return input

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
