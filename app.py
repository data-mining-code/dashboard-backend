import json
import numpy as np # linear algebr
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pyrebase
import socket
from flask import Flask, request
from random import randint
from UserClass import User, Request
from collections import Counter
from time import sleep

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
    print('Got Something', message)
    sleep(2)
    if message['path'] == '/':
        print('Everything')
        dataobject = message['data']
        for sess in dataobject:
            session_dic[sess] = User(dataobject[sess], sess)
            if session_dic[sess].usertype == "":
                aggregateData(session_dic[sess])
                db.child("logs").child(sess).set(session_dic[sess].firebase_save_format())
    else:
        print('Something')
        sessid = message['path'].split('/')[1]
        new_log = dict(db.child("logs").child(sessid).get().val())
        session_dic[sessid] = User(new_log,sessid)
        aggregateData(session_dic[sessid])
        db.child("logs").child(sessid).set(session_dic[sessid].firebase_save_format())

def aggregateData(UserObj):
    UserObj.get_usertype()
    UserObj.get_questions_asked()
    UserObj.get_shops_asked()
    UserObj.get_products_asked()

## These methods are called when the call form the frontend comes
def get_products_shops_user_type(resp,stats):
    # Get the products that were most often asked
    all_products_asked_for = []
    all_shops_asked_for = []
    all_types = []
    all_questions_cmp_string = []
    all_questions_dic = {}
    for sess in session_dic:
        for prdct in session_dic[sess].products_asked:
            all_products_asked_for.append(prdct)
        for shp in session_dic[sess].shops_asked:
            all_shops_asked_for.append(shp)
        for qst in session_dic[sess].questions_asked:
            all_questions_cmp_string.append(qst)
            if not qst in all_questions_dic:
                all_questions_dic[qst] = session_dic[sess].questions_asked[qst]
        all_types.append(session_dic[sess].usertype)

    products_count = Counter(all_products_asked_for).most_common(5)
    shops_count = Counter(all_shops_asked_for).most_common(5)
    type_count = Counter(all_types)
    questions_count = Counter(all_questions_cmp_string).most_common(3)

    resp['product'] = {}
    resp['shops'] = {}
    resp['user_type'] = {}
    resp['question'] = {}
    resp['stats'] = {}
    
    for product in products_count:
        resp['product'][product[0]] = {'times': product[1], 'percent': product[1] / len(all_products_asked_for)}
    for shops in shops_count:
        resp['shops'][shops[0].title()] = {'times': shops[1], 'percent': shops[1] / len(all_shops_asked_for)}
    for user_type in type_count:
        resp['user_type'][user_type] = {'times': type_count[user_type], 'percent': type_count[user_type] / len(all_types)}
    for question in questions_count:
        resp['question'][question[0]] = {'string': all_questions_dic[question[0]], 'times': question[1], 'percent': question[1] / len(all_questions_cmp_string)}
    for stat in stats:
        resp['stats'][stat] = stats[stat]
    return resp

## MAIN ##
global session_dic
session_dic = {}
#dataobject = ""
#my_stream = db.child("logs").stream(get_chatlog_stream)


@app.route("/")
def hello():
    stats = dict(db.child("stats").get().val())
    data = dict(db.child("logs").get().val())
    for sess in data:
        session_dic[sess] = User(data[sess], sess)
        if session_dic[sess].usertype == "":
            aggregateData(session_dic[sess])
            db.child("logs").child(sess).set(session_dic[sess].firebase_save_format())
    resp = {}
    resp = get_products_shops_user_type(resp,stats)
    resp_json = json.dumps(resp)
    return resp_json

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
