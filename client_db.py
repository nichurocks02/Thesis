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
        table_creation.execute(''' CREATE TABLE     client (sender, requester, doc_key, hash, signature,  timestamp , server_key  )   ''')
        table_creation.execute(''' CREATE TABLE     server(contract, doc_key,hash,signature) ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return conn
