import pygame as pg
import cores
import funcoes
import random
import math


class AgenteV2:

    qnt_agentes = 0

    def __init__(self, grid, grid_x, grid_y, cell_size, velocidade=4, cor=cores.vermelho,
                 orientacao_latente=0, orientacao_atual=0):

        self.id = AgenteV2.qnt_agentes
        AgenteV2.qnt_agentes += 1

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_grid = (grid_x, grid_y)

        self.pos_x = grid_x * cell_size + cell_size // 2
        self.pos_y = grid_y * cell_size + cell_size // 2
        self.pos = (self.pos_x, self.pos_y)

        self.celula_grid = None
        self.atualizar_celula_grid_inicial(grid)

        self.valor_velocidade = velocidade
        self.velocidade_x = self.valor_velocidade
        self.velocidade_y = self.valor_velocidade

        self.cor = cor

        if cell_size > 8:
            self.size = cell_size // 2
        else:
            self.size = 8

        self.cor = cor

        self.orientacao_latente = orientacao_latente
        self.orientacao_atual = orientacao_atual

        self.escolheu_destino = False
        self.destino_atual = None
        self.chegou_destino = False
        self.escolheu_caminho = False
        self.direcao_atual = None
        self.ultima_pos = None
        self.prox_pos = None
        self.caminho_atual = []

        self.chegou_pos_x_temp = False
        self.chegou_pos_y_temp = False

        # variaveis para resgatar estado inicial
        self.grid_x_inicial = grid_x
        self.grid_y_inicial = grid_y
        self.pos_grid_inicial = (grid_x, grid_y)

        self.pos_x_inicial = grid_x * cell_size + cell_size // 2
        self.pos_y_inicial = grid_y * cell_size + cell_size // 2
        self.pos_inicial = (self.pos_x_inicial, self.pos_y_inicial)

        self.orientacao_latente_inicial = orientacao_latente
        self.orientacao_atual_inicial = orientacao_atual

    def atualizar_celula_grid_inicial(self, grid):
        celula_inicial = grid.matriz_celulas[self.grid_y][self.grid_x]
        self.celula_grid = celula_inicial
        celula_inicial.lista_agentes_presentes.append(self)
        grid.lista_celulas_ocupadas.append(celula_inicial)

    def atualizar_pos_grid(self, grid, pos_nova_grid):
        self.ultima_pos = self.pos_grid

        self.grid_x = pos_nova_grid[0]
        self.grid_y = pos_nova_grid[1]
        self.pos_grid = pos_nova_grid

        self.celula_grid.lista_agentes_presentes.remove(self)
        self.celula_grid = grid.matriz_celulas[self.grid_y][self.grid_x]
        self.celula_grid.lista_agentes_presentes.append(self)
        self.celula_grid.visitas += 1
        self.celula_grid.update_cor_de_calor()

    def verificar_direcao_velocidade(self, grid, mov_randomico=False):
        if self.prox_pos is None:
            if mov_randomico is True:
                self.prox_pos = self.sortear_nova_pos_grid_vizinha(grid)
            else:
                self.prox_pos = self.caminho_atual.pop(0)

        dx = self.prox_pos[0] - self.pos_grid[0]
        dy = self.prox_pos[1] - self.pos_grid[1]

        direcao_x = 0
        direcao_y = 0

        if dx != 0:
            direcao_x = dx // abs(dx)

        if dy != 0:
            direcao_y = dy // abs(dy)

        self.direcao_atual = (direcao_x, direcao_y)
        self.velocidade_x = self.valor_velocidade * direcao_x
        self.velocidade_y = self.valor_velocidade * direcao_y

    def update_posicao(self, grid, mov_randomico=False):

        self.verificar_direcao_velocidade(grid, mov_randomico=mov_randomico)

        prox_pos_global = tuple(i * grid.cell_size + grid.cell_size // 2 for i in self.prox_pos)
        prox_pos_x_global = prox_pos_global[0]
        prox_pos_y_global = prox_pos_global[1]

        if self.chegou_pos_x_temp is False:             # analisando movimento horizontal
            if self.velocidade_x == 0:
                self.chegou_pos_x_temp = True

            if self.velocidade_x > 0:                   # movimento para a direita
                if self.pos_x < prox_pos_x_global:
                    self.pos_x += self.velocidade_x
                else:
                    self.pos_x = prox_pos_x_global
                    self.chegou_pos_x_temp = True

            if self.velocidade_x < 0:                   # movimento para a esquerda
                if self.pos_x > prox_pos_x_global:
                    self.pos_x += self.velocidade_x
                else:
                    self.pos_x = prox_pos_x_global
                    self.chegou_pos_x_temp = True

        if self.chegou_pos_y_temp is False:             # analisando movimento vertical
            if self.velocidade_y == 0:
                self.chegou_pos_y_temp = True

            if self.velocidade_y > 0:                   # movimento para baixo
                if self.pos_y < prox_pos_y_global:
                    self.pos_y += self.velocidade_y
                else:
                    self.pos_y = prox_pos_y_global
                    self.chegou_pos_y_temp = True

            if self.velocidade_y < 0:                   # movimento para cima
                if self.pos_y > prox_pos_y_global:
                    self.pos_y += self.velocidade_y
                else:
                    self.pos_y = prox_pos_y_global
                    self.chegou_pos_y_temp = True

        pos_nova = (self.pos_x, self.pos_y)
        self.pos = pos_nova
        pos_grid_atual = funcoes.converter_pos_para_coordenada_grid(self.pos, grid.cell_size)

        if self.chegou_pos_x_temp is True and self.chegou_pos_y_temp is True:
            self.chegou_pos_x_temp = False
            self.chegou_pos_y_temp = False

            if pos_grid_atual == self.prox_pos:
                self.atualizar_pos_grid(grid, pos_grid_atual)

            if mov_randomico is True:
                self.movimento_randomico(grid)
            else:
                if len(self.caminho_atual) > 0:
                    self.prox_pos = self.caminho_atual.pop(0)

    def update_posicao_randomica(self, grid):

        if self.direcao_atual is None:
            # print("o agente ainda n possui direcao")
            self.sortear_nova_direcao(grid)
        else:
            pos_x_apos_mov = self.pos_x + self.velocidade_x
            pos_y_apos_mov = self.pos_y + self.velocidade_y
            pos_global_apos_mov = (pos_x_apos_mov, pos_y_apos_mov)

            deslocamento_aceitavel = grid.verificar_se_posicao_eh_aceitavel(pos_x_apos_mov, pos_y_apos_mov, self.size)

            if deslocamento_aceitavel:
                pos_grid_apos_mov = funcoes.converter_pos_para_coordenada_grid(pos_global_apos_mov, grid.cell_size)
                self.pos_x = pos_x_apos_mov
                self.pos_y = pos_y_apos_mov
                self.pos = (self.pos_x, self.pos_y)
                self.atualizar_pos_grid(grid, pos_grid_apos_mov)
            else:
                self.sortear_nova_direcao(grid)

    def movimento_randomico(self, grid):

        direcao_x, direcao_y = self.direcao_atual
        prox_pos_grid_x = self.grid_x + direcao_x
        prox_pos_grid_y = self.grid_y + direcao_y

        prox_coordendas_aceitaveis = grid.verificar_se_coordenada_eh_andavel(prox_pos_grid_x, prox_pos_grid_y)

        if prox_coordendas_aceitaveis is True:
            self.prox_pos = (prox_pos_grid_x, prox_pos_grid_y)
        else:
            self.prox_pos = self.sortear_nova_pos_grid_vizinha(grid)

    def sortear_nova_pos_grid_vizinha(self, grid):
        lista_celulas_vizinhas = grid.obter_nodulos_vizinhos(self.celula_grid)
        lista_pos_vizinhas = [celula.pos_grid for celula in lista_celulas_vizinhas]
        if len(lista_pos_vizinhas) > 0:
            nova_pos_randomica = random.choice(lista_pos_vizinhas)
            return nova_pos_randomica
        else:
            return None

    def sortear_nova_direcao(self, grid):

        pos_grid_randomico = self.sortear_nova_pos_grid_vizinha(grid)
        pos_grid_x_rand, pos_grid_y_rand = pos_grid_randomico

        dx = pos_grid_x_rand - self.grid_x
        dy = pos_grid_y_rand - self.grid_y

        direcao_x = 0
        direcao_y = 0

        if dx != 0:
            direcao_x = dx // abs(dx)

        if dy != 0:
            direcao_y = dy // abs(dy)

        self.direcao_atual = (direcao_x, direcao_y)
        self.velocidade_x = self.valor_velocidade * direcao_x
        self.velocidade_y = self.valor_velocidade * direcao_y
        # print("direcao atual: ", self.direcao_atual)
        # print("velocidade x: ", self.velocidade_x)
        # print("velocidade y: ", self.velocidade_y)

    def configuracoes_chegou_destino(self):
        self.chegou_destino = True
        self.escolheu_destino = False
        self.destino_atual = None
        self.escolheu_caminho = False
        self.caminho_atual = []
        self.prox_pos = None
        self.celula_grid.lugar.lista_agentes_presentes.append(self)
        self.sortear_nova_orientacao()

    def configuracoes_proximo_destino(self, grid, lugar_destino, lugar_atual=None):
        if lugar_atual is not None:
            for lugar in lugar_atual.lista_caminhos:
                if lugar["destino"] == lugar_destino:
                    self.escolheu_destino = True
                    self.chegou_destino = False
                    self.destino_atual = lugar_destino
                    novo_caminho = lugar["caminho"][:]
                    self.caminho_atual = novo_caminho
                    self.escolheu_caminho = True
                    # print("o lugar ja tem um caminho pre definido: ", self.caminho_atual)

        else:
            self.escolheu_destino = True
            self.chegou_destino = False
            self.destino_atual = lugar_destino
            listas = grid.a_star_lugar(self.celula_grid, lugar_destino)
            lista_refinada = listas[1]
            self.caminho_atual = lista_refinada
            self.escolheu_caminho = True
            # print("n tem caminho pre definido, o caminho eh: ", self.caminho_atual)

    def contaminacao_agente(self, grid, orientacao_do_lugar, pesos, atualizar_cor=True):

        a, b, c = pesos[0], pesos[1], pesos[2]
        soma_pesos = sum(pesos)

        contaminacao = int((a*self.orientacao_latente + b*self.orientacao_atual + c*orientacao_do_lugar) / soma_pesos)
        self.orientacao_atual = contaminacao
        if atualizar_cor is True:
            # print("cor antes: ", self.cor)
            self.cor = funcoes.update_orientacao_cor(grid.dict_orientacoes_cores, self.orientacao_atual)
            # print("cor agora: ", self.cor)
            grid.dict_orientacoes_cores[str(self.orientacao_atual)] = self.cor

    def sortear_nova_orientacao(self):
        possiveis_orientacoes = list(range(0, 1100, 100))
        nova_orientacao = random.choice(possiveis_orientacoes)
        self.orientacao_latente = nova_orientacao

    # obsoleto, n funciona mas serviou para criar a v2
    def escolher_lugar(self, grid, lista_lugares, lugares_proibidos=None):
        # modelo que escolhe o local a partir da orientacao latente
        # escolhe o proximo local a ser visitado pelo agente
        # leva em consideracao a distancia e a diferencia de orientacao

        lista_lugares_final = lista_lugares[:]

        if self.celula_grid.lugar is not None:      # removendo o lugar em que o agente se encontra
            for lugar in lista_lugares_final:
                if self.celula_grid.lugar == lugar:
                    lista_lugares_final.remove(lugar)

        if lugares_proibidos is not None:
            for lugar in lugares_proibidos:
                print("lugar removido: ", lugar.id)
                lista_lugares_final.remove(lugar)   # removendo os lugares que n possui caminho

        print("possiveis lugares: \n")
        for lugar in lista_lugares_final:
            print("lugar: ", lugar.id)

        # agr deve-se achar o lugar que possui a menor distancia e dif de orientacao
        diferenca_orientacao_inicial = abs(self.orientacao_latente - lista_lugares_final[0].orientacao)
        coordenada_principal_inicial = lista_lugares_final[0].achar_coordenada_principal(self.pos_grid)
        distancia_inicial = round(funcoes.distancia_pitagorica(self.pos_grid, coordenada_principal_inicial))

        menor_e = diferenca_orientacao_inicial * distancia_inicial
        lugar_menor_e = lista_lugares_final[0]

        for lugar in lista_lugares_final:
            diferenca_orientacao_atual = abs(self.orientacao_latente - lugar.orientacao)
            coordenada_principal_atual = lugar.achar_coordenada_principal(self.pos_grid)
            distancia_atual = round(funcoes.distancia_pitagorica(self.pos_grid, coordenada_principal_atual))
            menor_e_atual = diferenca_orientacao_atual * distancia_atual

            if menor_e_atual < menor_e:
                menor_e = menor_e_atual
                lugar_menor_e = lugar

        # ja achou o lugar com menor distancia e dif de orientacao
        # devese saber se eh possivel, ou n, chegar nesse lugar
        # antes de saber se ha essa possibilidade, deve-se saber se o agente se encontra em algum lugar
        # assim, caso o agente esteja em algum lugar, o programa ira checar n lista de caminhos se ha um caminho
        # caso haja caminho, o lugar eh escolhido
        # caso n haja caminho, a funcao eh repetida onde esse lugar eh excluido das possibilidades
        # no caso onde o agente n esteja em um lugar, ele realiza o A* para ver se ha caminho ate o lugar
        # novamente, caso haja caminho, o lugar eh escolhido
        # caso contrario, a funcao eh repetida onde esse lugar eh excluido das possiblidades

        if self.celula_grid.lugar is not None:
            print("o agente esta em um lugar")
            for dicionario in self.celula_grid.lugar.lista_caminhos:
                if dicionario["destino"] == lugar_menor_e:      # achando o lugar de menor E na lista de caminhos do lugar em que o agente se encontra
                    if dicionario["possui_caminho"] is True:    # o lugar possui caminho e eh escolhido
                        print("o lugar escolhido possui caminho")
                        print("lugar id: ", lugar_menor_e.id)
                        return lugar_menor_e
                    else:                                       # o lugar n possui caminho e a funcao deve ser repetida
                        print("o lugar escolhido n possui caminho, deve-se escolher outro lugar")
                        if lugares_proibidos is None:           # neste caso, a funcao eh repetida pela primeira vez
                            lista_lugares_proibidos = [lugar_menor_e]
                            self.escolher_lugar(grid, lista_lugares, lugares_proibidos=lista_lugares_proibidos)
                        else:                                   # neste caso, a funcao ja foi repetida antes
                            nova_lista_lugares_proibidos = lugares_proibidos[:]
                            nova_lista_lugares_proibidos.append(lugar_menor_e)
                            self.escolher_lugar(grid, lista_lugares, lugares_proibidos=nova_lista_lugares_proibidos)

        else:                                                   # neste caso, o agente n se econtra em nenhum lugar
            print("o agente n se encontra em nenhum lugar")
            resultado_a_star = grid.a_star_lugar(self.celula_grid, lugar_menor_e)
            if resultado_a_star is None:                        # n possui caminho entre agente e o lugar
                print("lugar: ", lugar_menor_e.id)
                print("o lugar escolhido n possui caminho, deve-se escolher outro lugar")
                if lugares_proibidos is None:                   # neste caso, a funcao eh repetida pela primeira vez
                    lista_lugares_proibidos = [lugar_menor_e]
                    self.escolher_lugar(grid, lista_lugares, lugares_proibidos=lista_lugares_proibidos)
                else:                                           # neste caso, a funcao ja foi repetida antes
                    nova_lista_lugares_proibidos = lugares_proibidos[:]
                    nova_lista_lugares_proibidos.append(lugar_menor_e)
                    self.escolher_lugar(grid, lista_lugares, lugares_proibidos=nova_lista_lugares_proibidos)
            else:                                               # possui caminho entre agente e o lugar, lugar eh escolhido
                print("o lugar escolhido possui caminho")
                print("lugar id: ", lugar_menor_e.id)
                return lugar_menor_e

    def escolher_lugar_v2(self, grid):

        lugar_escolhido_eh_aceitavel = False
        lista_lugares_usaveis = grid.lista_lugares[:]
        lugar_onde_agente_esta = self.celula_grid.lugar

        if lugar_onde_agente_esta is not None:
            lista_lugares_usaveis.remove(lugar_onde_agente_esta)

        lugar_escolhido_final = lista_lugares_usaveis[0]

        while lugar_escolhido_eh_aceitavel is False:

            if len(lista_lugares_usaveis) == 0:
                # print("n ha lugares onde o agente possa ir")
                return None

            lugar_escolhido = funcoes.escolher_lugar_menor_e(self, lista_lugares_usaveis)
            # print("o lugar escolhido foi: ", lugar_escolhido.id)

            if lugar_onde_agente_esta is not None:
                # print("o agente se encontra no lugar: ", lugar_onde_agente_esta.id)

                for dicionario in lugar_onde_agente_esta.lista_caminhos:

                    if dicionario["destino"] == lugar_escolhido:
                        if dicionario["possui_caminho"] is True:
                            # print("o lugar {} ja possui caminho definido".format(lugar_escolhido.id))
                            lugar_escolhido_final = lugar_escolhido
                            lugar_escolhido_eh_aceitavel = True

                        if dicionario["possui_caminho"] is False:
                            # print("o lugar {} n possui caminho ate o agente".format(lugar_escolhido.id))
                            lista_lugares_usaveis.remove(lugar_escolhido)

            else:
                # print("o agente n se encontra em nenhum lugar")
                resultados_a_star = grid.a_star_lugar(self.celula_grid, lugar_escolhido)

                if resultados_a_star is None:
                    # print("n ha caminho entre a celula do agente e o lugar escolhido")
                    lista_lugares_usaveis.remove(lugar_escolhido)
                else:
                    # print("ha um caminho entre a celula do agente e o lugar escolhido")
                    lugar_escolhido_final = lugar_escolhido
                    lugar_escolhido_eh_aceitavel = True

        return lugar_escolhido_final

    def escolher_lugar_v3(self, grid):
        # usa o mesmo procemento que a funcao "escolher_lugar_v2"
        # a unica diferenca eh que, caso o agente esteja em um lugar
        # e caso n haja caminho entre o lugar atual e o lugar destino escolhido,
        # usa-se o A* para criar esse caminho, caso possivel, e armazena-lo na lista de caminhos deste lugar

        lugar_escolhido_eh_aceitavel = False
        lista_lugares_usaveis = grid.lista_lugares[:]
        lugar_onde_agente_esta = self.celula_grid.lugar

        if lugar_onde_agente_esta is not None:
            lista_lugares_usaveis.remove(lugar_onde_agente_esta)

        lugar_escolhido_final = lista_lugares_usaveis[0]

        while lugar_escolhido_eh_aceitavel is False:

            if len(lista_lugares_usaveis) == 0:
                # print("n ha lugares onde o agente possa ir")
                return None

            lugar_escolhido = funcoes.escolher_lugar_menor_e(self, lista_lugares_usaveis)
            # print("o agente {} escolheu o lugar {}".format(self.id, lugar_escolhido.id))

            if lugar_onde_agente_esta is not None:
                # print("o agente {} se encontra no lugar {} ".format(self.id, lugar_onde_agente_esta.id))

                checar_lugar_escolhido = lugar_onde_agente_esta.checar_existencia_lugar_na_lista_caminhos(lugar_escolhido)

                if checar_lugar_escolhido is False:
                    lugar_onde_agente_esta.add_caminho_lugar(lugar_escolhido, caminho_analisado=False)
                    lugar_escolhido.add_caminho_lugar(lugar_onde_agente_esta, caminho_analisado=False)

                for dicionario in lugar_onde_agente_esta.lista_caminhos:

                    if dicionario["destino"] == lugar_escolhido:

                        if dicionario["caminho_analisado"] is False:
                            # print("n foi checado se ha caminho entre os dois lugares")
                            resultados_a_star = grid.a_star_lugar_v2(lugar_onde_agente_esta, lugar_escolhido)

                            if resultados_a_star is None:
                                # print("n ha caminho entre os dois lugares")
                                lista_lugares_usaveis.remove(lugar_escolhido)
                                lugar_onde_agente_esta.atualizar_lista_caminhos(lugar_escolhido, False)
                                lugar_escolhido.atualizar_lista_caminhos(lugar_onde_agente_esta, False)
                                grid.atualizar_lista_caminhos_grid(lugar_onde_agente_esta.id, lugar_escolhido.id,
                                                                   possui_caminho=False)
                            else:
                                # print("ha caminho entre os dois lugares")
                                lugar_escolhido_final = lugar_escolhido
                                lugar_escolhido_eh_aceitavel = True
                                lista_refinada = resultados_a_star[1]
                                lugar_onde_agente_esta.atualizar_lista_caminhos(lugar_escolhido, True,
                                                                                caminho=lista_refinada)

                                caminho_volta = list(reversed(lista_refinada[:]))
                                lugar_escolhido.atualizar_lista_caminhos(lugar_onde_agente_esta, True,
                                                                         caminho=caminho_volta)

                                grid.atualizar_lista_caminhos_grid(lugar_onde_agente_esta.id, lugar_escolhido.id,
                                                                   possui_caminho=True, caminho=lista_refinada)
                        else:
                            # print("ja poi checado o caminho entre os dois lugares")
                            if dicionario["possui_caminho"] is True:
                                # print("o lugar {} ja possui caminho definido".format(lugar_escolhido.id))
                                lugar_escolhido_final = lugar_escolhido
                                lugar_escolhido_eh_aceitavel = True

                            if dicionario["possui_caminho"] is False:
                                # print("o lugar {} n possui caminho ate o agente".format(lugar_escolhido.id))
                                lista_lugares_usaveis.remove(lugar_escolhido)

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

    def escolher_lugar_v4(self, grid):
        # funciona da mesma forma que a funcao "escolher_lugar_v3"
        # o unico diferencial eh a retirada do parametro "caminho analisado" da lista caminhos
        # apos analisar o arquivo de caminhos, esse parametro eh redundante, desnecessario
        # para economizar memoria do arquivo caminhos, ele deve ser retirado mas a funcionalidade
        # da funcao deve ser a mesma, portanto a funcao deve ser adaptada

        lugar_escolhido_eh_aceitavel = False
        lista_lugares_usaveis = grid.lista_lugares[:]
        lugar_onde_agente_esta = self.celula_grid.lugar

        if lugar_onde_agente_esta is not None:
            lista_lugares_usaveis.remove(lugar_onde_agente_esta)

        lugar_escolhido_final = lista_lugares_usaveis[0]

        while lugar_escolhido_eh_aceitavel is False:

            if len(lista_lugares_usaveis) == 0:
                # print("n ha lugares onde o agente possa ir")
                return None

            # lugar_escolhido = funcoes.escolher_lugar_menor_e(self, lista_lugares_usaveis)
            lugar_escolhido = self.escolher_lugar_v5(lista_lugares_usaveis)
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

    def escolher_lugar_v5(self, lista_lugares, lista_pesos=(0.1, 0.1)):
        peso_dif_orientacao = lista_pesos[0]
        peso_distancia = lista_pesos[1]

        # é a lista que contém o peso de cada lugar ser sorteado
        # a ordem importa, peso da pos[0] é o peso do lugar na pos[0] na lista lugares
        lista_pesos = []

        for lugar in lista_lugares:
            dif_orientacao = abs(self.orientacao_atual - lugar.orientacao)
            coordenada_escolhida = lugar.achar_coordenada_principal(self.pos_grid)
            distancia = funcoes.obter_distancia_manhattan(coordenada_escolhida, self.pos_grid)

            fator_dif_orientacao = peso_dif_orientacao * dif_orientacao
            fator_distancia = peso_distancia * distancia

            expoente = fator_dif_orientacao + fator_distancia
            peso = math.exp(-expoente)
            lista_pesos.append(peso)

        soma_lista_pesos = sum(lista_pesos)
        # normalização
        lista_pesos_final = [i / soma_lista_pesos for i in lista_pesos]

        lugar_escolhido = funcoes.sorteio_com_pesos(lista_lugares, lista_pesos_final)[0]
        return lugar_escolhido

    def resgatar_estado_inicial(self):
        self.grid_x = self.grid_x_inicial
        self.grid_y = self.grid_y_inicial
        self.pos_grid = self.pos_grid_inicial

        self.pos_x = self.pos_x_inicial
        self.pos_y = self.pos_y_inicial
        self.pos = self.pos_inicial

        self.orientacao_latente = self.orientacao_latente_inicial
        self.orientacao_atual = self.orientacao_atual_inicial

    def draw(self, janela: pg.display):
        pg.draw.circle(janela, self.cor, self.pos, self.size)
