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
        table_creation.execute(''' CREATE TABLE     client( name,file )   ''')
        table_creation.execute(''' CREATE TABLE     server(contract json, doc_key,hash,signature) ''')
        table_creation.execute(''' CREATE TABLE     secretstore ( key )   ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return conn
