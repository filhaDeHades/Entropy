from numpy.core.fromnumeric import size
from Modelo_fast.ClasseCelulaGridV2Fast import CelulaGridV2Fast
from Modelo_fast.ClasseAgenteV2Fast import AgenteV2Fast
from Modelo_fast.ClasseLugarV2Fast import LugarV2Fast
import Modelo_fast.funcoes_fast as fst
import pandas as pd
import numpy as np
import random
import math
import cores


class GridV2Fast:

    def __init__(self, qnt_linhas, qnt_colunas, qnt_agentes, qnt_lugares, matriz_layout=None, 
                qnt_orientacoes=11, range_possiveis_orientacoes=(0, 1100, 100)):
        self.qnt_linhas = qnt_linhas
        self.qnt_colunas = qnt_colunas
        self.qnt_agentes = qnt_agentes
        self.qnt_lugares = qnt_lugares
        self.range_possiveis_orientacoes = range_possiveis_orientacoes

        self.array_celulas_grid = []

        if matriz_layout is None:
            self.obter_array_celulas_grid_manual()
        else:
            self.obter_array_celulas_grid_definido(matriz_layout)

        self.array_agentes = [] 
        self.gerar_agentes_aleatorios_v3(self.qnt_agentes)
        self.array_lugares = []
        self.gerar_lugares_aleatorios_v3()
        # self.gerar_lugares_aleatorios_v4(self.qnt_lugares)

        self.lista_caminhos = []

        self.qnt_orientacoes = qnt_orientacoes
        self.dict_orientacoes_cores = {}
        self.obter_dict_orientacoes_cores()

        self.qnt_caminhos_resgatados_arquivo = 0

    def obter_dict_orientacoes_cores(self):
        self.dict_orientacoes_cores = fst.converter_orientacao_para_cor_v3(self.qnt_orientacoes)

    def obter_array_celulas_grid_manual(self):
        lista_celulas_temp = []

        for y in range(self.qnt_linhas):
            for x in range(self.qnt_colunas):
                nova_celula = CelulaGridV2Fast(x, y)
                lista_celulas_temp.append(nova_celula)

        array_final = np.array(lista_celulas_temp)
        self.array_celulas_grid = array_final

    def obter_array_celulas_grid_definido(self, matriz_layout):

        lista_celulas_temp = []

        for y in range(self.qnt_linhas):
            for x in range(self.qnt_colunas):

                if matriz_layout[y][x] == 1: # É LUGAR
                    nova_celula = CelulaGridV2Fast(x, y, andavel=False)
                    lista_celulas_temp.append(nova_celula)
                else: # É ESPAÇO VAZIO
                    nova_celula = CelulaGridV2Fast(x, y, andavel=True)
                    lista_celulas_temp.append(nova_celula)

        array_final = np.array(lista_celulas_temp)

        self.array_celulas_grid = array_final

    def obter_celula_array_grid(self, x, y):
        pos_array = y * self.qnt_colunas + x
        celula = self.array_celulas_grid[pos_array]
        return celula

    def gerar_agentes_aleatorios_v3(self, qnt_agentes):

        lista_agentes = []

        lista_celulas_livres = [celula for celula in self.array_celulas_grid if celula.andavel is True]
        qnt_cel_livres = len(lista_celulas_livres)

        for agente in range(qnt_agentes):
            pos_aleatoria = random.randint(0, qnt_cel_livres - 1)
            celula_inicial = lista_celulas_livres.pop(pos_aleatoria)
            qnt_cel_livres -= 1

            x_inicial = celula_inicial.grid_x
            y_inicial = celula_inicial.grid_y

            orientacao_incial = self.range_possiveis_orientacoes[0]
            orientacao_final = self.range_possiveis_orientacoes[1]
            orientacao_escolhida = random.randint(orientacao_incial, orientacao_final)

            novo_agente = AgenteV2Fast(self, x_inicial, y_inicial, orientacao_latente=orientacao_escolhida,
                                       orientacao_atual=orientacao_escolhida)

            lista_agentes.append(novo_agente)

        array_agentes = np.array(lista_agentes)
        self.array_agentes = array_agentes

    def gerar_lugares_aleatorios_v2(self, qnt_lugares, ajustar_tam_lugar=True, fracao_espaco_vazio=0.5, tamanho_max_lugar=5, sem_cor_repetida=False, sem_orientacao_repetida=False):

        tamanho_maximo_lugar = tamanho_max_lugar

        if ajustar_tam_lugar == True:
            tam_total_grid = self.qnt_linhas * self.qnt_colunas * fracao_espaco_vazio
            tamanho_maximo_lugar = tam_total_grid // self.qnt_lugares
        
        print("tamanho maximo do lugar: ", tamanho_maximo_lugar)

        lista_lugares = []
        lista_cores = cores.lista_cores_coloridas[:]
        lista_orientacoes = list(self.range_possiveis_orientacoes)

        for lugar in range(qnt_lugares):
            celula_aceitavel = False
            celula_escolhida = None

            while celula_aceitavel is False:                        # sorteando celula inicial que n seja obstaculo
                x = random.randint(0, self.qnt_colunas - 1)
                y = random.randint(0, self.qnt_linhas - 1)
                celula_escolhida_temp = self.obter_celula_array_grid(x, y)

                if celula_escolhida_temp.andavel is True:
                    celula_escolhida = celula_escolhida_temp
                    celula_aceitavel = True

            lista_celulas_escolhidas = []
            tamanho_lugar_temp = 0

            while tamanho_lugar_temp < tamanho_maximo_lugar:           # sorteando as celulas vizinhas para formar o lugar
                lista_celulas_escolhidas.append(celula_escolhida)
                lista_vizinhos = self.obter_nodulos_vizinhos(celula_escolhida)
                set_vizinhos = None
                set_vizinhos_eh_usavel = False

                while set_vizinhos_eh_usavel is False:
                    set_vizinhos_temp = set(lista_vizinhos) - set(lista_celulas_escolhidas)
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

            lugar_novo = LugarV2Fast(self, veio_de_arquivo=False, lista_coordenadas=lista_coordenadas_escolhidas,
                                     cor=cor_escolhida, orientacao=orientacao_escolhida)

            lista_lugares.append(lugar_novo)
            print("lugar {} criado".format(lugar_novo.id))

        self.array_lugares = np.array(lista_lugares)

    def gerar_lugares_aleatorios_v3(self):

        # nessa funcao cada lugar tem exatamente 1 quadrado
        
        lista_lugares = []
        lista_celulas_ocupadas = [celula for celula in self.array_celulas_grid if celula.andavel is False]

        orientacao_inicial = self.range_possiveis_orientacoes[0]
        orientacao_final = self.range_possiveis_orientacoes[1]

        for celula in lista_celulas_ocupadas:
            lista_coordenadas = [celula.pos_grid]
            orientacao = random.randint(orientacao_inicial, orientacao_final)
            novo_lugar = LugarV2Fast(self, lista_coordenadas=lista_coordenadas, orientacao=orientacao)
            lista_lugares.append(novo_lugar)
        
        # for celula in self.array_celulas_grid:  #No momento esse FOR transforma todas as células em lugares
        #     lista_coordenadas = [celula.pos_grid]
        #     orientacao = random.randint(orientacao_inicial, orientacao_final)
        #     novo_lugar = LugarV2Fast(self, lista_coordenadas=lista_coordenadas, orientacao=orientacao)
        #     lista_lugares.append(novo_lugar)

        self.array_lugares = np.array(lista_lugares)

    def gerar_lugares_aleatorios_v4(self, qnt_lugares, ajustar_tam_lugar=True, fracao_espaco_vazio=0.5, tamanho_max_lugar=5, sem_cor_repetida=False, sem_orientacao_repetida=False):
        tamanho_maximo_lugar = tamanho_max_lugar

        if ajustar_tam_lugar == True:
            tam_total_grid = self.qnt_linhas * self.qnt_colunas * fracao_espaco_vazio
            tamanho_maximo_lugar = tam_total_grid // self.qnt_lugares
        
        # print("tamanho maximo do lugar: ", tamanho_maximo_lugar)

        lista_lugares = []
        lista_cores = cores.lista_cores_coloridas[:]
        lista_orientacoes = list(self.range_possiveis_orientacoes)
        lista_celulas_livres = [celula for celula in self.array_celulas_grid if celula.andavel is True]
        # print("qnt celulas livres: ", len(lista_celulas_livres))

        for lugar in range(qnt_lugares):

            pos_aleatoria = random.randint(0, len(lista_celulas_livres))
            celula_inicial = lista_celulas_livres.pop(pos_aleatoria)

            lista_celulas_escolhidas = [celula_inicial]
            tamanho_lugar_atual = 1

            indice_celula_referencia = 0
            
            # fazendo o loop e obtendo a lista de coordenas para o lugar 
            while (tamanho_lugar_atual < tamanho_maximo_lugar) and (indice_celula_referencia < len(lista_celulas_escolhidas)):
                
                celula_referencial = lista_celulas_escolhidas[indice_celula_referencia]
                lista_vizinhos = self.obter_nodulos_vizinhos(celula_referencial)
                
                # retirando da lista de vizinhos as celulas q ja foram adicionadas
                # na lista de celulas para lista de coordendas do lugar
                lista_vizinhos = list(set(lista_vizinhos) - set(lista_celulas_escolhidas))

                if len(lista_vizinhos) != 0:
                    vizinho = random.choice(lista_vizinhos)
                    lista_celulas_escolhidas.append(vizinho)
                    
                    # buscando o vizinho para retirar da lista das celulas livres
                    for i in range(len(lista_celulas_livres)):
                        if (vizinho.pos_grid == lista_celulas_livres[i].pos_grid):
                            lista_celulas_livres.pop(i)
                            break
                    
                    tamanho_lugar_atual += 1
                else:
                    indice_celula_referencia += 1


            # obtendo a lista de coordenadas
            lista_coordenadas = [celula.pos_grid for celula in lista_celulas_escolhidas]

            # obtendo orientacao do lugar
            orientacao_inicial = self.range_possiveis_orientacoes[0]
            orientacao_final = self.range_possiveis_orientacoes[1]
            orientacao = random.randint(orientacao_inicial, orientacao_final)

            novo_lugar = LugarV2Fast(self, lista_coordenadas=lista_coordenadas, orientacao=orientacao)
            lista_lugares.append(novo_lugar)
            #print("lugar {} criado!".format(novo_lugar.id))
            #print("o lugar feito tem tamanho: ", len(lista_celulas_escolhidas))
            # print("qnt de celulas livres: ", len(lista_celulas_livres))
            print("-------------\n\n")

        self.array_lugares = np.array(lista_lugares)


    # testando se os lugares tem todos coordenadas diferentes
    # delete me
    def teste_lugares_certo(self):
        
        lista_lugares = list(self.array_lugares)

        while len(lista_lugares) > 0:

            lugar_analisado = lista_lugares.pop(0)
            lista_coordenadas1 = list(lugar_analisado.array_coordenadas)

            for lugar in lista_lugares:
                lista_coordenadas2 = list(lugar.array_coordenadas)
                
                for c1 in lista_coordenadas1:
                    for c2 in lista_coordenadas2:
                        if c1[0] == c2[0] and c1[1] == c2[1]:
                            print("erro")
                            print("coordenada igual: ", c1)
                            print("lugar: ", lugar_analisado.id)
                            print("lugar: ", lugar.id)
                            return
            
            print("lugar {}: ok".format(lugar_analisado.id))
        
    
    def atualizar_status_andavel_celula(self, x, y, status):
        pos_array = y * self.qnt_colunas + x
        self.array_celulas_grid[pos_array].andavel = status

    def obter_lugar_pelo_id(self, num_id):
        for lugar in self.array_lugares:
            if lugar.id == num_id:
                return lugar

    def resgatar_lugares_arquivo(self, nome_arquivo_lugares):
        lista_lugares = fst.arquivo_csv_para_lista(nome_arquivo_lugares)
        print(lista_lugares)
        for lugar in lista_lugares:
            lugar_novo = LugarV2Fast(self, veio_de_arquivo=True, lista_arquivo=lugar)
            self.array_lugares = np.append(self.array_lugares, lugar_novo)

    def resgatar_caminhos_arquivo(self, nome_arquivo_caminhos):

        matriz_temp = fst.arquivo_csv_para_lista(nome_arquivo_caminhos)
        matriz_final = []

        for linha in matriz_temp:
            if len(linha) == 3:
                lista_chaves_sem_caminho = ["lugar_1", "lugar_2", "possui_caminho"]
                dicionario = fst.transformar_duas_listas_em_dict(lista_chaves_sem_caminho, linha)
                matriz_final.append(dicionario)
            if len(linha) == 4:
                lista_chaves_com_caminho = ["lugar_1", "lugar_2", "possui_caminho", "caminho"]
                dicionario = fst.transformar_duas_listas_em_dict(lista_chaves_com_caminho, linha)
                matriz_final.append(dicionario)

        self.lista_caminhos = matriz_final
        self.qnt_caminhos_resgatados_arquivo = len(self.lista_caminhos)
        # print("{} caminhos foram resgatados!".format(self.qnt_caminhos_resgatados_arquivo))

    def restaurar_caminhos_entre_lugares(self):
        # passa os caminhos da lista de caminhos do grid para a lista de caminhos dos lugares

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

    def mostrar_qnt_caminhos_lugares(self):
        for lugar in self.array_lugares:
            qnt_caminhos_lugar = len(lugar.lista_caminhos)
            print("o lugar {} possui {} caminhos ja salvos!".format(lugar.id, qnt_caminhos_lugar))

    def criar_arquivo_caminhos(self, nome_arquivo):
        lista_final = [[j for j in i.values()] for i in self.lista_caminhos]
        fst.lista_para_arquivo_csv(lista_final, nome_arquivo)

    def salvar_novos_caminhos_arquivo(self, nome_arquivo):
        novos_caminhos_temp = self.lista_caminhos[self.qnt_caminhos_resgatados_arquivo:]
        novos_caminhos = [[j for j in i.values()] for i in novos_caminhos_temp]
        fst.lista_para_arquivo_csv(novos_caminhos, nome_arquivo, tipo_operacao="a")
        print("{} novos caminhos foram salvos no arquivo: {}".format(len(novos_caminhos), nome_arquivo))

    def criar_ou_atualizar_arquivo_caminhos(self, nome_arquivo_caminhos):
        # junta as funcoes "salvar_caminhos_arquivo" e "salvar_novos_caminhos_arquivo"
        # primeiro, testa-se a existencia do arquivo de caminhos
        # caso n exista, a funcao "salvar_caminhos_arquivo" eh executada
        # caso contario, a funcao "salvar_novos_caminhos_arquivo" eh executada

        existencia_arquivo_caminhos = fst.checar_existencia_arquivo(nome_arquivo_caminhos)

        if existencia_arquivo_caminhos is False:
            self.criar_arquivo_caminhos(nome_arquivo_caminhos)
        else:
            self.salvar_novos_caminhos_arquivo(nome_arquivo_caminhos)

    def obter_dict_ocorrencia_orientacoes(self):

        lista_orientacoes_agentes = [math.ceil(agente.orientacao_atual / 100) * 100 for agente in self.array_agentes]
        lista_orientacoes_possiveis = list(range(0, 1100, 100))
        dict_ocorrencia_orientacoes = fst.contagem_ocorrencia_elementos_com_referencial(lista_orientacoes_agentes,
                                                                                        lista_orientacoes_possiveis)
        return dict_ocorrencia_orientacoes

    def calcular_entropia_agentes(self):

        lista_orientacoes_agentes = [math.ceil(agente.orientacao_latente / 100) * 100 for agente in self.array_agentes]
        dict_orientacoes_e_ocorrencias = fst.obter_dict_contagem_elementos_repetidos_v2(lista_orientacoes_agentes)
        qnt_total_agentes = len(self.array_agentes)
        frenquencia_orientacoes = {key: (value / qnt_total_agentes) for key, value in dict_orientacoes_e_ocorrencias.items()}

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

    def calcular_entropia_lugares(self):

        lista_orientacoes_lugares = [math.ceil(lugar.orientacao / 100) * 100 for lugar in self.array_lugares]
        dict_orientacoes_e_ocorrencias = fst.obter_dict_contagem_elementos_repetidos_v2(lista_orientacoes_lugares)
        qnt_total_lugares = len(self.array_lugares)
        frenquencia_orientacoes = {key: (value / qnt_total_lugares) for key, value in
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

    def calcular_entropia_geral(self):

        lista_orientacoes_agentes = [math.ceil(agente.orientacao_latente / 100) * 100 for agente in self.array_agentes]
        lista_orientacoes_lugares = [math.ceil(lugar.orientacao / 100) * 100 for lugar in self.array_lugares]
        lista_orientacoes_geral = lista_orientacoes_agentes + lista_orientacoes_lugares

        dict_orientacoes_e_ocorrencias = fst.obter_dict_contagem_elementos_repetidos_v2(lista_orientacoes_geral)
        qnt_total = len(self.array_lugares) + len(self.array_lugares)
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

                            celula_analisada = self.obter_celula_array_grid(pos_x, pos_y)

                            if excluir_obstaculos is True:
                                if celula_analisada.andavel is True:
                                    lista_vizinhos.append(celula_analisada)
                            else:
                                lista_vizinhos.append(celula_analisada)
        return lista_vizinhos

    def a_star_lugar(self, nodulo_inicial, lugar, retornar_procura_caminho=False):

        lugar.coordenada_principal = lugar.achar_coordenada_principal(nodulo_inicial.pos_grid)
        lugar.tornar_lugar_andavel()

        nodulo_inicial.g = 0
        nodulo_inicial.atualizar_h(lugar.coordenada_principal)
        nodulo_inicial.atualizar_f()
        nodulo_inicial.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(nodulo_inicial)

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]  # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual in lugar.array_celulas_grid:

                lista_refinada = []
                nodulo_regresso = None

                for nodulo in lugar.array_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != nodulo_inicial:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_final = {"lista_refinada": lista_refinada}

                celulas_para_serem_restauradas = fst.transformar_duas_listas_em_set(lista_aberta, lista_fechada)
                self.restaurar_mudancas_feitas_pelo_a_star(celulas_para_serem_restauradas, lugar1=lugar)

                if retornar_procura_caminho is True:
                    lista_bruta = [i.pos_grid for i in lista_fechada]
                    lista_final["lista_bruta"] = lista_bruta

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g()
                    vizinho.atualizar_h(lugar.coordenada_principal)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = fst.obter_distancia(nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)
        return None

    def a_star_lugar_v2(self, lugar1, lugar2, retornar_procura_caminho=False):

        lugar1.tornar_lugar_andavel()
        lugar2.tornar_lugar_andavel()
        self.encontrar_celulas_principais(lugar1, lugar2)

        lugar1.coordenada_principal.g = 0
        lugar1.coordenada_principal.atualizar_h(lugar2.coordenada_principal.pos_grid)
        lugar1.coordenada_principal.atualizar_f()
        lugar1.coordenada_principal.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(lugar1.coordenada_principal)

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]  # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual in lugar2.array_celulas_grid:

                lista_refinada = []

                nodulo_regresso = None

                for nodulo in lugar2.array_celulas_grid:
                    if nodulo_atual == nodulo:
                        nodulo_regresso = nodulo

                while nodulo_regresso != lugar1.coordenada_principal:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_refinada.insert(0, lugar1.coordenada_principal.pos_grid)

                lista_final = {"lista_refinada": lista_refinada}

                lugar1.tornar_lugar_n_andavel()
                lugar2.tornar_lugar_n_andavel()

                if retornar_procura_caminho is True:
                    lista_bruta = [i.pos_grid for i in lista_fechada]
                    lista_final["lista_bruta"] = lista_bruta

                celulas_para_serem_restauradas = fst.transformar_duas_listas_em_set(lista_aberta, lista_fechada)
                self.restaurar_mudancas_feitas_pelo_a_star(celulas_para_serem_restauradas, lugar1=lugar1, lugar2=lugar2)

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g()
                    vizinho.atualizar_h(lugar2.coordenada_principal.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = fst.obter_distancia(nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)
        return None

    @staticmethod
    def encontrar_celulas_principais(lugar1, lugar2):

        # funcao defina a "celula principal" dos dois lugares
        # assim, as celulas principais podem ser usadas no A* para achar a menor distancia entre os dois lugares

        menor_distancia = None
        par_de_celulas = (0, 0)

        for celula1 in lugar1.array_celulas_grid:
            for celula2 in lugar2.array_celulas_grid:

                par_celulas_atual = (celula1, celula2)
                distancia_atual = fst.obter_distancia_euclidiana(celula1.pos_grid, celula2.pos_grid)

                if menor_distancia is None:
                    menor_distancia = distancia_atual
                    par_de_celulas = par_celulas_atual

                else:
                    if distancia_atual < menor_distancia:
                        menor_distancia = distancia_atual
                        par_de_celulas = par_celulas_atual

        lugar1.coordenada_principal = par_de_celulas[0]
        lugar2.coordenada_principal = par_de_celulas[1]

    def restaurar_mudancas_feitas_pelo_a_star(self, lista_celulas, lugar1=None, lugar2=None):
        # reliaza todas as restauraçoes necessarias
        # restaura o estado inicial das celulas
        # restaura o estado inicial do(s) lugar(es)

        self.restaurar_estado_inicial_celulas_v2(lista_celulas)

        if lugar1 is not None:
            lugar1.restaurar_mudancas_a_star()

        if lugar2 is not None:
            lugar2.restaurar_mudancas_a_star()

    @staticmethod
    def restaurar_estado_inicial_celulas_v2(lista_celulas):

        for celula in lista_celulas:
            celula.parente = None
            celula.ja_foi_visitado = False
            celula.ja_foi_analisado = False
            celula.g = 0
            celula.h = 0
            celula.f = 0

    def add_caminho_lista_caminhos_grid_v2(self, lugar_1_id, lugar_2_id, possui_caminho, caminho=None):
        if possui_caminho is False:
            novo_dicionario = {"lugar_1": lugar_1_id, "lugar_2": lugar_2_id, "possui_caminho": False}
            self.lista_caminhos.append(novo_dicionario)
        else:
            novo_dicionario = {"lugar_1": lugar_1_id, "lugar_2": lugar_2_id, "possui_caminho": True, "caminho": caminho}
            self.lista_caminhos.append(novo_dicionario)

    def salvar_lugares_arquivo(self, nome_arquivo):
        lista_final = []

        for lugar in self.array_lugares:
            lugar_simplificado = [lugar.id, [tuple(i) for i in lugar.array_coordenadas], lugar.cor, lugar.orientacao]
            lista_final.append(lugar_simplificado)

        fst.lista_para_arquivo_csv(lista_final, nome_arquivo)

    def salvar_agentes_arquivo(self, nome_arquivo):
        lista_final = []

        for agente in self.array_agentes:
            agente_simplificado = [agente.grid_x, agente.grid_y, agente.orientacao_latente,
                                   agente.orientacao_atual, agente.id]
            lista_final.append(agente_simplificado)

        fst.lista_para_arquivo_csv(lista_final, nome_arquivo)

    def resgatar_agentes_arquivo(self, nome_arquivo_agentes_staticos):
        lista_agentes_simplificados = fst.arquivo_csv_para_lista(nome_arquivo_agentes_staticos)
        lista_agentes_final = []

        for info_agente in lista_agentes_simplificados:

            agente_recuperado = AgenteV2Fast(self, info_agente[0], info_agente[1],
                                             orientacao_latente=info_agente[2],
                                             orientacao_atual=info_agente[3],
                                             id_agente=info_agente[4])
            lista_agentes_final.append(agente_recuperado)

        self.array_agentes = np.array(lista_agentes_final)
