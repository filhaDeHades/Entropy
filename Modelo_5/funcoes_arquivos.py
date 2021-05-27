from Modelo_fast.ClasseGridV2Fast import GridV2Fast
from Modelo_fast.ClasseLugarV2Fast import LugarV2Fast
import Modelo_fast.funcoes_fast as fst
import numpy as np
import random
import cores
import os

"""
IMPORTANTE:

Arquivo tipo 1: contem somente matriz binaria (0 ou 1)

Arquivo tipo 2: contem info sobre o id dos lugares (podem ser quantos ids forem necessarios)

Arquivo tipo 3: conte info sobre id dos lugares e uso do solo (contem ids e cor dos ids)

Arquivo original: arquivo que recebo de Caio

Arquivo base: arquivo original copiado mas que possuem tipo e tamanho no nome

Ao receber um arquivo novo (arquivo original) deve-se mudar seu nome para transforma-lo em um arquivo base

Um arquivo base contem infos eu seu nome que sao necessarias para iniciar a simulacao
"""


def gerar_nome_arquivo_lugares(nome_arquivo_base):
    nome_temp = nome_arquivo_base.strip(".txt")
    nome_final = nome_temp + "_lugares.txt"
    return nome_final


def obter_path_completo_arquivo_lugares(nome_arquivo_lugares):
    path_arquivo_lugares = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares"
    path_final = os.path.join(path_arquivo_lugares, nome_arquivo_lugares)
    return path_final


def gerar_nome_arquivo_caminhos(nome_arquivo_base):
    nome_temp = nome_arquivo_base.strip(".txt")
    nome_final = nome_temp + "_caminhos.txt"
    return nome_final


def obter_path_completo_arquivo_caminhos(nome_arquivo_caminhos):
    path_arquivo_caminhos = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_caminhos"
    path_final = os.path.join(path_arquivo_caminhos, nome_arquivo_caminhos)
    return path_final


def gerar_nome_arquivo_resultados(nome_arquivo_base):
    nome_temp = nome_arquivo_base.strip(".txt")
    nome_final = nome_temp + "_resultados.txt"
    return nome_final


def obter_path_completo_arquivo_resultados(nome_arquivo_resultados):
    path_arquivos_resultados = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_resultados"
    path_final = os.path.join(path_arquivos_resultados, nome_arquivo_resultados)
    return path_final


def gerar_nome_arquivo_resultados_ts(nome_arquivo_base, num_sim):
    nome_temp = nome_arquivo_base.strip(".txt")
    nome_final = nome_temp + "_resultados_ts_{}.txt".format(num_sim)
    return nome_final


def gerar_nome_arquivos_lugares_ts(nome_arquivo_lugares, time_step_atual):
    novo_nome = nome_arquivo_lugares.strip(".txt") + "_ts{}.txt".format(time_step_atual)
    return novo_nome


def gerar_nome_arquivos_agentes_ts(nome_arquivo_agentes, time_step_atual):
    novo_nome = nome_arquivo_agentes.strip(".txt") + "_ts{}.txt".format(time_step_atual)
    return novo_nome


def atualizar_nome_arquivo_lugares_ts(nome_arquivo_lugares, time_step_atual):
    pass


def atualizar_nome_arquivo_agentes_ts(nome_arquivo_agentes, time_step_atual):
    pass


def criar_arquivo_lugares_tipo_1(nome_arquivo_base, qnt_linhas, qnt_colunas, path_arquivos_base=None,
                                 path_arquivos_lugares=None):

    # gera um arquivo lugares so a partir de matriz com 1s ou 0s
    # n tem info do ids dos lugares ou uso do solo

    nome_arquivo_base_com_path = nome_arquivo_base

    if path_arquivos_base is not None:
        nome_arquivo_base_com_path = os.path.join(path_arquivos_base, nome_arquivo_base)

    lista_layout_temp = fst.arquivo_csv_para_lista(nome_arquivo_base_com_path)
    lista_layout = [i[2] for i in lista_layout_temp]
    matriz_layout = fst.transformar_lista_em_matriz(lista_layout, qnt_linhas, qnt_colunas)
    grid = GridV2Fast(qnt_linhas, qnt_colunas, matriz_layout=matriz_layout)

    lista_lugares_temp = []

    for celula in grid.array_celulas_grid:

        if celula.andavel is False:
            if celula.ja_foi_visitado is False:

                celula.ja_foi_visitado = True
                lista_coordenadas_novo_lugar = [celula.pos_grid]
                lista_celulas_para_testar = [celula]

                while len(lista_celulas_para_testar) > 0:

                    celula_atual = lista_celulas_para_testar.pop(0)
                    celula_atual.ja_foi_analisado = True
                    lista_vizinhos = grid.obter_nodulos_vizinhos(celula_atual, excluir_obstaculos=False,
                                                                 excluir_diagonais=True)

                    for vizinho in lista_vizinhos:
                        if vizinho.andavel is False:
                            if vizinho.ja_foi_analisado is True:
                                continue
                            else:
                                if vizinho.ja_foi_visitado is False:
                                    vizinho.ja_foi_visitado = True
                                    lista_coordenadas_novo_lugar.append(vizinho.pos_grid)
                                    lista_celulas_para_testar.append(vizinho)

                possiveis_cores = cores.lista_cores_coloridas
                cor_escolhida = random.choice(possiveis_cores)

                possiveis_orientacoes = list(range(0, 1100, 100))
                orientacao_escolhida = random.choice(possiveis_orientacoes)

                novo_lugar = LugarV2Fast(grid, veio_de_arquivo=False, lista_coordenadas=lista_coordenadas_novo_lugar,
                                         orientacao=orientacao_escolhida, cor=cor_escolhida)

                lista_lugares_temp.append(novo_lugar)

    grid.array_lugares = lista_lugares_temp

    nome_arquivo_lugares = gerar_nome_arquivo_lugares(nome_arquivo_base)

    if path_arquivos_lugares is not None:
        nome_arquivo_lugares = os.path.join(path_arquivos_lugares, nome_arquivo_lugares)

    grid.salvar_lugares_arquivo(nome_arquivo_lugares)


# obsoleto, n funciona direito, so cria um lugar
def criar_arquivo_lugares_tipo_1_v2(nome_arquivo_base, qnt_linhas, qnt_colunas):
    nome_arquivo_base_com_path = obter_path_completo_arquivo_base(nome_arquivo_base)

    lista_layout_temp = fst.arquivo_csv_para_lista(nome_arquivo_base_com_path)
    lista_layout = [i[2] for i in lista_layout_temp]
    matriz_layout = fst.transformar_lista_em_matriz(lista_layout, qnt_linhas, qnt_colunas)
    grid = GridV2Fast(qnt_linhas, qnt_colunas, matriz_layout=matriz_layout)

    lista_celulas_totais = [celula for celula in grid.array_celulas_grid if celula.andavel is False]
    lista_lugares = []

    for celula in lista_celulas_totais:

        if celula.ja_foi_visitado is True:
            continue
        else:
            celula.ja_foi_visitado = True

            lista_coordenadas_novo_lugar = [celula.pos_grid]
            lista_celulas_para_testar = [celula]

            while len(lista_celulas_para_testar) > 0:

                celula_testada = lista_celulas_para_testar.pop(0)
                celula_testada.ja_foi_visitado = True
                lista_vizinhos = grid.obter_nodulos_vizinhos(celula_testada, excluir_obstaculos=False, excluir_diagonais=True)

                for vizinho in lista_vizinhos:
                    if vizinho.ja_foi_visitado is True:
                        continue
                    else:
                        lista_coordenadas_novo_lugar.append(vizinho.pos_grid)
                        lista_celulas_para_testar.append(vizinho)
                        vizinho.ja_foi_visitado = True

            possiveis_cores = cores.lista_cores_coloridas
            cor_escolhida = random.choice(possiveis_cores)

            possiveis_orientacoes = list(range(0, 1100, 100))
            orientacao_escolhida = random.choice(possiveis_orientacoes)

            novo_lugar = LugarV2Fast(grid, veio_de_arquivo=False, lista_coordenadas=lista_coordenadas_novo_lugar,
                                     orientacao=orientacao_escolhida, cor=cor_escolhida)

            lista_lugares.append(novo_lugar)

    nome_arquivo_lugares = gerar_nome_arquivo_lugares(nome_arquivo_base)
    nome_arquivo_lugares_com_path = obter_path_completo_arquivo_lugares(nome_arquivo_lugares)

    array_lugares_final = np.array(lista_lugares)
    grid.array_lugares = array_lugares_final
    print("lista lugares: ", len(lista_lugares))
    print("array lugares: ", len(array_lugares_final))
    print("grid lugares: ", len(grid.array_lugares))
    grid.salvar_lugares_arquivo(nome_arquivo_lugares_com_path)


def criar_arquivo_lugares_tipo_2(nome_arquivo_base, path_arquivos_base=None, path_arquivos_lugares=None):
    # gera um arquivo lugares a partir de uma arquivo matriz
    # tem info sobre os id de cada coordenada, ou seja, ids dos lugares
    # os lugares sao salvos na forma = [id, lista coordenadas, cor, orientação]

    nome_arquivo_base_com_path = nome_arquivo_base

    if path_arquivos_base is not None:
        nome_arquivo_base_com_path = os.path.join(path_arquivos_base, nome_arquivo_base)

    lista_lugares_temp = fst.arquivo_csv_para_lista(nome_arquivo_base_com_path)
    lista_chaves = ["x", "y", "id"]
    lista_lugares_temp_2 = fst.matriz_para_lista_dicionarios(lista_chaves, lista_lugares_temp)

    dict_orientacoes_cores = fst.converter_orientacao_para_cor_v3(11)

    lista_orientacoes = list(range(0, 1100, 100))
    lista_ids = []
    lista_lugares_final = []

    for dicionario in lista_lugares_temp_2:

        if dicionario["id"] == 1:
            continue
        else:

            nova_coordenada = (dicionario["x"], dicionario["y"])

            if dicionario["id"] not in lista_ids:
                lista_ids.append(dicionario["id"])
                orientacao_escolhida = random.choice(lista_orientacoes)
                cor_escolhida = (0, 0, 0)

                for orientacao, cor in dict_orientacoes_cores.items():
                    if orientacao_escolhida == int(orientacao):
                        cor_escolhida = cor

                novo_lugar = {"id": dicionario["id"], "lista_coordenadas": [nova_coordenada], "cor": cor_escolhida,
                              "orientacao": orientacao_escolhida}

                lista_lugares_final.append(novo_lugar)

            else:
                for lugar in lista_lugares_final:
                    if dicionario["id"] == lugar["id"]:
                        lugar["lista_coordenadas"].append(nova_coordenada)

    matriz_lugares = fst.lista_dicionarios_para_matriz(lista_lugares_final)
    nome_arquivo_lugares = gerar_nome_arquivo_lugares(nome_arquivo_base)

    if path_arquivos_lugares is not None:
        nome_arquivo_lugares = os.path.join(path_arquivos_lugares, nome_arquivo_lugares)

    fst.lista_para_arquivo_csv(matriz_lugares, nome_arquivo_lugares)


def obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base):
    index_1 = nome_arquivo_base.index("(")
    index_2 = nome_arquivo_base.index(")")
    str_tam = nome_arquivo_base[index_1 + 1:index_2]
    lista_tamanho = [int(i) for i in str_tam.split("x")]
    return lista_tamanho


def gerar_nome_arquivo_com_info_tamanho(nome_arquivo_original, qnt_linhas, qnt_colunas):
    info_tamanho = "({}x{})".format(qnt_linhas, qnt_colunas)
    nome_temp = nome_arquivo_original.strip(".txt")
    nome_final = nome_temp + info_tamanho + ".txt"
    return nome_final


def obter_tipo_grid_pelo_nome_arquivo(nome_arquivo_base):
    index_1 = nome_arquivo_base.index("[")
    index_2 = nome_arquivo_base.index("]")
    tipo_grid = nome_arquivo_base[index_1 + 1:index_2]
    return tipo_grid


def gerar_nome_arquivo_com_info_tipo(nome_arquivo_original, numero_tipo):
    info_tamanho = "[tipo_{}]".format(numero_tipo)
    nome_temp = nome_arquivo_original.strip(".txt")
    nome_final = nome_temp + info_tamanho + ".txt"
    return nome_final


def copiar_e_renomear_arquivo(nome_arquivo_original, nome_arquivo_final):
    arquivo_original = open(nome_arquivo_original, "r")
    lista_linhas = arquivo_original.readlines()
    arquivo_original.close()

    arquivo_final = open(nome_arquivo_final, "w")

    for linha in lista_linhas:
        arquivo_final.write(linha)

    arquivo_final.close()


def gerar_nome_arquivo_base(nome_arquivo_original, qnt_linhas, qnt_colunas, numero_tipo):
    nome_arquivo_base_temp = gerar_nome_arquivo_com_info_tamanho(nome_arquivo_original, qnt_linhas, qnt_colunas)
    nome_arquivo_base_final = gerar_nome_arquivo_com_info_tipo(nome_arquivo_base_temp, numero_tipo)
    return nome_arquivo_base_final


def obter_path_completo_arquivo_base(nome_arquivo_base):
    path_arquivo_base = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_base"
    path_final = os.path.join(path_arquivo_base, nome_arquivo_base)
    return path_final


def criar_arquivo_base(nome_arquivo_original, nome_arquivo_base):
    nome_arquivo_base_com_path = obter_path_completo_arquivo_base(nome_arquivo_base)
    copiar_e_renomear_arquivo(nome_arquivo_original, nome_arquivo_base_com_path)


def criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=None, path_arquivos_lugares=None):

    tipo_arquivo = obter_tipo_grid_pelo_nome_arquivo(nome_arquivo_base)

    if tipo_arquivo == "tipo_1":
        qnt_linhas, qnt_colunas = obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base)
        criar_arquivo_lugares_tipo_1(nome_arquivo_base, qnt_linhas, qnt_colunas, path_arquivos_base=path_arquivos_base,
                                     path_arquivos_lugares=path_arquivos_lugares)

    if tipo_arquivo == "tipo_2":
        criar_arquivo_lugares_tipo_2(nome_arquivo_base, path_arquivos_base=path_arquivos_base,
                                     path_arquivos_lugares=path_arquivos_lugares)


def corrigir_arquivo_invertido(nome_arquivo_invertido, nome_arquivo_certo):
    lista_arquivo = fst.arquivo_csv_para_lista(nome_arquivo_invertido)

    for lista in lista_arquivo:
        if lista[2] == 0:
            lista[2] = 1
        else:
            lista[2] = 0

    fst.lista_para_arquivo_csv(lista_arquivo, nome_arquivo_certo)


def contar_qnt_linhas_arq(nome_arq):

    qnt_linhas = 0

    arquivo = open(nome_arq, "r")

    for linha in arquivo:
        qnt_linhas += 1

    return qnt_linhas


def recebimento_arquivo_original(nome_arquivo_original, qnt_linhas, qnt_colunas, numero_tipo):

    # gerando o nome do arquivo base
    nome_arquivo_base = gerar_nome_arquivo_base(nome_arquivo_original, qnt_linhas, qnt_colunas, numero_tipo)

    # criando o arquivo base
    criar_arquivo_base(nome_arquivo_original, nome_arquivo_base)

    # criando o arquivo lugares
    criar_arquivo_lugares(nome_arquivo_base)


if __name__ == '__main__':
    nome_arquivo_original_recebido = "SaoPaulo_6-7.txt"
    nome_arquivo_original_final = None

    arquivo_invertido = True

    if arquivo_invertido is True:
        nome_arquivo_original_final = "SaoPaulo_6-7v2.txt"
        corrigir_arquivo_invertido(nome_arquivo_original_recebido, nome_arquivo_original_final)
    else:
        nome_arquivo_original_final = nome_arquivo_original_recebido

    qnt_linhas_arquivo = 1000
    qnt_colunas_arquivo = 1000
    tipo_arquivo_recebido = 1
    recebimento_arquivo_original(nome_arquivo_original_final, qnt_linhas_arquivo, qnt_colunas_arquivo,
                                 tipo_arquivo_recebido)