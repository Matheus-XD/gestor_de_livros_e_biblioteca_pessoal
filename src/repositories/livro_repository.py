

from database.conection_livros import conectar


def buscar_autor_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM autores WHERE LOWER(nome) = LOWER(?)", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def inserir_autor(nome, nacionalidade=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO autores (nome, nacionalidade) VALUES (?, ?)", (nome, nacionalidade))
    autor_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return autor_id

def listar_livros_por_usuario(usuario_id, status=None):
    conn = conectar()
    cursor = conn.cursor()

    if status:
        cursor.execute('''
            SELECT livros.id, livros.titulo, autores.nome, livros.status, livros.data_inicio, livros.data_fim
            FROM livros
            JOIN autores ON livros.autor_id = autores.id
            WHERE livros.status = ? AND livros.usuario_id = ?
        ''', (status, usuario_id))
    else:
        cursor.execute('''
            SELECT livros.id, livros.titulo, autores.nome, livros.status, livros.data_inicio, livros.data_fim
            FROM livros
            JOIN autores ON livros.autor_id = autores.id
            WHERE livros.usuario_id = ?
        ''', (usuario_id,))
    
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obter_pdf_por_id(id_livro):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT caminho_pdf FROM livros WHERE id = ?", (id_livro,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def listar_autores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, nacionalidade FROM autores")
    autores = cursor.fetchall()
    conn.close()
    return autores

def atualizar_livro_por_id(id_livro, usuario_id, novo_titulo, novo_autor, novo_status, nova_data_inicio, nova_data_fim, caminho_pdf):
    conn = conectar()
    cursor = conn.cursor()

    # Verifica se o livro pertence ao usuário
    cursor.execute("SELECT id FROM livros WHERE id = ? AND usuario_id = ?", (id_livro, usuario_id))
    if cursor.fetchone() is None:
        conn.close()
        return False

    cursor.execute('''
        UPDATE livros
        SET titulo = ?, autor_id = ?, status = ?, data_inicio = ?, data_fim = ?, caminho_pdf = ?
        WHERE id = ? AND usuario_id = ?
    ''', (
        novo_titulo, novo_autor, novo_status,
        nova_data_inicio, nova_data_fim, caminho_pdf,
        id_livro, usuario_id
    ))

    conn.commit()
    conn.close()
    return True


def excluir_livro_por_id(id_livro, usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM livros WHERE id = ? AND usuario_id = ?", (id_livro, usuario_id))
    if cursor.fetchone() is None:
        conn.close()
        return False

    cursor.execute('DELETE FROM livros WHERE id = ? AND usuario_id = ?', (id_livro, usuario_id))
    conn.commit()
    conn.close()
    return True

def inserir_livro_db(titulo, autor_id, status, data_inicio, data_fim, usuario_id, caminho_pdf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO livros (titulo, autor_id, status, data_inicio, data_fim, usuario_id, caminho_pdf)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, autor_id, status, data_inicio, data_fim, usuario_id, caminho_pdf))
    conn.commit()
    conn.close()