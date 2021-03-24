import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def gerarGraficoMultiplasLinhasEntropia(valoresX, matrizValoresY, listaCores, listaLabels, 
                                        eixoX="eixo x", eixoY="eixoY", titulo="Titulo"):
    
    plt.figure()

    for i in range(len(matrizValoresY)):
        valoresY = matrizValoresY[i]
        label = listaLabels[i]
        cor = listaCores[i]
        plt.plot(valoresX, valoresY,color=cor, label=label)
       
    plt.xlabel(eixoX)
    plt.ylabel(eixoY)
    plt.title(titulo)
    plt.legend()
    plt.show()


def gerarGraficoBarrasComparar2Fatores(valoresX, valoresY0, valoresZ0, valoresY1, valoresZ1):
    fig, axs = plt.subplots(1, 2)

    eixoXusavel = np.arange(len(valoresX))
    larguraBarra = 0.3

    graficoBarras1 = axs[0].bar(eixoXusavel, valoresY0, width=larguraBarra, label="distancia importa")
    graficoBarras2 = axs[0].bar(eixoXusavel+larguraBarra , valoresZ0, width=larguraBarra, label="distancia n importa")
    
    # gerarLabelBarras(graficoBarras1)
    # gerarLabelBarras(graficoBarras2)
    
    axs[0].legend()
    axs[0].set_xticks(eixoXusavel)
    axs[0].set_xticklabels(valoresX)
    axs[0].set_xlabel("orientações")
    axs[0].set_ylabel("ocorrencias")
    axs[0].set_title("inicio da simulação")

    graficoBarras3 = axs[1].bar(eixoXusavel, valoresY1, width=larguraBarra, label="distancia importa")
    graficoBarras4 = axs[1].bar(eixoXusavel+larguraBarra, valoresZ1, width=larguraBarra, label="distancia n importa")
    
    # gerarLabelBarras(graficoBarras3)
    # gerarLabelBarras(graficoBarras4)

    axs[1].legend()
    axs[1].set_xticks(eixoXusavel)
    axs[1].set_xticklabels(valoresX)
    axs[1].set_xlabel("orientações")
    axs[1].set_ylabel("ocorrencias")
    axs[1].set_title("inicio da simulação")
    
    plt.show()

