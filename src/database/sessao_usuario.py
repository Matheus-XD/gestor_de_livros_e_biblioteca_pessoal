usuario_logado = None
import sqlite3
import os
def set_usuario_logado(usuario):
    global usuario_logado
    usuario_logado = usuario

def get_usuario_logado():
    return usuario_logado

def logout():
    global usuario_logado
    usuario_logado = None


def verificar_login(email, senha):
    caminho_db = os.path.join(os.path.dirname(__file__), "..", "biblioteca.db")
    conexao = sqlite3.connect(caminho_db)
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()

    conexao.close()
    return usuario

