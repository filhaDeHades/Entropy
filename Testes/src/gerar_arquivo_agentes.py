from Modelo_fast.ClasseGridV2Fast import GridV2Fast
import Modelo_5.funcoes_arquivos as func_arq
import Testes.src.funcoes_geracao_nomes as fgn
import numpy as np
import pandas as pd
import os


def criar_agentes_staticos(nome_arquivo_base, path_arquivos_lugares, path_arquivos_agentes_staticos, qnt_agentes=100):
    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base)
    nome_arquivo_lugares_completo = os.path.join(path_arquivos_lugares, nome_arquivo_lugares)

    qnt_linhas, qnt_colunas = func_arq.obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base)
    grid = GridV2Fast(qnt_linhas, qnt_colunas)

    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_completo)

    grid.gerar_agentes_aleatorios_v3(qnt_agentes)

    nome_arquivo_agentes = fgn.gear_nome_arquivo_info_agentes_staticos(nome_arquivo_base)
    nome_arquivo_agentes_final = os.path.join(path_arquivos_agentes_staticos, nome_arquivo_agentes)

    print("nome do arquivo: ", nome_arquivo_agentes_final)
    grid.salvar_agentes_arquivo(nome_arquivo_agentes_final)

    print("agentes gerados com sucesso!")


def criar_arquivo_agentes_dinamicos(nome_arquivo_base, path):

    nome_arquivo_agentes_dinamicos = fgn.gerar_nome_arquivo_info_agentes_dinamicos(nome_arquivo_base)
    nome_arquivo_completo = os.path.join(path, nome_arquivo_agentes_dinamicos)
    df = pd.DataFrame(np.arange(1), columns=["teste"])
    df.to_csv(nome_arquivo_completo, index=False)


def criar_arquivo_lugares_dinamicos(nome_arquivo_base, path):
    nome_arquivo_lugares_dinamicos = fgn.gerar_nome_arquivo_info_lugares_dinamicos(nome_arquivo_base)
    nome_arquivo_completo = os.path.join(path, nome_arquivo_lugares_dinamicos)
    df = pd.DataFrame(np.arange(1), columns=["teste"])
    df.to_csv(nome_arquivo_completo, index=False)


if __name__ == "__main__":

    # LEGENDA:
    # 1 - criar agentes staticos
    # 2 - criar arquivo agentes dinamicos
    # 3 - criar arquivo lugares dinamicos

    lista_arquivos_base = ["new_york_ID(1000x1000)[tipo_2].txt"]

    operacao = 3

    if operacao == 1:

        arquivo_base_escolhido = lista_arquivos_base[0]
        nome_dir_arq_lugares = "..\\arquivos\\arquivos_lugares"
        path_arq_lugares = os.path.abspath(nome_dir_arq_lugares)
        print("path arquivos lugares: ", path_arq_lugares)

        nome_dir_arq_agentes_staticos = "..\\arquivos\\arquivos_agentes_staticos"
        path_arq_agentes_staticos = os.path.abspath(nome_dir_arq_agentes_staticos)
        print("path arquivos agentes staticos: ", path_arq_agentes_staticos)

        agentes = 100
        criar_agentes_staticos(arquivo_base_escolhido, path_arq_lugares, path_arq_agentes_staticos, qnt_agentes=agentes)

    if operacao == 2:

        arquivo_base_escolhido = lista_arquivos_base[0]
        nome_dir_agentes_dinamicos = "..\\arquivos\\arquivos_agentes_dinamicos"
        path_arq_agentes_dinamicos = os.path.abspath(nome_dir_agentes_dinamicos)

        criar_arquivo_agentes_dinamicos(arquivo_base_escolhido, path_arq_agentes_dinamicos)

    if operacao == 3:

        arquivo_base_escolhido = lista_arquivos_base[0]
        nome_dir_lugares_dinamicos = "..\\arquivos\\arquivos_lugares_dinamicos"
        path_arq_lugares_dinamicos = os.path.abspath(nome_dir_lugares_dinamicos)

        criar_arquivo_lugares_dinamicos(arquivo_base_escolhido, path_arq_lugares_dinamicos)
