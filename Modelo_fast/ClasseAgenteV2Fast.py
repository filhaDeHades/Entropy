import Modelo_fast.funcoes_fast as fst
import numpy as np
import random
import math
from math import sqrt, degrees, acos, cos, radians, sin


class AgenteV2Fast:

    qnt_agentes = 0

    def __init__(self, grid, grid_x, grid_y, orientacao_latente=0, orientacao_atual=0, id_agente=None):
        """Inicializa o agente, adicionando seu id, sua orientação latente,
            sua orientação atual, o grid e sua posição no grid.

        Args:
            grid (GridV2Fast): Instância da Classe GridV2Fast onde a simulação ocorre.
            grid_x (int): Posição X do agente no grid.
            grid_y (int): Posição Y do agente no grid.
            orientacao_latente (int, optional): Contém o valor da orientação latente do agente. Defaults to 0.
            orientacao_atual (int, optional): Contém o valor da orientação atual do agente. Defaults to 0.
            id_agente (int, optional): Número de identificação do agente. Defaults to None.
        """

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
        """Atualiza a célula do grid.

        Args:
            grid (GridV2Fast): Grid onde a simulação está sendo feita.
            x (int): Posição X da célula no grid.
            y (int): Posição Y da célula no grid.
        """

        celula = grid.obter_celula_array_grid(x, y)
        self.celula_grid = celula

    def atualizar_posicao_grid(self, grid, pos_nova_grid):
        """Atualiza a posição para a posição atual.

        Args:
            grid (GridV2Fast): Grid onde a simulação está sendo feita.
            pos_nova_grid (tuple): Tupla com a posição atual da célula.
        """

        self.grid_x = pos_nova_grid[0]
        self.grid_y = pos_nova_grid[1]
        self.pos_grid = pos_nova_grid
        self.atualizar_celula_grid(grid, self.grid_x, self.grid_y)

    def somaVetor(self,vetores):
        """Soma os vetores para o cálculo da nova orientação do agente.

        Args:
            vetores (list): Lista contendo 2 tuplas representando os vetores a ser somados.

        Returns:
            list: Retorna uma lista com a soma dos vetores.
        """

    #ve a quantidade de vetores
        qtdVetores = len(vetores)
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


    def contaminacao_agente(self, grid, orientacao_do_lugar, pesoContaminacaoAgente, atualizar_cor=True):
        """Calcula a contaminação do agente pela orientação do lugar.

        Args:
            orientacao_do_lugar (int): Orientação atual do lugar.
            pesos (tuple): Pesos C e D do agente.
        """

        a, b = pesoContaminacaoAgente[0],pesoContaminacaoAgente[1]
        aux1=[ ( a*cos(radians(self.orientacao_latente)) , a*sin(radians(self.orientacao_latente)) ) , ( b*cos(radians(orientacao_do_lugar)), b*sin(radians(orientacao_do_lugar)) ) ]
        contaminacao= int(self.anguloVX(self.somaVetor(aux1)))
        
        self.orientacao_atual=contaminacao

        # if atualizar_cor is True:
        #     # print("cor antes: ", self.cor)
        #     self.cor = fst.update_orientacao_cor(grid.dict_orientacoes_cores, self.orientacao_atual)
        #     # print("cor agora: ", self.cor)
        #     grid.dict_orientacoes_cores[str(self.orientacao_atual)] = self.cor


    def sortear_nova_orientacao(self):
        """Sorteia uma nova orientação para o agente, sem levar
            em consideração possíveis contaminações.
        """

        possiveis_orientacoes = list(range(0, 1100, 100))
        nova_orientacao = random.choice(possiveis_orientacoes)
        self.orientacao_atual = nova_orientacao
    

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
            if peso == 0.0:
                peso = np.nextafter(np.float32(0), np.float32(1))

            lista_pesos[i] = peso
            norma += peso

        # normalização
        lista_pesos_final = lista_pesos / norma
        lugar_escolhido = fst.sorteio_com_pesos(lista_lugares, lista_pesos_final)[0]
        return lugar_escolhido

    @staticmethod
    def sorteioComPesos(listaPossibilidades, listaPesos, qntElementosSorteados=1):
        """Faz um sorteio ponderado.

        Args:
            listaPossibilidades (list): Lista com as opções de escolhas
            listaPesos (list): Lista com os pesos que cada opção de escolha terá
                no sorteio (ordenada da mesma forma que a listaPossibilidades).
            qntElementosSorteados (int, optional): Define quantos elementos da
                listaPossibilidades devem ser sorteados utilizando os pesos
                informados. Defaults to 1.

        Returns:
            [list]: Lista contendo todos os valores sorteados.
        """

        listaElementosSorteados = random.choices(listaPossibilidades, weights=listaPesos, k=qntElementosSorteados)
        return listaElementosSorteados


    # funcao importada do modelo 1D, so esta sendo adaptada para o model 2D
    def escolher_lugar(self, listaLugares, pesos):
        """É atribuido os pesos que cada lugar terá no sorteio do próximo destino
            do agente.

        Args:
            listaLugares (list): Lista contendo todos os lugares do grid.
            pesos (tupla): Pesos C e D dos agentes

        Returns:
            [LugarV2Fast]: Lugar escolhido como próximo destino na simulação.
        """

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
                peso = np.nextafter(np.float32(0), np.float32(1))
            
            listaPesos.append(peso)
        
        somaListaPesos = sum(listaPesos)

        # normalização
        listaPesosFinal = [i/somaListaPesos for i in listaPesos]

        lugarEscolhido = self.sorteioComPesos(listaLugares, listaPesosFinal)[0]
        return lugarEscolhido


    def resgatar_estado_inicial(self):
        """Resgata o estado inicial da célula, ou seja, o estado
            padrão antes das mudanças feitas pelo A*
        """

        self.grid_x = self.grid_x_inicial
        self.grid_y = self.grid_y_inicial
        self.pos_grid = self.pos_grid_inicial

        self.orientacao_latente = self.orientacao_latente_inicial
        self.orientacao_atual = self.orientacao_atual_inicial
