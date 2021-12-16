import cores
import funcoes
import random


class LugarV2:

    qnt_lugares = 0

    def __init__(self, grid, veio_de_arquivo=False, lista_arquivo=None, lista_coordenadas=None, cor=cores.verde, orientacao=0):

        if veio_de_arquivo is False:
            self.id = LugarV2.qnt_lugares
            LugarV2.qnt_lugares += 1

            self.lista_coordenadas = lista_coordenadas

            self.lista_celulas_grid = []
            self.atualizar_lista_celulas_grid(grid)

            self.lista_pontos_fronteira = []
            self.coordenada_principal = None
            self.celula_principal = None
            self.cell_size = grid.cell_size
            self.cor = cor
            self.cor_original = cor
            self.orientacao = orientacao
            self.orientacao_inicial = orientacao
            self.lista_caminhos = []
            self.ja_teve_caminhos_atualizados = False
            self.display_caminhos = False
            self.lista_agentes_presentes = []

            self.lista_celulas_grid_acessiveis = []
            self.display_celulas_acessiveis = False

        else:
            self.id = lista_arquivo[0]
            self.lista_coordenadas = lista_arquivo[1]
            self.cor = lista_arquivo[2]
            self.cor_original = lista_arquivo[2]
            self.orientacao = lista_arquivo[3]
            self.orientacao_inicial = lista_arquivo[3]

            self.lista_celulas_grid = []
            self.atualizar_lista_celulas_grid(grid)

            self.lista_pontos_fronteira = []
            self.coordenada_principal = None
            self.celula_principal = None
            self.cell_size = grid.cell_size
            self.lista_caminhos = []
            self.ja_teve_caminhos_atualizados = False
            self.display_caminhos = False
            self.lista_agentes_presentes = []

            self.lista_celulas_grid_acessiveis = []
            self.display_celulas_acessiveis = False

    def atualizar_lista_celulas_grid(self, grid):
        for coordenada in self.lista_coordenadas:
            x = coordenada[0]
            y = coordenada[1]
            celula_lugar = grid.matriz_celulas[y][x]
            celula_lugar.andavel = False
            celula_lugar.lugar = self
            grid.lista_celulas_ocupadas.append(celula_lugar)
            self.lista_celulas_grid.append(celula_lugar)

    def tornar_lugar_andavel(self):
        for celula in self.lista_celulas_grid:
            celula.andavel = True

    def tornar_lugar_n_andavel(self):
        for celula in self.lista_celulas_grid:
            celula.andavel = False

    def achar_coordenada_principal(self, ponto_referencia):

        menor_distancia = funcoes.distancia_pitagorica(ponto_referencia, self.lista_coordenadas[0])
        coordenada_escolhida = self.lista_coordenadas[0]

        for coordenada in self.lista_coordenadas:

            distancia_analisada = funcoes.distancia_pitagorica(ponto_referencia, coordenada)

            if distancia_analisada < menor_distancia:
                menor_distancia = distancia_analisada
                coordenada_escolhida = coordenada

        self.coordenada_principal = coordenada_escolhida
        return coordenada_escolhida

    def achar_coordenada_principal_v2(self, ponto_referencia):

        # faz a mesma coisa que a função achar_coordenada_principal, mas usa a distancia manhattan

        """
        :param ponto_referencia: coordenada do agente
        :return: coordenda mais proxima do agente
        """

        menor_distancia = funcoes.obter_distancia_manhattan(ponto_referencia, self.lista_coordenadas[0])
        coordenada_escolhida = self.lista_coordenadas[0]

        for coordenada in self.lista_coordenadas:

            distancia_analisada = funcoes.obter_distancia_manhattan(ponto_referencia, coordenada)

            if distancia_analisada < menor_distancia:
                menor_distancia = distancia_analisada
                coordenada_escolhida = coordenada

        self.coordenada_principal = coordenada_escolhida
        return coordenada_escolhida

    def add_caminho_lugar(self, lugar, caminho_analisado=True, possui_caminho=True, lista_caminho=None):

        if caminho_analisado is False:
            novo_caminho = {'destino': lugar, 'caminho_analisado': False}
            self.lista_caminhos.append(novo_caminho)
        else:
            if possui_caminho is True:
                novo_caminho = {'destino': lugar, 'caminho_analisado': True, "possui_caminho": True,
                                'caminho': lista_caminho}
                self.lista_caminhos.append(novo_caminho)
            else:
                novo_caminho = {'destino': lugar, 'caminho_analisado': True, "possui_caminho": False}
                self.lista_caminhos.append(novo_caminho)

    def add_caminho_lugar_v2(self, lugar_destino, possui_caminho, caminho=None):
        # faz a mesma coisa que a a funcao "add_caminho_lugar"
        # apenas retira a chave "caminho analisado" visto que ela ficou obsoleta

        if possui_caminho is True:
            novo_dicionario = {'destino': lugar_destino, "possui_caminho": True, 'caminho': caminho}
            self.lista_caminhos.append(novo_dicionario)
        else:
            novo_dicionario = {'destino': lugar_destino, "possui_caminho": False}
            self.lista_caminhos.append(novo_dicionario)

    def atualizar_lista_caminhos(self, lugar_destino, possui_caminho, caminho=None):

        for dicionario in self.lista_caminhos:
            if dicionario["destino"] == lugar_destino:
                dicionario["caminho_analisado"] = True
                if possui_caminho is False:
                    dicionario["possui_caminho"] = False
                else:
                    dicionario["possui_caminho"] = True
                    dicionario["caminho"] = caminho
                # print("lista atualizada!\n")

    def contaminacao_lugar(self, pesos, mudar_cor=True, grid=None):
        peso_lugar = pesos[0]
        peso_agentes = pesos[1]

        soma_pesos = sum(pesos)
        lista_orientacao_agentes = [i.orientacao_latente for i in self.lista_agentes_presentes]

        soma_orientacoes_agentes = sum(lista_orientacao_agentes)
        qnt_agentes = len(lista_orientacao_agentes)

        media_orientacao_agentes = soma_orientacoes_agentes // qnt_agentes

        nova_orientacao = (peso_lugar*self.orientacao + peso_agentes*media_orientacao_agentes) // soma_pesos
        self.orientacao = nova_orientacao

        if mudar_cor is True:
            self.cor = funcoes.update_orientacao_cor(grid.dict_orientacoes_cores, self.orientacao, 1000)

    def resgatar_estado_inicial(self):
        self.orientacao = self.orientacao_inicial

    def achar_pontos_fronteiras(self, grid):

        lista_pontos_fronteira = []

        lista_celulas_analisadas = self.lista_celulas_grid[:]

        for celula in lista_celulas_analisadas:

            print("\n")
            print("a celula eh: \n", celula.pos_grid)

            lista_vizinhos = grid.obter_nodulos_vizinhos(celula, excluir_obstaculos=False)
            for vizinho in lista_vizinhos:
                print("vizinho eh: ", vizinho.pos_grid)

            vizinho_direita = None
            vizinho_esquerda = None
            vizinho_cima = None
            vizinho_baixo = None
            vizinho_direita_cima = None
            vizinho_direita_baixo = None
            vizinho_esquerda_cima = None
            vizinho_esquerda_baixo = None

            vizinho_direita_aceitavel = False
            vizinho_esquerda_aceitavel = False
            vizinho_cima_aceitavel = False
            vizinho_baixo_aceitavel = False
            vizinho_direita_cima_aceitavel = False
            vizinho_direita_baixo_aceitavel = False
            vizinho_esquerda_cima_aceitavel = False
            vizinho_esquerda_baixo_aceitavel = False

            for vizinho in lista_vizinhos:

                x_cel, y_cel = celula.grid_x, celula.grid_y
                x_viz, y_viz = vizinho.grid_x, vizinho.grid_y

                dx = x_viz - x_cel
                dy = y_viz - y_cel

                print("celula = ", celula.pos_grid)
                print("vizinho = ", vizinho.pos_grid)
                print("dx = ", dx)
                print("dy = ", dy)

                if dx == 0:
                    if dy > 0:
                        vizinho_baixo = vizinho
                    if dy < 0:
                        vizinho_cima = vizinho

                if dx > 0:
                    if dy == 0:
                        vizinho_direita = vizinho
                    if dy > 0:
                        vizinho_direita_baixo = vizinho
                    if dy < 0:
                        vizinho_direita_cima = vizinho

                if dx < 0:
                    if dy == 0:
                        vizinho_esquerda = vizinho
                    if dy > 0:
                        vizinho_esquerda_baixo = vizinho
                    if dy < 0:
                        vizinho_esquerda_cima = vizinho

            if vizinho_direita is None or vizinho_direita not in self.lista_celulas_grid:
                vizinho_direita_aceitavel = True

            if vizinho_esquerda is None or vizinho_esquerda not in self.lista_celulas_grid:
                vizinho_esquerda_aceitavel = True

            if vizinho_cima is None or vizinho_cima not in self.lista_celulas_grid:
                vizinho_cima_aceitavel = True

            if vizinho_baixo is None or vizinho_baixo not in self.lista_celulas_grid:
                vizinho_baixo_aceitavel = True

            if vizinho_direita_cima is None or vizinho_direita_cima not in self.lista_celulas_grid:
                vizinho_direita_cima_aceitavel = True

            if vizinho_direita_baixo is None or vizinho_direita_baixo not in self.lista_celulas_grid:
                vizinho_direita_baixo_aceitavel = True

            if vizinho_esquerda_cima is None or vizinho_esquerda_cima not in self.lista_celulas_grid:
                vizinho_esquerda_cima_aceitavel = True

            if vizinho_esquerda_baixo is None or vizinho_esquerda_baixo not in self.lista_celulas_grid:
                vizinho_esquerda_baixo_aceitavel = True

            print("vizinho direita: ", vizinho_direita)
            print("vizinho esquerda: ", vizinho_esquerda)
            print("vizinho cima: ", vizinho_cima)
            print("vizinho baixo: ", vizinho_baixo)
            print("vizinho direita cima: ", vizinho_direita_cima)
            print("vizinho direita baixo: ", vizinho_direita_baixo)
            print("vizinho esquerda cima: ", vizinho_esquerda_cima)
            print("vizinho esquerda baixo: ", vizinho_esquerda_baixo)
            print("--------------------------------------------------")

            ponto_superior_esquerdo = (celula.grid_x * celula.cell_size, celula.grid_y * celula.cell_size)
            ponto_superior_direito = (celula.grid_x * celula.cell_size + celula.cell_size,
                                      celula.grid_y * celula.cell_size)
            ponto_inferior_esquerdo = (celula.grid_x * celula.cell_size,
                                       celula.grid_y * celula.cell_size + celula.cell_size)
            ponto_inferior_direito = (celula.grid_x * celula.cell_size + celula.cell_size,
                                      celula.grid_y * celula.cell_size + celula.cell_size)

            print("ponto superior esquerdo: ", ponto_superior_esquerdo)
            print("ponto superior direito: ", ponto_superior_direito)
            print("ponto inferior esquerdo: ", ponto_inferior_esquerdo)
            print("ponto inferior direito: ", ponto_inferior_direito)

            # testando o ponto superior esquerdo
            if vizinho_cima_aceitavel is True:
                if vizinho_esquerda_aceitavel is True:
                    # if vizinho_esquerda_cima_aceitavel is True:
                    if ponto_superior_esquerdo not in lista_pontos_fronteira:
                        lista_pontos_fronteira.append(ponto_superior_esquerdo)

            # if vizinho_cima_aceitavel is False:
            #     if vizinho_esquerda_aceitavel is False:
            #         if vizinho_esquerda_cima_aceitavel is True:
            #             if ponto_superior_esquerdo not in lista_pontos_fronteira:
            #                 lista_pontos_fronteira.append(ponto_superior_esquerdo)

            # if vizinho_esquerda_cima_aceitavel is True:
            #     if ponto_superior_esquerdo not in lista_pontos_fronteira:
            #         lista_pontos_fronteira.append(ponto_superior_esquerdo)

            # testando o ponto superior direito
            if vizinho_cima_aceitavel is True:
                if vizinho_direita_aceitavel is True:
                    # if vizinho_direita_cima_aceitavel is True:
                    if ponto_inferior_direito not in lista_pontos_fronteira:
                        lista_pontos_fronteira.append(ponto_superior_direito)

            # if vizinho_cima_aceitavel is False:
            #     if vizinho_direita_aceitavel is False:
            #         if vizinho_direita_cima_aceitavel is True:
            #             if ponto_inferior_direito not in lista_pontos_fronteira:
            #                 lista_pontos_fronteira.append(ponto_superior_direito)

            # if vizinho_direita_cima_aceitavel is True:
            #     if ponto_inferior_direito not in lista_pontos_fronteira:
            #         lista_pontos_fronteira.append(ponto_superior_direito)

            # testando o ponto inferior esquerdo
            if vizinho_baixo_aceitavel is True:
                if vizinho_esquerda_aceitavel is True:
                    # if vizinho_esquerda_baixo_aceitavel is True:
                    if ponto_inferior_esquerdo not in lista_pontos_fronteira:
                        lista_pontos_fronteira.append(ponto_inferior_esquerdo)

            # if vizinho_baixo_aceitavel is False:
            #     if vizinho_esquerda_aceitavel is False:
            #         if vizinho_esquerda_baixo_aceitavel is True:
            #             if ponto_inferior_esquerdo not in lista_pontos_fronteira:
            #                 lista_pontos_fronteira.append(ponto_inferior_esquerdo)

            # if vizinho_esquerda_baixo_aceitavel is True:
            #     if ponto_inferior_esquerdo not in lista_pontos_fronteira:
            #         lista_pontos_fronteira.append(ponto_inferior_esquerdo)

            # testando o ponto inferior direito
            if vizinho_baixo_aceitavel is True:
                if vizinho_direita_aceitavel is True:
                    # if vizinho_direita_baixo_aceitavel is True:
                    if ponto_inferior_direito not in lista_pontos_fronteira:
                        lista_pontos_fronteira.append(ponto_inferior_direito)

            # if vizinho_baixo_aceitavel is False:
            #     if vizinho_direita_aceitavel is False:
            #         if vizinho_direita_baixo_aceitavel is True:
            #             if ponto_inferior_direito not in lista_pontos_fronteira:
            #                 lista_pontos_fronteira.append(ponto_inferior_direito)

            # if vizinho_direita_baixo_aceitavel is True:
            #     if ponto_inferior_direito not in lista_pontos_fronteira:
            #         lista_pontos_fronteira.append(ponto_inferior_direito)

        self.lista_pontos_fronteira = lista_pontos_fronteira

    def achar_celulas_acessiveis(self, grid):

        celula_lugar_inicial_escolhida = None
        lista_possiveis_celulas_lugar = self.lista_celulas_grid[:]
        celula_lugar_inicial_aceitavel = False

        while celula_lugar_inicial_aceitavel is False:

            celula_lugar_inicial_temp = random.choice(lista_possiveis_celulas_lugar)
            lista_vizinhos = grid.obter_nodulos_vizinhos(celula_lugar_inicial_temp)

            if len(lista_vizinhos) > 0:
                celula_lugar_inicial_escolhida = celula_lugar_inicial_temp
                celula_lugar_inicial_aceitavel = True
            else:
                lista_possiveis_celulas_lugar.remove(celula_lugar_inicial_temp)

        lista_aberta = []
        lista_fechada = []

        lista_aberta.append(celula_lugar_inicial_escolhida)

        while len(lista_aberta) > 0:

            celula_analisada = lista_aberta.pop(0)
            lista_fechada.append(celula_analisada)
            # print("a celula analisada eh: ", celula_analisada.pos_grid)

            lista_vizinhos = grid.obter_nodulos_vizinhos(celula_analisada)

            for vizinho in lista_vizinhos:
                # print("o vizinho eh: ", vizinho.pos_grid)
                if vizinho in lista_aberta or vizinho in lista_fechada:
                    # print("o vizinho ja foi analisado")
                    continue
                else:
                    lista_aberta.append(vizinho)
                    # print("o vizinho n foi analisado ainda")

        self.lista_celulas_grid_acessiveis = lista_fechada

    def checar_existencia_lugar_na_lista_caminhos(self, lugar_destino):

        lugar_ja_esta_na_lista = False

        for dicionario in self.lista_caminhos:
            if dicionario["destino"] == lugar_destino:
                lugar_ja_esta_na_lista = True
                break

        return lugar_ja_esta_na_lista
