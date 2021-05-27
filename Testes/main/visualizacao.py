from Modelo_5.ClasseGridV2 import GridV2
import Modelo_5.funcoes_arquivos as func_arq
from Modelo_5.simulacao2 import simulacao2
import Testes.src.funcoes_geracao_nomes as fgn
import funcoes
import os


def visualizacao():

    path_arquivos_base = "Testes\\arquivos\\arquivos_base"
    lista_de_arquivos = os.listdir(path=path_arquivos_base)

    for i in range(len(lista_de_arquivos)):
        nome_arquivo = lista_de_arquivos[i]
        print("nome: {} / numero: {}".format(nome_arquivo, i))

    print("------------------------\n")

    indice_escolhido = int(input("digite o numero do arquivo: "))
    arquivo_escolhido = lista_de_arquivos[indice_escolhido]

    tam_grid = func_arq.obter_tam_grid_pelo_nome_arquivo(arquivo_escolhido)
    qnt_linhas = tam_grid[0]
    qnt_colunas = tam_grid[1]
    tamanho_celula = 1
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout, display_agentes=False)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(arquivo_escolhido)
    path_arquivo_lugares = "Testes\\arquivos\\arquivos_lugares"
    path_arquivo_lugares = os.path.abspath(path_arquivo_lugares)
    nome_arquivo_lugares_completo = os.path.join(path_arquivo_lugares, nome_arquivo_lugares)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_completo)

    # nome_arquivo_lugares_dinamicos = fgn.gerar_nome_arquivo_info_lugares_dinamicos(arquivo_escolhido)
    # path_arquivos_lugares_dinamicos = "Testes\\arquivos\\arquivos_lugares_dinamicos"
    # path_arquivos_lugares_dinamicos = os.path.join(path_arquivos_lugares_dinamicos)
    # nome_arquivo_lugares_dinamicos_completo = os.path.join(path_arquivos_lugares_dinamicos, nome_arquivo_lugares_dinamicos)
    # grid.arquivo_lugares_dinamicos = nome_arquivo_lugares_dinamicos_completo

    pesos_teste = (1, 1, 1)
    qnt_time_steps_teste = 1000

    simulacao2(pesos_teste, grid, qnt_time_steps_teste)
