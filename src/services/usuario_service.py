
from repositories.usuario_repository import inserir_usuario, buscar_usuario_por_email_senha

def service_cadastrar_usuario(nome, email, senha):
    sucesso = inserir_usuario(nome, email, senha)
    if sucesso:
        print("Usuário cadastrado com sucesso!")
    else:
        print("Falha ao cadastrar usuário.")
    return sucesso

def service_verificar_login(email, senha):
    usuario = buscar_usuario_por_email_senha(email, senha)
    if usuario:
        print(f"Login bem-sucedido. Bem-vindo(a), {usuario[1]}!")
    else:
        print("Email ou senha inválidos.")
    return usuario
