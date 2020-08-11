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
    return [private_key, public_key]

target_host = '127.0.0.1'
target_port = 80
server_host = '127.0.0.1'
server_port = 5001
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,target_port))

msg = client.recv(4096).decode('utf-8')
