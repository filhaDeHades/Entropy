import random
import math


class Agente1D:

    qnt_agentes = 0
    
    def __init__(self, orientacaoLatente, orientacaoAtual, posicao, id_agente=None):

        Agente1D.qnt_agentes += 1

        if id_agente is None:
            self.id = Agente1D.qnt_agentes
        else:
            self.id = id_agente

        self.orientacaoLatente = orientacaoLatente
        self.orientacaoAtual = orientacaoAtual
        self.posicao = posicao

        self.orientcaoLatenteInicial = orientacaoLatente
        self.orientacaoAtualInicial = orientacaoAtual
    
    def sortearNovaOrientacao(self, listaPossiveisOrientacoes):
        self.orientacaoAtual = random.choice(listaPossiveisOrientacoes)

    def sortear_nova_posicao(self, qnt_novas_posicoes):
        self.posicao = random.randint(0, qnt_novas_posicoes)

    @staticmethod
    def sorteioComPesos(listaPossibilidades, listaPesos, qntElementosSorteados=1):
        listaElementosSorteados = random.choices(listaPossibilidades, weights=listaPesos, k=qntElementosSorteados)
        return listaElementosSorteados

    def escolherLugar(self, listaLugares, pesos):
        pesoDifOrientacao = pesos[0]
        pesoDistancia = pesos[1]

        # é a lista que contém o peso de cada lugar ser sorteado
        # a ordem importa, peso da pos[0] é o peso do lugar na pos[0] na lista lugares
        listaPesos = []

        for lugar in listaLugares:
            difOrientacao = abs(self.orientacaoAtual - lugar.orientacao)
            distancia = abs(self.posicao - lugar.posicao)
            
            fatorDifOrientacao = pesoDifOrientacao * difOrientacao
            fatorDistancia = pesoDistancia * distancia

            expoente = fatorDifOrientacao + fatorDistancia
            peso = math.exp(-expoente)
            listaPesos.append(peso)
        
        somaListaPesos = sum(listaPesos)
        # normalização
        listaPesosFinal = [i/somaListaPesos for i in listaPesos]
        # print("lista pesos final: ", sum(listaPesosFinal))

        lugarEscolhido = self.sorteioComPesos(listaLugares, listaPesosFinal)[0]
        return lugarEscolhido

    def escolher_lugar_v2(self, listaLugares, pesos):
        pesoDifOrientacao = pesos[0]    # Peso A
        pesoDistancia = pesos[1]        # Peso B

        # é a lista que contém o peso de cada lugar ser sorteado
        # a ordem importa: peso da pos[0] é o peso do lugar na pos[0] na lista lugares
        listaPesos = []

        for lugar in listaLugares:
            difOrientacao = abs(self.orientacaoLatente - lugar.orientacao)
            distancia = abs(self.posicao - lugar.posicao)

            fatorDifOrientacao = pesoDifOrientacao * difOrientacao
            fatorDistancia = pesoDistancia * distancia

            expoente = fatorDifOrientacao + fatorDistancia
            peso = math.exp(-expoente)
            listaPesos.append(peso)

        somaListaPesos = sum(listaPesos)
        # normalização
        listaPesosFinal = [i / somaListaPesos for i in listaPesos]
        # print("lista pesos final: ", sum(listaPesosFinal))

        lugarEscolhido = self.sorteioComPesos(listaLugares, listaPesosFinal)[0]
        return lugarEscolhido

    def contaminacaoAgente(self, lugar, pesos):
        pesoOrientacaoLatente = pesos[0]
        pesosOrientacaoAtual = pesos[1]
        pesosOrientacaoLugar = pesos[2]

        somaPesos = sum(pesos)

        fatorOrientacaoLatente = pesoOrientacaoLatente * self.orientacaoLatente
        fatorOrientacaoAtual = pesosOrientacaoAtual * self.orientacaoAtual
        fatorOrientacaoLugar = pesosOrientacaoLugar * lugar.orientacao

        # print("latente: ", fatorOrientacaoLatente)
        # print("atual: ", fatorOrientacaoAtual)
        # print("lugar: ", fatorOrientacaoLugar)
        
        # eh uma media ponderada entre os fatores
        nova_orientacao = (fatorOrientacaoLatente + fatorOrientacaoAtual + fatorOrientacaoLugar) / somaPesos
        self.orientacaoLatente = round(nova_orientacao, 3)

        # print("nova orientacao: ", self.orientacaoLatente)

    def contaminacao_agente_v2(self, lugar, pesos=(1, 0.1)):

        peso_orientacao_latente = pesos[0]
        peso_orientacao_lugar = pesos[1]

        soma_pesos = pesos[0] + pesos[1]

        fator_orientacao_latente = peso_orientacao_latente * self.orientacaoLatente
        fator_orientacao_lugar = peso_orientacao_lugar * lugar.orientacao

        # print("latente: ", fator_orientacao_latente)
        # print("lugar: ", fator_orientacao_lugar)

        nova_orientacao_latente = (fator_orientacao_latente + fator_orientacao_lugar) / soma_pesos
        self.orientacaoLatente = round(nova_orientacao_latente, 3)
        # print("nova orientacao: ", self.orientacaoLatente)

    def resgatarEstadoInicial(self):
        self.orientacaoLatente = self.orientcaoLatenteInicial
        self.orientacaoAtual = self.orientacaoAtualInicial
