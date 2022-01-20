from Modelo_5.funcoes_arquivos import criar_arquivo_lugares
import Testes.main.testes_parametros as tp
import Testes.src.funcoes_geracao_nomes as fgn
import Testes.main.testes_modelo2D as t2d
#import Testes.main.teste1 as t1
import numpy as np
import shutil
import os
import Modelo_5.apresentacoes as m5ap
#import Modelo_fast.testes_novos_pesos as tnp
import Testes.main.visualizacao as v5
#import recebe_arquivo_original as rao
import Scripts.inverte_e_cria_arquivo as ica
import pyautogui

#ica.cria_Invertido()

#m5ap.simulacao_com_arquivo_2()
#t2d.teste_modelo_2d()

# so pra rodar esse teste Caio, vou deixar os testes q eu to rodando comentados pra vc
# tp.testes_colormap_entropia_v2()

# teste 1
# pesos_contaminacao_agente1 = (1, 0.1)
# pesos_contaminacao_lugar1 = (1, 0.01)
# path_relativo_folder1 = "Testes\\main\\resultados6"
# tp.teste_pesos_escolha_lugar_media(pesos_contaminacao_agente1, pesos_contaminacao_lugar1, path_relativo_folder1)

# # teste 2
# pesos_contaminacao_agente2 = (1, 0.01)
# pesos_contaminacao_lugar2 = (1, 0.005)
# path_relativo_folder2 = "Testes\\main\\resultados7"
# tp.teste_pesos_escolha_lugar_media(pesos_contaminacao_agente2, pesos_contaminacao_lugar2, path_relativo_folder2)

# tp.testes()
# tp.salvar_graficos_resultados("resultados6", "graficos_resultados6")
# tp.salvar_graficos_resultados("resultados7", "graficos_resultados7")

# nome_arquivo_testes = "teste_(1.0, 1.00000567).txt"
# peso = fgn.obter_peso_por_nome(nome_arquivo_testes)
# peso = eval(peso)
# peso = tuple([round(i, 2) for i in peso])
# peso = "({:.2f}, {:.2f})".format(peso[0], peso[1])
# print("peso = ", peso)
# print("tipo: ", type(peso))

# nome_novo_arq_testes = "teste_" + peso + ".txt"
# print("nome: ", nome_novo_arq_testes)

# os.rename(nome_arquivo_testes, nome_novo_arq_testes)


# ----------------------------------------------------------------------------------------------
#  funcao para renomear os arquivos que Caio mandou
# lista_arquivos = os.listdir("resultados_entropia_renomeados")

# for arquivo in lista_arquivos:
#     peso = fgn.obter_peso_por_nome(arquivo)
#     peso = eval(peso)
#     peso = tuple([round(i, 2) for i in peso])
#     peso = "({:.2f}, {:.2f})".format(peso[0], peso[1])
#     novo_nome = "resultados_entropia_" + peso + ".csv"

#     nome_antigo_completo = os.path.join("resultados_entropia", arquivo)
#     nome_novo_completo = os.path.join("resultados_entropia_renomeados", novo_nome)

#     shutil.copyfile(nome_antigo_completo, nome_novo_completo)

# print("-- arquivos renomeados --")
# ----------------------------------------------------------------------------------------------

# com 71 pesos utilizados nos parametros 'a' e 'b', teriamos:
# 71 x 71 = 5041 arquivos diferentes, mas ha 5034, faltam 7 simualcoes a serem feitas
# tenho que criar o codigo para varrer o dir e achar os pesos que nao foram usados em simulacoes

# pesos_a = np.arange(0.1, 1.52, 0.02)
# pesos_b = np.arange(0.1, 1.52, 0.02)

# pesos_a = [round(a, 2) for a in pesos_a]
# pesos_b = [round(b, 2) for b in pesos_b]

# lista_pesos = [(a, b) for a in pesos_a for b in pesos_b]

# lista_arquivos = os.listdir("resultados_entropia_renomeados")
# print("qnt arquivos: ", len(lista_arquivos))

# lista_arquivos_extras = []

# arquivos_normais = 0
# arquivos_extras = 0

# for arquivo in lista_arquivos:
#     i0 = arquivo.index("(")
#     i1 = arquivo.index(")")
#     peso = arquivo[i0:i1+1]
#     peso = eval(peso)
    # print(peso)
    # peso_string = "({:.2f}, {:.2f})".format(peso[0], peso[1])
    # nome_arquivo = "resultados_entropia_" + peso_string + ".csv"

    # arquivos que vao ser copiados para o novo dir
#     if peso in lista_pesos:
#         arquivos_normais += 1

#         nome_antigo = os.path.join("resultados_entropia_renomeados", arquivo)
#         nome_novo = os.path.join("resultados_entropia_renomeados2", arquivo)

#         shutil.copyfile(nome_antigo, nome_novo)

#     else:
#         arquivos_extras += 1
#         lista_arquivos_extras.append(peso)

# print("arquivos copiados: ", arquivos_normais)
# print("arquivos extras: ", arquivos_extras, "\n")

# print("arquivos nao copiados:")
# for arquivo in lista_arquivos_extras:
#     print(arquivo)


# tp.ver_colormap_entropia("resultados_entropia_renomeados2")

# ---------------------------------------------------------------------------
# testes no modelo 2D

"""
for arquetipo in range(6):

    #lista_arquivos_base = ["Sao_Paulo(1000x1000)[tipo_1].txt"]
    lista_arquivos_base = ["modelo1(42x42)[tipo_1].txt",    # 0
                        "modelo2-inv(42x42)[tipo_1].txt",    # 1
                        "modelo3-inv(42x42)[tipo_1].txt",   # 2
                        "modelo4(42x42)[tipo_1].txt",    # 3
                        "modelo5(42x42)[tipo_1].txt",    # 4
                        "modelo6(42x42)[tipo_1].txt"]    # 5'''

    # -- fazendo as simulacoes 2d (demorou quase um dia) --
    pesos_escolha_lugar = (0.1, 0.5) #alfa e beta
    pesos_contaminacao_agentes = (0.5, 0.5) #C e D dos agentes
    pesos_contaminacao_lugares = (0.5, 0.5) #C e D dos lugares
    resultados = t2d.teste_modelo_2d_com_arquivo(lista_arquivos_base[arquetipo], 2000, pesos_escolha_lugar, pesos_contaminacao_agentes, pesos_contaminacao_lugares)

    # -- plotando os graficos dos resultados das simulacoes 2D--
    
    nome_dir_origem = "Testes\\2d_resultados\\arquetipos\\time_steps_2000\\agentes_atualizados\\(0-1)(0-5)" #devem ser pastas já existentes
    nome_dir_destino = f"modelo{arquetipo+1}" #deve ser o nome de uma nova pasta
    tp.salvar_graficos_resultados_v2(resultados, nome_dir_destino, nome_dir_origem)

"""
"""    #faz o recebimento dos arquivos originais, enviados pelo Caio
path_originais="C:\\Users\\julio\\Desktop\\Entropy\\Arquivos\\Arquivos_originais"
path_base="C:\\Users\\julio\\Desktop\\Entropy\\Arquivos\\Arquivos_base"
path_lugares="C:\\Users\\julio\\Desktop\\Entropy\\Arquivos\\Arquivos_lugares"
ica.cria_Invertido()
    #fazendo as simulações com o modelo animado
"""

arqBase = "cenarioNovoCorreto(25x25)[tipo_1].txt"
pesos_escolha_lugar=(0.1,0.2) # A e B
pesos_contaminacao_agentes = (0.5,5) #C e D
pesos_contaminacao_lugares = (0.5, 0.5) #C e D
    #path_relativo_folder_reusltados = "Testes\\2d_resultados"
resultados=m5ap.simulacao_com_arquivo(arqBase,pesos_escolha_lugar,pesos_contaminacao_agentes,pesos_contaminacao_lugares)
    #m5ap.simulacao_com_arquivo(lista_arquivos_base[arquetipo])

# ---------------------------------------------------------------------------
# testes no modelo 1D - analisando os padroes gerados pela mudancas nos pesos de contaminacao

# faznendo as simulacoes
# path_folder = "Testes\\main\\resultados_contaminacao"
# tp.teste_pesos_contaminacao_medio(path_folder)

# print("\n---------------------------------\n")

# fazendo os graficos
# nome_folder_origem = "resultados_contaminacao"
# nome_folder_destino = "resultados_contaminacao_graficos"
# tp.salvar_graficos_resultados(nome_folder_origem, nome_folder_destino)

# ---------------------------------------------------------------------------
# testes para crair heatmap com entropia 

# nome_dir_origem = "Testes\\main\\resultados_contaminacao"
# nome_dir_destino = "Testes\\main\\resultados_contaminacao_graficos"
# tp.heatmap_entropia_agentes(nome_dir_origem, 5, 5, nome_dir_destino)

# ---------------------------------------------------------------------------
# testes do modelo com variacoes nos pesos de contaminação 28/04

# **** Teste 1 - peso escolha lugar = (0, 0) ****

# path_relativo_folder_origem = "Testes\\main\\resultados_contaminacao_PeL(0, 0)"
# qnt_time_steps = 4000
# peso_escolha_lugar = (0, 0)
# tp.teste_pesos_contaminacao_medio(path_relativo_folder_origem, qnt_time_steps=qnt_time_steps, peso_escolha_lugar=peso_escolha_lugar)

# path_relativo_folder_destino = "Testes\\main\\resultados_contaminacao_PeL(0, 0)_graficos"
# tp.salvar_graficos_resultados(path_relativo_folder_origem, path_relativo_folder_destino)


# **** Teste 2 - peso escolha lugar = (0.5, 0.5) ****

# path_relativo_folder_origem = "Testes\\main\\resultados_contaminacao_PeL(0.5, 0.5)"
# qnt_time_steps = 4000
# peso_escolha_lugar = (0.5, 0.5)
# tp.teste_pesos_contaminacao_medio(path_relativo_folder_origem, qnt_time_steps=qnt_time_steps, peso_escolha_lugar=peso_escolha_lugar)

# path_relativo_folder_destino = "Testes\\main\\resultados_contaminacao_PeL(0.5, 0.5)_graficos"
# tp.salvar_graficos_resultados(path_relativo_folder_origem, path_relativo_folder_destino)



# **** Teste 3 - peso escolha lugar = (0.1, 1.0) ****

# path_relativo_folder_origem = "Testes\\main\\resultados_contaminacao_PeL(0.1, 1.0)"
# qnt_time_steps = 4000
# peso_escolha_lugar = (0.1, 1.0)
# tp.teste_pesos_contaminacao_medio(path_relativo_folder_origem, qnt_time_steps=qnt_time_steps, peso_escolha_lugar=peso_escolha_lugar)

# path_relativo_folder_destino = "Testes\\main\\resultados_contaminacao_PeL(0.1, 1.0)_graficos"
# tp.salvar_graficos_resultados(path_relativo_folder_origem, path_relativo_folder_destino)



# **** Teste 4 - peso escolha lugar = (1.0, 0.1) ****
# - esse teste foi rodado por Caio, ele mandou os resultados para a minha maquina junto com os graficos

# path_relativo_folder_origem = "Testes\\main\\resultados_contaminacao_PeL(1.0, 0.1)"
# qnt_time_steps = 4000
# peso_escolha_lugar = (1.0, 0.1)
# tp.teste_pesos_contaminacao_medio(path_relativo_folder_origem, qnt_time_steps=qnt_time_steps, peso_escolha_lugar=peso_escolha_lugar)

# path_relativo_folder_destino = "Testes\\main\\resultados_contaminacao_PeL(1.0, 0.1)_graficos"
# tp.salvar_graficos_resultados(path_relativo_folder_origem, path_relativo_folder_destino)

# ----------------------------------------------------------------
# 18/05: fazendo testes com o modelo 2d para ver se esta tudo certo

# t2d.teste_modelo_2d()

# ----------------------------------------------------------------
# 27/05/2021: testando Modelo 5 para apresentacoes

#m5ap.simulacao_3()
# v5.visualizacao()