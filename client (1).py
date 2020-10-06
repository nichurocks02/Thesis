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
from _thread import *
import threading
import select
import requests
import rsa
import _pickle as cPickle
from flask import Flask, request,redirect
from flask import *
extension='alice.db'

#b = '\'
#a='C:\Users\nishk\OneDrive\Desktop\thesis_sourcecode\Thesis' +
create_connection(extension)


def key_generation(myfile):
    
    document_id = myfile # identifier of the doc simillar to serial number

    with open(myfile,'r') as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes.encode('utf-8')).hexdigest();
    hash_byte=hash.encode('utf-8')
    sk = SigningKey.generate() # uses NIST192p #private key
    vk = sk.verifying_key # public key
    signature = sk.sign(hash_byte)
    skhex = sk.to_string().hex()
    vkhex = vk.to_string().hex()
    return [document_id,hash_byte, skhex,vkhex,signature]
    #assert vk.verify(signature, b"message") -> assertion on wether the verifying_key and SigningKey are true or false (match)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome from the sender client\n'

@app.route('/client_receive',methods=['GET','POST'])
def client_receive():
    value1=request.args.get('name',default = 0 , type = str)
    value2=request.args.get('file',default = 0, type = str)
    
    path = '/home/vars/' + value2
    assertion = os.path.isfile(path)

    x='{"name":"bob","file":"requirements"}'
    y=json.dumps(x)
    #w='aaa'
    if assertion is True :
        a=key_generation(path)
        conn = sqlite3.connect(extension)
        cur = conn.cursor()
        cur.execute('''INSERT INTO client(name,file) VALUES(?,?)''',(value1,value2))
        cur.execute('''INSERT INTO server(contract, doc_key,hash,signature) VALUES (?,?,?,?)''',(y,a[0],a[1],a[-1]))
        conn.commit()
        conn.close()
        return 'request succesfully processed'
    else :
        print('no such file exists')
        return 'no such file exists'
#function for hashing a given file
#elliptic key_generation

@app.route('/add_contract',methods=['GET','POST'])
def add_contract():

    response = redirect("http://127.0.0.1:6000/mine_block?contact={'name':'bob','file':'requirements'}")
    
    return response

@app.route('/senddata',methods=['GET','POST'])
def senddata():
    n=[]
    conn = sqlite3.connect(extension)
    cur = conn.cursor()
    cur.execute("SELECT * FROM server")
    rows = cur.fetchall()
    item=rows[0][1]

    return str(item).encode('utf-8')
    
    

@app.route('/secretkey',methods=['GET','POST'])
def secretkey():
    response = requests.get("http://127.0.0.1:8080/secretstore")
    value = response.content 
    conn = sqlite3.connect(extension)
    cur = conn.cursor()
    cur.execute('''INSERT INTO secretstore (key) VALUES(?)''',(value))
    conn.commit()
    conn.close()
    
    return value

@app.route('/encrypt',methods=['GET','POST'])
def encrypt():
    response = requests.get('http://127.0.0.1:8000/secretstore')
    res = response.content
    print(res)
    value=int(res)
    print(value)
    message = 'Hello from alice'
    a=cipher(message)
    value2=hex(value).lstrip("0x").rstrip("L")
    print(value2)

    value3 = bytearray.fromhex(value2)
    print(type(value2))
    conn = sqlite3.connect(extension)
    cur = conn.cursor()
    cur.execute('''SELECT * FROM  server ''')
    
    rows=cur.fetchall()

    for row in range(len(rows)):
        if row ==0:
            hashing = rows[row][2]
            string = SigningKey.from_string(value3)
            encrypted = string.sign(b'Hello from alice')
        else:
            pass
    return encrypted 
    
if __name__ == '__main__':
   app.run(debug = True, host='127.0.0.1',port = 4000 )