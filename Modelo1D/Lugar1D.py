import random


class Lugar1D:

    qnt_lugares = 0

    def __init__(self, orientacao, posicao, id_lugar=None):
        Lugar1D.qnt_lugares += 1

        if id_lugar is None:
            self.id = Lugar1D.qnt_lugares
        else:
            self.id = id_lugar

        self.orientacao = orientacao
        self.posicao = posicao
        self.listaAgentesPresentes = []

        self.orientacaoInicial = orientacao
        
    def sortearNovaOrientacao(self, listaPossiveisOrientacoes):
        self.orientacaoAtual = random.choice(listaPossiveisOrientacoes)

    # VER COM FABIANO
    def contaminacaoLugar(self, pesos=(1, 0.1)):
        pesoLugar = pesos[0]
        pesoAgentes = pesos[1]
        somaPesos = sum(pesos)

        listaOrientacoesAgentes = [i.orientacaoAtual for i in self.listaAgentesPresentes]
        somaOrientacaoAgentes = sum(listaOrientacoesAgentes)
        qntAgentes = len(self.listaAgentesPresentes)
        mediaOrientacoesAgentes = somaOrientacaoAgentes / qntAgentes

        fatorLugar = pesoLugar * self.orientacao
        fatorAgentes = pesoAgentes * mediaOrientacoesAgentes

        # media ponderada
        self.orientacao = (fatorLugar + fatorAgentes) / somaPesos

    def resgatarEstadoInicial(self):
        self.orientacao = self.orientacaoInicial
