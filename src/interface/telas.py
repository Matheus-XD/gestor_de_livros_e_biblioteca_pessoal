
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog as fd
import shutil
from database.banco import conectar
from database.funcoes_livros import inserir_ou_obter_autor, inserir_livro, listar_livros, atualizar_livro, excluir_livro
from database.funcoes_usuario import cadastrar_usuario, verificar_login
from database.sessao_usuario import set_usuario_logado, get_usuario_logado
from utils.exportar_pdf import exportar_livros_para_pdf


import re
import subprocess


def toggle_fullscreen(event=None):
    janela = event.widget.winfo_toplevel()
    is_fullscreen = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not is_fullscreen)



def tela_inicial():
    janela_inicial = tk.Tk()
    janela_inicial.title("Bem-vindo ao Gerenciador de Livros")
    janela_inicial.attributes("-fullscreen", True)
    janela_inicial.bind_all("<Escape>", toggle_fullscreen)

    # Frame central para manter os botões centralizados
    frame = tk.Frame(janela_inicial, bg="#f0f0f0", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o frame na janela

    # Título
    tk.Label(frame, text="Bem-vindo ao Gerenciador de Livros", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

    # Opções
    tk.Label(frame, text="Selecione uma opção:", font=("Arial", 14)).pack(pady=10)
    tk.Button(frame, text="Login", width=20, command=lambda: abrir_tela_login(janela_inicial), font=("Arial", 12), bg="#4169E1", fg="white").pack(pady=5)
    tk.Button(frame, text="Cadastrar", width=20, command=lambda: abrir_tela_cadastro(janela_inicial), font=("Arial", 12), bg="#4169E1", fg="white").pack(pady=5)

    # Botão de fechar com o mesmo tamanho que os outros botões
    tk.Button(frame, text="Fechar o programa", command=lambda: fechar_programa(janela_inicial), font=("Arial", 12), bg="#F44336", fg="white").pack(pady=5)

    janela_inicial.mainloop()


# Tela cadastro


# Função para validar o formato do email
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|outlook\.com)$'
    return re.match(regex, email) is not None


# tela cadastro

import re  # coloque esse import no início do seu arquivo, se ainda não tiver

def abrir_tela_cadastro(janela_inicial):
    janela_inicial.destroy()
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.attributes("-fullscreen", True)
    janela_cadastro.bind_all("<Escape>", toggle_fullscreen)

    # Frame centralizado
    frame_cadastro = tk.Frame(janela_cadastro, bg="#f0f0f0", padx=20, pady=20)
    frame_cadastro.place(relx=0.5, rely=0.5, anchor="center")

    # Cabeçalho
    tk.Label(frame_cadastro, text="Cadastro de Usuário", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Campos de cadastro
    tk.Label(frame_cadastro, text="Nome:", font=("Arial", 12)).pack(anchor="w", pady=5)
    entry_nome = tk.Entry(frame_cadastro, font=("Arial", 12))
    entry_nome.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_cadastro, text="Email:", font=("Arial", 12)).pack(anchor="w", pady=5)
    entry_email = tk.Entry(frame_cadastro, font=("Arial", 12))
    entry_email.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_cadastro, text="Senha:", font=("Arial", 12)).pack(anchor="w", pady=5)
    entry_senha = tk.Entry(frame_cadastro, show="*", font=("Arial", 12))
    entry_senha.pack(fill="x", padx=10, pady=5)

    # Função para validar email
    def email_valido(email):
        padrao = r"^[\w\.-]+@(?:gmail\.com|hotmail\.com|outlook\.com|yahoo\.com)$"
        return re.match(padrao, email) is not None

    # Função para realizar o cadastro
    def realizar_cadastro():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if not email_valido(email):
            messagebox.showerror("Email inválido", "Use um email válido (@gmail.com, @hotmail.com, etc).")
            return

        sucesso = cadastrar_usuario(nome, email, senha)

        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela_cadastro.destroy()
            tela_inicial()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar usuário.")

    # Função para voltar para a tela inicial
    def voltar_para_tela_inicial():
        janela_cadastro.destroy()
        tela_inicial()  # Chama a função que abre a tela inicial

    # Botões
    tk.Button(frame_cadastro, text="Cadastrar", width=20, height=2, font=("Arial", 12), bg="#4CAF50", fg="white", 
              command=realizar_cadastro).pack(pady=20)

    tk.Button(frame_cadastro, text="Voltar para a Tela Inicial", width=20, height=2, font=("Arial", 12), bg="#f44336", fg="white", 
              command=voltar_para_tela_inicial).pack(pady=10)

    janela_cadastro.mainloop()





# Tela de login

# Função para validar o formato do email
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|outlook\.com)$'
    return re.match(regex, email) is not None

def abrir_tela_login(janela_anterior):
    janela_anterior.destroy()
    janela_login = tk.Toplevel()
    janela_login.title("Login de Usuário")
    janela_login.attributes("-fullscreen", True)
    janela_login.bind_all("<Escape>", toggle_fullscreen)

    # Frame centralizado
    frame_login = tk.Frame(janela_login, bg="#f0f0f0", padx=20, pady=20)
    frame_login.place(relx=0.5, rely=0.5, anchor="center")

    # Cabeçalho
    tk.Label(frame_login, text="Login de Usuário", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Campos de login
    tk.Label(frame_login, text="Email:", font=("Arial", 12)).pack(anchor="w", pady=5)
    entry_email = tk.Entry(frame_login, font=("Arial", 12))
    entry_email.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_login, text="Senha:", font=("Arial", 12)).pack(anchor="w", pady=5)
    entry_senha = tk.Entry(frame_login, show="*", font=("Arial", 12))
    entry_senha.pack(fill="x", padx=10, pady=5)

    # Função para validar o login
    def realizar_login():
        email = entry_email.get()
        senha = entry_senha.get()

        # Verificar se o e-mail é válido
        if not validar_email(email):
            messagebox.showwarning("E-mail inválido", "Digite um e-mail válido, como exemplo@gmail.com.")
            return

        usuario = verificar_login(email, senha)

        if usuario:
            set_usuario_logado(usuario)
            messagebox.showinfo("Bem-vindo", f"Olá, {usuario[1]}!")
            janela_login.destroy()
            abrir_menu_principal()
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    # Função para voltar para a tela inicial
    def voltar_para_tela_inicial():
        janela_login.destroy()
        tela_inicial()  # Chama a função que abre a tela inicial

    # Botões
    tk.Button(frame_login, text="Entrar", width=20, height=2, font=("Arial", 12), bg="#4CAF50", fg="white", 
              command=realizar_login).pack(pady=20)

    tk.Button(frame_login, text="Voltar para a Tela Inicial", width=20, height=2, font=("Arial", 12), bg="#f44336", fg="white", 
              command=voltar_para_tela_inicial).pack(pady=10)

    janela_login.mainloop()


# tela menu principal

def abrir_menu_principal():
    usuario = get_usuario_logado()
    if not usuario:
        messagebox.showerror("Erro", "Nenhum usuário logado.")
        return

    global janela_principal
    janela_principal = tk.Toplevel()
    janela_principal.title("Menu Principal")
    janela_principal.attributes("-fullscreen", True)
    janela_principal.configure(bg="#f0f4fc")  # Fundo claro azul

    janela_principal.bind_all("<Escape>", toggle_fullscreen)

    # Centralização com grid
    for i in range(7):
        janela_principal.rowconfigure(i, weight=1)
    janela_principal.columnconfigure(0, weight=1)

    # Cabeçalho
    tk.Label(
        janela_principal,
        text=f"Bem-vindo(a), {usuario[1]}!",
        font=("Helvetica", 24, "bold"),
        bg="#f0f4fc",
        fg="#2c3e50"
    ).grid(row=0, column=0, pady=10)

    estilo_botao = {
        "width": 30,
        "height": 3,
        "font": ("Arial", 14, "bold"),
        "bg": "#3498db",
        "fg": "white",
        "activebackground": "#2980b9",
        "activeforeground": "white",
        "bd": 0
    }

    # Botões
    tk.Button(
        janela_principal,
        text="Inserir Livro",
        command=abrir_janela_inserir_livro,
        **estilo_botao
    ).grid(row=1, column=0, pady=10)

    tk.Button(
        janela_principal,
        text="Ver Lista de Livros",
        command=lambda: abrir_lista_livros(janela_principal),
        **estilo_botao
    ).grid(row=2, column=0, pady=10)

    tk.Button(
        janela_principal,
        text="Estatísticas de Leitura",
        command=lambda: mostrar_estatisticas(janela_principal),
        **estilo_botao
    ).grid(row=3, column=0, pady=10)

    tk.Button(
        janela_principal,
        text="Sair da conta",
        command=lambda: realizar_logout(janela_principal),
        bg="#e74c3c",
        activebackground="#c0392b",
        **{k: v for k, v in estilo_botao.items() if k not in ["bg", "activebackground"]}
    ).grid(row=4, column=0, pady=30)





# Tela inserir livros
'''def abrir_janela_inserir_livro():
    janela_inserir = tk.Toplevel()
    janela_inserir.title("Inserir Livro")
    janela_inserir.attributes("-fullscreen", True)
    janela_inserir.configure(bg="#f0f0f0")  # cor de fundo suave

    fonte_padrao = ("Arial", 14)

    # Título
    tk.Label(janela_inserir, text="Título do Livro", font=fonte_padrao, bg="#f0f0f0").pack(pady=(40, 5))
    entry_titulo = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_titulo.pack(pady=5)

    # Autor
    tk.Label(janela_inserir, text="Autor", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_autor = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_autor.pack(pady=5)

    

    # Status
    tk.Label(janela_inserir, text="Status", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    combo_status = ttk.Combobox(janela_inserir, values=["Lido", "Lendo", "Quero ler"], font=fonte_padrao, width=38)
    combo_status.pack(pady=5)

    # Data de Início
    tk.Label(janela_inserir, text="Data de Início da leitura", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_inicio = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_inicio.pack(pady=5)

    # Data de Fim
    tk.Label(janela_inserir, text="Data de Fim da leitura", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_fim = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_fim.pack(pady=5)

    # PDF do Livro
    tk.Label(janela_inserir, text="inserir livro (PDF)", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    frame_pdf = tk.Frame(janela_inserir, bg="#f0f0f0")
    frame_pdf.pack(pady=5)

    entry_pdf = tk.Entry(frame_pdf, width=30, font=fonte_padrao)
    entry_pdf.pack(side=tk.LEFT, padx=(0, 10))

    def selecionar_pdf():
        caminho_pdf = fd.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, caminho_pdf)

    tk.Button(frame_pdf, text="Escolher Arquivo", font=fonte_padrao, command=selecionar_pdf).pack(side=tk.LEFT)

    # Botão Salvar
    tk.Button(
        janela_inserir,
        text="Salvar Livro",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        command=lambda: salvar_livro(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf)

    ).pack(pady=20)

    # Botão Voltar
    tk.Button(
        janela_inserir,
        text="Voltar ao Menu",
        font=fonte_padrao,
        bg="#f44336",
        fg="white",
        width=20,
        height=2,
        command=lambda: [janela_inserir.destroy(), abrir_menu_principal()]
    ).pack(pady=10)'''

import tkinter.filedialog as fd

# Tela inserir livros
def abrir_janela_inserir_livro():
    janela_inserir = tk.Toplevel()
    janela_inserir.title("Inserir Livro")
    janela_inserir.attributes("-fullscreen", True)
    janela_inserir.configure(bg="#f0f0f0")  # cor de fundo suave

    fonte_padrao = ("Arial", 14)

    # Título
    tk.Label(janela_inserir, text="Título do Livro", font=fonte_padrao, bg="#f0f0f0").pack(pady=(40, 5))
    entry_titulo = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_titulo.pack(pady=5)

    # Autor
    tk.Label(janela_inserir, text="Autor", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_autor = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_autor.pack(pady=5)

    # Selecionar PDF
    tk.Label(janela_inserir, text="Selecionar PDF do Livro (opcional)", font=fonte_padrao, bg="#f0f0f0").pack(pady=10)

    frame_pdf = tk.Frame(janela_inserir, bg="#f0f0f0")
    frame_pdf.pack(pady=5)

    entry_pdf = tk.Entry(frame_pdf, width=40, font=fonte_padrao)
    entry_pdf.pack(side=tk.LEFT, padx=(0, 10))

    def selecionar_pdf():
        caminho_pdf = fd.askopenfilename(
            title="Selecione o PDF do livro",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho_pdf:
            entry_pdf.delete(0, tk.END)
            entry_pdf.insert(0, caminho_pdf)

    tk.Button(frame_pdf, text="Selecionar PDF", command=selecionar_pdf, font=fonte_padrao, bg="#2196F3", fg="white").pack(side=tk.LEFT)


    # Status
    tk.Label(janela_inserir, text="Status", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    combo_status = ttk.Combobox(janela_inserir, values=["Lido", "Lendo", "Quero ler"], font=fonte_padrao, width=38)
    combo_status.pack(pady=5)

    # Data de Início
    tk.Label(janela_inserir, text="Data de Início da leitura", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_inicio = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_inicio.pack(pady=5)

    # Data de Fim
    tk.Label(janela_inserir, text="Data de Fim da leitura", font=fonte_padrao, bg="#f0f0f0").pack(pady=5)
    entry_fim = tk.Entry(janela_inserir, width=40, font=fonte_padrao)
    entry_fim.pack(pady=5)



    # Botão Salvar
    tk.Button(
        janela_inserir,
        text="Salvar Livro",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        command=lambda: salvar_livro(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf)
    ).pack(pady=20)


    # Botão Voltar
    tk.Button(
        janela_inserir,
        text="Voltar ao Menu",
        font=fonte_padrao,
        bg="#f44336",
        fg="white",
        width=20,
        height=2,
        command=lambda: [janela_inserir.destroy(), abrir_menu_principal()]
    ).pack(pady=10)



def salvar_livro(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf):
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    status = combo_status.get()
    data_inicio = entry_inicio.get()
    data_fim = entry_fim.get()
    caminho_pdf = entry_pdf.get()


    if not titulo or not autor or not status:
        messagebox.showwarning("Campos obrigatórios", "Preencha título, autor e status.")
        return

    # Define o diretório onde os PDFs serão armazenados (dentro da pasta src)
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_destino = os.path.join(diretorio_atual, "livros_pdf")

    # Cria a pasta de PDFs se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Copia o PDF para a pasta do projeto, se tiver sido fornecido
    nome_pdf = ""
    if caminho_pdf:
        nome_arquivo = os.path.basename(caminho_pdf)
        destino_pdf = os.path.join(pasta_destino, nome_arquivo)

        try:
            shutil.copy(caminho_pdf, destino_pdf)
            nome_pdf = os.path.join("livros_pdf", nome_arquivo)  # Caminho relativo
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar o PDF: {str(e)}")
            return

    # Insere no banco
    autor_id = inserir_ou_obter_autor(autor)
    inserir_livro(titulo, autor_id, status, data_inicio, data_fim, caminho_pdf)


    messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
    limpar_campos(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf)


def limpar_campos(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf):
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    combo_status.set("")
    entry_inicio.delete(0, tk.END)
    entry_fim.delete(0, tk.END)
    entry_pdf.delete(0, tk.END)




# Tela ver livros
def abrir_lista_livros(janela_principal):
    janela_principal.destroy()

    def filtrar():
        status_filtrado = combo_filtro.get()
        tree.delete(*tree.get_children())  # Limpa a tabela

        for livro in listar_livros(status=status_filtrado if status_filtrado else None):
            tree.insert("", tk.END, values=livro)

    janela_lista = tk.Toplevel()
    janela_lista.title("Lista de Livros")
    janela_lista.attributes("-fullscreen", True)
    janela_lista.configure(bg="#f2f2f2")

    largura_tela = janela_lista.winfo_screenwidth()
    altura_tela = janela_lista.winfo_screenheight()

    # Título
    tk.Label(janela_lista, text="Lista de Livros", font=("Helvetica", 24, "bold"), bg="#f2f2f2").place(x=largura_tela//2, y=40, anchor="center")

    # Filtro
    tk.Label(janela_lista, text="Filtrar por status:", font=("Arial", 14), bg="#f2f2f2").place(x=largura_tela//2, y=100, anchor="center")
    combo_filtro = ttk.Combobox(janela_lista, values=["", "Lido", "Lendo", "Quero ler"], font=("Arial", 12), width=20)
    combo_filtro.place(x=largura_tela//2, y=140, anchor="center")

    tk.Button(
        janela_lista, 
        text="Aplicar Filtro", 
        font=("Arial", 12), 
        bg="#2196F3", 
        fg="white", 
        width=20, 
        height=2, 
        command=filtrar
    ).place(x=largura_tela//2, y=190, anchor="center")

    # Tabela
    tree = ttk.Treeview(janela_lista, columns=("ID", "Título", "Autor", "Status", "Início", "Fim"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Autor", text="Autor")
    tree.heading("Status", text="Status")
    tree.heading("Início", text="Início")
    tree.heading("Fim", text="Fim")

    for livro in listar_livros():
        tree.insert("", tk.END, values=livro)

    tree.place(x=largura_tela//2, y=altura_tela//2, anchor="center", width=largura_tela - 200, height=400)

    

    #função para abrir o modo leitura ao clicar simples
    def ao_clicar_simples(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            livro_id = valores[0]

            # Buscar o caminho do PDF pelo ID
            caminho_pdf = obter_caminho_pdf_por_id(livro_id)

            if caminho_pdf:
                # Garante o caminho absoluto correto
                caminho_completo = os.path.abspath(caminho_pdf)

                if os.path.exists(caminho_completo):
                    try:
                        os.startfile(caminho_completo)  # Windows
                    except AttributeError:
                        subprocess.call(["open", caminho_completo])  # macOS
                    except Exception:
                        subprocess.call(["xdg-open", caminho_completo])  # Linux
                else:
                    messagebox.showinfo("Arquivo não encontrado", f"PDF não encontrado em:\n{caminho_completo}")
            else:
                messagebox.showinfo("Sem PDF", "Este livro não possui PDF associado.")


    tree.bind("<ButtonRelease-1>", ao_clicar_simples)

    def ao_clicar_direito(event):
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)  # Seleciona o item clicado
            menu_popup.tk_popup(event.x_root, event.y_root)
    tree.bind("<Button-3>", ao_clicar_direito)


    # Menu popup (botão direito)
    menu_popup = tk.Menu(janela_lista, tearoff=0)
    menu_popup.add_command(label="Editar", command=lambda: acao_menu_popup("editar"))
    menu_popup.add_command(label="Excluir", command=lambda: acao_menu_popup("excluir"))

    def acao_menu_popup(acao):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            if acao == "editar":
                abrir_edicao_livro(valores)
            elif acao == "excluir":
                excluir_livro(valores[0])

    # Exportar PDF
    tk.Button(
        janela_lista, 
        text="Exportar Lista em PDF", 
        font=("Arial", 12), 
        bg="#4CAF50", 
        fg="white", 
        width=25, 
        height=2, 
        command=exportar_pdf
    ).place(x=largura_tela//2, y=altura_tela - 120, anchor="center")

    # Voltar ao Menu
    tk.Button(
        janela_lista,
        text="Voltar ao Menu",
        font=("Arial", 12),
        bg="#f44336",
        fg="white",
        width=25,
        height=2,
        command=lambda: [janela_lista.destroy(), abrir_menu_principal()]
    ).place(x=largura_tela//2, y=altura_tela - 60, anchor="center")



def obter_caminho_pdf_por_id(livro_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT caminho_pdf FROM livros WHERE id = ?", (livro_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None






#tela edição
def abrir_edicao_livro(dados):
    id_livro, titulo_atual, autor_atual, status_atual, inicio_atual, fim_atual = dados

    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Livro")
    janela_edicao.geometry("400x300")

    tk.Label(janela_edicao, text="Título:").pack()
    entrada_titulo = tk.Entry(janela_edicao)
    entrada_titulo.insert(0, titulo_atual)
    entrada_titulo.pack()

    tk.Label(janela_edicao, text="Status:").pack()
    combo_status = ttk.Combobox(janela_edicao, values=["Lido", "Lendo", "Quero ler"])
    combo_status.set(status_atual)
    combo_status.pack()

    tk.Label(janela_edicao, text="Data Início (YYYY-MM-DD):").pack()
    entrada_inicio = tk.Entry(janela_edicao)
    entrada_inicio.insert(0, inicio_atual)
    entrada_inicio.pack()

    tk.Label(janela_edicao, text="Data Fim (YYYY-MM-DD):").pack()
    entrada_fim = tk.Entry(janela_edicao)
    entrada_fim.insert(0, fim_atual)
    entrada_fim.pack()

    def salvar_alteracoes():
        novo_titulo = entrada_titulo.get()
        novo_status = combo_status.get()
        nova_data_inicio = entrada_inicio.get()
        nova_data_fim = entrada_fim.get()

        atualizar_livro(id_livro, novo_titulo, novo_status, nova_data_inicio, nova_data_fim)
        janela_edicao.destroy()

    def deletar():
        excluir_livro(id_livro)
        janela_edicao.destroy()

    tk.Button(janela_edicao, text="Salvar Alterações", command=salvar_alteracoes).pack(pady=5)
    tk.Button(janela_edicao, text="Excluir Livro", command=deletar, fg="red").pack()

from database.funcoes_estatisticas import contar_livros_por_mes

#tela estatisticas
def mostrar_estatisticas(janela_principal):
    janela_principal.destroy()
    janela = tk.Toplevel()
    janela.title("Estatísticas de Leitura")
    janela.attributes("-fullscreen", True)
    janela.bind_all("<Escape>", toggle_fullscreen)

    # Frame centralizado
    frame_estatisticas = tk.Frame(janela, bg="#f9f9f9", padx=20, pady=20)
    frame_estatisticas.place(relx=0.5, rely=0.5, anchor="center")

    # Cabeçalho
    tk.Label(frame_estatisticas, text="Estatísticas de Leitura", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Exibição das estatísticas
    estatisticas = contar_livros_por_mes()

    if not estatisticas:
        tk.Label(frame_estatisticas, text="Nenhum dado de leitura encontrado.", font=("Arial", 12)).pack(pady=20)
    else:
        for mes, qtd in sorted(estatisticas.items()):
            tk.Label(frame_estatisticas, text=f"{mes}: {qtd} livro(s)", font=("Arial", 12)).pack(pady=5)

    # Botão Voltar ao Menu
    tk.Button(
        frame_estatisticas,
        text="Voltar ao Menu",
        command=lambda: [janela.destroy(), abrir_menu_principal()],
        width=20, height=2,
        font=("Arial", 12),
        bg="#f44336", fg="white"
    ).pack(pady=20)

    janela.mainloop()


def exportar_pdf():
    exportar_livros_para_pdf()
    messagebox.showinfo("Exportação concluída", "O PDF foi salvo na pasta Downloads.")


def realizar_logout(janela_atual):
    set_usuario_logado(None)
    janela_atual.destroy()
    tela_inicial()  

# Função para fechar o programa corretamente
def fechar_programa(janela_inicial):
    janela_inicial.quit()  # Encerra o loop principal
    janela_inicial.destroy()  # Destrói a janela inicial
    exit()  # Garante que o programa seja finalizado corretamente
