import streamlit as st
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# Criar a tabela de livros
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano INTEGER NOT NULL
)
''')
conn.commit()

st.title("📚 Biblioteca Digital")

# Adicionar novo livro
with st.form("add_book_form"):
    
    
    if cadastrar:
        cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)", (titulo, autor, ano))
        conn.commit()
        st.success(f"Livro '{titulo}' adicionado com sucesso!")

# Listar acervo
dados = cursor.execute("SELECT * FROM livros").fetchall()
st.subheader("📖 Acervo da Biblioteca")
for livro in dados:
    st.write(f"{livro[0]} - {livro[1]} ({livro[2]}, {livro[3]})")

# Atualizar informações de um livro
st.subheader("✏️ Atualizar Livro")
id_livro = st.number_input("ID do Livro para Atualizar", min_value=1, step=1)
novo_titulo = st.text_input("Novo Título")
novo_autor = st.text_input("Novo Autor")
novo_ano = st.number_input("Novo Ano", min_value=1000, max_value=9999, step=1)
if st.button("Atualizar Livro"):
    cursor.execute("UPDATE livros SET titulo=?, autor=?, ano=? WHERE id=?", (novo_titulo, novo_autor, novo_ano, id_livro))
    conn.commit()
    st.success("Livro atualizado com sucesso!")

# Excluir livro
st.subheader("🗑️ Excluir Livro")
id_excluir = st.number_input("ID do Livro para Excluir", min_value=1, step=1)
if st.button("Excluir Livro"):
    cursor.execute("DELETE FROM livros WHERE id=?", (id_excluir,))
    conn.commit()
    st.warning("Livro excluído!")

# Buscar livros por autor
st.subheader("🔎 Buscar por Autor")
busca_autor = st.text_input("Digite o nome do autor")
if st.button("Buscar"):
    resultados = cursor.execute("SELECT * FROM livros WHERE autor LIKE ?", (f"%{busca_autor}%",)).fetchall()
    for livro in resultados:
        st.write(f"{livro[0]} - {livro[1]} ({livro[2]}, {livro[3]})")

conn.close()
