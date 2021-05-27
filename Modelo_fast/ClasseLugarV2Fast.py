import Modelo_fast.funcoes_fast as fst
import numpy as np
import cores


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

    def contaminacao_lugar(self, pesos_contaminacao=(1, 1), mudar_cor=False, grid=None):

        peso_lugar = pesos_contaminacao[0]
        peso_agentes = pesos_contaminacao[1]

        soma_pesos = sum(pesos_contaminacao)
        lista_orientacao_agentes = [i.orientacao_latente for i in self.lista_agentes_presentes]

        soma_orientacoes_agentes = sum(lista_orientacao_agentes)
        qnt_agentes = len(lista_orientacao_agentes)

        media_orientacao_agentes = soma_orientacoes_agentes // qnt_agentes

        nova_orientacao = (peso_lugar*self.orientacao + peso_agentes*media_orientacao_agentes) // soma_pesos
        self.orientacao = nova_orientacao

        if mudar_cor is True:
            self.cor = fst.update_orientacao_cor(grid.dict_orientacoes_cores, self.orientacao)

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

