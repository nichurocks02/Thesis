#!/usr/bin/python

import os
import time
import hashlib
import sqlite3
from client_db import create_connection
from ecdsa import SigningKey
from onetimepad import *
import socket
import sys
from flask import Flask,request,redirect
from flask import *
from _thread import *
import threading
import select

def key_generation():
    sk = SigningKey.generate() # uses NIST192p #private key
    vk = sk.verifying_key # public key
    private_key = sk.to_string()
    public_key = vk.to_string()
    return [private_key.hex(), public_key.hex()]

app = Flask(__name__)

@app.route('/')
def index():
    return 'welcome to the second node of secret store\n'

@app.route('/generate_key',methods=['GET','POST'])
def generate_key():
    generate=key_generation()
    a=generate[0]
    b=generate[1]
    return a + " , " +b 


   
if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1',port = 7000 )


