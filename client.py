#!/usr/bin/python

import os
import time
import hashlib
from client_db import create_connection
from ecdsa import SigningKey

info=input('enter your name')
extension=info + '.db'
#b = '\'
#a='C:\Users\nishk\OneDrive\Desktop\thesis_sourcecode\Thesis' +
create_connection(extension)

#function for hashing a given file
def file(myfile):

    with open(myfile,'r') as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes).hexdigest();

    return hash
#elliptic key_generation
def key_generation():
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    signature = sk.sign(file(myfile))

    #assert vk.verify(signature, b"message") -> assertion on wether the verifying_key and SigningKey are true or false (match)
