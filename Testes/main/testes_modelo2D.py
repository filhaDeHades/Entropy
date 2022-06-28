from Modelo_fast.ClasseGridV2Fast import GridV2Fast
from Modelo_fast.ClasseAgenteV2Fast import AgenteV2Fast
from Modelo_fast.ClasseLugarV2Fast import LugarV2Fast
from Modelo_fast.simulacao_fast4 import simulacao_fast4
from Modelo_fast.apresentacoes_fast2 import simulacao_com_arquivo
import Modelo_5.funcoes_arquivos as func_arq
import Modelo_5.simulacao2 as s2
import Modelo_5.apresentacoes as apr
from Modelo_5.apresentacoes import simulacao_com_arquivo_2
from Modelo_5.simulacao import simulacao
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import Modelo_fast.funcoes_fast as fst
import numpy as np
import os



def testes_pesos_escolha_lugar_media(pesos_contaminacao_agente, pesos_contaminacao_lugar, path_relativo_folder):

    salvar_resultados = True

    qnt_linhas = 100
    qnt_colunas = 100
    qnt_agentes = 100
    qnt_lugares = 100
    range_orientacoes = (0, 1001, 1)
    grid = GridV2Fast(qnt_linhas, qnt_colunas, qnt_agentes, qnt_lugares, range_possiveis_orientacoes=range_orientacoes)

    lista_pesos_a = np.linspace(0.1, 1.0, 5)
    lista_pesos_b = np.linspace(0.1, 1.0, 5)

    lista_pesos_esolha_lugar = []

    for a in lista_pesos_a:
        for b in lista_pesos_b:
            peso = (a, b)
            lista_pesos_esolha_lugar.append(peso)

    # pesos_a = [round(i / 10, 1) for i in range(1, 16)]
    # pesos_b = [round(i / 10, 1) for i in range(1, 16)]
    #
    # lista_pesos = [(a, b) for a in pesos_a for b in pesos_b]
    #
    # set_pesos_novos = set(lista_pesos) - set(lista_pesos_esolha_lugar)
    # lista_pesos_novos = list(set_pesos_novos)
    # lista_pesos_novos.sort()

    rodagens_por_peso = 10
    qnt_time_steps = 2000

    for peso in lista_pesos_esolha_lugar:

        info_agentes = None
        info_lugares = None
        info_entropia = None

        for i in range(rodagens_por_peso):

            resultados = simulacao_fast4(grid, pesosContaminacaoAgente=pesos_contaminacao_agente, pesosContaminacaoLugar=pesos_contaminacao_lugar, 
                                    pesosEscolhaLugar=peso, qntTimeSteps=qnt_time_steps)

            # *** OBS IMPORTANTE ***
            # o Pandas oferece uma funcionalidade muito boa de somar Data Frames
            # quando somamos um DF com outro, os valores de cada linha e coluna são somados de maneira correspondente
            # Ex: valor da linha 1 com a coluna 1 do DF1 eh somado com o valor da linha 1 e coluna 1 do DF2
            #     e assim em diante com todos os valores dos DF's

            # print("i = ", i)
            # print(resultados["resultados_agentes"], "\n")

            # AGENTES
            if info_agentes is None:
                info_agentes = resultados["resultados_agentes"]
            else:
                info_agentes += resultados["resultados_agentes"]

            # LUGARES
            if info_lugares is None:
                info_lugares = resultados["resultados_lugares"]
            else:
                info_lugares += resultados["resultados_lugares"]

            # ENTROPIA
            if info_entropia is None:
                info_entropia = resultados["resultados_entropia"]
            else:
                info_entropia = resultados["resultados_entropia"]

            print("fim a simulacao {} / peso {}".format(i, peso))

        print("fim das simulações / pesos = {} / time steps = {} / qnt rodagens = {}".format(peso, qnt_time_steps, rodagens_por_peso))

        # ja tenho todos os Data Frames somados, eh preciso dividir os DF's pelo numero de vezes que cada simulação foi
        # rodada para obter os valores medios

        info_agentes /= rodagens_por_peso
        info_lugares /= rodagens_por_peso
        info_entropia /= rodagens_por_peso

        if salvar_resultados is True:
            path_resultados = os.path.abspath(path_relativo_folder)
            nome_folder = "contAgentes_{}_contLugares{}_pesos_{}_ts_{}_media_{}".format(pesos_contaminacao_agente, pesos_contaminacao_lugar,
                                                                                         peso, qnt_time_steps, rodagens_por_peso)
            nome_folder_completo = os.path.join(path_resultados, nome_folder)
            os.mkdir(nome_folder_completo)

            nome_arquivo_agentes = "df_agentes.csv"
            nome_arquivo_agentes= os.path.join(nome_folder_completo, nome_arquivo_agentes)
            info_agentes.to_csv(nome_arquivo_agentes, index=False)

            nome_arquivo_lugares = "df_lugares.csv"
            nome_arquivo_lugares = os.path.join(nome_folder_completo, nome_arquivo_lugares)
            info_lugares.to_csv(nome_arquivo_lugares, index=False)

            nome_arquivo_entropia = "df_entropia.csv"
            nome_arquivo_entropia = os.path.join(nome_folder_completo, nome_arquivo_entropia)
            info_entropia.to_csv(nome_arquivo_entropia, index=False)



def teste_modelo_2d():

    qnt_linhas = 10
    qnt_colunas = 10
    qnt_agentes = 100
    qnt_lugares = 100
    range_orientacoes = (0, 1001, 1)
    grid = GridV2Fast(qnt_linhas, qnt_colunas, qnt_agentes, qnt_lugares, range_possiveis_orientacoes=range_orientacoes)
    # grid.teste_lugares_certo()

    qnt_time_steps = 2000
    pesos_escolha_lugar = (0.1, 0.1)
    peso_contaminacao_agente = (1, 1)
    peso_contaminacao_lugar = (1, 1)

    resultados = simulacao_fast4(grid, 
                                pesosContaminacaoAgente=peso_contaminacao_agente,
                                pesosContaminacaoLugar=peso_contaminacao_lugar, 
                                pesosEscolhaLugar=pesos_escolha_lugar, 
                                qntTimeSteps=qnt_time_steps)
    
    info_statica = resultados["resultados_staticos"]
    info_agentes = resultados["resultados_agentes"]
    info_lugares = resultados["resultados_lugares"]
    info_entropia = resultados["resultados_entropia"]

    # ------ GRAFICOS --------

    # ------------------------------------------------------------------------------------------------------------------

    # GRAFICO ENTROPIA AGENTES

    valores_entropia_agentes = list(info_entropia["entropia_agentes"])
    valores_entropia_agentes_media = fst.obter_lista_media(valores_entropia_agentes)

    qnt_linhas, qnt_colunas = info_entropia.shape
    eixo_x = list(range(1, qnt_linhas + 1))

    plt.plot(eixo_x, valores_entropia_agentes_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia")
    plt.title("entropia média agentes x time steps")
    plt.grid()
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICO ENTROPIA LUGARES

    qnt_linhas, qnt_colunas = info_entropia.shape
    eixo_x = list(range(1, qnt_linhas + 1))

    valores_entropia_lugares = list(info_entropia["entropia_lugares"])
    valores_entropia_lugares_media = fst.obter_lista_media(valores_entropia_lugares)
    plt.plot(eixo_x, valores_entropia_lugares_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia media lugares")
    plt.title("entropia média lugares x time steps")
    plt.grid()
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICO ENTROPIA GERAL

    valores_entropia_geral = list(info_entropia["entropia_geral"])
    valores_entropia_geral_media = fst.obter_lista_media(valores_entropia_geral)
    plt.plot(eixo_x, valores_entropia_geral_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia media geral")
    plt.title("entropia media geral x time steps")
    plt.grid()
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICOS ENTROPIA (3 GRAFICOS)
    #
    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    #
    # valores_entropia_agentes = list(info_entropia["entropia_agentes"])
    # valores_entropia_agentes_media = fst.obter_lista_media(valores_entropia_agentes)
    # ax1.plot(eixo_x, valores_entropia_agentes_media, color=(1, 0, 0))
    # ax1.set_xlabel("time steps")
    # ax1.set_ylabel("entropia media agentes")
    # ax1.set_title("entropia media agentes x time steps")
    #
    # valores_entropia_lugares = list(info_entropia["entropia_lugares"])
    # valores_entropia_lugares_media = fst.obter_lista_media(valores_entropia_lugares)
    # ax2.plot(eixo_x, valores_entropia_lugares_media, color=(1, 0, 0))
    # ax2.set_xlabel("time steps")
    # ax2.set_ylabel("entropia media lugares")
    # ax2.set_title("entropia media lugares x time steps")
    #
    # valores_entropia_geral = list(info_entropia["entropia_geral"])
    # valores_entropia_geral_media = fst.obter_lista_media(valores_entropia_geral)
    # ax3.plot(eixo_x, valores_entropia_geral_media, color=(1, 0, 0))
    # ax3.set_xlabel("time steps")
    # ax3.set_ylabel("entropia media geral")
    # ax3.set_title("entropia media geral x time steps")
    #
    # plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # COLORMAP AGENTES

    lista_colunas_agentes = list(info_agentes.columns)
    grid_agentes = []

    for coluna in lista_colunas_agentes:
        coluna_agente = list(info_agentes[coluna])
        grid_agentes.append(coluna_agente)

    fig, ax1 = plt.subplots()
    grafico1 = ax1.pcolor(grid_agentes, cmap="jet", vmin=0, vmax=1000)
    fig.colorbar(grafico1, ax=ax1)
    ax1.set_xlabel("time steps")
    ax1.set_ylabel("id agentes")
    ax1.set_title("orientações agentes X time steps")
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # COLORMAP LUGARES

    fig, ax1 = plt.subplots()

    lista_colunas_lugares = list(info_lugares.columns)
    grid_lugares = []

    for coluna in lista_colunas_lugares:
        coluna_lugar = list(info_lugares[coluna])
        grid_lugares.append(coluna_lugar)

    grafico2 = ax1.pcolor(grid_lugares, cmap="jet", vmin=0, vmax=1000)
    fig.colorbar(grafico2, ax=ax1)
    ax1.set_xlabel("time steps")
    ax1.set_ylabel("id lugares")
    ax1.set_title("orientações lugares X time steps")
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICO LINHAS ORIENTACAO AGENTES E LUGARES

    for agente in grid_agentes:
        plt.plot(eixo_x, agente, color=(1, 0, 0), linewidth=0.5)

    for lugar in grid_lugares:
        plt.plot(eixo_x, lugar, color=(0, 0, 1), linewidth=0.5)

    legenda = [Line2D([0], [0], color="r", label="agentes"),
               Line2D([0], [0], color="b", label="lugares")]

    plt.title("orientações agentes/lugares X time steps")
    plt.xlabel("time steps")
    plt.ylabel("orientações")
    plt.legend(handles=legenda)
    #plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICO DE BARRAS ORIENTACOES AGENTES - INICIO VS FIM

    # info_time_steps2 = info_time_steps.drop(columns=["listaEntropias"])
    # lista_orientacoes = list(info_time_steps2.columns)
    #
    # orientacoes_ts0 = list(info_time_steps2.iloc[0])
    # orientacoes_ts99 = list(info_time_steps2.iloc[99])
    #
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    #
    # ax1.bar(lista_orientacoes, orientacoes_ts0, color="#6097D8")
    # ax1.set_title("orientacoes agentes / time step 0")
    # ax1.set_xlabel("orientações")
    # ax1.set_ylabel("ocorrências")
    #
    # ax2.bar(lista_orientacoes, orientacoes_ts99, color="#6097D8")
    # ax2.set_title("orientacoes agentes / time step 99")
    # ax2.set_xlabel("orientações")
    # ax2.set_ylabel("ocorrências")
    #
    # plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # COLORMAP AZUL DIF ORIENTACOES AGENTES E LUGARES

    # fazendo o colormap da diferença absoulta de orientações de agentes e orientações de lugares
    # nesse grafico são comparados todos os agentes com todos os lugares
    # em apenas 2 time steps: o primeiro e o ultimo

    # matriz_dif_orientacoes_inicial = []
    # matriz_dif_orientacoes_final = []

    # qnt_linhas, qnt_colunas = info_agentes.shape
    # ultima_linha = qnt_linhas - 1

    # lista_agentes = list(info_agentes.columns)
    # lista_lugares = list(info_lugares.columns)

    # for agente in lista_agentes:

    #     linha_inicio = []
    #     linha_fim = []

    #     for lugar in lista_lugares:
    #         orientacao_agente_inicial = info_agentes.loc[0, agente]
    #         orientacao_lugar_inicial = info_lugares.loc[0, lugar]
    #         dif_orientacao_inicial = abs(orientacao_agente_inicial - orientacao_lugar_inicial)
    #         linha_inicio.append(dif_orientacao_inicial)

    #         orientacao_agente_final = info_agentes.loc[ultima_linha, agente]
    #         orientacao_lugar_final = info_lugares.loc[ultima_linha, lugar]
    #         dif_orientacao_final = abs(orientacao_agente_final - orientacao_lugar_final)
    #         linha_fim.append(dif_orientacao_final)

    #     matriz_dif_orientacoes_inicial.append(linha_inicio)
    #     matriz_dif_orientacoes_final.append(linha_fim)

    # fig, (ax1, ax2) = plt.subplots(2, 1)

    # grafico1 = ax1.pcolor(matriz_dif_orientacoes_inicial, cmap="PuBu")
    # fig.colorbar(grafico1, ax=ax1)
    # ax1.set_title("diferença orientações agente X lugar (início)")
    # ax1.set_ylabel("agentes")

    # grafico2 = ax2.pcolor(matriz_dif_orientacoes_final, cmap="PuBu")
    # fig.colorbar(grafico2, ax=ax2)
    # ax2.set_title("diferença orientações agente X lugar (fim)")
    # ax2.set_xlabel("lugares")
    # ax2.set_ylabel("agentes")

    # plt.show()

    # # ------------------------------------------------------------------------------------------------------------------
    # # COLORMAP AZUL DIF ORIENTACOES AGENTE E LUGAR MSM ID AO LONGO DO TEMPO

    # # fazendo o colormap de diferencas absolutas de orientacoes entre agentes e lugares
    # # desta vez compara-se apenas os agentes e lugares de mesma posicao (agente 1 no lugar 1, agente 2 no lugar 2, etc)
    # # mas se observa todos os time steps

    # qnt_linhas, qnt_colunas = info_agentes.shape

    # lista_lugares = list(info_lugares.columns)
    # lista_agentes = list(info_agentes.columns)

    # matriz_dif_orientacoes_ts = []

    # for agente, lugar in zip(lista_agentes, lista_lugares):

    #     linha = []

    #     for time_step in range(qnt_linhas):
    #         orientacao_agente = info_agentes.loc[time_step, agente]
    #         orientacao_lugar = info_lugares.loc[time_step, lugar]
    #         dif_orientacao = abs(orientacao_agente - orientacao_lugar)
    #         linha.append(dif_orientacao)

    #     matriz_dif_orientacoes_ts.append(linha)

    # fig, ax = plt.subplots(1)

    # grafico = ax.pcolor(matriz_dif_orientacoes_ts, cmap="PuBu")
    # fig.colorbar(grafico, ax=ax)
    # ax.set_title("dif orientações agente e lugar X time Steps")
    # ax.set_xlabel("time steps")
    # ax.set_ylabel("agentes e lugares")

    # plt.show()


def teste_modelo_2d_com_arquivo(nomeArquivo, qnt_time_step=2000,fQA=2.5, peso_escolha_lugar=(0.1, 0.1), peso_cont_agente=(1,1), peso_cont_lugar=(1,1)):
    """Essa função faz a simulação 2D a partir de um arquivo e retorna seus resultados.

    Args:
        nomeArquivo (String): Arquivo base do qual sairá o grid para a simulação
        qnt_time_step (int, optional): Time steps da simulação. Defaults to 2000.
        peso_escolha_lugar (tuple, optional): Pesos Alfa e Beta (float). Defaults to (0.1, 0.1).
        peso_cont_agente (tuple, optional): Pesos C e D dos agentes (float). Defaults to (1,1).
        peso_cont_lugar (tuple, optional): Pesos C e D dos lugares (float). Defaults to (1,1).

    Returns:
        dict: Dados resultantes da simulação
    """

    qnt_time_steps = qnt_time_step
    pesos_escolha_lugar = peso_escolha_lugar
    peso_contaminacao_agente = peso_cont_agente
    peso_contaminacao_lugar = peso_cont_lugar

    resultados = simulacao_com_arquivo(nomeArquivo, pesos_escolha_lugar=pesos_escolha_lugar, peso_cont_agente=peso_contaminacao_agente,
                                        peso_cont_lugar=peso_contaminacao_lugar,qnt_time_steps=qnt_time_steps, fQA=fQA,
                                        salvar_resultados=True, mostrar_grafico_entropia=True, retornar_resultados_ts=False)
    
    info_agentes = resultados["resultados_agentes"]
    info_lugares = resultados["resultados_lugares"]
    info_entropia = resultados["resultados_entropia"]

    return resultados

def teste_modelo_2d_visual(nomeArquivo, qnt_time_step=2000, fQA=2.5, peso_escolha_lugar=(0.1, 0.1), peso_cont_agente=(1,1), peso_cont_lugar=(1,1)):
    qnt_time_steps = qnt_time_step
    pesos_escolha_lugar = peso_escolha_lugar
    peso_contaminacao_agente = peso_cont_agente
    peso_contaminacao_lugar = peso_cont_lugar

    resultados = apr.simulacao_com_arquivo_V(nomeArquivo, qnt_time_steps, pesos_escolha_lugar, peso_contaminacao_agente, peso_contaminacao_lugar, fQA=fQA)

    # resultados = simulacao_com_arquivo(nomeArquivo, pesos_escolha_lugar=pesos_escolha_lugar, peso_cont_agente=peso_contaminacao_agente,
    #                                     peso_cont_lugar=peso_contaminacao_lugar,qnt_time_steps=qnt_time_steps,
    #                                     salvar_resultados=True, mostrar_grafico_entropia=True, retornar_resultados_ts=False)
    
    # info_agentes = resultados["resultados_agentes"]
    # info_lugares = resultados["resultados_lugares"]
    # info_entropia = resultados["resultados_entropia"]

    return resultados