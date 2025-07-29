from database.sessao_usuario import get_usuario_logado
from database.conection_livros import conectar
from repositories.livro_repository import (
    listar_livros_por_usuario, 
    obter_pdf_por_id,
    listar_autores,
    atualizar_livro_por_id,
    excluir_livro_por_id,
    buscar_autor_por_nome,
    inserir_autor,
    inserir_livro_db
    
)
def inserir_ou_obter_autor(nome, nacionalidade=None):
    resultado = buscar_autor_por_nome(nome)
    if resultado:
        return resultado[0]
    return inserir_autor(nome, nacionalidade)

def inserir_livro(titulo, autor_id, status, data_inicio=None, data_fim=None, caminho_pdf=None):
    usuario = get_usuario_logado()
    if usuario is None:
        print("Nenhum usuário logado.")
        return
    usuario_id = usuario[0]
    inserir_livro_db(titulo, autor_id, status, data_inicio, data_fim, usuario_id, caminho_pdf)
def service_listar_livros(status=None):
    usuario = get_usuario_logado()
    if usuario is None:
        print("Nenhum usuário logado.")
        return []
    return listar_livros_por_usuario(usuario_id=usuario[0], status=status)

def service_obter_pdf_por_id(id_livro):
    return obter_pdf_por_id(id_livro)
 
def service_listar_autores():
    return listar_autores()

def service_atualizar_livro(id_livro, novo_titulo, novo_autor_nome, novo_status, nova_data_inicio, nova_data_fim, caminho_pdf):
    usuario = get_usuario_logado()
    if usuario is None:
        print("Nenhum usuário logado.")
        return

    # Buscar o autor pelo nome e obter o ID
    autor = buscar_autor_por_nome(novo_autor_nome)
    if autor:
        autor_id = autor[0]
    else:
        print("Autor não encontrado.")
        return

    # Se o caminho_pdf não foi alterado, manter o que já estava no banco
    if not caminho_pdf:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT caminho_pdf FROM livros WHERE id = ? AND usuario_id = ?", (id_livro, usuario[0]))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            caminho_pdf = resultado[0]

    sucesso = atualizar_livro_por_id(
        id_livro, usuario[0],
        novo_titulo, autor_id, novo_status,
        nova_data_inicio, nova_data_fim, caminho_pdf
    )

    if not sucesso:
        print("Você não tem permissão para editar este livro.")

def service_excluir_livro(id_livro):
    usuario = get_usuario_logado()
    if usuario is None:
        print("Nenhum usuário logado.")
        return
    sucesso = excluir_livro_por_id(id_livro, usuario[0])
    if not sucesso:
        print("Você não tem permissão para excluir este livro.")
