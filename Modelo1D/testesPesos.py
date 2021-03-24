from Modelo1D.Grid1D import Grid1D
from Modelo1D.simulacao1D import simulacao1D
import Modelo1D.graficos as gg
import Modelo1D.funcoes1D as f1
import pandas as pd


def testes_pesos(testeAnalisado=1):
    
    tamGrid1D = 100
    qntAgentes = 100
    qntLugares = 100
    grid = Grid1D(tamGrid1D, qntAgentes, qntLugares)

    # legenda
    # 1 - grafico de multiplas linhas de entropia / 125 combinacoes de pesos
    # 2 - grafico de barras comparativo: inicio e final da simulacao / distancia importa vs distancia n importa 

    if testeAnalisado == 1:
        
        pesosA = [2, 4, 6]
        pesosB = [2, 4, 6]
        pesosC = [2, 4, 6]

        listaDataFramesStaticos = []
        listaDataFramesTimeSteps = []

        for a in pesosA:
            for b in pesosB:
                for c in pesosC:

                    pesoContaminacao = (a, b, c)

                    resultados = simulacao1D(grid, pesosContaminacao=pesoContaminacao)
                    
                    infoStatica = resultados["resultadosStaticos"]
                    dataFrameStatico = pd.DataFrame(infoStatica)
                    listaDataFramesStaticos.append(dataFrameStatico)

                    infoTimeSteps = resultados["resultadosTimeSteps"]
                    dataFrameTimeSteps = pd.DataFrame(infoTimeSteps)
                    listaDataFramesTimeSteps.append(dataFrameTimeSteps)

                    print("fim de uma simulacao / peso = ", pesoContaminacao)

        matrizEntropias = []

        for df in listaDataFramesTimeSteps:
            matrizEntropias.append(df["listaEntropias"])

        matrizEntropiasMedias = []
        
        for listaEntropia in matrizEntropias:
            listaEntropiaMedia = f1.obterListaMedia(listaEntropia)
            matrizEntropiasMedias.append(listaEntropiaMedia)
        
        listaStrPesos = []

        for df in listaDataFramesStaticos:
            # strPeso = str(df.loc[[0], ["pesosContaminacao"]])
            strPeso = str(df["pesosContaminacao"][0])
            # print(strPeso)
            listaStrPesos.append(strPeso)

        listaCoresRgb = []

        for df in listaDataFramesStaticos:
            cor = df["pesosContaminacao"][0]
            corFinal = tuple([i/10 for i in cor])
            # print(corFinal)
            listaCoresRgb.append(corFinal)

        eixoX = list(range(1, 31))
        gg.gerarGraficoMultiplasLinhasEntropia(eixoX, matrizEntropiasMedias, listaCoresRgb, listaStrPesos, 
                                            eixoX="time steps", eixoY="entropias", titulo="entropias por peso")
    
    elif testeAnalisado == 2:
        
        # resultados sim: distancia importa
        pesoEscolhaLugar = (0.1, 0.1)
        resultados = simulacao1D(grid, pesosEscolhaLugar=pesoEscolhaLugar)
        # print("fim da simulação")

        infoStatica = resultados["resultadosStaticos"]
        dataFrameStatico = pd.DataFrame(infoStatica)
    
        infoTimeSteps = resultados["resultadosTimeSteps"]
        dataFrameTimeSteps = pd.DataFrame(infoTimeSteps)

        eixoX = list(dataFrameTimeSteps.columns)[:-1]
        valoresY0 = list(dataFrameTimeSteps.iloc[0])[:-1]
        valoresY1 = list(dataFrameTimeSteps.iloc[29])[:-1]
        # print(eixoX)
        # print(valoresY0)
        # print(valoresY1)

        # resultados sim: distancia n importa
        pesoEscolhaLugar2 = (0.1, 0)
        resultados2 = simulacao1D(grid, pesosEscolhaLugar=pesoEscolhaLugar2)

        infoTimeSteps2 = resultados2["resultadosTimeSteps"]
        dataFrameTimeSteps2 = pd.DataFrame(infoTimeSteps2)

        valoresZ0 = list(dataFrameTimeSteps2.iloc[0])[:-1]
        valoresZ1 = list(dataFrameTimeSteps2.iloc[29])[:-1]

        gg.gerarGraficoBarrasComparar2Fatores(eixoX, valoresY0, valoresZ0, valoresY1, valoresZ1)
