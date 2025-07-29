
import sqlite3
import os

def conectar():
    caminho_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), "biblioteca.db")
    return sqlite3.connect(caminho_db)
