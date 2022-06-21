from Modelo1D.Agente1D import Agente1D
from Modelo1D.Lugar1D import Lugar1D
import numpy as np
import random
import math


class Grid1D:

    def __init__(self, tamGrid, qntAgentes, qntLugares, rangePossiveisOrientacoes=(0, 1000),
                 agentes_aleatorios=False, lugares_aleatorios=False):
        self.qntAgentes = qntAgentes
        self.qntLugares = qntLugares
        self.tamGrid = tamGrid
        self.listaDeOrientacoes = self.obterListaDeOrientacoes(rangePossiveisOrientacoes)

        if agentes_aleatorios is False:
            self.arrayAgentes = self.criar_agentes()
        else:
            self.arrayAgentes = self.criarAgentesAleatorios()

        if lugares_aleatorios is False:
            self.arrayLugares = self.criar_lugares()
        else:
            self.arrayLugares = self.criarLugaresAleatorios()

    def obterListaDeOrientacoes(self, rangeOrientacoes):
        primeiraOrientacao = rangeOrientacoes[0]
        ultimaOrientacao = rangeOrientacoes[1]
        step = 1

        if len(rangeOrientacoes) == 3:
            step = rangeOrientacoes[2]

        possiveisOrientacoes = list(range(primeiraOrientacao, ultimaOrientacao, step))
        return possiveisOrientacoes

    def criar_agentes(self):
        lista_agentes = []

        for i in range(self.qntAgentes):
            orientacao_latente = random.choice(self.listaDeOrientacoes)
            orientacao_atual = random.choice(self.listaDeOrientacoes)
            novo_agente = Agente1D(orientacao_latente, orientacao_atual, i, id_agente=i)
            lista_agentes.append(novo_agente)

        array_agentes = np.array(lista_agentes)
        return array_agentes

    def criarAgentesAleatorios(self):
        listaAgentes = []

        possiveisPosicoesUsaveis = list(range(self.tamGrid))

        for agente in range(self.qntAgentes):
            orientcaoLatente = random.choice(self.listaDeOrientacoes)
            orientacaoAtual = random.choice(self.listaDeOrientacoes)
            i = random.randint(0, len(possiveisPosicoesUsaveis)-1)
            pos = possiveisPosicoesUsaveis.pop(i)
            novoAgente = Agente1D(orientcaoLatente, orientacaoAtual, pos)
            listaAgentes.append(novoAgente)

        arrayAgentes = np.array(listaAgentes)
        return arrayAgentes

    def criar_lugares(self):

        lista_lugares = []

        for i in range(self.qntLugares):
            orientacao = random.choice(self.listaDeOrientacoes)
            novo_lugar = Lugar1D(orientacao, i, id_lugar=i)
            lista_lugares.append(novo_lugar)

        array_lugares = np.array(lista_lugares)
        return array_lugares

    def criarLugaresAleatorios(self):
        listaLugares = []

        possiveisPosicoesUsaveis = list(range(self.tamGrid))

        for lugar in range(self.qntLugares):
            orientacao = random.choice(self.listaDeOrientacoes)
            i = random.randint(0, len(possiveisPosicoesUsaveis)-1)
            pos = possiveisPosicoesUsaveis.pop(i)
            novoLugar = Lugar1D(orientacao, pos)
            listaLugares.append(novoLugar)

        arrayLugares = np.array(listaLugares)
        return arrayLugares
    
    @staticmethod
    def obterDictContagemElementosLista(listaElementos):
        dictContagem = {}

        setElementos = set(listaElementos)
        
        for elemento in setElementos:
            qntElemento = listaElementos.count(elemento)
            dictContagem[str(elemento)] = qntElemento
        
        return dictContagem

    @staticmethod
    def obterDictContagemElementosComReferenial(listaElementos, listaReferencial):
        dictContagem = {}

        for elemento in listaReferencial:
            contagem = listaElementos.count(elemento)
            dictContagem[str(elemento)] = contagem
        
        return dictContagem

    def obterDictOcorrenciaOrientacoesAgentes(self):
        listaOrientacoesAgentes = [math.ceil(agente.orientacaoAtual / 100) * 100 for agente in self.arrayAgentes]
        contagemOrientacoes = self.obterDictContagemElementosComReferenial(listaOrientacoesAgentes, self.listaDeOrientacoes)
        return contagemOrientacoes

    def obterDictOcorrenciaOrientacoesAgentes_v2(self):
        listaOrientacoesAgentes = [math.ceil(agente.orientacaoLatente / 100) * 100 for agente in self.arrayAgentes]
        contagemOrientacoes = self.obterDictContagemElementosComReferenial(listaOrientacoesAgentes, self.listaDeOrientacoes)
        return contagemOrientacoes

    def calcularEntropia(self):
        listaOrientacoesAgentes = [math.ceil(agente.orientacaoAtual / 100) * 100 for agente in self.arrayAgentes]
        contagemOrientacoes = self.obterDictContagemElementosLista(listaOrientacoesAgentes)
        frequenciaOrientacoes = {key: (value / self.qntAgentes) for key, value in contagemOrientacoes.items()}
        listaEntropia = [value * math.log(value) for value in frequenciaOrientacoes.values()]
        entropiaFinal = -sum(listaEntropia)
        entropiaFinal = round(entropiaFinal, 3)
        return entropiaFinal

    def calcular_entropia_v2(self):
        listaOrientacoesAgentes = [math.ceil(agente.orientacaoLatente / 100) * 100 for agente in self.arrayAgentes]
        contagemOrientacoes = self.obterDictContagemElementosLista(listaOrientacoesAgentes)
        # print("ha {} orientacoes diferentes".format(len(contagemOrientacoes)))
        # for key, value in contagemOrientacoes.items():
        #     print("{}: {} vez(es)".format(key, value))
        # print("-------------------------------------")
        frequenciaOrientacoes = {key: (value / self.qntAgentes) for key, value in contagemOrientacoes.items()}
        listaEntropia = [value * math.log(value) for value in frequenciaOrientacoes.values()]
        entropiaFinal = -sum(listaEntropia)
        entropiaFinal = round(entropiaFinal, 3)
        return entropiaFinal

    def calcular_entropia_lugares(self):
        lista_orientacoes_lugares = [math.ceil(lugar.orientacao / 100) * 100 for lugar in self.arrayLugares]
        contagemOrientacoes = self.obterDictContagemElementosLista(lista_orientacoes_lugares)
        # print("ha {} orientacoes diferentes".format(len(contagemOrientacoes)))
        # for key, value in contagemOrientacoes.items():
        #     print("{}: {} vez(es)".format(key, value))
        # print("-------------------------------------")
        frequenciaOrientacoes = {key: (value / self.qntLugares) for key, value in contagemOrientacoes.items()}
        listaEntropia = [value * math.log(value) for value in frequenciaOrientacoes.values()]
        entropiaFinal = -sum(listaEntropia)
        entropiaFinal = round(entropiaFinal, 3)
        return entropiaFinal

    def calcular_entropia_geral(self):
        listaOrientacoesAgentes = [math.ceil(agente.orientacaoLatente / 100) * 100 for agente in self.arrayAgentes]
        lista_orientacoes_lugares = [math.ceil(lugar.orientacao / 100) * 100 for lugar in self.arrayLugares]

        lista_orientacoes_geral = listaOrientacoesAgentes + lista_orientacoes_lugares
        contagemOrientacoes = self.obterDictContagemElementosLista(lista_orientacoes_geral)
        # print("ha {} orientacoes diferentes".format(len(contagemOrientacoes)))
        # for key, value in contagemOrientacoes.items():
        #     print("{}: {} vez(es)".format(key, value))
        # print("-------------------------------------")

        qnt_total_elementos = self.qntAgentes + self.qntLugares
        frequenciaOrientacoes = {key: (value / qnt_total_elementos) for key, value in contagemOrientacoes.items()}
        listaEntropia = [value * math.log(value) for value in frequenciaOrientacoes.values()]
        entropiaFinal = -sum(listaEntropia)
        entropiaFinal = round(entropiaFinal, 3)
        return entropiaFinal
