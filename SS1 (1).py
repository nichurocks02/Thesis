#!/usr/bin/python

import os
import time
import hashlib
import sqlite3
from server_db import create_connection
from ecdsa import SigningKey
from onetimepad import *
import socket
import sys
import datetime 
from _thread import *
import threading
import select
from flask import Flask, request,redirect,Response
from flask import *
import requests
global a,b,c,d,e,f,g,h

print(type(g))

 
create_connection('secretstore.db')
app = Flask(__name__)
def key_generation():
    sk = SigningKey.generate() # uses NIST192p #private key
    vk = sk.verifying_key # public key
    private_key = sk.to_string()
    public_key = vk.to_string()
    return [private_key,public_key]
@app.route('/')
def index():
    return 'Welcome from to the secret store\n'


@app.route('/secretstore', methods=['GET','POST'])
def secretstore():
        ss1 = key_generation()
        '''a=requests.get('http://127.0.0.1:4000/senddata')
        b=requests.get('http://127.0.0.1:6000/receive')
        c=a.text
        d=b.text'''
        conn = sqlite3.connect('secretstore.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO server1(contract, doc_key,signing_key,verifying_key) VALUES(?,?,?,?) ''',('bob','requirements',ss1[0],ss1[1]))
        conn.commit()
        conn.close()
        b=ss1[0].hex()
        c=int(b,16)
        return str(c)
    

@app.route('/verifying_key', methods=['GET','POST'])
def verifying_key():
    conn=sqlite3.connect('secretstore.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM server1''')
    rows=cur.fetchall()
    key=rows[0][3]
    c=key.hex()
    d=int(c,16)
    return str(d)



@app.route('/signing_key', methods=['GET','POST'])
def signing_key():
    ss1 = key_generation()
    now = time.time()
    e=requests.get('http://127.0.0.1:7000/generate_key')
    f=requests.get('http://127.0.0.1:7500/generate_key')
    later= time.time()
    g=e.text
    h=f.text  
    hexa=g.split(" , ")
    hexb=h.split(" , ")
    
    public_key1 = ss1[0].hex()+hexa[0]+hexb[0]
    private_key1 = ss1[1].hex()+hexa[0]+hexb[1]
    public_key = int(public_key1,16)
    private_key = int(private_key1,16)
    conn = sqlite3.connect('secretstore.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO server2(public_key,private_key) VALUES(?,?) ''',(public_key1,private_key1))
    conn.commit()
    conn.close()
    return str(public_key)



@app.route('/verification_key', methods=['GET','POST'])
def verification_key():
    conn = sqlite3.connect('secretstore.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM server2''')
    rows = cur.fetchall()
    for row in range(len(rows)):
        if row == 0:
            key = rows[row][1]
        else :
            pass
    conn.commit()
    conn.close()
    return key


if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1',port = 8000 )


