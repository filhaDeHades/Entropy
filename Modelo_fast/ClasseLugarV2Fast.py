import Modelo_fast.funcoes_fast as fst
import numpy as np
import cores
from math import sqrt, degrees, acos, cos, radians, sin

class LugarV2Fast:

    qnt_lugares = 0

    def __init__(self, grid, veio_de_arquivo=False, lista_arquivo=None, lista_coordenadas=None, orientacao=0, cor=cores.verde):

        if veio_de_arquivo is False:

            self.id = LugarV2Fast.qnt_lugares
            LugarV2Fast.qnt_lugares += 1

            self.array_coordenadas = np.array(lista_coordenadas)
            self.array_celulas_grid = self.init_array_celulas_grid(grid)
            self.coordenada_principal = None

            self.cor = cor

            self.orientacao = orientacao
            self.orientacao_inicial = orientacao

            self.lista_caminhos = []

            self.ja_teve_caminhos_atualizados = False
            self.lista_agentes_presentes = []

        else:
            self.id = lista_arquivo[0]
            self.array_coordenadas = lista_arquivo[1]
            self.cor = lista_arquivo[2]
            self.orientacao = lista_arquivo[3]
            self.orientacao_inicial = lista_arquivo[3]

            self.array_celulas_grid = self.init_array_celulas_grid(grid)

            self.lista_caminhos = []

            self.ja_teve_caminhos_atualizados = False
            self.lista_agentes_presentes = []

    def init_array_celulas_grid(self, grid):
        lista_celulas_grid = []

        for coordenada in self.array_coordenadas:
            x = coordenada[0]
            y = coordenada[1]
            grid.atualizar_status_andavel_celula(x, y, False)

            celula_lugar = grid.obter_celula_array_grid(x, y)
            celula_lugar.lugar = self
            lista_celulas_grid.append(celula_lugar)

        array_celulas_grid = np.array(lista_celulas_grid)
        return array_celulas_grid

    def achar_coordenada_principal(self, ponto_referencia):

        menor_distancia = fst.obter_distancia_manhattan(ponto_referencia, self.array_coordenadas[0])
        coordenada_escolhida = self.array_coordenadas[0]

        for coordenada in self.array_coordenadas:

            distancia_analisada = fst.obter_distancia_manhattan(ponto_referencia, coordenada)

            if distancia_analisada < menor_distancia:
                menor_distancia = distancia_analisada
                coordenada_escolhida = coordenada

        return coordenada_escolhida

    def somaVetor(self,vetores):
    #ve a quantidade de vetores
        qtdVetores = (len(vetores))
        #verifica se todos tem a mesma dimencao
        for i in range(qtdVetores):
            for j in range(i + 1, qtdVetores):
                if len(vetores[i]) != len(vetores[j]):
                    return -1
        dim = len(vetores[0])
        s = []
        # faz a soma das coornadas caso todos possuam as mesmas dimenssões (vetor resultante) 
        # e acha o vetor resultante
        for col in range(dim):
            soma = 0
            for lin in range(qtdVetores):
                soma += vetores[lin][col]
            s.append(soma)
        return s

    def anguloVX(self,vetor):
        x = vetor[0]
        y = vetor[1]
        tam = max(sqrt(x * x + y * y), np.nextafter(np.float32(0), np.float32(1)))
        cosseno = x / tam
        ang = degrees(acos(cosseno))
        #produto positivo implica em quadrante impar
        if x * y > 0:
            if x > 0:
                return ang
            else:
                return ang + 180
        #produto negativo implica em quadrante par
        elif x * y < 0:
            if y > 0:
                return ang
            else:
                return ang + 180
        elif x*y == 0:
            if x==0 and y>0:
                return 90
            elif x==0 and y<0:
                return 270
            elif x>0 and y==0:
                return 0
            else: 
                return 180

    def contaminacao_lugar(self,pesosContaminacaoLugar, mudar_cor=True, grid=None):
        
        peso_lugar = pesosContaminacaoLugar[0]
        peso_agentes = pesosContaminacaoLugar[1]
        
        lista_orientacao_agentes = [(cos(radians(i.orientacao_atual)), sin(radians(i.orientacao_atual))) for i in self.lista_agentes_presentes]

        media_orientacao_agentes=self.anguloVX(self.somaVetor(lista_orientacao_agentes))
        aux=[ ( peso_agentes*cos(radians(media_orientacao_agentes)) ,peso_agentes*sin(radians(media_orientacao_agentes)) ),( peso_lugar*cos(radians(self.orientacao)), peso_lugar*sin(radians(self.orientacao)) ) ]
        nova_orientacao = round(self.anguloVX(self.somaVetor(aux)))
        self.orientacao = nova_orientacao

        #if mudar_cor is True:
            #self.cor = fst.update_orientacao_cor(grid.dict_orientacoes_cores, self.orientacao, 1000)

    def resgatar_estado_inicial(self):
        self.orientacao = self.orientacao_inicial

    def tornar_lugar_andavel(self):
        for celula in self.array_celulas_grid:
            celula.andavel = True

    def tornar_lugar_n_andavel(self):
        for celula in self.array_celulas_grid:
            celula.andavel = False

    def resetar_coordenada_principal(self):
        self.coordenada_principal = None

    def restaurar_mudancas_a_star(self):
        self.tornar_lugar_n_andavel()
        self.resetar_coordenada_principal()

    def add_caminho_lugar_v2(self, lugar_destino, possui_caminho, caminho=None):

        if possui_caminho is True:
            novo_dicionario = {'destino': lugar_destino, "possui_caminho": True, 'caminho': caminho}
            self.lista_caminhos.append(novo_dicionario)
        else:
            novo_dicionario = {'destino': lugar_destino, "possui_caminho": False}
            self.lista_caminhos.append(novo_dicionario)

