from database.conection_livros import conectar
def inserir_usuario(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        return True
    except Exception as e:
        print("Erro ao inserir usuário:", e)
        return False
    finally:
        conn.close()

def buscar_usuario_por_email_senha(email, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario  # (id, nome) ou None
