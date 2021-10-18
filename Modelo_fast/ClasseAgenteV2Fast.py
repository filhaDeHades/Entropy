import Modelo_fast.funcoes_fast as fst
import numpy as np
import random
import math


class AgenteV2Fast:

    qnt_agentes = 0

    def __init__(self, grid, grid_x, grid_y, orientacao_latente=0, orientacao_atual=0, id_agente=None):

        if id_agente is None:
            self.id = AgenteV2Fast.qnt_agentes
            AgenteV2Fast.qnt_agentes += 1
        else:
            self.id = id_agente

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_grid = (grid_x, grid_y)

        self.celula_grid = None
        self.atualizar_celula_grid(grid, self.grid_x, self.grid_y)

        self.orientacao_latente = orientacao_latente
        self.orientacao_atual = orientacao_atual

        # variaveis de estado inicial

        self.grid_x_inicial = grid_x
        self.grid_y_inicial = grid_y
        self.pos_grid_inicial = (grid_x, grid_y)

        self.orientacao_latente_inicial = orientacao_latente
        self.orientacao_atual_inicial = orientacao_atual

    def atualizar_celula_grid(self, grid, x, y):
        celula = grid.obter_celula_array_grid(x, y)
        self.celula_grid = celula

    def atualizar_posicao_grid(self, grid, pos_nova_grid):
        self.grid_x = pos_nova_grid[0]
        self.grid_y = pos_nova_grid[1]
        self.pos_grid = pos_nova_grid
        self.atualizar_celula_grid(grid, self.grid_x, self.grid_y)

    def contaminacao_agente(self, orientacao_do_lugar, pesos):
        a, b = pesos[0], pesos[1]
        soma_pesos = a + b

        contaminacao = int((a*self.orientacao_latente + b*orientacao_do_lugar) / soma_pesos)
        self.orientacao_latente = contaminacao

    def sortear_nova_orientacao(self):
        possiveis_orientacoes = list(range(0, 1100, 100))
        nova_orientacao = random.choice(possiveis_orientacoes)
        self.orientacao_atual = nova_orientacao
        # print("(SORTEIO) o agente agr possui orientacao latente de: ", self.orientacao_latente)

    def escolher_lugar_v4(self, grid):

        lugar_escolhido_eh_aceitavel = False
        lista_lugares_usaveis = list(grid.array_lugares[:])
        lugar_onde_agente_esta = self.celula_grid.lugar

        if lugar_onde_agente_esta is not None:
            lista_lugares_usaveis.remove(lugar_onde_agente_esta)

        lugar_escolhido_final = lista_lugares_usaveis[0]

        while lugar_escolhido_eh_aceitavel is False:

            if len(lista_lugares_usaveis) == 0:
                # print("n ha lugares onde o agente possa ir")
                return None

            lugar_escolhido = fst.escolher_lugar_menor_e(self, lista_lugares_usaveis)
            # print("o agente {} escolheu o lugar {}".format(self.id, lugar_escolhido.id))

            if lugar_onde_agente_esta is not None:
                # print("o agente {} se encontra no lugar {} ".format(self.id, lugar_onde_agente_esta.id))

                caminho_ja_foi_analisado = False
                dicionario_ja_existente = None

                if len(lugar_onde_agente_esta.lista_caminhos) > 0:
                    for dicionario in lugar_onde_agente_esta.lista_caminhos:
                        if dicionario["destino"] == lugar_escolhido:
                            caminho_ja_foi_analisado = True
                            dicionario_ja_existente = dicionario
                            # print("ja foi analisado o caminho entre o lugar {} e o lugar {}"
                            # .format(lugar_onde_agente_esta.id, lugar_escolhido.id))
                            break

                if caminho_ja_foi_analisado is False:
                    # print("n foi analisado ainda o caminho entre o lugar {} e o lugar {}"
                    # .format(lugar_onde_agente_esta.id, lugar_escolhido.id))

                    resultados_a_star = grid.a_star_lugar_v2(lugar_onde_agente_esta, lugar_escolhido)

                    if resultados_a_star is None:
                        # print("n ha caminho entre o lugar {} e o lugar {}".format(lugar_onde_agente_esta.id,
                        #                                                           lugar_escolhido.id))
                        lista_lugares_usaveis.remove(lugar_escolhido)
                        lugar_onde_agente_esta.add_caminho_lugar_v2(lugar_escolhido, False)
                        lugar_escolhido.add_caminho_lugar_v2(lugar_onde_agente_esta, False)
                        grid.add_caminho_lista_caminhos_grid_v2(lugar_onde_agente_esta.id, lugar_escolhido.id, False)
                    else:
                        # print("ha caminho entre o lugar {} e o lugar {}".format(lugar_onde_agente_esta.id,
                        #                                                         lugar_escolhido.id))
                        lugar_escolhido_final = lugar_escolhido
                        lugar_escolhido_eh_aceitavel = True
                        lista_refinada = resultados_a_star["lista_refinada"]
                        lugar_onde_agente_esta.add_caminho_lugar_v2(lugar_escolhido, True, caminho=lista_refinada)
                        caminho_volta = list(reversed(lista_refinada[:]))
                        lugar_escolhido.add_caminho_lugar_v2(lugar_onde_agente_esta, True, caminho=caminho_volta)
                        grid.add_caminho_lista_caminhos_grid_v2(lugar_onde_agente_esta.id, lugar_escolhido.id, True,
                                                                caminho=lista_refinada)
                else:
                    if dicionario_ja_existente["possui_caminho"] is False:
                        lista_lugares_usaveis.remove(lugar_escolhido)
                    else:
                        lugar_escolhido_final = lugar_escolhido
                        lugar_escolhido_eh_aceitavel = True
            else:
                # print("o agente {} n se encontra em nenhum lugar".format(self.id))
                resultados_a_star = grid.a_star_lugar(self.celula_grid, lugar_escolhido)

                if resultados_a_star is None:
                    # print("n ha caminho entre a celula do agente {} e o lugar escolhido".format(self.id))
                    lista_lugares_usaveis.remove(lugar_escolhido)
                else:
                    # print("ha um caminho entre a celula do agente {} e o lugar escolhido".format(self.id))
                    lugar_escolhido_final = lugar_escolhido
                    lugar_escolhido_eh_aceitavel = True

        return lugar_escolhido_final

    def escolher_lugar_v5(self, lista_lugares, lista_pesos=(0.1, 0.1), modelo_fabiano=False):

        orientacao_usada = self.orientacao_atual

        if modelo_fabiano is True:
            orientacao_usada = self.orientacao_latente

        peso_dif_orientacao = lista_pesos[0]
        peso_distancia = lista_pesos[1]

        # é a lista que contém o peso de cada lugar ser sorteado
        # a ordem importa, peso da pos[0] é o peso do lugar na pos[0] na lista lugares
        lista_pesos = np.zeros(len(lista_lugares))
        norma = 0

        for i in range(len(lista_lugares)):
            lugar = lista_lugares[i]
            dif_orientacao = abs(orientacao_usada - lugar.orientacao)
            coordenada_escolhida = lugar.achar_coordenada_principal(self.pos_grid)
            distancia = fst.obter_distancia_manhattan(coordenada_escolhida, self.pos_grid)

            fator_dif_orientacao = peso_dif_orientacao * dif_orientacao
            fator_distancia = peso_distancia * distancia

            expoente = fator_dif_orientacao + fator_distancia
            peso = np.exp(-expoente)
            lista_pesos[i] = peso
            norma += peso

        # normalização
        lista_pesos_final = lista_pesos / norma
        lugar_escolhido = fst.sorteio_com_pesos(lista_lugares, lista_pesos_final)[0]
        return lugar_escolhido

    @staticmethod
    def sorteioComPesos(listaPossibilidades, listaPesos, qntElementosSorteados=1):
        listaElementosSorteados = random.choices(listaPossibilidades, weights=listaPesos, k=qntElementosSorteados)
        return listaElementosSorteados

    # funcao importada do modelo 1D, so esta sendo adaptada para o model 2D
    def escolher_lugar(self, listaLugares, pesos):
        pesoDifOrientacao = pesos[0]
        pesoDistancia = pesos[1]

        # é a lista que contém o peso de cada lugar ser sorteado
        # a ordem importa, peso da pos[0] é o peso do lugar na pos[0] na lista lugares
        listaPesos = []

        for lugar in listaLugares:
            difOrientacao = abs(self.orientacao_latente - lugar.orientacao)
            coordenada_principal = lugar.achar_coordenada_principal(self.pos_grid)
            distancia = fst.obter_distancia_manhattan(self.pos_grid, coordenada_principal)
            
            fatorDifOrientacao = pesoDifOrientacao * difOrientacao
            fatorDistancia = pesoDistancia * distancia

            expoente = fatorDifOrientacao + fatorDistancia
            peso = math.exp(-expoente)
            if peso == 0.0:
                peso = 0.1
            
            listaPesos.append(peso)
        
        somaListaPesos = sum(listaPesos)
        #print(f"LISTA PESOS: {listaPesos}\nSOMA: {somaListaPesos}\n")
        # normalização
        listaPesosFinal = [i/somaListaPesos for i in listaPesos]
        # print("lista pesos final: ", sum(listaPesosFinal))

        lugarEscolhido = self.sorteioComPesos(listaLugares, listaPesosFinal)[0]
        return lugarEscolhido

    def resgatar_estado_inicial(self):
        self.grid_x = self.grid_x_inicial
        self.grid_y = self.grid_y_inicial
        self.pos_grid = self.pos_grid_inicial

        self.orientacao_latente = self.orientacao_latente_inicial
        self.orientacao_atual = self.orientacao_atual_inicial
