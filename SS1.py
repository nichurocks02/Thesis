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

def key_generation():
    sk = SigningKey.generate() # uses NIST192p #private key
    vk = sk.verifying_key # public key
    private_key = sk.to_string()
    public_key = vk.to_string()
    return [private_key,public_key]

bind_ip = '127.0.0.1'
bind_port = 80
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((bind_ip,bind_port))
server.listen(100)
clients=[]
address=[]
clients.append(server)

print('in process')

def handle_client(client_socket,addr):
    global requester
    global doc_key
    global signature
    if addr[1] != 5001  :
        request = client_socket.receive(1024).decode('utf-8')
        data=request.split(',')
        requester=data[0]
        doc_key=data[1]
        signature=data[2]
        message = 'received '
        client_socket.sendall(message.encode('utf-8'))
        print(request)
    return 'success'


while True:
    conn , addr = server.accept()
    clients.append(conn)
    handle_client(conn,addr)
#    client_handler = threading.Thread(target=handle_client,args=(conn,addr))
#    client_handler.start()

conn.close()
server.close()
