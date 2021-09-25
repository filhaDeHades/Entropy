from Modelo_fast.apresentacoes_fast2 import simulacao_com_arquivo
import Modelo_fast.funcoes_fast as fst
import matplotlib.pyplot as plt
#import mplcursors
import Modelo_fast.graficos_matplotly as gm
import numpy as np

lista_arquivos_base = ["modelo1(42x42)[tipo_1].txt",    # 0
                       "modelo2-inv(42x42)[tipo_1].txt",    # 1
                       "modelo4(42x42)[tipo_1].txt",    # 2
                       "modelo5(42x42)[tipo_1].txt",    # 3
                       "modelo6(42x42)[tipo_1].txt"]    # 4


arquivo_usado = lista_arquivos_base[0]

pesos_dif_orientacao = np.linspace(0, 1, 100)
pesos_distancia = np.linspace(0, 1, 100)

numero_simulacao = 0
qnt_time_steps_teste = 30

matriz_entropias = []
lista_cores = []
lista_labels = []

for peso_orientacao in pesos_dif_orientacao:
    for peso_distancia in pesos_distancia:

        numero_simulacao += 1

        peso_atual = (peso_orientacao, peso_distancia)
        df_resultados = simulacao_com_arquivo(arquivo_usado, pesos_escolha_lugar=peso_atual, salvar_resultados=False,
                                              retornar_resultados_ts=True, num_sim_atual=numero_simulacao)

        lista_entropia = list(df_resultados["lista_ent"])
        lista_entropia_media = fst.obter_lista_media(lista_entropia)
        matriz_entropias.append(lista_entropia_media)

        cor_atual = (peso_atual[0], peso_atual[1], 1)
        lista_cores.append(cor_atual)
        lista_labels.append(str(peso_atual))

        print("simulacao {} finalziada / pesos = {}".format(numero_simulacao, peso_atual))

    # ------------------------------------------------------------
# df_resultados = simulacao_com_arquivo(arquivo_usado, pesos_escolha_lugar=(0.5, 0.5, 1), salvar_resultados=False,
#                                         retornar_resultados_ts=True, num_sim_atual=numero_simulacao)

# lista_entropia = list(df_resultados["lista_ent"])
# lista_entropia_media = fst.obter_lista_media(lista_entropia)
# matriz_entropias.append(lista_entropia_media)

# cor_atual = (0.5, 0.5, 1)
# lista_cores.append(cor_atual)
# lista_labels.append(str((0.5, 0.5)))
    # ------------------------------------------------------------
    

eixo_x = list(range(1, qnt_time_steps_teste+1))

fig, ax = plt.subplots()

for i in range(len(matriz_entropias)):
    linha = matriz_entropias[i]
    cor = lista_cores[i]
    label = lista_labels[i]
    plt.plot(eixo_x, linha, color=cor, label=label)

#trocar por funções do matplotlib:
#mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

plt.legend()
plt.show()
