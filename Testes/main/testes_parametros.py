from Modelo1D.Grid1D import Grid1D
from Modelo1D.simulacao1D import simulacao1D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import Modelo_fast.funcoes_fast as fst
import numpy as np
import pandas as pd
import os


def teste_pesos_escolha_lugar():
    tam_grid_1D = 100
    qnt_agentes = 100
    qnt_lugares = 100
    range_orientacoes = (0, 1001, 1)
    grid = Grid1D(tam_grid_1D, qnt_agentes, qnt_lugares, agentes_aleatorios=False, lugares_aleatorios=False,
                  rangePossiveisOrientacoes=range_orientacoes)

    # print("lista orietacoes: ", grid.listaDeOrientacoes)

    pesos_escolha_lugar = (0.1, 0.1)
    pesos_contaminacao = (1, 0.1)

    resultados = simulacao1D(grid, pesosContaminacao=pesos_contaminacao, pesosEscolhaLugar=pesos_escolha_lugar,
                             qntTimeSteps=100, modelo_fabiano=True)

    info_statica = resultados["resultados_staticos"]
    info_time_steps = resultados["resultados_time_steps"]
    info_agentes = resultados["resultados_agentes"]
    info_lugares = resultados["resultados_lugares"]
    info_entropia = resultados["resultados_entropia"]

    # print("INFO STATICA:\n")
    # print(info_statica)
    #
    # print("\n---------------------------------\n")
    #
    # print("INFO TIME STEPS:\n")
    # print(info_time_steps)
    #
    # print("\n---------------------------------\n")
    #
    # print("INFO AGENTES:\n")
    # print(info_agentes)
    #
    # print("\n---------------------------------\n")
    #
    # print("INFO LUGARES: \n")
    # print(info_lugares)
    #
    # print("\n---------------------------------\n")

    # ------------------------------------------------------------------------------------------------------------------
    # grafico de entropia

    valores_entropia = list(info_time_steps["listaEntropias"])
    valores_entropia_media = fst.obter_lista_media(valores_entropia)
    # print("lista entropia: ", valores_entropia)

    qnt_linhas, qnt_colunas = info_time_steps.shape
    eixo_x = list(range(1, qnt_linhas+1))

    plt.plot(eixo_x, valores_entropia_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia")
    plt.title("entropia média x time steps / pesos = {}".format(pesos_escolha_lugar))
    plt.grid()
    plt.show()

    qnt_linhas, qnt_colunas = info_entropia.shape
    eixo_x = list(range(1, qnt_linhas + 1))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    valores_entropia_agentes = list(info_entropia["entropia_agentes"])
    valores_entropia_agentes_media = fst.obter_lista_media(valores_entropia_agentes)
    ax1.plot(eixo_x, valores_entropia_agentes_media, color=(1, 0, 0))
    ax1.set_xlabel("time steps")
    ax1.set_ylabel("entropia media agentes")
    ax1.set_title("entropia media agentes x time steps")

    valores_entropia_lugares = list(info_entropia["entropia_lugares"])
    valores_entropia_lugares_media = fst.obter_lista_media(valores_entropia_lugares)
    ax2.plot(eixo_x, valores_entropia_lugares_media, color=(1, 0, 0))
    ax2.set_xlabel("time steps")
    ax2.set_ylabel("entropia media lugares")
    ax2.set_title("entropia media lugares x time steps")

    valores_entropia_geral = list(info_entropia["entropia_geral"])
    valores_entropia_geral_media = fst.obter_lista_media(valores_entropia_geral)
    ax3.plot(eixo_x, valores_entropia_geral_media, color=(1, 0, 0))
    ax3.set_xlabel("time steps")
    ax3.set_ylabel("entropia media geral")
    ax3.set_title("entropia media geral x time steps")

    plt.show()

    # Fazendo o colormap dos agentes e lugares
    # colormap dos agentes

    lista_colunas_agentes = list(info_agentes.columns)
    grid_agentes = []

    for coluna in lista_colunas_agentes:
        coluna_agente = list(info_agentes[coluna])
        grid_agentes.append(coluna_agente)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    grafico1 = ax1.pcolor(grid_agentes, cmap="jet", vmin=0, vmax=1000)
    fig.colorbar(grafico1, ax=ax1)
    ax1.set_xlabel("time steps")
    ax1.set_ylabel("id agentes")
    ax1.set_title("orientações agentes X time steps")

    # colormap dos lugares
    lista_colunas_lugares = list(info_lugares.columns)
    grid_lugares = []

    for coluna in lista_colunas_lugares:
        coluna_lugar = list(info_lugares[coluna])
        grid_lugares.append(coluna_lugar)

    grafico2 = ax2.pcolor(grid_lugares, cmap="jet", vmin=0, vmax=1000)
    fig.colorbar(grafico2, ax=ax2)
    ax2.set_xlabel("time steps")
    ax2.set_ylabel("id lugares")
    ax2.set_title("orientações lugares X time steps")

    fig.tight_layout()
    plt.show()

    # fazendo grafico de linhas de orientacoes de agentes e lugares (agentes vermelhos e lugares azuis)
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
    plt.show()

    # fazendo graficos de barras das orientações dos agentes

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

    # fazendo o colormap da diferennça absoulta de orientações de agentes e orientações de lugares
    # nesse grafico são comparados todos os agentes com todos os lugares
    # em apenas 2 time steps: o primeiro e o ultimo

    matriz_dif_orientacoes_inicial = []
    matriz_dif_orientacoes_final = []

    qnt_linhas, qnt_colunas = info_agentes.shape
    ultima_linha = qnt_linhas - 1

    lista_agentes = list(info_agentes.columns)
    lista_lugares = list(info_lugares.columns)

    for agente in lista_agentes:

        linha_inicio = []
        linha_fim = []

        for lugar in lista_lugares:

            orientacao_agente_inicial = info_agentes.loc[0, agente]
            orientacao_lugar_inicial = info_lugares.loc[0, lugar]
            dif_orientacao_inicial = abs(orientacao_agente_inicial - orientacao_lugar_inicial)
            linha_inicio.append(dif_orientacao_inicial)

            orientacao_agente_final = info_agentes.loc[ultima_linha, agente]
            orientacao_lugar_final = info_lugares.loc[ultima_linha, lugar]
            dif_orientacao_final = abs(orientacao_agente_final - orientacao_lugar_final)
            linha_fim.append(dif_orientacao_final)

        matriz_dif_orientacoes_inicial.append(linha_inicio)
        matriz_dif_orientacoes_final.append(linha_fim)

    fig, (ax1, ax2) = plt.subplots(2, 1)

    grafico1 = ax1.pcolor(matriz_dif_orientacoes_inicial, cmap="PuBu")
    fig.colorbar(grafico1, ax=ax1)
    ax1.set_title("dif orientacoes agente X lugar - início")
    ax1.set_ylabel("agentes")

    grafico2 = ax2.pcolor(matriz_dif_orientacoes_final, cmap="PuBu")
    fig.colorbar(grafico2, ax=ax2)
    ax2.set_title("dif orientacoes agente X lugar - fim")
    ax2.set_xlabel("lugares")
    ax2.set_ylabel("agentes")

    plt.show()

    # fazendo o colormap de diferencas absolutas de orientacoes entre agentes e lugares
    # desta vez compara-se apenas os agentes e lugares de mesma posicao (agente 1 no lugar 1, agente 2 no lugar 2, etc)
    # mas se observa todos os time steps

    qnt_linhas, qnt_colunas = info_agentes.shape

    lista_lugares = list(info_lugares.columns)
    lista_agentes = list(info_agentes.columns)

    matriz_dif_orientacoes_ts = []

    for agente, lugar in zip(lista_agentes, lista_lugares):

        linha = []

        for time_step in range(qnt_linhas):

            orientacao_agente = info_agentes.loc[time_step, agente]
            orientacao_lugar = info_lugares.loc[time_step, lugar]
            dif_orientacao = abs(orientacao_agente - orientacao_lugar)
            linha.append(dif_orientacao)

        matriz_dif_orientacoes_ts.append(linha)

    fig, ax = plt.subplots(1)

    grafico = ax.pcolor(matriz_dif_orientacoes_ts, cmap="PuBu")
    fig.colorbar(grafico, ax=ax)
    ax.set_title("dif orientacoes agente e lugar X time Steps")
    ax.set_xlabel("time steps")
    ax.set_ylabel("agentes e lugares")

    plt.show()


def teste_pesos_escolha_lugar_media(pesos_contaminacao_agente, pesos_contaminacao_lugar, path_relativo_folder):

    salvar_resultados = True

    tam_grid_1D = 100
    qnt_agentes = 100
    qnt_lugares = 100
    range_orientacoes = (0, 1001, 1)
    grid = Grid1D(tam_grid_1D, qnt_agentes, qnt_lugares, agentes_aleatorios=False, lugares_aleatorios=False,
                  rangePossiveisOrientacoes=range_orientacoes)

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

        info_time_steps = None
        info_agentes = None
        info_lugares = None
        info_entropia = None

        for i in range(rodagens_por_peso):

            resultados = simulacao1D(grid, pesosContaminacaoAgente=pesos_contaminacao_agente, pesosContaminacaoLugar=pesos_contaminacao_lugar, 
                                    pesosEscolhaLugar=peso, qntTimeSteps=qnt_time_steps, modelo_fabiano=True)

            # *** OBS IMPORTANTE ***
            # o Pandas oferece uma funcionalidade muito boa de somar Data Frames
            # quando somamos um DF com outro, os valores de cada linha e coluna são somados de maneira correspondente
            # Ex: valor da linha 1 com a coluna 1 do DF1 eh somado com o valor da linha 1 e coluna 1 do DF2
            #     e assim em diante com todos os valores dos DF's

            # print("i = ", i)
            # print(resultados["resultados_agentes"], "\n")

            # TIME STEPS
            if info_time_steps is None:
                info_time_steps = resultados["resultados_time_steps"]
            else:
                info_time_steps += resultados["resultados_time_steps"]

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

        info_time_steps /= rodagens_por_peso
        info_agentes /= rodagens_por_peso
        info_lugares /= rodagens_por_peso
        info_entropia /= rodagens_por_peso

        if salvar_resultados is True:
            path_resultados = os.path.abspath(path_relativo_folder)
            nome_folder = "contAgentes_{}_contLugares{}_pesos_{}_ts_{}_media_{}".format(pesos_contaminacao_agente, pesos_contaminacao_lugar,
                                                                                         peso, qnt_time_steps, rodagens_por_peso)
            nome_folder_completo = os.path.join(path_resultados, nome_folder)
            os.mkdir(nome_folder_completo)

            nome_arquivo_ts = "df_time_steps.csv"
            nome_arquivo_ts = os.path.join(nome_folder_completo, nome_arquivo_ts)
            info_time_steps.to_csv(nome_arquivo_ts, index=False)

            nome_arquivo_agentes = "df_agentes.csv"
            nome_arquivo_agentes= os.path.join(nome_folder_completo, nome_arquivo_agentes)
            info_agentes.to_csv(nome_arquivo_agentes, index=False)

            nome_arquivo_lugares = "df_lugares.csv"
            nome_arquivo_lugares = os.path.join(nome_folder_completo, nome_arquivo_lugares)
            info_lugares.to_csv(nome_arquivo_lugares, index=False)

            nome_arquivo_entropia = "df_entropia.csv"
            nome_arquivo_entropia = os.path.join(nome_folder_completo, nome_arquivo_entropia)
            info_entropia.to_csv(nome_arquivo_entropia, index=False)


def testes_colormap_entropia():
    tam_grid_1D = 100
    qnt_agentes = 100
    qnt_lugares = 100
    grid = Grid1D(tam_grid_1D, qnt_agentes, qnt_lugares, agentes_aleatorios=False, lugares_aleatorios=False)

    pesos_a = np.arange(0.1, 1.52, 0.02)
    pesos_b = np.arange(0.1, 1.52, 0.02)

    pesos_contaminacao = (1, 0.1)

    grid_entropia_agentes = []
    grid_entropia_lugares = []
    grid_entropia_geral = []

    for a in pesos_a:

        linha_agentes = []
        linha_lugares = []

        for b in pesos_b:

            peso_escolha_lugar = (a, b)

            resultados = simulacao1D(grid, pesosContaminacao=pesos_contaminacao, pesosEscolhaLugar=peso_escolha_lugar,
                                     qntTimeSteps=2000,
                                     modelo_fabiano=True)

            df_entropia = resultados["resultados_entropia"]

            lista_entropia_agentes = list(df_entropia["entropia_agentes"])
            entropia_media = round(sum(lista_entropia_agentes) / len(lista_entropia_agentes), 3)
            linha_agentes.append(entropia_media)

            lista_entropia_lugares = list(df_entropia["entropia_lugares"])
            entropia_media_lugares = round(sum(lista_entropia_lugares)/len(lista_entropia_lugares), 3)
            linha_lugares.append(entropia_media_lugares)

            print("simulacao concluida / pesos = ", peso_escolha_lugar)

        grid_entropia_agentes.append(linha_agentes)
        grid_entropia_lugares.append(linha_lugares)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    grafico1 = ax1.pcolor(grid_entropia_agentes, cmap="OrRd", vmin=0)
    fig.colorbar(grafico1, ax=ax1)
    ax1.set_xlabel("valores de B")
    ax1.set_ylabel("valores de A")
    ax1.set_title("entropia agentes X pesos")

    grafico2 = ax2.pcolor(grid_entropia_lugares, cmap="OrRd", vmin=0)
    fig.colorbar(grafico2, ax=ax2)
    ax2.set_xlabel("valores de B")
    ax2.set_ylabel("valores de A")
    ax2.set_title("entropia lugares X pesos")

    plt.show()


def testes_colormap_entropia_v2():
    tam_grid_1D = 100
    qnt_agentes = 100
    qnt_lugares = 100
    grid = Grid1D(tam_grid_1D, qnt_agentes, qnt_lugares, agentes_aleatorios=False, lugares_aleatorios=False)

    pesos_a = np.arange(0.1, 1.52, 0.02)
    pesos_b = np.arange(0.1, 1.52, 0.02)

    pesos_contaminacao = (1, 0.1)

    for a in pesos_a:

        for b in pesos_b:

            peso_escolha_lugar = (a, b)

            resultados = simulacao1D(grid, pesosContaminacao=pesos_contaminacao, pesosEscolhaLugar=peso_escolha_lugar,
                                     qntTimeSteps=2000,
                                     modelo_fabiano=True)

            df_entropia = resultados["resultados_entropia"]
            path = os.path.abspath("Testes\\main\\resultados_entropia")
            nome_arquivo = "resultados_entropia_{}".format(peso_escolha_lugar)
            nome_arquivo_completo = os.path.join(path, nome_arquivo)
            df_entropia.to_csv(nome_arquivo_completo, index=False)
            print("arquivo: {} salvo com sucesso".format(nome_arquivo_completo))


def ver_graficos_resultados():
    lista_resultados = [i for i in os.listdir(os.getcwd()) if os.path.isdir(i) is True]

    for i in range(len(lista_resultados)):
        print("{} - {}".format(i, lista_resultados[i]))

    a0 = int(input("selecione o dir: "))
    dir_sel_inicial = lista_resultados[a0]

    path = os.path.abspath(dir_sel_inicial)
    lista_dir = os.listdir(path)

    for i in range(len(lista_dir)):
        print("{} - {}".format(i, lista_dir[i]))

    a = int(input("\nselecione o resultado que deseja ver: "))
    dir_sel = lista_dir[a]

    path2 = os.path.join(path, dir_sel)
    lista_arq = os.listdir(path2)

    info_time_steps = None
    info_agentes = None
    info_lugares = None
    info_entropia = None

    for i in range(len(lista_arq)):

        nome_arquivo_com_path = os.path.join(path2, lista_arq[i])

        if i == 0:
            info_agentes = pd.read_csv(nome_arquivo_com_path)
        elif i == 1:
            info_entropia = pd.read_csv(nome_arquivo_com_path)
        elif i == 2:
            info_lugares = pd.read_csv(nome_arquivo_com_path)
        elif i == 3:
            info_time_steps = pd.read_csv(nome_arquivo_com_path)

    # ------ GRAFICOS --------

    # ------------------------------------------------------------------------------------------------------------------

    # GRAFICO ENTROPIA AGENTES

    valores_entropia_agentes = list(info_entropia["entropia_agentes"])
    valores_entropia_agentes_media = fst.obter_lista_media(valores_entropia_agentes)

    qnt_linhas, qnt_colunas = info_time_steps.shape
    eixo_x = list(range(1, qnt_linhas + 1))

    plt.plot(eixo_x, valores_entropia_agentes_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia")
    plt.title("entropia média agentes x time steps")
    plt.grid()
    plt.show()

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
    plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # GRAFICO ENTROPIA GERAL

    valores_entropia_geral = list(info_entropia["entropia_geral"])
    valores_entropia_geral_media = fst.obter_lista_media(valores_entropia_geral)
    plt.plot(eixo_x, valores_entropia_geral_media, color=(1, 0, 0))
    plt.xlabel("time steps")
    plt.ylabel("entropia media geral")
    plt.title("entropia media geral x time steps")
    plt.grid()
    plt.show()

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
    plt.show()

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
    plt.show()

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
    plt.show()

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

    matriz_dif_orientacoes_inicial = []
    matriz_dif_orientacoes_final = []

    qnt_linhas, qnt_colunas = info_agentes.shape
    ultima_linha = qnt_linhas - 1

    lista_agentes = list(info_agentes.columns)
    lista_lugares = list(info_lugares.columns)

    for agente in lista_agentes:

        linha_inicio = []
        linha_fim = []

        for lugar in lista_lugares:
            orientacao_agente_inicial = info_agentes.loc[0, agente]
            orientacao_lugar_inicial = info_lugares.loc[0, lugar]
            dif_orientacao_inicial = abs(orientacao_agente_inicial - orientacao_lugar_inicial)
            linha_inicio.append(dif_orientacao_inicial)

            orientacao_agente_final = info_agentes.loc[ultima_linha, agente]
            orientacao_lugar_final = info_lugares.loc[ultima_linha, lugar]
            dif_orientacao_final = abs(orientacao_agente_final - orientacao_lugar_final)
            linha_fim.append(dif_orientacao_final)

        matriz_dif_orientacoes_inicial.append(linha_inicio)
        matriz_dif_orientacoes_final.append(linha_fim)

    fig, (ax1, ax2) = plt.subplots(2, 1)

    grafico1 = ax1.pcolor(matriz_dif_orientacoes_inicial, cmap="PuBu")
    fig.colorbar(grafico1, ax=ax1)
    ax1.set_title("diferença orientações agente X lugar (início)")
    ax1.set_ylabel("agentes")

    grafico2 = ax2.pcolor(matriz_dif_orientacoes_final, cmap="PuBu")
    fig.colorbar(grafico2, ax=ax2)
    ax2.set_title("diferença orientações agente X lugar (fim)")
    ax2.set_xlabel("lugares")
    ax2.set_ylabel("agentes")

    plt.show()

    # ------------------------------------------------------------------------------------------------------------------
    # COLORMAP AZUL DIF ORIENTACOES AGENTE E LUGAR MSM ID AO LONGO DO TEMPO

    # fazendo o colormap de diferencas absolutas de orientacoes entre agentes e lugares
    # desta vez compara-se apenas os agentes e lugares de mesma posicao (agente 1 no lugar 1, agente 2 no lugar 2, etc)
    # mas se observa todos os time steps

    qnt_linhas, qnt_colunas = info_agentes.shape

    lista_lugares = list(info_lugares.columns)
    lista_agentes = list(info_agentes.columns)

    matriz_dif_orientacoes_ts = []

    for agente, lugar in zip(lista_agentes, lista_lugares):

        linha = []

        for time_step in range(qnt_linhas):
            orientacao_agente = info_agentes.loc[time_step, agente]
            orientacao_lugar = info_lugares.loc[time_step, lugar]
            dif_orientacao = abs(orientacao_agente - orientacao_lugar)
            linha.append(dif_orientacao)

        matriz_dif_orientacoes_ts.append(linha)

    fig, ax = plt.subplots(1)

    grafico = ax.pcolor(matriz_dif_orientacoes_ts, cmap="PuBu")
    fig.colorbar(grafico, ax=ax)
    ax.set_title("dif orientações agente e lugar X time Steps")
    ax.set_xlabel("time steps")
    ax.set_ylabel("agentes e lugares")

    plt.show()


def testes():

    a = np.linspace(0.1, 1.0, 5)
    print(a)
