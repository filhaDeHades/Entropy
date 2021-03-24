import pandas as pd
import random
import math
import os


def obter_distancia(pos_grid_inicial, pos_grid_final, custo_menor_mov=10, custo_maior_mov=14):

    dx = abs(pos_grid_final[0] - pos_grid_inicial[0])
    dy = abs(pos_grid_final[1] - pos_grid_inicial[1])

    if dx > dy:
        distancia = custo_maior_mov * dy + custo_menor_mov * (dx - dy)
    else:
        distancia = custo_maior_mov * dx + custo_menor_mov * (dy - dx)

    return distancia


def arquivo_csv_para_lista(nome_arquivo, separador="\t"):
    arquivo = open(nome_arquivo, "r")
    lista_arquivo = arquivo.readlines()
    arquivo.close()

    lista_temp = [item.strip("\n").split(separador) for item in lista_arquivo]
    lista_final = [list(map(eval, i)) for i in lista_temp]

    return lista_final


def lista_para_arquivo_csv(lista_origem, nome_arquivo_destino, separador="\t", tipo_operacao="w"):

    lista_temp = [list(map(str, i)) for i in lista_origem]
    lista_temp_2 = [separador.join(i) for i in lista_temp]
    lista_final = ["{}\n".format(i) for i in lista_temp_2]

    arquivo_destino = open(nome_arquivo_destino, tipo_operacao)

    for linha in lista_final:
        arquivo_destino.write(linha)

    arquivo_destino.close()


def obter_distancia_euclidiana(ponto_inicial, ponto_final):

    x_inicial = ponto_inicial[0]
    x_final = ponto_final[0]

    y_inicial = ponto_inicial[1]
    y_final = ponto_final[1]

    distancia = math.sqrt((x_final - x_inicial)**2 + (y_final - y_inicial)**2)

    return distancia


def obter_distancia_manhattan(coordenada1, coordenada2):
    distancia_eixo_x = abs(coordenada1[0] - coordenada2[1])
    distancia_eixo_y = abs(coordenada1[1] - coordenada2[1])

    distancia_total = distancia_eixo_x + distancia_eixo_y
    return distancia_total


def obter_grid_manual(linhas, colunas):
    grid = []

    for y in range(linhas):
        linha = [0]*colunas
        grid.append(linha)

    return grid


def escolher_lugar_menor_e(agente, lista_lugares):
    lista_lugares_usaveis = list(lista_lugares)
    lugar_atual_agente = None

    if agente.celula_grid.lugar is not None:
        lugar_atual_agente = agente.celula_grid.lugar

    if lugar_atual_agente is not None:
        lista_lugares_usaveis.remove(lugar_atual_agente)

    diferenca_orientacao_inicial = abs(agente.orientacao_latente - lista_lugares[0].orientacao)
    coordenada_principal_inicial = lista_lugares[0].achar_coordenada_principal(agente.pos_grid)
    distancia_inicial = round(obter_distancia_euclidiana(agente.pos_grid, coordenada_principal_inicial))

    menor_e = (diferenca_orientacao_inicial + 100) * distancia_inicial
    lugar_menor_e = lista_lugares[0]

    for lugar in lista_lugares:

        diferenca_orientacao_analisada = abs(agente.orientacao_latente - lugar.orientacao)
        coordenada_principal_analisada = lugar.achar_coordenada_principal(agente.pos_grid)
        distancia_analisada = round(obter_distancia_euclidiana(agente.pos_grid, coordenada_principal_analisada))

        menor_e_analisado = (diferenca_orientacao_analisada + 100) * distancia_analisada

        if menor_e_analisado < menor_e:
            menor_e = menor_e_analisado
            lugar_menor_e = lugar

    return lugar_menor_e


def escolher_lugar_mais_parecido(agente, lista_lugares):
    # escolhendo um lugar baseado somente na diferenca de orientacao do agente com um lugar
    lista_lugares_usaveis = list(lista_lugares)
    lugar_atual_agente = None

    if agente.celula_grid.lugar is not None:
        lugar_atual_agente = agente.celula_grid.lugar

    if lugar_atual_agente is not None:
        lista_lugares_usaveis.remove(lugar_atual_agente)

    menor_dif_ort = None
    lugar_menor_dif = None

    for lugar in lista_lugares_usaveis:
        dif_atual = abs(agente.orientacao_latente - lugar.orientacao)

        if menor_dif_ort is None:
            menor_dif_ort = dif_atual
            lugar_menor_dif = lugar
        else:
            if dif_atual < menor_dif_ort:
                menor_dif_ort = dif_atual
                lugar_menor_dif = lugar

    return lugar_menor_dif


def escolher_lugar_mais_parecido_v2(agente, lista_lugares):
    lista_lugares_usaveis = list(lista_lugares)
    lugar_atual_agente = None

    if agente.celula_grid.lugar is not None:
        lugar_atual_agente = agente.celula_grid.lugar

    # caso o agentes esteja em algum lugar, esse lugar precisa ser retirado dos lugares que o agente possa escolher
    if lugar_atual_agente is not None:
        lista_lugares_usaveis.remove(lugar_atual_agente)

    menor_dif_ort = None
    lista_lugares_menor_dif_ort = []

    for lugar in lista_lugares_usaveis:
        dif_atual = abs(agente.orientacao_latente - lugar.orientacao)

        if menor_dif_ort is None:
            menor_dif_ort = dif_atual
            lista_lugares_menor_dif_ort.append(lugar)
        else:
            if dif_atual < menor_dif_ort:
                menor_dif_ort = dif_atual
                lista_lugares_menor_dif_ort.clear()
                lista_lugares_menor_dif_ort.append(lugar)

            elif dif_atual == menor_dif_ort:
                lista_lugares_menor_dif_ort.append(lugar)

    # caso a lista de lugares possiveis seja composta por um lugar, este lugar eh escolhido
    if len(lista_lugares_menor_dif_ort) == 0:
        return lista_lugares_menor_dif_ort[0]

    # caso contrario, sortendo igualmente os lugares que tem a mesma orientação
    else:
        indice_escolhido = random.randint(0, len(lista_lugares_menor_dif_ort)-1)
        lugar_sorteado = lista_lugares_menor_dif_ort[indice_escolhido]
        return lugar_sorteado


def obter_lista_com_elementos_repetidos(dict_contagem_elementos_repetidos):

    lista_com_elementos_repetidos = []

    for key, value in dict_contagem_elementos_repetidos.items():
        for i in range(value):
            lista_com_elementos_repetidos.append(key)

    return lista_com_elementos_repetidos


def obter_dict_contagem_elementos_repetidos_v2(lista_com_elementos_repetidos):
    set_elementos = set(lista_com_elementos_repetidos)
    dicionario_contagem_repeticoes = {i: lista_com_elementos_repetidos.count(i) for i in set_elementos}
    return dicionario_contagem_repeticoes


def contagem_ocorrencia_elementos_com_referencial(lista_analisada, lista_referencial):
    dict_contagem = {}

    for elemento in lista_referencial:
        contagem = lista_analisada.count(elemento)
        dict_contagem[str(elemento)] = contagem

    return dict_contagem


def obter_media(lista):
    media = sum(lista) / len(lista)
    return media


def obter_moda(lista):
    dict_contagem = obter_dict_contagem_elementos_repetidos_v2(lista)

    maior_ocorrencia = 0
    elemento_maior_ocorrencia = 0

    for key, value in dict_contagem.items():
        if value > maior_ocorrencia:
            maior_ocorrencia = value
            elemento_maior_ocorrencia = key

    return elemento_maior_ocorrencia


def obter_mediana(lista):
    lista.sort()
    # print("lista ordenada: ", lista)
    indice_meio = len(lista) // 2
    elemento_meio_lista = lista[indice_meio]
    return elemento_meio_lista


def checar_existencia_arquivo(nome_arquivo):
    resultado = os.path.isfile(nome_arquivo)
    return resultado


def transformar_duas_listas_em_dict(lista_chaves, lista_valores):
    dicionario = {chave: valor for chave, valor in zip(lista_chaves, lista_valores)}
    return dicionario


def obter_path_completo_arquivo(path, nome_arquivo):
    path_completo = os.path.join(path, nome_arquivo)
    return path_completo


def obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo):
    path = None

    if tipo_arquivo == "base":
        path = obter_path_arquivos_base()

    if tipo_arquivo == "lugares":
        path = obter_path_arquivos_lugares()

    if tipo_arquivo == "caminhos":
        path = obter_path_arquivos_caminhos()

    if tipo_arquivo == "resultados":
        path = obter_path_arquivos_resultados()

    if tipo_arquivo == "resultados_ts":
        path = obter_path_arquivos_resultados_ts()

    nome_arquivo_completo = obter_path_completo_arquivo(path, nome_arquivo)
    return nome_arquivo_completo


def obter_path_arquivos_base():
    path_arquivos_base = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_base"
    return path_arquivos_base


def obter_path_arquivos_lugares():
    path_arquivos_lugares = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares"
    return path_arquivos_lugares


def obter_path_arquivos_caminhos():
    path_arquivos_caminhos = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_caminhos"
    return path_arquivos_caminhos


def obter_path_arquivos_resultados():
    path_arquivos_resultados = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_resultados"
    return path_arquivos_resultados


def obter_path_arquivos_resultados_ts():
    path_arquivos_resultados_ts = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_resultados_ts"
    return path_arquivos_resultados_ts


def transformar_duas_listas_em_set(lista_1, lista_2):
    set_1 = set(lista_1)
    set_2 = set(lista_2)
    set_final = set_1.union(set_2)
    return set_final


def transformar_lista_em_matriz(lista_original, qnt_linhas, qnt_colunas):

    matriz_final = []

    for i in range(qnt_linhas):
        linha_temp = []
        for j in range(qnt_colunas):
            n = i * qnt_colunas + j
            linha_temp.append(lista_original[n])
        matriz_final.append(linha_temp)

    return matriz_final


def transformar_matriz_em_lista(matriz):
    lista_final = []

    for linha in matriz:
        for elemento in linha:
            lista_final.append(elemento)

    return lista_final


def contar_linhas_e_colunas_matriz(matriz):
    qnt_linhas = len(matriz)
    qnt_colunas = len(matriz[0])
    print("qnt de linhas: ", qnt_linhas)
    print("qnt_colunas: ", qnt_colunas)


def matriz_para_lista_dicionarios(lista_chaves, lista_valores):
    lista_dict = [{key: value for key, value in zip(lista_chaves, i)} for i in lista_valores]
    return lista_dict


def converter_orientacao_para_cor_v3(qnt_orientacoes):
    numero_total_cores = 256 * 256 * 256

    faixa = numero_total_cores // qnt_orientacoes
    # print(faixa)

    dict_orientacao_cores = {}

    for n in range(1, qnt_orientacoes + 1):

        orientacao = n * 100 - 100

        indice_cor = n * faixa
        # print("indice cor = ", indice_cor)

        cor_r = indice_cor // (256 * 256)
        # print("cor r = ", cor_r)

        cor_g = (indice_cor % (256 * 256)) // 256
        # print("cor g = ", cor_g)

        cor_b = (indice_cor % (256 * 256)) % 256
        # print("cor b = ", cor_b)

        cor_final = (cor_r, cor_g, cor_b)
        # print("cor final = ", cor_final)

        # print("orientação = {} / cor = {}".format(orientacao, cor_final))

        dict_orientacao_cores[str(orientacao)] = cor_final

        # print("--------------------\n")

    return dict_orientacao_cores


def converter_orientacao_para_cor_v4(orientacao):

    cor_r = orientacao // (256 * 256)
    cor_g = (orientacao % (256 * 256)) // 256
    cor_b = (orientacao % (256 * 256)) % 256

    cor_final = (cor_r, cor_g, cor_b)

    return cor_final


def lista_dicionarios_para_matriz(lista_dicionarios):
    matriz_final = [list(i.values()) for i in lista_dicionarios]
    return matriz_final


# pandas
def transformar_resultado_em_linha_csv(dict_resultado, nome_arquivo_destino):
    a = {key: value[0] for key, value in dict_resultado.items()}
    b = [i for i in a.values()]
    c = [b]
    lista_para_arquivo_csv(c, nome_arquivo_destino, separador=",", tipo_operacao="a")


def criar_ou_atualizar_arquivo_resultados(path, nome_arquivo_resultados, dict_resultado):
    arquivo_resultado_com_path = obter_path_completo_arquivo(path, nome_arquivo_resultados)
    existencia_arquivo_resultados = checar_existencia_arquivo(arquivo_resultado_com_path)

    if existencia_arquivo_resultados is False:
        data_frame = pd.DataFrame(dict_resultado)
        data_frame.to_csv(arquivo_resultado_com_path, index=False)
    else:
        transformar_resultado_em_linha_csv(dict_resultado, arquivo_resultado_com_path)


def sorteio_com_pesos(lista_possibilidades, lista_pesos, qnt_elementos_sorteados=1):
    lista_elementos_sorteados = random.choices(lista_possibilidades, weights=lista_pesos, k=qnt_elementos_sorteados)
    return lista_elementos_sorteados


def obter_lista_media(lista_original):
    lista_media = []

    for i in range(1, len(lista_original) + 1):
        recorte = lista_original[:i]
        media = sum(recorte) / len(recorte)
        lista_media.append(media)

    return lista_media


def update_orientacao_cor(dict_orientacoes_cores, orientacao_analisada, qnt_orientacoes=11):
    numero_total_cores = 256 * 256 * 256
    faixa = numero_total_cores // qnt_orientacoes

    menor_diferanca_orientacao = None
    orientacao_escolhida = None

    for orientacao, cor in dict_orientacoes_cores.items():
        orientacao_int = int(orientacao)
        diferenca_orientacao = orientacao_int - orientacao_analisada

        if menor_diferanca_orientacao is None:
            menor_diferanca_orientacao = diferenca_orientacao
            orientacao_escolhida = orientacao_int
        else:
            if abs(diferenca_orientacao) < abs(menor_diferanca_orientacao):
                menor_diferanca_orientacao = diferenca_orientacao
                orientacao_escolhida = orientacao_int

    if str(orientacao_escolhida) in dict_orientacoes_cores:
        cor_final = dict_orientacoes_cores[str(orientacao_escolhida)]
        return cor_final
    else:
        n = (orientacao_escolhida + 100) // 100
        indice_cor = n * faixa + menor_diferanca_orientacao

        cor_r = indice_cor // (256 * 256)
        cor_g = (indice_cor % (256 * 256)) // 256
        cor_b = (indice_cor % (256 * 256)) % 256

        cor_final = (cor_r, cor_g, cor_b)
        return cor_final


def descobir_dif_media(lista):

    lista_difs = []

    for i in range(1, len(lista)):
        dif = abs(lista[i] - lista[i-1])
        lista_difs.append(dif)

    dif_media = obter_media(lista_difs)

    return lista_difs


def descobrir_num_casa_decimais(n):

    i = 0

    while n - int(n) != 0:
        i += 1

    return i



