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

def get_chatlog_stream(message):
    if message['path'] == '/':
        dataobject = message['data'] 
        for sess in dataobject:
            session_dic[sess] = User(dataobject[sess], sess)
        print (session_dic)
    else:
        sessid = message['path'].split('/')[1]
        new_log = dict(db.child("logs").child(sessid).get().val())
        session_dic[sessid] = User(new_log,sessid)

        
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
