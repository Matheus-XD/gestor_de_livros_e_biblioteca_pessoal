from .banco import conectar
from collections import defaultdict
import datetime

def contar_livros_por_mes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT data_fim FROM livros
        WHERE status = 'Lido' AND data_fim IS NOT NULL
    ''')
    datas = cursor.fetchall()
    conn.close()

    contagem = defaultdict(int)
    for (data_fim,) in datas:
        for formato in ("%Y-%m-%d", "%d/%m/%Y"):  # tenta os dois formatos
            try:
                data = datetime.datetime.strptime(data_fim, formato)
                chave = data.strftime("%B %Y")  # Ex: "Junho 2025"
                contagem[chave] += 1
                break
            except:
                continue  # tenta o próximo formato

    return dict(contagem)

