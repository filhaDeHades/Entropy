import matplotlib.pyplot as plt
import numpy as np


def gerar_grafico_multiplas_linhas(valores_x, matriz_valores_y, utilizar_cores=False, lista_cores=None,
                                   utilizar_labels=False, lista_labels=None, eixo_x="eixo x", eixo_y="eixoY",
                                   titulo="Titulo"):
    plt.figure()

    for i in range(len(matriz_valores_y)):
        valores_y = matriz_valores_y[i]

        if utilizar_cores is True and utilizar_labels is True:
            label = lista_labels[i]
            cor = lista_cores[i]
            plt.plot(valores_x, valores_y, color=cor, label=label)
        else:
            plt.plot(valores_x, valores_y)

    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.legend()
    plt.show()


def gerarGraficoBarrasComparar2Fatores(valoresX, valoresY0, valoresZ0, valoresY1, valoresZ1):
    fig, axs = plt.subplots(1, 2)

    eixoXusavel = np.arange(len(valoresX))
    larguraBarra = 0.3

    graficoBarras1 = axs[0].bar(eixoXusavel, valoresY0, width=larguraBarra, label="distancia importa")
    graficoBarras2 = axs[0].bar(eixoXusavel + larguraBarra, valoresZ0, width=larguraBarra, label="distancia n importa")

    # gerarLabelBarras(graficoBarras1)
    # gerarLabelBarras(graficoBarras2)

    axs[0].legend()
    axs[0].set_xticks(eixoXusavel)
    axs[0].set_xticklabels(valoresX)
    axs[0].set_xlabel("orientações")
    axs[0].set_ylabel("ocorrencias")
    axs[0].set_title("inicio da simulação")

    graficoBarras3 = axs[1].bar(eixoXusavel, valoresY1, width=larguraBarra, label="distancia importa")
    graficoBarras4 = axs[1].bar(eixoXusavel + larguraBarra, valoresZ1, width=larguraBarra, label="distancia n importa")

    # gerarLabelBarras(graficoBarras3)
    # gerarLabelBarras(graficoBarras4)

    axs[1].legend()
    axs[1].set_xticks(eixoXusavel)
    axs[1].set_xticklabels(valoresX)
    axs[1].set_xlabel("orientações")
    axs[1].set_ylabel("ocorrencias")
    axs[1].set_title("inicio da simulação")

    plt.show()

