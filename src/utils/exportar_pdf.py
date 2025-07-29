import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from textwrap import wrap
from services.livro_service import service_listar_livros
def exportar_livros_para_pdf(status=None, nome_arquivo="lista_livros.pdf"):
    livros = service_listar_livros(status)

    if not livros:
        print("Nenhum livro encontrado para exportar.")
        return

    pasta_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)

    c = canvas.Canvas(caminho_arquivo, pagesize=A4)
    largura_pagina, altura_pagina = A4
    y = altura_pagina - 3 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, y, "Relatório de Livros")
    y -= 1.5 * cm

    # Configuração de colunas
    colunas = ["ID", "Título", "Autor", "Status", "Início", "Término"]
    larguras_colunas = [1.5 * cm, 6 * cm, 4 * cm, 3 * cm, 2.5 * cm, 2.5 * cm]
    posicoes_x = [1.5 * cm]
    for largura in larguras_colunas[:-1]:
        posicoes_x.append(posicoes_x[-1] + largura)

    padding = 0.2 * cm
    altura_linha_base = 0.6 * cm
    altura_linha_minima = 0.8 * cm
    fonte = "Helvetica"
    tamanho_fonte = 10
    altura_fonte = 0.4 * cm

    def desenhar_linha(y_topo, dados, negrito=False):
        c.setFont(f"{fonte}{'-Bold' if negrito else ''}", tamanho_fonte)

        linhas_por_campo = []
        for i, texto in enumerate(dados):
            largura_util = larguras_colunas[i] - 2 * padding
            if i == 1:  # Título pode ser longo
                linhas = wrap(texto, width=35)
            else:
                linhas = wrap(texto, width=20)
            linhas_por_campo.append(linhas)

        num_linhas = max(len(linhas) for linhas in linhas_por_campo)
        altura_caixa = max(num_linhas * altura_linha_base + 2 * padding, altura_linha_minima)

        # Desenhar caixas
        for i in range(len(dados)):
            x = posicoes_x[i]
            c.rect(x, y_topo - altura_caixa, larguras_colunas[i], altura_caixa)

        # Desenhar textos
        for i, linhas in enumerate(linhas_por_campo):
            x = posicoes_x[i]
            largura_coluna = larguras_colunas[i]
            total_texto_altura = len(linhas) * altura_linha_base
            y_texto_base = y_topo - ((altura_caixa - total_texto_altura) / 2) - (altura_linha_base / 2)



            for j, linha in enumerate(linhas):
                largura_texto = c.stringWidth(linha, fonte, tamanho_fonte)
                x_texto = x + (largura_coluna - largura_texto) / 2
                y_texto = y_texto_base - j * altura_linha_base
                c.drawString(x_texto, y_texto, linha)

        return altura_caixa

    # Cabeçalho
    altura = desenhar_linha(y, colunas, negrito=True)
    y -= altura

    # Dados
    for livro in livros:
        if y < 3 * cm:
            c.showPage()
            y = altura_pagina - 3 * cm
            altura = desenhar_linha(y, colunas, negrito=True)
            y -= altura

        dados = [
            str(livro[0]),
            str(livro[1]),
            str(livro[2]),
            str(livro[3]),
            livro[4] or "N/A",
            livro[5] or "N/A"
        ]

        altura = desenhar_linha(y, dados)
        y -= altura

    c.save()
    print(f"PDF gerado com sucesso em: {caminho_arquivo}")
