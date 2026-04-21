import mysql.connector
from flask import g

def db_connection():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='barang_skincare'
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()