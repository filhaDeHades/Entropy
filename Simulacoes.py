import Testes.main.testes_parametros as tp
# import Testes.src.funcoes_geracao_nomes as fgn
import Testes.main.testes_modelo2D as t2d
# import numpy as np
# import shutil
# import os
# import Modelo_5.apresentacoes as m5ap
# import Testes.main.visualizacao as v5
# import Scripts.inverte_e_cria_arquivo as ica

#------------- Scripts -------------
#import Testes.main.recebe_arquivo_original as rao
#import Modelo_fast.testes_novos_pesos as tnp
#import Testes.main.teste1 as t1


# testes no modelo 2D
arquivo = open('inputSimulacao.txt')
linhas = arquivo.readlines()

fast = 0
alfa = 0.1
beta = 0.1
cAgentes = 0.5
dAgentes = 0.5
cLugares = 0.5
dLugares = 0.5
timeStep = 2000
caminho = ''
nome = ''
arquivos = []

for linha in range(len(linhas)):
    if linha == 0:
        fast = int(linhas[linha][0])
    elif linha == 1:
        alfaEBeta = linhas[linha].split()
        alfa = float(alfaEBeta[0])
        beta = float(alfaEBeta[0])
    elif linha == 2:
        cEd = linhas[linha].split()
        cAgentes = float(cEd[0])
        dAgentes = float(cEd[1])
    elif linha == 3:
        cEd = linhas[linha].split()
        cLugares = float(cEd[0])
        cLugares = float(cEd[1])
    elif linha == 4:
        timeStep = int(linhas[linha])
    elif linha == 5:
        caminho = linhas[linha].strip('\n')
    elif linha == 6:
        nome = linhas[linha].strip('\n')
    else:
        arquivos.append(linhas[linha].strip('\n'))

for arquetipo in range(len(arquivos)):

    if(fast):
        resultados = t2d.teste_modelo_2d_com_arquivo(arquivos[arquetipo], timeStep, (alfa, beta), (cAgentes, dAgentes), (cLugares, dLugares))

    # -- plotando os graficos dos resultados das simulacoes 2D--
    
    nome_dir_origem = caminho #devem ser pastas já existentes
    nome_dir_destino = f"{nome}{arquetipo+1}" #deve ser o nome de uma nova pasta
    tp.salvar_graficos_resultados_v2(resultados, nome_dir_destino, nome_dir_origem)