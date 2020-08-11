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

target_host='127.0.0.1'
target_port=4996
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host,target_port))
message = 'requirements.txt'
client.sendall(message.encode('utf-8'))
client.close()
