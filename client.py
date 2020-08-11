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

info=input('enter your name')
extension=info + '.db'
#b = '\'
#a='C:\Users\nishk\OneDrive\Desktop\thesis_sourcecode\Thesis' +
create_connection(extension)

#function for hashing a given file
#elliptic key_generation
a=r"C:\Users\nishk\OneDrive\Desktop\thesis_sourcecode\Thesis\requirements.txt"
def key_generation():
    myfile = r"C:\Users\nishk\OneDrive\Desktop\thesis_sourcecode\Thesis\requirements.txt"
    document_id = cipher(myfile) # identifier of the doc simillar to serial number

    with open(myfile,'r') as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes.encode('utf-8')).hexdigest();
    hash_byte=hash.encode('utf-8')
    sk = SigningKey.generate() # uses NIST192p #private key
    vk = sk.verifying_key # public key
    signature = sk.sign(hash_byte)

    print(sk)
    print((sk.to_string()))
    print(str(vk))
    print(type(signature))
    print(document_id)

    return [document_id,hash_byte, sk.to_string(),vk.to_string(),signature]
    #assert vk.verify(signature, b"message") -> assertion on wether the verifying_key and SigningKey are true or false (match)



sender_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#creates a socket object with address of IPV4 type and TCP socket
sender_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#the above command is used for resuing the address each and every time i restart the program

sender_client_IPaadr = '127.0.0.1'
sender_client_port = 4996
sender_client_addr = sender_client_IPaadr + ':' +str(sender_client_port)
sender_client.bind((sender_client_IPaadr, sender_client_port))
print('server binded at to its ip addr %s and port %s',sender_client_IPaadr,sender_client_port)
sender_client.listen(100)

clients=[]
files = []
address=[]
clients.append(sender_client)

def secret_store(target_host,target_port):
    global a
    sender_client.connect((target_host,target_port))
    a = key_generation()
    conn = sqlite3.connect(extension)
    cur = conn.cursor()
    cur.execute('''INSERT INTO server(contract, doc_key,hash,signature) VALUES (?,?,?,?)''',(str(addr),a[0],a[1],a[-1]))
    cur.commit()
    message = str(addr)+','+a[0]+','+a[-1] #sends contract/requester id its identifier and its signature
    sender_client.sendall(message.encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    sender_client.close()
    conn.close()
    print(response)
    return [response,a[0]]
def handle_client(client_socket,addr):
    request = client_socket.recv(1024).decode('utf-8')
    files.append(request)
    #secret = secret_store(target_host,target_port)
    #secret_sign =
    #conn = sqlite3.connect(extension)
    print(request)
    return request
        #if addr[1] != 80:

while True:
    conn , addr = sender_client.accept()
    target_host='127.0.0.1'
    target_port=80
    print(addr[0]+" has connected")

    clients.append(conn)
    address.append(addr)

    handle_client(conn,addr)
    secret_store(target_host,target_port)
    #start_new_thread(handle_client,(conn,addr))

conn.close()
sender_client.close()
