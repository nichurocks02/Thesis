#!/usr/bin/python

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        table_creation = conn. cursor()
        table_creation.execute(''' CREATE TABLE     server1(contract, doc_key,hash,signature,server_key,public_key,private_key,timestamp) ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return conn
