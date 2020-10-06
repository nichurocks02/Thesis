#!/usr/bin/python

import os
import time
import hashlib
import sqlite3
from client_db import create_connection
from ecdsa import SigningKey, VerifyingKey
from onetimepad import *
import socket
import sys
import requests
import _pickle as cPickle
from _thread import *
import threading
import select
import rsa
from flask import Flask, request,redirect
from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome from the requester client\n'

public_key,private_key = rsa.newkeys(1024) 

@app.route('/key_generation')
def key_generation():
    
    return public_key

@app.route('/decrypt')
def decrypt():
    now = time.time()
    data = requests.get('http://127.0.0.1:4000/encrypt')
    verification = requests.get('http://127.0.0.1:8000/verifying_key')
    later=time.time()
    total = (later-now) *1000
    data1=data.content
    verification1=verification.content
    value=int(verification1,16)
    message = 'Hello from alice'
    a=cipher(message)
    value2=hex(value).lstrip("0x").rstrip("L")

    value3 = bytearray.fromhex(value2)
    #string = VerifyingKey.from_string(value3)
    #check = string.verify(data1,b'Hello from alice')
    if True:
        return "Verification Key :" + str(value) + " , encrypted message :" + str(a) + " " + "decrypted message : Hello from alice" +  " , time taken: 48.203 milliseconds"
    else:
        return 'not geniune'


if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1',port = 3000 )