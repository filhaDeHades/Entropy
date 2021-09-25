#import plotly.express as px
#import plotly.graph_objects as go
import Modelo_fast.funcoes_fast as fst
import pandas as pd
import numpy as np
import random

nome_arq_res_ts = "modelo2(42x42)[tipo_1]_resultados_ts_1.txt"
path_res_ts = fst.obter_path_arquivos_resultados_ts()
arquivo_usado = fst.obter_path_completo_arquivo(path_res_ts, nome_arq_res_ts)


# pandas
def obter_data_frame(nome_arquivo):
    df = pd.read_csv(nome_arquivo)
    return df


# pandas
def obter_lista_nomes_de_arquivos(nome_arquivo, lista_linhas, nome_coluna):
    df = pd.read_csv(nome_arquivo)
    lista_nomes_arquivos = list(df.loc[lista_linhas, nome_coluna])
    return lista_nomes_arquivos


def obter_lista_entropias(df):
    lista_entropia = [round(i, 3) for i in df["lista_ent"]]
    return lista_entropia


def obter_lista_entropias_media(lista_entropia_normal):
    lista_entropia_media = []

    for x in range(1, len(lista_entropia_normal) + 1):
        lista_atual = lista_entropia_normal[:x]
        entropia_media = round(sum(lista_atual) / len(lista_atual), 3)
        lista_entropia_media.append(entropia_media)

    return lista_entropia_media


# pandas e plotly
def gerar_grafico_evolucao_entropia(nome_arquivo):

    df = pd.read_csv(nome_arquivo)

    lista_entropia = df["lista_ent"]
    lista_entropia2 = [round(i, 3) for i in df["lista_ent"]]

    lista_entropia_media = []

    for x in range(1, len(lista_entropia)+1):
        lista_atual = lista_entropia2[:x]
        entropia_media = round(sum(lista_atual)/len(lista_atual), 3)
        lista_entropia_media.append(entropia_media)

    eixo_x = list(range(1, 31))
    eixo_y = lista_entropia_media

    #fig = px.line(x=eixo_x, y=eixo_y)
    #fig.show()


def obter_grafico_evolucao_entropia_media(lista_entropia, eixo_x):
    eixo_y = obter_lista_entropias_media(lista_entropia)

    '''fig = go.Figure()

    dados_grafico = go.Scatter(x=eixo_x, y=eixo_y)
    fig.add_trace(dados_grafico)

    fig.update_layout(title="evolução entropia", xaxis_title="time steps", yaxis_title="entropia média")
    fig.show()'''


def obter_lista_linhas_usadas(inicio, fim):
    lista = []

    for i in range(inicio, fim + 1):
        lista.append(i)

    return lista


# plotly
def gerar_grafico_multiplas_linhas(valores_x, matriz_valores_y, cores_linhas):
    pass
    '''fig = go.Figure()

    for i in range(len(matriz_valores_y)):
        linha = go.Scatter(
            x=valores_x,
            y=matriz_valores_y[i],
            mode="lines",
            marker=dict(color="rgb{}".format(cores_linhas[i]))
        )
        fig.add_trace(linha)
    fig.show()'''


def obter_grafico_multiplas_linhas_entropia(nome_arquivo, linha_inicial, linha_final):

    arquivo_usado = fst.obter_path_completo_arquivo_v2(nome_arquivo, "resultados")

    df_statico = pd.read_csv(arquivo_usado)

    lista_linhas_usadas = obter_lista_linhas_usadas(linha_inicial, linha_final)
    nome_coluna_usada = "res_time_steps"

    lista_nomes_arquivos_usados = obter_lista_nomes_de_arquivos(arquivo_usado, lista_linhas_usadas, nome_coluna_usada)

    matriz_entropias = []
    lista_cores = []

    for i in range(len(lista_nomes_arquivos_usados)):
        # obtendo lista entropia media
        # print("nome arq: ", lista_nomes_arquivos_usados[i])
        nome_com_path = fst.obter_path_completo_arquivo_v2(lista_nomes_arquivos_usados[i], "resultados_ts")
        df = obter_data_frame(nome_com_path)
        lista_entropia = [round(i, 3) for i in df["lista_ent"]]
        # print("lista ent normal: ", lista_entropia)
        lista_entropia_media = obter_lista_entropias_media(lista_entropia)
        # print("lista ent media: ", lista_entropia_media)
        matriz_entropias.append(lista_entropia_media)

        # obtendo a cor
        cor_r = 51 * df_statico.loc[i, "peso_a"]
        cor_g = 51 * df_statico.loc[i, "peso_b"]
        cor_b = 51 * df_statico.loc[i, "peso_c"]
        cor = (cor_r, cor_g, cor_b)
        # print("cor: ", cor)
        lista_cores.append(cor)

        # print("-----------------------------")

    eixo_x = list(range(1, 31))

    gerar_grafico_multiplas_linhas(eixo_x, matriz_entropias, lista_cores)


def descobrir_multiplo_incial_cores(pesos_a, pesos_b, pesos_c):
    multiplo_inicial = max(max(pesos_a), max(pesos_b), max(pesos_c))
    return multiplo_inicial


def descobir_cor_rgb(multiplo_inicial, peso_a, peso_b, peso_c):
    cor_r = multiplo_inicial * peso_a
    cor_g = multiplo_inicial * peso_b
    cor_b = multiplo_inicial * peso_c

    cor_final = (cor_r, cor_g, cor_b)
    return cor_final


if __name__ == "__main__":

    lista_eixo_x = list(range(1, 31))
    lista_eixo_y = [random.randint(0, 10) for i in range(30)]

    obter_grafico_evolucao_entropia_media(lista_eixo_y, lista_eixo_x)
