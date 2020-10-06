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
        table_creation.execute(''' CREATE TABLE  server1(contract , doc_key,signing_key,verifying_key) ''')
        table_creation.execute('''CREATE TABLE server2 (public_key,private_key)''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return conn
