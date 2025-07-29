import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog as fd
import shutil
from database.banco import conectar
from services.livro_service import inserir_ou_obter_autor, buscar_autor_por_nome, inserir_livro, service_listar_livros, service_atualizar_livro, service_excluir_livro
from services.usuario_service import service_cadastrar_usuario, service_verificar_login
from database.sessao_usuario import set_usuario_logado, get_usuario_logado
from utils.exportar_pdf import exportar_livros_para_pdf
from PIL import Image, ImageTk
import re
import subprocess
import sqlite3

def toggle_fullscreen(event=None):
    janela = event.widget.winfo_toplevel()
    is_fullscreen = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not is_fullscreen)


def criar_botao(master, texto, comando, cor_original="#4169E1", cor_hover="#27408B", cor_texto="white"):
    botao = tk.Button(
        master,
        text=texto,
        command=comando,
        font=("Arial", 15),
        bg=cor_original,
        fg=cor_texto,
        relief="flat",
        width=20,
        height=2,
        bd=0,
        highlightthickness=0,
    )
    botao.config(cursor="hand2")

    def on_enter(e):
        botao['bg'] = cor_hover

    def on_leave(e):
        botao['bg'] = cor_original

    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

    return botao


#Tela Inicial
def tela_inicial(janela_inicial):
    # Configurações da janela
    janela_inicial.title("Bem-vindo ao Gerenciador de Livros")
    janela_inicial.state('zoomed') 
    janela_inicial.bind_all("<Escape>", toggle_fullscreen)

    janela_inicial.update()

    # Dimensões da tela
    largura = janela_inicial.winfo_screenwidth()
    altura = janela_inicial.winfo_screenheight()

    # Caminho da imagem (pode ser relativo, se preferir portabilidade)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_imagem = os.path.join(BASE_DIR, "interface", "imagem", "e-books.jpg")
    imagem = Image.open(caminho_imagem)
    imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
    fundo_img = ImageTk.PhotoImage(imagem)

    # Define a imagem de fundo
    fundo_label = tk.Label(janela_inicial, image=fundo_img)
    fundo_label.image = fundo_img  # mantém referência
    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Título no topo
    tk.Label(
        janela_inicial, 
        text="Bem-vindo ao Gerenciador de Livros", 
        font=("Helvetica", 26, "bold")
    ).place(x=largura//2, y=100, anchor="center")


    # Frame centralizado com os botões
    frame = tk.Frame(janela_inicial, bg="", padx=0, pady=0)
    frame.place(relx=0.50, rely=0.56, anchor="center")

    tk.Label(frame, text="Selecione uma opção:", font=("Arial", 20)).pack(pady=10)

    criar_botao(frame, "Login", lambda: abrir_tela_login(janela_inicial), cor_original="#4169E1", cor_hover="#000000").pack(pady=7)
    criar_botao(frame, "Cadastrar", lambda: abrir_tela_cadastro(janela_inicial), cor_original="#4169E1", cor_hover="#000000").pack(pady=7)
    criar_botao(frame, "Fechar o programa", lambda: fechar_programa(janela_inicial), cor_original="#F44336", cor_hover="#000000").pack(pady=7)



# Tela cadastro

# Função para validar o formato do email
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|outlook\.com)$'
    return re.match(regex, email) is not None


# Função para abrir a tela de cadastro
def abrir_tela_cadastro(janela_inicial):
    janela_inicial.withdraw()  # Esconde a janela inicial
    
    # Criando uma nova janela (Toplevel)
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.state('zoomed') 
    janela_cadastro.bind_all("<Escape>", toggle_fullscreen)  # Bind do teclado para tela cheia
    
    # Tamanho da tela
    largura = janela_cadastro.winfo_screenwidth()
    altura = janela_cadastro.winfo_screenheight()

    # Caminho da imagem de fundo
    caminho_imagem = os.path.join(os.path.dirname(__file__), "imagem", "cadastro.png")

    try:
        # Carregar e redimensionar a imagem
        imagem = Image.open(caminho_imagem)
        imagem = imagem.resize((largura, altura), Image.Resampling.LANCZOS)
        imagem_fundo = ImageTk.PhotoImage(imagem)

        # Label de fundo da janela principal
        label_fundo = tk.Label(janela_cadastro, image=imagem_fundo)
        label_fundo.image = imagem_fundo  # Mantém referência
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        messagebox.showwarning("Imagem não encontrada", f"Não foi possível carregar a imagem:\n{caminho_imagem}")

    # Frame centralizado com fundo branco
    frame_cadastro = tk.Frame(janela_cadastro, bg="#FFFFFF", padx=0, pady=0)

    # Posicionando o frame centralizado
    frame_cadastro.place(relx=0.25, rely=0.5, anchor="center")

    # Cabeçalho
    tk.Label(frame_cadastro, text="Cadastro de Usuário", font=("Helvetica", 28, "bold"), bg="#FFFFFF").pack(pady=20)

    # Campos de cadastro
    tk.Label(frame_cadastro, text="Nome:", font=("Arial", 18), bg="#FFFFFF").pack(anchor="w", pady=5)
    entry_nome = tk.Entry(frame_cadastro, font=("Arial", 15), bg="#e2e2e2", fg="#00210f")
    entry_nome.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_cadastro, text="Email:", font=("Arial", 18), bg="#FFFFFF").pack(anchor="w", pady=5)
    entry_email = tk.Entry(frame_cadastro, font=("Arial", 15), bg="#e2e2e2", fg="#00210f")
    entry_email.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_cadastro, text="Senha:", font=("Arial", 18), bg="#FFFFFF").pack(anchor="w", pady=5)
    entry_senha = tk.Entry(frame_cadastro, show="*", font=("Arial", 15), bg="#e2e2e2", fg="#00210f")
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

        sucesso = service_cadastrar_usuario(nome, email, senha)

        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            janela_cadastro.withdraw()
            janela_inicial.deiconify() # Chama a função que abre a tela inicial
            tela_inicial(janela_inicial)

        else:
            messagebox.showerror("Erro", "Erro ao cadastrar usuário.")

    # Função para voltar para a tela inicial
    def voltar_para_tela_inicial():
        janela_cadastro.withdraw()
        janela_inicial.deiconify() # Chama a função que abre a tela inicial
        tela_inicial(janela_inicial)

    # Botões
    frame_botoes = tk.Frame(frame_cadastro)
    frame_botoes.pack(pady=20)  # Espaçamento vertical entre os campos e os botões

    # Botão Entrar
    tk.Button(
        frame_botoes, text="Cadastrar", width=18, height=2,
        font=("Arial", 15), bg="#4CAF50", fg="white",
        command=realizar_cadastro
    ).pack(side="left", padx=10)  # Espaçamento horizontal entre os botões

    # Botão Voltar para a Tela Inicial
    tk.Button(
        frame_botoes, text="Home", width=18, height=2,
        font=("Arial", 15), bg="#f44336", fg="white",
        command=voltar_para_tela_inicial
    ).pack(side="left", padx=10)

    # tk.Button(frame_cadastro, text="Cadastrar", width=20, height=2, font=("Arial", 12), bg="#4CAF50", fg="white", 
    #         command=realizar_cadastro).pack(pady=20)

    # tk.Button(frame_cadastro, text="Voltar para a Tela Inicial", width=20, height=2, font=("Arial", 12), bg="#f44336", fg="white", 
    #         command=voltar_para_tela_inicial).pack(pady=10)







# Tela de login

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|outlook\.com)$'
    return re.match(regex, email) is not None

def abrir_tela_login(janela_inicial):
    # Oculta a tela anterior
    janela_inicial.withdraw()

    # Cria nova janela de login
    janela_login = tk.Toplevel()
    janela_login.title("Login de Usuário")
    janela_login.state('zoomed') 
    janela_login.bind_all("<Escape>", lambda e: janela_login.attributes("-fullscreen", False))  # Permite alternar entre fullscreen

    # Caminho relativo para a imagem de fundo
    caminho_imagem = os.path.join(os.path.dirname(__file__), "imagem", "login.png")
    
    try:
        # Carregar e redimensionar a imagem
        imagem_fundo = Image.open(caminho_imagem)
        largura = janela_login.winfo_screenwidth()
        altura = janela_login.winfo_screenheight()
        imagem_fundo = imagem_fundo.resize((largura, altura), Image.Resampling.LANCZOS)
        img_fundo = ImageTk.PhotoImage(imagem_fundo)

        # Label para imagem de fundo na janela_login
        label_fundo = tk.Label(janela_login, image=img_fundo)
        label_fundo.image = img_fundo  # Mantém referência da imagem
        label_fundo.place(x=0, y=0, relwidth=1, relheight=1)  # Posiciona a imagem de fundo

    except FileNotFoundError:
        messagebox.showerror("Erro", f"Imagem não encontrada no caminho: {caminho_imagem}")
        return

    # Frame central (sem adicionar imagem de fundo novamente)
    frame_login = tk.Frame(janela_login, bg="", padx=50, pady=50)

    # Posicionando o frame centralizado
    frame_login.place(relx=0.25, rely=0.47, anchor="center")

    # Título
    tk.Label(frame_login, text="Login de Usuário", font=("Helvetica", 28, "bold"), bg = "#FFFFFF").pack(pady=20)

    # E-mail
    tk.Label(frame_login, text="Email:", font=("Arial", 18), bg = "#FFFFFF").pack(anchor="w", pady=5)
    entry_email = tk.Entry(frame_login, font=("Arial", 15), bg="#e2e2e2", fg="#00210f")  # Cor escura de fundo, texto branco
    entry_email.pack(fill="x", padx=8, pady=4)

    # Senha
    tk.Label(frame_login, text="Senha:", font=("Arial", 18), bg = "#FFFFFF").pack(anchor="w", pady=5)
    entry_senha = tk.Entry(frame_login, show="*", font=("Arial",18), bg="#e2e2e2", fg="#00210f")  # Cor escura de fundo, texto branco
    entry_senha.pack(fill="x", padx=8, pady=4)

    # Função de login
    def realizar_login():
        email = entry_email.get()
        senha = entry_senha.get()

        # Verificar se os campos estão vazios
        if not email or not senha:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
            return

        if not validar_email(email):
            messagebox.showwarning("E-mail inválido", "Digite um e-mail válido, como exemplo@gmail.com.")
            return

        usuario = service_verificar_login(email, senha)

        if usuario:
            set_usuario_logado(usuario)
            messagebox.showinfo("Bem-vindo", f"Olá, {usuario[1]}!")
            janela_login.withdraw()
            abrir_menu_principal()
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    # Função de voltar
    def voltar_para_tela_inicial():
        janela_login.withdraw()
        janela_inicial.deiconify()
        tela_inicial(janela_inicial)

    # Botões Login
    frame_botoes = tk.Frame(frame_login)
    frame_botoes.pack(pady=20)  # Espaçamento vertical entre os campos e os botões

    # Botão Entrar
    tk.Button(
        frame_botoes, text="Entrar", width=18, height=2,
        font=("Arial", 15), bg="#4CAF50", fg="white",
        command=realizar_login
    ).pack(side="left", padx=10)  # Espaçamento horizontal entre os botões

    # Botão Voltar para a Tela Inicial
    tk.Button(
        frame_botoes, text="Home", width=18, height=2,
        font=("Arial", 15), bg="#f44336", fg="white",
        command=voltar_para_tela_inicial
    ).pack(side="left", padx=10)

    janela_login.mainloop()


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


def abrir_menu_principal():
    usuario = get_usuario_logado()
    if not usuario:
        messagebox.showerror("Erro", "Nenhum usuário logado.")
        return

    # Criar janela principal
    global janela_principal
    janela_principal = tk.Toplevel()
    janela_principal.title("Menu Principal")
    janela_principal.state('zoomed')  # Tela cheia

    # Carregar imagem de fundo
    imagem_tk = carregar_imagem_fundo(janela_principal)

    # Exibir imagem como fundo
    label_fundo = tk.Label(janela_principal, image=imagem_tk)
    label_fundo.image = imagem_tk  # evitar garbage collection
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # Container central
    container = tk.Frame(janela_principal, bg="white")
    container.place(relx=0.22, rely=0.47, anchor="center")

    # Cabeçalho
    tk.Label(
        container,
        text=f"Bem-vindo(a), {usuario[1]}!",
        font=("Helvetica", 24, "bold"),
        fg="#2c3e50",
        bg="white"
    ).pack(pady=20)

    # Botões do menu
    botoes = [
        ("Inserir Livro", lambda: [janela_principal.destroy(), abrir_janela_inserir_livro()]),
        ("Ver Lista de Livros", lambda: abrir_lista_livros(janela_principal)),
        ("Estatísticas de Leitura", lambda: mostrar_estatisticas(janela_principal)),
        ("Fechar o programa", lambda: fechar_programa(janela_principal)),
    ]

    estilo_botao = {
        "width": 30,
        "height": 2,
        "font": ("Arial", 14, "bold"),
        "fg": "white",
        "activeforeground": "white",
        "bd": 3,
        "relief": "raised",
        "highlightthickness": 0,
    }

    frame_botoes = tk.Frame(container, bg="white")
    frame_botoes.pack()

    for texto, comando in botoes:
        cor_normal = "#e74c3c" if "Fechar" in texto else "#3498db"
        cor_hover = "#c0392b" if "Fechar" in texto else "#2980b9"

        botao = tk.Button(
            frame_botoes,
            text=texto,
            command=comando,
            bg=cor_normal,
            activebackground=cor_hover,
            **{k: v for k, v in estilo_botao.items() if k not in ["bg", "activebackground"]}
        )
        botao.bind("<Enter>", lambda e, b=botao, c=cor_hover: b.config(bg=c))
        botao.bind("<Leave>", lambda e, b=botao, c=cor_normal: b.config(bg=c))
        botao.pack(pady=12)

    # Frame de conteúdo dinâmico
    global frame_conteudo
    frame_conteudo = tk.Frame(janela_principal, bg="white")
    frame_conteudo.place(relx=0.7, rely=0.5, anchor="center")

    janela_principal.bind_all("<Escape>", lambda e: toggle_fullscreen(e, janela=janela_principal))




def carregar_imagem_fundo(janela_principal):
    caminho_imagem = os.path.join(os.path.dirname(__file__), "imagem", "principal.png")
    imagem_fundo = Image.open(caminho_imagem).convert("RGBA")
    largura = janela_principal.winfo_screenwidth()
    altura = janela_principal.winfo_screenheight()
    imagem_fundo = imagem_fundo.resize((largura, altura), Image.LANCZOS)
    return ImageTk.PhotoImage(imagem_fundo)





# Tela inserir livros

def abrir_janela_inserir_livro():
    janela_inserir = tk.Toplevel()
    janela_inserir.title("Inserir Livro")
    janela_inserir.state('zoomed')
    janela_inserir.configure(bg="#e6f2ff")  # tom azul claro agradável

    fonte_titulo = ("Arial", 24, "bold")
    fonte_padrao = ("Arial", 14)

    # Container principal centralizado
    container = tk.Frame(janela_inserir, bg="#ffffff", bd=2, relief="groove")
    container.place(relx=0.5, rely=0.5, anchor="center")

    # Título da Janela
    tk.Label(container, text="Cadastro de Novo Livro", font=fonte_titulo, bg="#ffffff", fg="#333").pack(pady=(30, 20))

    def criar_entrada(rotulo, entry_var=None, tipo="entry"):
        tk.Label(container, text=rotulo, font=fonte_padrao, bg="#ffffff", anchor="w").pack(fill="x", padx=30, pady=(10, 2))
        if tipo == "entry":
            entrada = tk.Entry(container, width=50, font=fonte_padrao)
        elif tipo == "combo":
            entrada = ttk.Combobox(container, values=["Lido", "Lendo", "Quero ler"], font=fonte_padrao, width=48)
        entrada.pack(padx=30, pady=2)
        return entrada

    entry_titulo = criar_entrada("Título do Livro")
    entry_autor = criar_entrada("Autor")

    # PDF
    tk.Label(container, text="Selecionar PDF do Livro (opcional)", font=fonte_padrao, bg="#ffffff").pack(fill="x", padx=30, pady=(10, 2))
    frame_pdf = tk.Frame(container, bg="#ffffff")
    frame_pdf.pack(padx=30, pady=5, fill="x")

    entry_pdf = tk.Entry(frame_pdf, width=42, font=fonte_padrao)
    entry_pdf.pack(side=tk.LEFT, padx=(0, 10))

    def selecionar_pdf():
        caminho_pdf = fd.askopenfilename(title="Selecione o PDF do livro", filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho_pdf:
            entry_pdf.delete(0, tk.END)
            entry_pdf.insert(0, caminho_pdf)

    tk.Button(frame_pdf, text="Selecionar PDF", command=selecionar_pdf,
              font=("Arial", 12, "bold"), bg="#2196F3", fg="white", padx=10).pack(side=tk.LEFT)

    combo_status = criar_entrada("Status", tipo="combo")
    entry_inicio = criar_entrada("Data de Início da leitura")
    entry_fim = criar_entrada("Data de Fim da leitura")

    # Botões
    frame_botoes = tk.Frame(container, bg="#ffffff")
    frame_botoes.pack(pady=30)

    tk.Button(frame_botoes, text="Salvar Livro", font=("Arial", 14, "bold"),
              bg="#4CAF50", fg="white", width=18, height=2,
              command=lambda: salvar_livro(entry_titulo, entry_autor, combo_status, entry_inicio, entry_fim, entry_pdf)
              ).pack(side=tk.LEFT, padx=20)

    tk.Button(frame_botoes, text="Voltar ao Menu", font=("Arial", 14, "bold"),
              bg="#f44336", fg="white", width=18, height=2,
              command=lambda: [janela_inserir.destroy(), abrir_menu_principal()]
              ).pack(side=tk.LEFT, padx=20)



#função salvar livro

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

    # Define o diretório onde os PDFs serão armazenados (src/interface/livros_pdf)
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_destino = os.path.join(diretorio_atual, "..", "interface", "livros_pdf")
    pasta_destino = os.path.abspath(pasta_destino)

    # Cria a pasta de PDFs se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    nome_pdf = ""
    if caminho_pdf:
        nome_arquivo = os.path.basename(caminho_pdf)
        destino_pdf = os.path.join(pasta_destino, nome_arquivo)

        try:
            shutil.copy(caminho_pdf, destino_pdf)
            # Caminho relativo começando por Gestor-de-Leitura-e-Biblioteca-Pessoal
            nome_pdf = os.path.join(
                "Gestor-de-Leitura-e-Biblioteca-Pessoal", "src", "interface", "livros_pdf", nome_arquivo
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar o PDF: {str(e)}")
            return

    # Insere no banco
    autor_id = inserir_ou_obter_autor(autor)
    inserir_livro(titulo, autor_id, status, data_inicio, data_fim, nome_pdf)

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
        for livro in service_listar_livros(status=status_filtrado if status_filtrado else None):
            tree.insert("", tk.END, values=livro)

    janela_lista = tk.Toplevel()
    janela_lista.title("Lista de Livros")
    janela_lista.state('zoomed')
    janela_lista.configure(bg="#f2f2f2")

    largura_tela = janela_lista.winfo_screenwidth()
    altura_tela = janela_lista.winfo_screenheight()

    fonte_titulo = ("Helvetica", 26, "bold")
    fonte_padrao = ("Arial", 14)
    fonte_tabela = ("Arial", 13)

    # Título
    tk.Label(janela_lista, text="📚 Lista de Livros", font=fonte_titulo, bg="#f2f2f2", fg="#333").pack(pady=(30, 10))

    # Filtro
    filtro_frame = tk.Frame(janela_lista, bg="#f2f2f2")
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Filtrar por status:", font=fonte_padrao, bg="#f2f2f2").pack(side=tk.LEFT, padx=10)
    combo_filtro = ttk.Combobox(filtro_frame, values=["", "Lido", "Lendo", "Quero ler"], font=fonte_padrao, width=20)
    combo_filtro.pack(side=tk.LEFT, padx=10)

    tk.Button(
        filtro_frame,
        text="Aplicar Filtro",
        font=fonte_padrao,
        bg="#2196F3",
        fg="white",
        width=15,
        height=1,
        command=filtrar
    ).pack(side=tk.LEFT, padx=10)

    # Tabela
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), foreground="#333")
    style.configure("Treeview", font=fonte_tabela, rowheight=30)

    tree = ttk.Treeview(
        janela_lista,
        columns=("ID", "Título", "Autor", "Status", "Início", "Fim"),
        show="headings"
    )
    for col in ("ID", "Título", "Autor", "Status", "Início", "Fim"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for livro in service_listar_livros():
        tree.insert("", tk.END, values=livro)

    tree.pack(pady=20, padx=50, fill="both", expand=True)

    # Função de leitura ao clique simples
    def ao_clicar_simples(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            livro_id = valores[0]
            caminho_pdf = obter_caminho_pdf_por_id(livro_id)
            if caminho_pdf:
                caminho_completo = os.path.abspath(caminho_pdf)
                if os.path.exists(caminho_completo):
                    try:
                        os.startfile(caminho_completo)
                    except AttributeError:
                        subprocess.call(["open", caminho_completo])
                    except Exception:
                        subprocess.call(["xdg-open", caminho_completo])
                else:
                    messagebox.showinfo("Arquivo não encontrado", f"PDF não encontrado em:\n{caminho_completo}")
            else:
                messagebox.showinfo("Sem PDF", "Este livro não possui PDF associado.")

    tree.bind("<ButtonRelease-1>", ao_clicar_simples)

    # Clique direito (menu popup)
    def ao_clicar_direito(event):
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)
            menu_popup.tk_popup(event.x_root, event.y_root)

    tree.bind("<Button-3>", ao_clicar_direito)

    menu_popup = tk.Menu(janela_lista, tearoff=0, font=fonte_padrao, bg="#ffffff", fg="#000000", relief="flat")
    menu_popup.add_command(label="✏️ Editar", command=lambda: acao_menu_popup("editar"))
    menu_popup.add_command(label="🗑️ Excluir", command=lambda: acao_menu_popup("excluir"))

    def acao_menu_popup(acao):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            if acao == "editar":
                abrir_edicao_livro(valores)
            elif acao == "excluir":
                service_excluir_livro(valores[0])

    # Botões de ações finais
    botoes_frame = tk.Frame(janela_lista, bg="#f2f2f2")
    botoes_frame.pack(pady=30)

    tk.Button(
        botoes_frame,
        text="📤 Exportar Lista em PDF",
        font=fonte_padrao,
        bg="#4CAF50",
        fg="white",
        width=25,
        height=2,
        command=exportar_pdf
    ).pack(side=tk.LEFT, padx=20)

    tk.Button(
        botoes_frame,
        text="⬅️ Voltar ao Menu",
        font=fonte_padrao,
        bg="#f44336",
        fg="white",
        width=25,
        height=2,
        command=lambda: [janela_lista.destroy(), abrir_menu_principal()]
    ).pack(side=tk.LEFT, padx=20)



def obter_caminho_pdf_por_id(livro_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT caminho_pdf FROM livros WHERE id = ?", (livro_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None




# tela edição
def abrir_edicao_livro(dados):
    id_livro, titulo_atual, autor_atual, status_atual, inicio_atual, fim_atual = dados

    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Livro")
    janela_edicao.geometry("400x700")
    janela_edicao.config(bg="#f4f4f9")

    def on_enter_salvar(event):
        btn_salvar.config(bg="#388e3c", fg="white")

    def on_leave_salvar(event):
        btn_salvar.config(bg="#e2e2e2", fg="black")

    def on_enter_deletar(event):
        btn_deletar.config(bg="#d32f2f", fg="white")

    def on_leave_deletar(event):
        btn_deletar.config(bg="#e2e2e2", fg="black")

    tk.Label(janela_edicao, text="Editar Livro", font=("Helvetica", 16, "bold"), bg="#f4f4f9", fg="#333333").pack(pady=20)

    tk.Label(janela_edicao, text="Título:", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    entrada_titulo = tk.Entry(janela_edicao, font=("Arial", 12), bg="#e2e2e2", fg="#333333", bd=2, relief="solid")
    entrada_titulo.insert(0, titulo_atual)
    entrada_titulo.pack(fill="x", padx=20, pady=10)

    tk.Label(janela_edicao, text="Autor:", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    entrada_autor = tk.Entry(janela_edicao, font=("Arial", 12), bg="#e2e2e2", fg="#333333", bd=2, relief="solid")
    entrada_autor.insert(0, autor_atual)
    entrada_autor.pack(fill="x", padx=20, pady=10)

    caminho_pdf_selecionado = tk.StringVar()

    def selecionar_pdf():
        caminho_original = fd.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if caminho_original:
            # Pasta destino correta (interface/livros_pdf)
            pasta_destino = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "src", "interface", "livros_pdf")
            os.makedirs(pasta_destino, exist_ok=True)

            nome_arquivo = os.path.basename(caminho_original)
            caminho_destino = os.path.join(pasta_destino, nome_arquivo)

            try:
                shutil.copy(caminho_original, caminho_destino)

                # Definir o caminho padrão que queremos salvar no banco
                caminho_relativo_no_banco = os.path.join(
                    "Gestor-de-Leitura-e-Biblioteca-Pessoal",
                    "src",
                    "interface",
                    "livros_pdf",
                    nome_arquivo
                )

                caminho_pdf_selecionado.set(caminho_relativo_no_banco)
                label_pdf.config(text=nome_arquivo)
            except Exception as e:
                print(f"Erro ao copiar o arquivo PDF: {e}")
                caminho_pdf_selecionado.set("")
                label_pdf.config(text="Erro ao selecionar PDF")

    tk.Label(janela_edicao, text="PDF do livro (opcional):", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    btn_pdf = tk.Button(janela_edicao, text="Selecionar PDF", font=("Arial", 10), command=selecionar_pdf)
    btn_pdf.pack(padx=20, pady=(0, 5))

    label_pdf = tk.Label(janela_edicao, text="Nenhum arquivo selecionado", font=("Arial", 10), bg="#f4f4f9", fg="gray")
    label_pdf.pack(padx=20, pady=(0, 10))

    tk.Label(janela_edicao, text="Status:", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    combo_status = ttk.Combobox(janela_edicao, values=["Lido", "Lendo", "Quero ler"], font=("Arial", 12), state="readonly")
    combo_status.set(status_atual)
    combo_status.pack(fill="x", padx=20, pady=10)

    tk.Label(janela_edicao, text="Data do inicio da leitura:", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    entrada_inicio = tk.Entry(janela_edicao, font=("Arial", 12), bg="#e2e2e2", fg="#333333", bd=2, relief="solid")
    entrada_inicio.insert(0, inicio_atual)
    entrada_inicio.pack(fill="x", padx=20, pady=10)

    tk.Label(janela_edicao, text="Data do fim da leitura:", font=("Arial", 12), bg="#f4f4f9").pack(anchor="w", padx=20, pady=5)
    entrada_fim = tk.Entry(janela_edicao, font=("Arial", 12), bg="#e2e2e2", fg="#333333", bd=2, relief="solid")
    entrada_fim.insert(0, fim_atual)
    entrada_fim.pack(fill="x", padx=20, pady=10)

    def salvar_alteracoes():
        novo_titulo = entrada_titulo.get()
        novo_status = combo_status.get()
        nova_data_inicio = entrada_inicio.get()
        nova_data_fim = entrada_fim.get()
        novo_pdf = caminho_pdf_selecionado.get() if caminho_pdf_selecionado.get() else None
        novo_autor = entrada_autor.get()

        service_atualizar_livro(id_livro, novo_titulo, novo_autor, novo_status, nova_data_inicio, nova_data_fim, novo_pdf)
        janela_edicao.destroy()

    def deletar():
        service_excluir_livro(id_livro)
        janela_edicao.destroy()

    # Botão salvar
    btn_salvar = tk.Button(janela_edicao, text="Salvar Alterações", font=("Arial", 12), bg="#e2e2e2", fg="black", command=salvar_alteracoes)
    btn_salvar.pack(fill="x", padx=20, pady=10)
    btn_salvar.bind("<Enter>", on_enter_salvar)
    btn_salvar.bind("<Leave>", on_leave_salvar)

    # Botão deletar
    btn_deletar = tk.Button(janela_edicao, text="Excluir Livro", font=("Arial", 12), bg="#e2e2e2", fg="black", command=deletar)
    btn_deletar.pack(fill="x", padx=20, pady=10)
    btn_deletar.bind("<Enter>", on_enter_deletar)
    btn_deletar.bind("<Leave>", on_leave_deletar)



from database.funcoes_estatisticas import contar_livros_por_mes

def mostrar_estatisticas(janela_principal):
    janela_principal.destroy()
    janela = tk.Toplevel()
    janela.title("Estatísticas de Leitura")
    janela.state('zoomed') 
    janela.bind_all("<Escape>", toggle_fullscreen)

    largura_tela = janela_principal.winfo_screenwidth()
    altura_tela = janela_principal.winfo_screenheight()


    # Frame centralizado
    frame_estatisticas = tk.Frame(janela, bg="#f9f9f9", padx=20, pady=20)
    frame_estatisticas.place(relx=0.5, rely=0.5, anchor="center")

    # Cabeçalho
    tk.Label(frame_estatisticas, text="Estatísticas de Leitura", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Dicionário para traduzir nomes dos meses do inglês para o português
    meses_pt = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março",
        "April": "Abril", "May": "Maio", "June": "Junho",
        "July": "Julho", "August": "Agosto", "September": "Setembro",
        "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }

    # Exibição das estatísticas com nomes de meses em português
    estatisticas = contar_livros_por_mes()

    if not estatisticas:
        tk.Label(frame_estatisticas, text="Nenhum dado de leitura encontrado.", font=("Arial", 12)).pack(pady=20)
    else:
        for mes, qtd in sorted(estatisticas.items()):
            nome_mes_pt = meses_pt.get(mes, mes)  # Pega a versão traduzida, se existir
            tk.Label(frame_estatisticas, text=f"{nome_mes_pt}: {qtd} livro(s)", font=("Arial", 12)).pack(pady=5)

    # Botão para voltar ao menu principal
    tk.Button(
        frame_estatisticas,
        text="Voltar ao Menu",
        command=lambda: [janela.destroy(), abrir_menu_principal()],
        width=20, height=2,
        font=("Arial", 12),
        bg="#f44336", fg="white"
    ).pack(pady=20)

    tk.Button(frame_estatisticas, text="Voltar ao Menu", font=("Arial", 14, "bold"),
              bg="#f44336", fg="white", width=18, height=2,
              command=lambda: [frame_estatisticas.destroy(), abrir_menu_principal()]
              ).pack(side=tk.LEFT, padx=20)
    janela.mainloop()



from tkinter import Canvas, Toplevel, Frame, Label, Button, messagebox
from PIL import Image, ImageTk

# Função para alternar entre fullscreen
def toggle_fullscreen(event=None, janela=None):
    is_fullscreen = janela.state() == 'zoomed'
    janela.state('normal' if is_fullscreen else 'zoomed')

# Função fictícia para contar livros por mês
def contar_livros_por_mes():
    return {
        'Janeiro 2025': 5,
        'Fevereiro 2025': 3,
        'Março 2025': 8,
    }

# Voltar da tela de estatísticas para o menu
def voltar_ao_menu(janela_estatisticas, janela_principal):
    janela_estatisticas.destroy()
    janela_principal.deiconify()

def mostrar_estatisticas(janela_principal):
    janela_principal.withdraw()  # Oculta a janela principal temporariamente

    janela = Toplevel()
    janela.title("Estatísticas de Leitura")
    janela.state('zoomed')
    janela.bind_all("<Escape>", lambda event: toggle_fullscreen(event, janela))

    caminho_imagem = os.path.join(os.path.dirname(__file__), "..", "interface", "imagem", "estatisticas.jpg")
    print("Caminho da imagem:", caminho_imagem)

    if not os.path.exists(caminho_imagem):
        print("Imagem não encontrada:", caminho_imagem)
        messagebox.showerror("Erro", "Imagem de fundo não encontrada.")
        janela.destroy()
        janela_principal.deiconify()
        return

    imagem_pil = Image.open(caminho_imagem).convert("RGB")
    imagem_pil = imagem_pil.resize(
        (janela.winfo_screenwidth(), janela.winfo_screenheight()),
        Image.Resampling.LANCZOS
    )
    fundo_imagem = ImageTk.PhotoImage(imagem_pil)

    canvas = Canvas(janela, width=janela.winfo_screenwidth(), height=janela.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=fundo_imagem)
    canvas.fundo_imagem = fundo_imagem  # evita coleta de lixo

    frame_estatisticas = Frame(janela, bg="#f9f9f9", padx=20, pady=20)
    frame_estatisticas.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame_estatisticas, text="Estatísticas de Leitura", font=("Helvetica", 18, "bold")).pack(pady=20)

    estatisticas = contar_livros_por_mes()
    if not estatisticas:
        Label(frame_estatisticas, text="Nenhum dado de leitura encontrado.", font=("Arial", 12)).pack(pady=20)
    else:
        for mes_ano, qtd in estatisticas.items():
            Label(frame_estatisticas, text=f"{mes_ano}: {qtd} livro(s)", font=("Arial", 12)).pack(pady=5)

    Button(
        frame_estatisticas,
        text="Voltar ao Menu",
        command=lambda: voltar_ao_menu(janela, janela_principal),
        width=20, height=2,
        font=("Arial", 12),
        bg="#f44336", fg="white"
    ).pack(pady=20)

# Função para criar a tela principal
def abrir_tela_principal():
    janela = tk.Tk()
    janela.title("Menu Principal")
    janela.state('zoomed')
    janela.configure(bg="#ffffff")

    Label(
        janela,
        text="Bem-vindo ao Gestor de Leitura",
        font=("Helvetica", 20, "bold"),
        bg="#ffffff"
    ).pack(pady=40)

    Button(
        janela,
        text="Ver Estatísticas de Leitura",
        command=lambda: mostrar_estatisticas(janela),
        font=("Arial", 14),
        bg="#2196F3", fg="white",
        width=25, height=2
    ).pack(pady=20)

    janela.mainloop()

# Executar
if __name__ == "__main__":
    abrir_tela_principal()











#função para deixar os meses em portugues e ordenar corretamente na tela estatisticas
import sqlite3
import os
from collections import defaultdict

def contar_livros_por_mes():
    # Caminho absoluto do banco de dados
    caminho_banco = os.path.join(os.path.dirname(__file__), '..', 'biblioteca.db')
    conn = sqlite3.connect(os.path.abspath(caminho_banco))
    cursor = conn.cursor()

    # Consulta para pegar todas as datas de fim dos livros lidos
    cursor.execute("SELECT data_fim FROM livros WHERE status = 'Lido'")
    datas = cursor.fetchall()

    conn.close()

    # Verifique se as datas foram retornadas
    if not datas:
        print("Nenhum livro encontrado com o status 'Lido'.")
        return {}

    contagem_por_mes = defaultdict(int)

    # Nomes dos meses em português
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    for (data_fim,) in datas:
        if data_fim:
            try:
                # Divida a data no formato 'DD/MM/YYYY'
                dia, mes, ano = map(int, data_fim.split("/"))
                nome_mes = nomes_meses.get(mes, f"Mês {mes}")
                chave = (ano, mes)  # Usando (ano, mês) para ordenação correta
                contagem_por_mes[chave] += 1
            except ValueError:
                print(f"Erro ao processar a data: {data_fim}")
                continue

    # Ordenando as chaves (ano, mês) corretamente
    contagem_por_mes_ordenada = sorted(contagem_por_mes.items())

    # Agora transformamos as chaves de volta para o formato 'Mês Ano' para exibir
    contagem_por_mes_final = {}
    for (ano, mes), qtd in contagem_por_mes_ordenada:
        nome_mes = nomes_meses.get(mes, f"Mês {mes}")
        chave_formatada = f"{nome_mes} {ano}"
        contagem_por_mes_final[chave_formatada] = qtd

    return contagem_por_mes_final



def selecionar_pdf_e_copiar():
    # Deixa o usuário escolher o arquivo
    caminho_original = fd.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not caminho_original:
        print("Nenhum arquivo selecionado.")
        return None

    # Caminho da pasta onde vamos guardar os PDFs no projeto
    pasta_destino = os.path.join(os.path.dirname(os.path.dirname(__file__)), "interface", "livros_pdf")

    # Cria a pasta se ela não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Pega o nome do arquivo selecionado
    nome_arquivo = os.path.basename(caminho_original)

    # Define o novo caminho
    novo_caminho = os.path.join(pasta_destino, nome_arquivo)

    try:
        # Copia o arquivo para a pasta do projeto
        shutil.copy2(caminho_original, novo_caminho)
        print(f"Arquivo copiado para {novo_caminho}")

        # Retorna o caminho relativo para salvar no banco
        caminho_relativo = os.path.relpath(novo_caminho, start=os.path.dirname(os.path.dirname(__file__)))
        return caminho_relativo
    except Exception as e:
        print(f"Erro ao copiar o arquivo: {e}")
        return None
    

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
