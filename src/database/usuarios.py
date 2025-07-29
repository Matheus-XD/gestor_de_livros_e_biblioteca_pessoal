from .banco import conectar

def cadastrar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', (username, senha))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def verificar_login(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE username=? AND senha=?', (username, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
