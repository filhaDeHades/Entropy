from Modelo_5.ClasseCelulaGridV2 import CelulaGridV2
from Modelo_5.ClasseLugarV2 import LugarV2
from Modelo_5.ClasseAgenteV2 import AgenteV2
from Modelo_5.ClasseHeapCelulasGrid import HeapCelulasGrid
import Testes.src.funcoes_geracao_nomes as fgn
import Modelo_5.funcoes_arquivos as func_arq
import pygame as pg
import cores
import funcoes
import random
import math
import time
import pandas as pd

class GridV2:

    def __init__(self, qnt_linhas, qnt_colunas, cell_size, matriz_layout, qnt_orientacoes=11, display_agentes=True):

        self.qnt_linhas = qnt_linhas
        self.qnt_colunas = qnt_colunas
        self.qnt_agentes = 0
        self.cell_size = cell_size
        self.largura = qnt_colunas * cell_size
        self.altura = qnt_linhas * cell_size
        self.tamanho_tela = (self.largura, self.altura)
        self.custo_menor_mov = 10
        self.custo_maior_mov = 14
        self.matriz_celulas = []
        self.lista_celulas_ocupadas = []
        self.array_agentes = []
        self.qnt_orientacoes = qnt_orientacoes
        self.dict_orientacoes_cores = {}
        self.obter_dict_orientacoes_cores()

        for y in range(qnt_linhas):
            linha = []
            for x in range(qnt_colunas):
                andavel = True

                if matriz_layout[y][x] == 1:
                    andavel = False

                if andavel is True:
                    novo_nodulo = CelulaGridV2(x, y, cell_size, andavel)
                    self.array_agentes.append(novo_nodulo)
                else:
                    novo_nodulo = CelulaGridV2(x, y, cell_size, andavel, cor=cores.preto)

                linha.append(novo_nodulo)

                if andavel is False:
                    self.lista_celulas_ocupadas.append(novo_nodulo)

            self.matriz_celulas.append(linha)

        self.nodulo_partida = None
        self.nodulo_partida_selecionado = False
        self.nodulo_chegada = None
        self.nodulo_chegada_selecionado = False

        self.permissao_mudar_estado = True
        self.permissao_criar_lugares_manuais = False
        self.lista_coordenadas_lugar_temp = []
        self.partida_e_chegada_definidos = False

        self.permissao_display_linhas_grid = False
        self.permissao_display_procura_caminho = False
        self.lista_procura_caminho_atual = []
        self.permissao_display_menor_caminho = False
        self.lista_menor_caminho_atual = []
        self.lista_agentes = []
        self.lista_lugares = []
        self.lista_caminhos = []
        self.qnt_caminhos_resgatados_arquivo = 0
        self.display_agentes = display_agentes
        self.arquivo_lugares_dinamicos = None

    def obter_dict_orientacoes_cores(self):
        self.dict_orientacoes_cores = funcoes.converter_orientacao_para_cor_v3(self.qnt_orientacoes)

    def print_dict_orientacoes_cores(self):
        print("LISTA ORIENTACOES/CORES")
        for orientacao, cor in self.dict_orientacoes_cores.items():
            print("orientacao: {} / cor: {}".format(orientacao, cor))

    def update_grid(self, janela: pg.display):

        for linha in self.matriz_celulas:
            for celula in linha:
                celula.draw(janela)

        self.display_procura_caminho(self.lista_procura_caminho_atual, janela)

        self.display_menor_caminho(self.lista_menor_caminho_atual, janela)

        self.display_linhas_grid(janela)

        if self.display_agentes is True:
            for agente in self.lista_agentes:
                agente.draw(janela)

        for lugar in self.lista_lugares:

            if lugar.display_caminhos is True:
                for item in lugar.lista_caminhos:
                    if item["possui_caminho"] is True:
                        self.display_menor_caminho(item['caminho'], janela)

            if lugar.display_celulas_acessiveis is True:
                for celula in lugar.lista_celulas_grid_acessiveis:
                    celula.cor = cores.verde_claro

    def mudar_estado_celula(self, celula):
        x = celula.grid_x
        y = celula.grid_y
        self.matriz_celulas[y][x].mudar_estado()

    def selecinar_nodulo(self, pos_nodulo_clicado):
        pos_x, pos_y = pos_nodulo_clicado[0], pos_nodulo_clicado[1]
        nodulo_selecionado = self.matriz_celulas[pos_y][pos_x]

        return nodulo_selecionado

    def verificar_se_coordenada_eh_andavel(self, coordenada_x, coordenada_y):

        if 0 <= coordenada_x <= self.qnt_colunas - 1 and 0 <= coordenada_y <= self.qnt_linhas - 1:
            celula_analisada = self.matriz_celulas[coordenada_y][coordenada_x]
            if celula_analisada.andavel is True:
                return True

        return False

    def verificar_se_posicao_eh_aceitavel(self, pos_x, pos_y, tamanho_agente):

        limite_esquerda = tamanho_agente
        limite_direita = self.largura - tamanho_agente
        # print("lim esquerda: ", limite_esquerda)
        # print("lim direita: ", limite_direita)
        # print("pos x agente: ", pos_x)

        # print("--------------------")

        limite_cima = tamanho_agente
        limite_baixo = self.altura - tamanho_agente
        # print("lim cima: ", limite_cima)
        # print("lim baixo: ", limite_baixo)
        # print("pos y agente: ", pos_y)
        #
        # print("--------------------")

        if (limite_esquerda <= pos_x <= limite_direita) and (limite_cima <= pos_y <= limite_baixo):
            # print("o agente se encontra dentro do grid")
            pos_global = (pos_x, pos_y)
            # print("pos global: ", pos_global)
            pos_grid_global = funcoes.converter_pos_para_coordenada_grid(pos_global, self.cell_size)
            # print("pos grid: ", pos_grid_global)
            pos_grid_x, pos_grid_y = pos_grid_global
            celula_analisada = self.matriz_celulas[pos_grid_y][pos_grid_x]

            if celula_analisada.andavel is True:
                # print("o agente pode se mover nesta direcao")
                return True
        # print("o agente n pode se mover nesta direcao")
        return False

    def obter_nodulos_vizinhos(self, celula, excluir_obstaculos=True, excluir_diagonais=False):

        lista_vizinhos = []

        for y in range(-1, 2):
            for x in range(-1, 2):

                if excluir_diagonais is True:
                    if abs(x) == 1 and abs(y) == 1:
                        continue

                pos_x = celula.grid_x + x
                pos_y = celula.grid_y + y

                if (pos_x, pos_y) == celula.pos_grid:
                    continue
                else:
                    if 0 <= pos_x <= self.qnt_colunas - 1:
                        if 0 <= pos_y <= self.qnt_linhas - 1:

                            celula_analisada = self.matriz_celulas[pos_y][pos_x]

                            if excluir_obstaculos is True:
                                if celula_analisada.andavel is True:
                                    lista_vizinhos.append(celula_analisada)
                            else:
                                lista_vizinhos.append(celula_analisada)
        return lista_vizinhos

    def display_vizinhos(self, janela: pg.display, lista_vizinhos, cor=cores.azul):

        for vizinho in lista_vizinhos:
            pg.draw.rect(janela, cor, (vizinho.grid_x * self.cell_size, vizinho.grid_y * self.cell_size,
                                       self.cell_size, self.cell_size))

    def a_star(self, nodulo_inicial, nodulo_final):

        nodulo_inicial.g = 0
        nodulo_inicial.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, nodulo_final.pos_grid)
        nodulo_inicial.atualizar_f()
        nodulo_inicial.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(nodulo_inicial)

        # chegou_destino = False

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]      # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual == nodulo_final:

                lista_bruta = [i.pos_grid for i in lista_fechada]
                lista_refinada = []

                nodulo_regresso = nodulo_final

                while nodulo_regresso != nodulo_inicial:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_final = (lista_bruta, lista_refinada)
                self.restaurar_estado_inicial_celulas()
                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g(self.custo_menor_mov, self.custo_maior_mov)
                    vizinho.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, nodulo_final.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = funcoes.distancia_sebastiana(self.custo_menor_mov, self.custo_maior_mov,
                                                                nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)

    def a_star_lugar(self, nodulo_inicial, lugar):

        lugar.achar_coordenada_principal(nodulo_inicial.pos_grid)

        lugar.tornar_lugar_andavel()

        nodulo_inicial.g = 0
        nodulo_inicial.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar.coordenada_principal)
        nodulo_inicial.atualizar_f()
        nodulo_inicial.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(nodulo_inicial)

        # chegou_destino = False

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]  # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual in lugar.lista_celulas_grid:

                lista_bruta = [i.pos_grid for i in lista_fechada]
                lista_refinada = []

                nodulo_regresso = None

                for nodulo in lugar.lista_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != nodulo_inicial:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_final = (lista_bruta, lista_refinada)
                self.restaurar_estado_inicial_celulas()
                lugar.tornar_lugar_n_andavel()
                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g(self.custo_menor_mov, self.custo_maior_mov)
                    vizinho.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar.coordenada_principal)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = funcoes.distancia_sebastiana(self.custo_menor_mov, self.custo_maior_mov,
                                                                nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)
        return None

    def a_star_lugar_v2(self, lugar1, lugar2, retornar_procura_caminho=False, retornar_tempo=False):

        tempo_inicial = time.perf_counter()
        funcoes.encontrar_celulas_principais(lugar1, lugar2)

        lugar1.tornar_lugar_andavel()
        lugar2.tornar_lugar_andavel()

        lugar1.celula_principal.g = 0
        lugar1.celula_principal.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar2.celula_principal.pos_grid)
        lugar1.celula_principal.atualizar_f()
        lugar1.celula_principal.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(lugar1.celula_principal)

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]  # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual in lugar2.lista_celulas_grid:

                lista_refinada = []

                nodulo_regresso = None

                for nodulo in lugar2.lista_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != lugar1.celula_principal:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_refinada.insert(0, lugar1.celula_principal.pos_grid)

                lista_final = {"lista_refinada": lista_refinada}
                self.restaurar_estado_inicial_celulas()
                lugar1.tornar_lugar_n_andavel()
                lugar2.tornar_lugar_n_andavel()

                if retornar_procura_caminho is True:
                    lista_bruta = [i.pos_grid for i in lista_fechada]
                    lista_final["lista_bruta"] = lista_bruta

                tempo_final = time.perf_counter()
                if retornar_tempo is True:
                    tempo_gasto = tempo_final - tempo_inicial
                    lista_final["tempo_gasto"] = tempo_gasto

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g(self.custo_menor_mov, self.custo_maior_mov)
                    vizinho.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar2.celula_principal.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = funcoes.distancia_sebastiana(self.custo_menor_mov, self.custo_maior_mov,
                                                                nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)
        return None

    def a_star_lugar_v3(self, lugar1, lugar2, retornar_procura_caminho=False, retornar_qnt_comparacoes=False,
                        retornar_tempo=False):
        """
        optimizacoes em relacao a versao anterior:

        - lista aberta agr eh uma heap, o que significa que menos comparacoes
        sao feitos a ela na hora de rerirar ou add celulas na lista aberta

        - uso do parametro 'ja_foi_analisado' nas celulas, agr as celulas ja testadas tem esse parametro igual a True,
        o que faz que as celulas vizinhas n tenham que procurar na lista fechada para ver se ja foram testadas

        - a lista fechada so serve exclusivamente para restaurar o estado inicial das celulas testadas, o que eh uma
        melhoria em relacao ao modo anterior que fazia esse processo para todas as celulas do grid, ate as que n
        precisavam pq n foram testadas. a lista aberta e a lista fechada sao unidas por meio de um set (conjunto) para
        que somente as celulas que sofreram alteracoes sejam restauradas ao seu estado inicial

        novo parametro: retornar procura caminho. quando este parametro eh True, retorna a lista bruta, que contem a
        procura do caminho. o padrao eh false para que quando n se precisa saber a procura do caminho, a funcao seja
        mais rapida

        novo parametro: retornar_qnt_comparacoes. quando este parametro eh True, retorna a quandtidade de vezes que
        comparacoes foram feitas na lista aberta, na heap. Eh um parametro de controle que serve para comparar em
        relacoa a funcao a_star_lugar_v2

        novo parametro: reornar_tempo. quando este parametro eh True, retorna o tempo gasto na funcao. paramto de
        controle para comparar com a versao anterior

        """
        tempo_inicial = time.perf_counter()
        funcoes.encontrar_celulas_principais(lugar1, lugar2)

        lugar1.tornar_lugar_andavel()
        lugar2.tornar_lugar_andavel()

        lugar1.celula_principal.g = 0
        lugar1.celula_principal.atualizar_h(self.custo_menor_mov, self.custo_maior_mov,
                                            lugar2.celula_principal.pos_grid)
        lugar1.celula_principal.atualizar_f()
        lugar1.celula_principal.ja_foi_visitado = True

        lista_aberta = HeapCelulasGrid()
        lista_fechada = []
        lista_aberta.add_celula_heap(lugar1.celula_principal)

        qnt_comparacoes = 0

        while len(lista_aberta.lista_heap_celulas) > 0:

            nodulo_atual = lista_aberta.remover_primeira_celula_heap()
            # nodulo_atual.ja_foi_analisado = True
            lista_fechada.append(nodulo_atual)

            if retornar_qnt_comparacoes is True:
                qnt_comparacoes += lista_aberta.qnt_comparacoes_ultima_operacao
                lista_aberta.zerar_contagem_comparacoes()

            if nodulo_atual in lugar2.lista_celulas_grid:

                lista_bruta = []
                lista_refinada = []

                if retornar_procura_caminho is True:
                    lista_bruta = [i.pos_grid for i in lista_fechada]

                nodulo_regresso = None

                for nodulo in lugar2.lista_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != lugar1.celula_principal:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_refinada.insert(0, lugar1.celula_principal.pos_grid)

                set_celulas_para_serem_restauradas = funcoes.transformar_duas_listas_em_set(lista_aberta.lista_heap_celulas,
                                                                                            lista_fechada)
                self.restaurar_estado_inicial_celulas_v2(set_celulas_para_serem_restauradas)

                lugar1.tornar_lugar_n_andavel()
                lugar2.tornar_lugar_n_andavel()

                lista_final = {"lista_refinada": lista_refinada}

                if retornar_procura_caminho is True:
                    lista_final["lista_bruta"] = lista_bruta

                if retornar_qnt_comparacoes is True:
                    lista_final["qnt_comparacoes"] = qnt_comparacoes

                tempo_final = time.perf_counter()

                if retornar_tempo is True:
                    tempo_total = tempo_final - tempo_inicial
                    lista_final["tempo_gasto"] = tempo_total

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g(self.custo_menor_mov, self.custo_maior_mov)
                    vizinho.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar2.celula_principal.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = funcoes.distancia_sebastiana(self.custo_menor_mov, self.custo_maior_mov,
                                                                nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                vizinho_na_lista_aberta = False

                if vizinho in lista_aberta.lista_heap_celulas:
                    vizinho_na_lista_aberta = True

                if novo_mov_para_vizinho < vizinho.g or vizinho_na_lista_aberta is False:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho_na_lista_aberta is False:
                        lista_aberta.add_celula_heap(vizinho)
                        if retornar_qnt_comparacoes is True:
                            qnt_comparacoes += lista_aberta.qnt_comparacoes_ultima_operacao
                            lista_aberta.zerar_contagem_comparacoes()

        return None

    def a_star_lugar_v4(self, lugar1, lugar2, retornar_procura_caminho=False, retornar_qnt_comparacoes=False,
                        retornar_tempo=False):
        """
        optimizacoes em relacao a versao anterior:

        - lista aberta agr eh uma heap, o que significa que menos comparacoes
        sao feitos a ela na hora de rerirar ou add celulas na lista aberta

        - uso do parametro 'ja_foi_analisado' nas celulas, agr as celulas ja testadas tem esse parametro igual a True,
        o que faz que as celulas vizinhas n tenham que procurar na lista fechada para ver se ja foram testadas

        - a lista fechada so serve exclusivamente para restaurar o estado inicial das celulas testadas, o que eh uma
        melhoria em relacao ao modo anterior que fazia esse processo para todas as celulas do grid, ate as que n
        precisavam pq n foram testadas. a lista aberta e a lista fechada sao unidas por meio de um set (conjunto) para
        que somente as celulas que sofreram alteracoes sejam restauradas ao seu estado inicial

        novo parametro: retornar procura caminho. quando este parametro eh True, retorna a lista bruta, que contem a
        procura do caminho. o padrao eh false para que quando n se precisa saber a procura do caminho, a funcao seja
        mais rapida

        novo parametro: retornar_qnt_comparacoes. quando este parametro eh True, retorna a quandtidade de vezes que
        comparacoes foram feitas na lista aberta, na heap. Eh um parametro de controle que serve para comparar em
        relacoa a funcao a_star_lugar_v2

        novo parametro: reornar_tempo. quando este parametro eh True, retorna o tempo gasto na funcao. paramto de
        controle para comparar com a versao anterior

        """
        tempo_inicial = time.perf_counter()
        funcoes.encontrar_celulas_principais(lugar1, lugar2)

        lugar1.tornar_lugar_andavel()
        lugar2.tornar_lugar_andavel()

        lugar1.celula_principal.g = 0
        lugar1.celula_principal.atualizar_h(self.custo_menor_mov, self.custo_maior_mov,
                                            lugar2.celula_principal.pos_grid)
        lugar1.celula_principal.atualizar_f()
        lugar1.celula_principal.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(lugar1.celula_principal)

        qnt_comparacoes = 0

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta.pop(0)
            nodulo_atual.ja_foi_analisado = True
            lista_fechada.append(nodulo_atual)

            if nodulo_atual.lugar == lugar2:

                lista_refinada = []

                nodulo_regresso = None

                for nodulo in lugar2.lista_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != lugar1.celula_principal:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_refinada.insert(0, lugar1.celula_principal.pos_grid)

                set_celulas_para_serem_restauradas = funcoes.transformar_duas_listas_em_set(lista_aberta, lista_fechada)
                self.restaurar_estado_inicial_celulas_v2(set_celulas_para_serem_restauradas)

                lugar1.tornar_lugar_n_andavel()
                lugar2.tornar_lugar_n_andavel()

                lista_final = {"lista_refinada": lista_refinada}

                if retornar_procura_caminho is True:
                    lista_bruta = [i.pos_grid for i in lista_fechada]
                    lista_final["lista_bruta"] = lista_bruta

                if retornar_qnt_comparacoes is True:
                    lista_final["qnt_comparacoes"] = qnt_comparacoes

                tempo_final = time.perf_counter()

                if retornar_tempo is True:
                    tempo_total = tempo_final - tempo_inicial
                    lista_final["tempo_gasto"] = tempo_total

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.andavel is False or vizinho.ja_foi_analisado is True:
                    continue

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g(self.custo_menor_mov, self.custo_maior_mov)
                    vizinho.atualizar_h(self.custo_menor_mov, self.custo_maior_mov, lugar2.celula_principal.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                distacia_vizinho = funcoes.distancia_sebastiana(self.custo_menor_mov, self.custo_maior_mov,
                                                                nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                vizinho_na_lista_aberta = False

                if vizinho in lista_aberta:
                    vizinho_na_lista_aberta = True

                if novo_mov_para_vizinho < vizinho.g or vizinho_na_lista_aberta is False:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho_na_lista_aberta is False:
                        if len(lista_aberta) == 0:
                            lista_aberta.append(vizinho)
                        else:
                            for i in range(len(lista_aberta)):
                                if vizinho.f < lista_aberta[i].f:
                                    lista_aberta.insert(i, vizinho)
                                    break
                                elif vizinho.f == lista_aberta[i].f and vizinho.h < lista_aberta[i].h:
                                    lista_aberta.insert(i, vizinho)
                                    break
                                elif i == len(lista_aberta) - 1:
                                    lista_aberta.append(vizinho)

                        if retornar_qnt_comparacoes is True:
                            qnt_comparacoes += 1

        return None

    def display_linhas_grid(self, janela: pg.display, cor_linha=cores.preto, tam_linha=1):
        if self.permissao_display_linhas_grid is True:
            for x in range(self.qnt_colunas):
                pg.draw.line(janela, cor_linha, (x * self.cell_size, 0), (x * self.cell_size, self.altura), tam_linha)
            for y in range(self.qnt_linhas):
                pg.draw.line(janela, cor_linha, (0, y * self.cell_size), (self.largura, y * self.cell_size), tam_linha)

    def display_partida_e_chegada(self, janela: pg.display, cor_partida=cores.verde, cor_chegada=cores.vermelho):
        if self.nodulo_partida_selecionado is True:
            x_partida, y_partida = self.nodulo_partida.pos_grid[0], self.nodulo_partida.pos_grid[1]
            pg.draw.rect(janela, cor_partida, (x_partida*self.cell_size, y_partida*self.cell_size,
                                               self.cell_size, self.cell_size))

        if self.nodulo_chegada_selecionado is True:
            x_chegada, y_chegada = self.nodulo_chegada.pos_grid[0], self.nodulo_chegada.pos_grid[1]
            pg.draw.rect(janela, cor_chegada, (x_chegada * self.cell_size, y_chegada * self.cell_size,
                                               self.cell_size, self.cell_size))

    def display_procura_caminho(self, lista, janela: pg.display, cor=cores.roxo):
        if self.permissao_display_procura_caminho is True:
            for passo in lista:
                x = passo[0]
                y = passo[1]
                pg.draw.rect(janela, cor, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

    def display_menor_caminho(self, lista, janela: pg.display, cor=cores.azul):
        if self.permissao_display_menor_caminho is True:
            for passo in lista:
                x = passo[0]
                y = passo[1]
                pg.draw.rect(janela, cor, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

    def remover_display_caminhos(self):
        self.permissao_display_procura_caminho = False
        self.permissao_display_menor_caminho = False
        self.lista_procura_caminho_atual.clear()
        self.lista_menor_caminho_atual.clear()

    # obsoleto, n funcional
    def gerar_lugares_aleatorios(self, qnt_lugares, tamanho_max_lugar, sem_cor_repetida=True):

        lista_cores = cores.lista_cores_random

        for lugar in range(qnt_lugares):

            x = random.randint(0, self.qnt_colunas - 1)
            y = random.randint(0, self.qnt_linhas - 1)
            celula_escolhida = self.matriz_celulas[y][x]
            celula_aceitavel = False

            if celula_escolhida.andavel is True:
                celula_aceitavel = True

            while celula_aceitavel is False:

                x = random.randint(0, self.qnt_colunas - 1)
                y = random.randint(0, self.qnt_linhas - 1)
                celula_escolhida = self.matriz_celulas[y][x]
                celula_aceitavel = False

                if celula_escolhida.andavel is True:
                    celula_aceitavel = True

            tamanho_max_temp = tamanho_max_lugar
            lista_coordendas_temp = []

            while tamanho_max_temp != 0:

                lista_coordendas_temp.append(celula_escolhida.pos_grid)
                lista_vizihos = self.obter_nodulos_vizinhos(celula_escolhida)
                celula_escolhida = random.choice(lista_vizihos)
                tamanho_max_temp -= 1

            cor_escolhida = random.choice(lista_cores)

            if sem_cor_repetida is True:
                lista_cores.remove(cor_escolhida)

            novo_lugar = LugarV2(self.cell_size, veio_de_arquivo=False, lista_coordenadas=None)
            self.lista_lugares.append(novo_lugar)

        self.atualizar_celulas_com_lugares()

    def gerar_lugares_aleatorios_v2(self, qnt_lugares, tamanho_max_lugar, sem_cor_repetida=False, sem_orientacao_repetida=False):

        lista_lugares = []
        lista_cores = cores.lista_cores_random[:]
        lista_orientacoes = list(range(0, 1000))

        for lugar in range(qnt_lugares):
            celula_aceitavel = False
            celula_escolhida = None

            while celula_aceitavel is False:                        # sorteando celula inicial que n seja obstaculo
                x = random.randint(0, self.qnt_colunas - 1)
                y = random.randint(0, self.qnt_linhas - 1)
                celula_escolhida_temp = self.matriz_celulas[y][x]

                if celula_escolhida_temp not in self.lista_celulas_ocupadas:
                    celula_escolhida = celula_escolhida_temp
                    celula_aceitavel = True

            lista_celulas_escolhidas = []
            tamanho_lugar_temp = 0

            while tamanho_lugar_temp < tamanho_max_lugar:           # sorteando as celulas vizinhas para forar o lugar
                lista_celulas_escolhidas.append(celula_escolhida)
                self.lista_celulas_ocupadas.append(celula_escolhida)
                lista_vizinhos = self.obter_nodulos_vizinhos(celula_escolhida)
                set_vizinhos = None
                set_vizinhos_eh_usavel = False

                while set_vizinhos_eh_usavel is False:
                    set_vizinhos_temp = set(lista_vizinhos) - set(lista_celulas_escolhidas) - set(self.lista_celulas_ocupadas)
                    if len(set_vizinhos_temp) == 0:
                        nova_celula_escolhida = random.choice(lista_celulas_escolhidas)
                        lista_vizinhos = self.obter_nodulos_vizinhos(nova_celula_escolhida)
                    else:
                        set_vizinhos = set_vizinhos_temp
                        set_vizinhos_eh_usavel = True

                lista_vizinhos_final = list(set_vizinhos)
                celula_escolhida = random.choice(lista_vizinhos_final)
                tamanho_lugar_temp += 1

            cor_escolhida = random.choice(lista_cores)              # sorteando a cor
            if sem_cor_repetida is True:
                lista_cores.remove(cor_escolhida)

            orientacao_escolhida = random.choice(lista_orientacoes) # sorteando a orientacao
            if sem_orientacao_repetida is True:
                lista_orientacoes.remove(orientacao_escolhida)

            lista_coordenadas_escolhidas = [i.pos_grid for i in lista_celulas_escolhidas]

            lugar_novo = LugarV2(self, veio_de_arquivo=False, lista_coordenadas=lista_coordenadas_escolhidas,
                                 cor=cor_escolhida, orientacao=orientacao_escolhida)

            lista_lugares.append(lugar_novo)

        self.lista_lugares = lista_lugares

    # obsoleto, n funcional
    def gerar_agentes_aleatorios(self, qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False):

        lista_cores = cores.lista_cores_random
        lista_orientacoes = list(range(0, 1000))

        for agente in range(qnt_agentes):

            pos_inicial_agente_aceitavel = False
            pos_x_inicial = None
            pos_y_inicial = None

            while pos_inicial_agente_aceitavel is False:
                pos_x_inicial = random.randint(0, self.qnt_colunas - 1)
                pos_y_inicial = random.randint(0, self.qnt_linhas - 1)
                celula_escolhida = self.matriz_celulas[pos_y_inicial][pos_x_inicial]

                if celula_escolhida not in self.lista_celulas_ocupadas:
                    pos_inicial_agente_aceitavel = True
                    self.lista_celulas_ocupadas.append(celula_escolhida)

            cor_escolhida = random.choice(lista_cores)
            if sem_cor_repetida is True:
                lista_cores.remove(cor_escolhida)

            orientacao_escolhida = random.choice(lista_orientacoes)
            if sem_orientacao_repetida is True:
                lista_orientacoes.remove(orientacao_escolhida)

            novo_agente = AgenteV2(pos_x_inicial, pos_y_inicial, self.cell_size, cor=cor_escolhida,
                                   orientacao_latente=orientacao_escolhida, orientacao_atual=orientacao_escolhida)
            self

            self.lista_agentes.append(novo_agente)
            print("novo agente criado!")
        self.atualizar_celulas_com_agentes()

    def gerar_agentes_aleatorios_v2(self, sem_cor_repetida=False, sem_orientacao_repetida=False):

        lista_celulas_livres = []

        for linha in self.matriz_celulas:
            for celula in linha:
                if celula.andavel is True:
                    lista_celulas_livres.append(celula)

        lista_cores = cores.lista_cores_random
        lista_orientacoes = list(range(0, 1000))

        qnt_agentes = int(len(self.lista_lugares) * 2.5)

        for agente in range(qnt_agentes):

            celula_escolhida = random.choice(lista_celulas_livres)
            lista_celulas_livres.remove(celula_escolhida)

            pos_x_inicial = celula_escolhida.grid_x
            pos_y_inicial = celula_escolhida.grid_y

            print(lista_cores)
            cor_escolhida = random.choice(lista_cores)
            # if sem_cor_repetida is True:
            #     lista_cores.remove(cor_escolhida)

            orientacao_escolhida = random.choice(lista_orientacoes)
            if sem_orientacao_repetida is True:
                lista_orientacoes.remove(orientacao_escolhida)

            novo_agente = AgenteV2(self, pos_x_inicial, pos_y_inicial, self.cell_size, cor=cor_escolhida,
                                   orientacao_latente=orientacao_escolhida, orientacao_atual=orientacao_escolhida)

            self.lista_agentes.append(novo_agente)

            self.qnt_agentes = qnt_agentes

    def criar_lugar_manual(self):
        lista_coordenadas_finais = [celula.pos_grid for celula in self.lista_coordenadas_lugar_temp]
        lista_coordendas_finais_usaveis = lista_coordenadas_finais[:]

        possiveis_orientacoes = list(range(0, 1000))
        orientacao_escolhida = random.choice(possiveis_orientacoes)

        novo_lugar_manual = LugarV2(self, lista_coordenadas=lista_coordendas_finais_usaveis,
                                    orientacao=orientacao_escolhida)

        self.lista_lugares.append(novo_lugar_manual)
        self.lista_coordenadas_lugar_temp.clear()
        self.permissao_criar_lugares_manuais = False

    def gerar_todos_caminhos(self):

        lista_lugares_temp = self.lista_lugares[:]
        qnt_caminhos_possiveis = funcoes.combinacao(len(lista_lugares_temp), 2)
        qnt_caminhos_criados = 0
        qnt_caminhos_n_criados = 0

        while len(lista_lugares_temp) > 1:

            lugar_temp = lista_lugares_temp.pop(0)

            for lugar_destino in lista_lugares_temp:

                print("id lugar inicial: ", lugar_temp.id)
                print("id lugar final: : ", lugar_destino.id)
                listas = self.a_star_lugar_v2(lugar_temp, lugar_destino)
                if listas is not None:
                    lista_refinada = listas[1]
                    novo_caminho = {"lugar_1": lugar_temp.id, "lugar_2": lugar_destino.id, "possui_caminho": True,
                                    "caminho": lista_refinada}
                    self.lista_caminhos.append(novo_caminho)
                    lugar_temp.add_caminho_lugar(lugar_destino, lista_caminho=lista_refinada)
                    caminho_volta = lista_refinada[:]
                    caminho_volta.reverse()
                    lugar_destino.add_caminho_lugar(lugar_temp, lista_caminho=caminho_volta)
                    qnt_caminhos_criados += 1
                    print("achou caminho")
                    print("------------------")
                else:
                    novo_caminho = {"lugar_1": lugar_temp.id, "lugar_2": lugar_destino.id, "possui_caminho": False}
                    lugar_temp.add_caminho_lugar(lugar_destino, possui_caminho=False)
                    lugar_destino.add_caminho_lugar(lugar_temp, possui_caminho=False)
                    self.lista_caminhos.append(novo_caminho)
                    qnt_caminhos_n_criados += 1
                    print("nenhum caminho encontrado")
                    print("------------------")

            lugar_temp.ja_teve_caminhos_atualizados = True

        porcentagem_caminhos_criados = funcoes.porcentagem_relativa(qnt_caminhos_possiveis, qnt_caminhos_criados)
        porcentagem_caminhos_n_criados = funcoes.porcentagem_relativa(qnt_caminhos_possiveis, qnt_caminhos_n_criados)

        print("caminhos possiveis: ", qnt_caminhos_possiveis)
        print("caminhos criados: ", qnt_caminhos_criados)
        print("caminhos n criados: ", qnt_caminhos_n_criados)
        print("{}% dos caminhos foram criados".format(round(porcentagem_caminhos_criados, 2)))
        print("{}% dos caminhos n foram criados".format(round(porcentagem_caminhos_n_criados, 2)))

    def restaurar_estado_inicial_celulas(self):
        for linha in self.matriz_celulas:
            for celula in linha:

                celula.parente = None
                celula.ja_foi_visitado = False
                celula.g = 0
                celula.h = 0
                celula.f = 0

    @staticmethod
    def restaurar_estado_inicial_celulas_v2(lista_celulas):

        for celula in lista_celulas:
            celula.parente = None
            celula.ja_foi_visitado = False
            celula.ja_foi_analisado = False
            celula.g = 0
            celula.h = 0
            celula.f = 0

    def atualizar_fronteiras_lugares(self):
        for lugar in self.lista_lugares:
            lugar.achar_pontos_fronteiras(self)

    def salvar_lugares_arquivo(self, nome_arquivo):
        lista_final = []

        for lugar in self.lista_lugares:
            lugar_simplificado = [lugar.id, lugar.lista_coordenadas, lugar.cor, lugar.orientacao]
            lista_final.append(lugar_simplificado)

        funcoes.lista_para_arquivo_csv(lista_final, nome_arquivo)

    def resgatar_lugares_arquivo(self, nome_arquivo_lugares):
        lista_lugares = funcoes.arquivo_csv_para_lista(nome_arquivo_lugares)
        for lugar in lista_lugares:
            lugar_novo = LugarV2(self, veio_de_arquivo=True, lista_arquivo=lugar)
            print("resgatou o lugar {}".format(lugar_novo.id))
            self.lista_lugares.append(lugar_novo)

    def salvar_caminhos_arquivo(self, nome_arquivo):
        lista_final = [[j for j in i.values()] for i in self.lista_caminhos]
        funcoes.lista_para_arquivo_csv(lista_final, nome_arquivo)

    def salvar_novos_caminhos_arquivo(self, nome_arquivo):
        novos_caminhos_temp = self.lista_caminhos[self.qnt_caminhos_resgatados_arquivo:]
        novos_caminhos = [[j for j in i.values()] for i in novos_caminhos_temp]
        funcoes.lista_para_arquivo_csv(novos_caminhos, nome_arquivo, tipo_operacao="a")
        print("{} novos caminhos foram salvos no arquivo: {}".format(len(novos_caminhos), nome_arquivo))

    def salvar_caminhos_arquivo_v2(self, nome_arquivo_caminhos):
        # junta as funcoes "salvar_caminhos_arquivo" e "salvar_novos_caminhos_arquivo"
        # primeiro, testa-se a existencia do arquivo de caminhos
        # caso n exista, a funcao "salvar_caminhos_arquivo" eh executada
        # caso contario, a funcao "salvar_novos_caminhos_arquivo" eh executada

        existencia_arquivo_caminhos = funcoes.checar_existencia_arquivo(nome_arquivo_caminhos)

        if existencia_arquivo_caminhos is False:
            self.salvar_caminhos_arquivo(nome_arquivo_caminhos)
        else:
            self.salvar_novos_caminhos_arquivo(nome_arquivo_caminhos)

    def resgatar_caminhos_arquivo(self, nome_arquivo):
        matriz_temp = funcoes.arquivo_csv_para_lista(nome_arquivo)
        matriz_final = []

        for linha in matriz_temp:
            if len(linha) == 3:
                lista_chaves_sem_caminho_analisado = ["lugar_1", "lugar_2", "caminho_analisado"]
                dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves_sem_caminho_analisado, linha)
                matriz_final.append(dicionario)
            if len(linha) == 4:
                lista_chaves_sem_caminho = ["lugar_1", "lugar_2", "caminho_analisado", "possui_caminho"]
                dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves_sem_caminho, linha)
                matriz_final.append(dicionario)
            if len(linha) == 5:
                lista_chaves_com_caminho = ["lugar_1", "lugar_2", "caminho_analisado", "possui_caminho", "caminho"]
                dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves_com_caminho, linha)
                matriz_final.append(dicionario)

        self.lista_caminhos = matriz_final
        self.qnt_caminhos_resgatados_arquivo = len(self.lista_caminhos)

    def resgatar_caminhos_arquivo_v2(self, nome_arquivo_caminhos):
        # mesma funcao que "resgatar_caminhos_arquivo" mas sem o campo "caminho_analisado"

        existencia_arquivo_caminhos = funcoes.checar_existencia_arquivo(nome_arquivo_caminhos)

        if existencia_arquivo_caminhos is False:
            print("nao existe arquivo caminhos para este arquivo base")
        else:
            matriz_temp = funcoes.arquivo_csv_para_lista(nome_arquivo_caminhos)
            matriz_final = []

            for linha in matriz_temp:
                if len(linha) == 3:
                    lista_chaves_sem_caminho = ["lugar_1", "lugar_2", "possui_caminho"]
                    dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves_sem_caminho, linha)
                    matriz_final.append(dicionario)
                if len(linha) == 4:
                    lista_chaves_com_caminho = ["lugar_1", "lugar_2", "possui_caminho", "caminho"]
                    dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves_com_caminho, linha)
                    matriz_final.append(dicionario)

            self.lista_caminhos = matriz_final
            self.qnt_caminhos_resgatados_arquivo = len(self.lista_caminhos)
            print("foram resgatados {} caminhos do arquivo {}".format(self.qnt_caminhos_resgatados_arquivo, nome_arquivo_caminhos))

    def salvar_matriz_arquivo(self, nome_arquivo):

        matriz_final = []

        for linha in self.matriz_celulas:
            linha_final = []
            for celula in linha:
                if celula.andavel is True or celula.andavel is False and celula.lugar is not None:
                    celula_final = 0
                else:
                    celula_final = 1
                linha_final.append(celula_final)
            matriz_final.append(linha_final)

        funcoes.lista_para_arquivo_csv(matriz_final, nome_arquivo)

    def resgatar_matriz_arquivo(self, nome_arquivo):

        matriz_layout = funcoes.arquivo_csv_para_lista(nome_arquivo)

        for i in range(self.qnt_linhas):
            for j in range(self.qnt_colunas):

                if matriz_layout[i][j] == 0:
                    self.matriz_celulas[i][j].andavel = True
                else:
                    self.matriz_celulas[i][j].andavel = False
                    self.matriz_celulas[i][j].cor = cores.preto

    def salvar_celulas_acessiveis_lugares(self, nome_arquivo):
        lista_para_arquivo = []

        for lugar in self.lista_lugares:
            linha = [lugar.id, lugar.lista_celulas_grid_acessiveis]
            lista_para_arquivo.append(linha)

        funcoes.lista_para_arquivo_csv(lista_para_arquivo, nome_arquivo)

    def resgatar_celulas_acessiveis_lugares(self, nome_arquivo):
        matriz_celulas_acessiveis_lugares = funcoes.arquivo_csv_para_lista(nome_arquivo)
        lista_chaves = ["id", "lista_celulas_acessiveis"]
        lista_dicionarios_celulas_acessiveis = funcoes.matriz_para_lista_dicionarios(lista_chaves,
                                                                                     matriz_celulas_acessiveis_lugares)

        for lugar in self.lista_lugares:
            for dicionario in lista_dicionarios_celulas_acessiveis:

                if lugar.id == dicionario["id"]:
                    lugar.lista_celulas_grid_acessiveis = dicionario["lista_celulas_acessiveis"]

    def obter_lugar_pelo_id(self, num_id):
        for lugar in self.lista_lugares:
            if lugar.id == num_id:
                return lugar

    def restaurar_caminhos_entre_lugares(self):

        for dicionario in self.lista_caminhos:

            lugar_1 = self.obter_lugar_pelo_id(dicionario["lugar_1"])
            lugar_2 = self.obter_lugar_pelo_id(dicionario["lugar_2"])

            if dicionario["caminho_analisado"] is True:
                if dicionario["possui_caminho"] is True:
                    rota_1 = dicionario["caminho"]
                    rota_2 = list(reversed(rota_1[:]))
                    dicionario_1 = {"destino": lugar_2, "caminho_analisado": True, "possui_caminho": True,
                                    "caminho": rota_1}
                    dicionario_2 = {"destino": lugar_1, "caminho_analisado": True, "possui_caminho": True,
                                    "caminho": rota_2}
                    lugar_1.lista_caminhos.append(dicionario_1)
                    lugar_2.lista_caminhos.append(dicionario_2)
                else:
                    dicionario_1 = {"destino": lugar_2, "caminho_analisado": True, "possui_caminho": False}
                    dicionario_2 = {"destino": lugar_1, "caminho_analisado": True, "possui_caminho": False}
                    lugar_1.lista_caminhos.append(dicionario_1)
                    lugar_2.lista_caminhos.append(dicionario_2)

    def restaurar_caminhos_entre_lugares_v2(self):
        # mesma coisa que "restaurar_caminhos_entre_lugares" mas sem o campo "caminho analisado"

        for dicionario in self.lista_caminhos:

            lugar_1 = self.obter_lugar_pelo_id(dicionario["lugar_1"])
            lugar_2 = self.obter_lugar_pelo_id(dicionario["lugar_2"])

            if dicionario["possui_caminho"] is True:
                rota_1 = dicionario["caminho"]
                rota_2 = list(reversed(rota_1[:]))
                dicionario_1 = {"destino": lugar_2, "possui_caminho": True, "caminho": rota_1}
                dicionario_2 = {"destino": lugar_1, "possui_caminho": True, "caminho": rota_2}
                lugar_1.lista_caminhos.append(dicionario_1)
                lugar_2.lista_caminhos.append(dicionario_2)
            else:
                dicionario_1 = {"destino": lugar_2, "possui_caminho": False}
                dicionario_2 = {"destino": lugar_1, "possui_caminho": False}
                lugar_1.lista_caminhos.append(dicionario_1)
                lugar_2.lista_caminhos.append(dicionario_2)

    def obter_dict_ocorrencia_orientacoes(self):

        lista_orientacoes = [math.ceil(agente.orientacao_atual / 100) * 100 for agente in self.lista_agentes]
        dict_ocorrencia_orientacoes_temp = funcoes.obter_dict_contagem_elementos_repetidos_v2(lista_orientacoes)
        dict_ocorrencia_orientacoes_final = {str(key): value for key, value in dict_ocorrencia_orientacoes_temp.items()}
        return dict_ocorrencia_orientacoes_final

    def calcular_entropia(self):

        dict_orientacoes_e_ocorrencias = self.obter_dict_ocorrencia_orientacoes()
        qnt_total_agentes = AgenteV2.qnt_agentes
        frenquencia_orientacoes = {key: (value / qnt_total_agentes) for key, value in dict_orientacoes_e_ocorrencias.items()}

        lista_entropia = [value * math.log(value) for value in frenquencia_orientacoes.values()]
        entropia_final = -sum(lista_entropia)
        entropia_final = round(entropia_final, 3)
        return entropia_final
    
    def calcular_entropia_geral(self):
        lista_orientacoes_agentes = [math.ceil(agente.orientacao_latente / 100) * 100 for agente in self.lista_agentes]
        lista_orientacoes_lugares = [math.ceil(lugar.orientacao / 100) * 100 for lugar in self.lista_lugares]
        lista_orientacoes_geral = lista_orientacoes_agentes + lista_orientacoes_lugares

        dict_orientacoes_e_ocorrencias = funcoes.obter_dict_contagem_elementos_repetidos_v2(lista_orientacoes_geral)
        qnt_total = len(self.lista_lugares) + len(self.lista_lugares)
        frenquencia_orientacoes = {key: (value / qnt_total) for key, value in
                                   dict_orientacoes_e_ocorrencias.items()}

        lista_entropia = []

        for value in frenquencia_orientacoes.values():
            if value == 0:
                lista_entropia.append(value)
            else:
                resultado = value * math.log(value)
                lista_entropia.append(resultado)

        entropia_final = -sum(lista_entropia)
        entropia_final = round(entropia_final, 3)
        return entropia_final

    def todos_lugares_pretos(self):
        for lugar in self.lista_lugares:
            lugar.cor = cores.preto

    def restaurar_cor_lugares(self):
        for lugar in self.lista_lugares:
            lugar.cor = lugar.cor_original

    def achar_lugar(self):
        id_escolhido = int(input("digite o id do lugar: "))

        for lugar in self.lista_lugares:
            if lugar.id == id_escolhido:
                lugar.cor = lugar.cor_original

    def achar_lugar_v2(self, id_lugar):
        for lugar in self.lista_lugares:
            if lugar.id == id_lugar:
                return lugar

    def add_caminho_lista_caminhos_grid(self, lugar_1_id, lugar_2_id, caminho_analisado=False,
                                        possui_caminho=False, caminho=None):

        if caminho_analisado is False:
            lista_chaves = ["lugar_1", "lugar_2", "caminho_analisado"]
            lista_valores = [lugar_1_id, lugar_2_id, caminho_analisado]
            dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves, lista_valores)
            self.lista_caminhos.append(dicionario)
        else:
            if possui_caminho is False:
                lista_chaves = ["lugar_1", "lugar_2", "caminho_analisado", "possui_caminho"]
                lista_valores = [lugar_1_id, lugar_2_id, caminho_analisado, possui_caminho]
                dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves, lista_valores)
                self.lista_caminhos.append(dicionario)
            else:
                lista_chaves = ["lugar_1", "lugar_2", "caminho_analisado", "possui_caminho", "caminho"]
                lista_valores = [lugar_1_id, lugar_2_id, caminho_analisado, possui_caminho, caminho]
                dicionario = funcoes.transformar_duas_listas_em_dict(lista_chaves, lista_valores)
                self.lista_caminhos.append(dicionario)

    def add_caminho_lista_caminhos_grid_v2(self, lugar_1_id, lugar_2_id, possui_caminho, caminho=None):
        if possui_caminho is False:
            novo_dicionario = {"lugar_1": lugar_1_id, "lugar_2": lugar_2_id, "possui_caminho": False}
            self.lista_caminhos.append(novo_dicionario)
        else:
            novo_dicionario = {"lugar_1": lugar_1_id, "lugar_2": lugar_2_id, "possui_caminho": True, "caminho": caminho}
            self.lista_caminhos.append(novo_dicionario)

    def atualizar_lista_caminhos_grid(self, lugar_1_id, lugar_2_id, possui_caminho, caminho=None):

        primeira_analise = False

        for dicionario in self.lista_caminhos:
            if dicionario["lugar_1"] == lugar_1_id and dicionario["lugar_2"] == lugar_2_id:
                primeira_analise = True
                dicionario["caminho_analisado"] = True
                if possui_caminho is False:
                    dicionario["possui_caminho"] = False
                if possui_caminho is True:
                    dicionario["possui_caminho"] = True
                    dicionario["caminho"] = caminho

        if primeira_analise is False:
            self.add_caminho_lista_caminhos_grid(lugar_1_id, lugar_2_id, caminho_analisado=True,
                                                 possui_caminho=possui_caminho, caminho=caminho)

    # obsoleto
    def init_lista_caminho_lugares(self):

        lista_lugares_usaveis = self.lista_lugares[:]

        while len(lista_lugares_usaveis) > 0:

            lugar_origem = lista_lugares_usaveis.pop(0)

            for lugar_destino in lista_lugares_usaveis:
                lugar_origem.add_caminho_lugar(lugar_destino, caminho_analisado=False)
                lugar_destino.add_caminho_lugar(lugar_origem, caminho_analisado=False)
                self.add_caminho_lista_caminhos_grid(lugar_origem.id, lugar_destino.id, caminho_analisado=False)

    def atualizar_cor_lugares(self):
        df_lugares = pd.read_csv(self.arquivo_lugares_dinamicos)
        qnt_linhas, qnt_colunas = df_lugares.shape

        time_step_selecionado = int(input("digite o time step (de 0 ate {}): ".format(qnt_linhas-1)))

        lista_colunas = list(df_lugares.columns)
        linha_selecionada = list(df_lugares.iloc[time_step_selecionado])

        for coluna, orientacao in zip(lista_colunas, linha_selecionada):
            id_lugar = fgn.string_to_id(coluna)
            lugar_escolhido = self.achar_lugar_v2(id_lugar)
            lugar_escolhido.orientacao = orientacao
            lugar_escolhido.cor = funcoes.update_orientacao_cor(self.dict_orientacoes_cores, lugar_escolhido.orientacao)

        print("cor dos lugares atualizada!")
