import random
import math
import numpy as np
import matplotlib.pyplot as plt
import os


# desenhando o grid uma vez no console
def print_grid(matriz):
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] == 1:
                print('1', end='  ')
            if matriz[y][x] == 0:
                print('0', end='  ')
            if matriz[y][x] == 2:
                print('2', end='  ')
            if matriz[y][x] == 3:
                print('3', end='  ')
        print('\n')
    print('------------------------------------------------------')
    print('\n')


# funcao que muda o agente com um bloco do seu lado, simbolizando movimento
def atualizar_grid(level, pos_x_antiga, pos_y_antiga, pos_x_nova, pos_y_nova):
    level[pos_x_antiga][pos_y_antiga], level[pos_x_nova][pos_y_nova] = level[pos_x_nova][pos_y_nova], level[pos_x_antiga][pos_y_antiga]
    return level


# funcao que escollhe um movimento aleatorio pro agente, o agente n pode voltar pelo caminho que fez
def movimento_aleatorio(matriz, linha_matriz, coluna_matriz, ultimo_mov):
    # vendo qual movimento pode ser realizado
    # todos os possiveis movimentos na lista a seguir
    # os movimentos proibidos serao retirados da lista
    # por fim, sera sorteado o movimento restante

    mov_volta = (0, 0)

    mov_possiveis = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

    if matriz[linha_matriz][coluna_matriz - 1] == 0:    # ver se pode andar para a esquerda
        mov_possiveis.remove((0, -1))
    if matriz[linha_matriz][coluna_matriz+1] == 0:    # ver se pode andar para a direita
        mov_possiveis.remove((0, +1))
    if matriz[linha_matriz-1][coluna_matriz] == 0:    # ver se pode andar para cima
        mov_possiveis.remove((-1, 0))
    if matriz[linha_matriz+1][coluna_matriz] == 0:  # ver se pode andar para baixo
        mov_possiveis.remove((+1, 0))

    if ultimo_mov == (0, 0):
        pass
    else:
        mov_volta = (ultimo_mov[0] * (-1), ultimo_mov[1] * (-1))
        mov_possiveis.remove(mov_volta)

    if len(mov_possiveis) == 0:
        return mov_volta
    else:
        movimento_escolhido = random.choice(mov_possiveis)
        return movimento_escolhido


# funcao que atualiza a posicao do agente no grid
def proxima_posicao(prox_mov, linha_matriz, coluna_matriz):
    prox_pos = (prox_mov[0] + linha_matriz, prox_mov[1] + coluna_matriz)
    return prox_pos


def menor_caminho(level, y0, x0, y1, x1):

    # lista de movimentos possiveis
    direita = (+1, 0)
    esquerda = (-1, 0)
    baixo = (0, +1)
    cima = (0, -1)

    dx = x1 - x0
    dy = y1 - x0

    if dx == 0 and dy == 0:
        return (0, 0)
    else:
        if dx > 0:
            mov_horizontal = direita
        elif dx < 0:
            mov_horizontal = esquerda

        sentido_horizontal = mov_horizontal[0]

        if dy > 0:
            mov_vertical = baixo
        elif dy < 0:
            mov_vertical = cima

        sentido_vertical = mov_vertical[1]

        if level[y0+sentido_vertical][x0] == 1 and level[y0][x0+sentido_horizontal] == 1:
            return (1, 1)

        elif dx > dy:
            if level[y0][x0+sentido_horizontal] == 0:
                return mov_horizontal
            elif level[y0+sentido_vertical][x0] == 0:
                return mov_vertical
        else:
            if level[y0+sentido_vertical][x0] == 0:
                return mov_vertical
            elif level[y0][x0+sentido_horizontal] == 0:
                return mov_horizontal


# modelo para simular isovistas
# modelo para o agente lembrar dos locais que passa
def lembrar_local_v1(locais, y0, x0):
    for local in locais:
        if y0 == local['local'][0] and x0 == local['local'][1]:
            return local
    return 0


def lembrar_local_v2(locais, y0, x0):
    pos_y = y0-1
    pos_x = x0-1

    for y in range(3):
        for x in range(3):
            for local in locais:
                if pos_y + y == local['local'][0] and pos_x + x == local['local'][1]:
                    return local
    return 0


def grid_isovistas_v1(level, y0, x0):
    # grid azul vazio q ria receber as coordenadas q o agente pode ver
    grid_azul = set()

    campo_de_visao_cima = 4
    campo_de_visao_baixo = 4
    campo_de_visao_direita = 4
    campo_de_visao_esquerda = 4
    alcance_visao = 4

    # campo de visao da parte de cima
    for i in range(alcance_visao):
        nova_cell = (y0 - i, x0)
        if level[y0 - i][x0] == 0:
            break
        elif level[y0 - i][x0] == 1 or level[y0 - i][x0] == 2:
            grid_azul.add(nova_cell)

            # checando o lado direito
            for j in range(campo_de_visao_cima):
                nova_cell = (y0 - i, x0 + j)
                if level[y0 - i][x0 + j] == 0:
                    break
                elif level[y0 - i][x0 + j] == 1:
                    grid_azul.add(nova_cell)

            # checando o lado esquerdo
            for j in range(campo_de_visao_cima):
                nova_cell = (y0 - i, x0 - j)
                if level[y0 - i][x0 - j] == 0:
                    break
                elif level[y0 - i][x0 - j] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_cima -= 1

    # campo de visao parte de baixo
    for i in range(alcance_visao):
        nova_cell = (y0 + i, x0)
        if level[y0 + i][x0] == 0:
            break
        elif level[y0 + i][x0] == 1 or level[y0 + i][x0] == 2:
            grid_azul.add(nova_cell)

            # checando o lado direito
            for j in range(campo_de_visao_baixo):
                nova_cell = (y0 + i, x0 + j)
                if level[y0 + i][x0 + j] == 0:
                    break
                elif level[y0 + i][x0 + j] == 1:
                    grid_azul.add(nova_cell)

            # checando o lado esquerdo
            for j in range(campo_de_visao_baixo):
                nova_cell = (y0 + i, x0 - j)
                if level[y0 + i][x0 - j] == 0:
                    break
                elif level[y0 + i][x0 - j] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_baixo -= 1

    # fazendo campo de visao da direita
    for i in range(alcance_visao):
        nova_cell = (y0, x0 + i)
        if level[y0][x0 + i] == 0:
            break
        elif level[y0][x0 + i] == 1 or level[y0][x0 + i] == 2:
            grid_azul.add(nova_cell)

            # checando a parte de cima
            for j in range(campo_de_visao_direita):
                nova_cell = (y0 - j, x0 + i)
                if level[y0 - j][x0 + i] == 0:
                    break
                elif level[y0 - j][x0 + i] == 1:
                    grid_azul.add(nova_cell)

            # checando a parte de baixo
            for j in range(campo_de_visao_direita):
                nova_cell = (y0 + j, x0 + i)
                if level[y0 + j][x0 + i] == 0:
                    break
                elif level[y0 + j][x0 + i] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_direita -= 1

    # fazendo campo de visao da esquerda
    for i in range(alcance_visao):
        nova_cell = (y0, x0 - i)
        if level[y0][x0 - i] == 0:
            break
        elif level[y0][x0 - i] == 1 or level[y0][x0 - i] == 2:
            grid_azul.add(nova_cell)

            # checando a parte de cima
            for j in range(campo_de_visao_esquerda):
                nova_cell = (y0 - j, x0 - i)
                if level[y0 - j][x0 - i] == 0:
                    break
                elif level[y0 - j][x0 - i] == 1:
                    grid_azul.add(nova_cell)

            # checando a parte de baixo
            for j in range(campo_de_visao_esquerda):
                nova_cell = (y0 + j, x0 - i)
                if level[y0 + j][x0 - i] == 0:
                    break
                elif level[y0 + j][x0 - i] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_esquerda -= 1

    return grid_azul


def grid_isovistas_v2(level, y0, x0):
    #grid azul vazio q ria receber as coordenadas q o agente pode ver
    grid_azul = set()

    campo_de_visao_cima = 4
    campo_de_visao_baixo = 4
    campo_de_visao_direita = 4
    campo_de_visao_esquerda = 4
    alcance_visao = 4

    # campo de visao da parte de cima
    for i in range(alcance_visao):
        nova_cell = (y0 - i, x0)
        if level[y0-i][x0] == 0:
            grid_azul.add(nova_cell)
            break
        elif level[y0-i][x0] == 1 or level[y0-i][x0] == 2:
            grid_azul.add(nova_cell)

            # checando o lado direito
            for j in range(campo_de_visao_cima):
                nova_cell = (y0-i, x0+j)
                if level[y0-i][x0+j] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0-i][x0+j] == 1:
                    grid_azul.add(nova_cell)

            # checando o lado esquerdo
            for j in range(campo_de_visao_cima):
                nova_cell = (y0-i, x0-j)
                if level[y0-i][x0-j] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0-i][x0-j] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_cima -= 1

    # campo de visao parte de baixo
    for i in range(alcance_visao):
        nova_cell = (y0+i, x0)
        if level[y0+i][x0] == 0:
            grid_azul.add(nova_cell)
            break
        elif level[y0+i][x0] == 1 or level[y0+i][x0] == 2:
            grid_azul.add(nova_cell)

            # checando o lado direito
            for j in range(campo_de_visao_baixo):
                nova_cell = (y0+i, x0+j)
                if level[y0+i][x0+j] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0+i][x0+j] == 1:
                    grid_azul.add(nova_cell)

            # checando o lado esquerdo
            for j in range(campo_de_visao_baixo):
                nova_cell = (y0+i, x0-j)
                if level[y0+i][x0-j] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0+i][x0-j] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_baixo -= 1

    # fazendo campo de visao da direita
    for i in range(alcance_visao):
        nova_cell = (y0, x0+i)
        if level[y0][x0+i] == 0:
            grid_azul.add(nova_cell)
            break
        elif level[y0][x0+i] == 1 or level[y0][x0+i] == 2:
            grid_azul.add(nova_cell)

            # checando a parte de cima
            for j in range(campo_de_visao_direita):
                nova_cell = (y0-j, x0+i)
                if level[y0-j][x0+i] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0-j][x0+i] == 1:
                    grid_azul.add(nova_cell)

            # checando a parte de baixo
            for j in range(campo_de_visao_direita):
                nova_cell = (y0+j, x0+i)
                if level[y0+j][x0+i] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0+j][x0+i] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_direita -= 1

    # fazendo campo de visao da esquerda
    for i in range(alcance_visao):
        nova_cell = (y0, x0 - i)
        if level[y0][x0-i] == 0:
            grid_azul.add(nova_cell)
            break
        elif level[y0][x0-i] == 1 or level[y0][x0-i] == 2:
            grid_azul.add(nova_cell)

            # checando a parte de cima
            for j in range(campo_de_visao_esquerda):
                nova_cell = (y0-j, x0-i)
                if level[y0-j][x0-i] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0-j][x0-i] == 1:
                    grid_azul.add(nova_cell)

            # checando a parte de baixo
            for j in range(campo_de_visao_esquerda):
                nova_cell = (y0+j, x0-i)
                if level[y0+j][x0-i] == 0:
                    grid_azul.add(nova_cell)
                    break
                elif level[y0+j][x0-i] == 1:
                    grid_azul.add(nova_cell)

            campo_de_visao_esquerda -= 1

    return grid_azul

# funcoes para isovistas final

def gerar_vetor(x0, y0, u, v):
    ponto_inicial = (x0, y0)
    vetor_direcao = (u, v)

    vetor = (ponto_inicial, vetor_direcao)
    return vetor


# IMPORTANTE
def gerar_vetores_circular(qnt_vetores, raio):

    angulo_por_divisao = qnt_vetores/2

    lista_cos = set()

    for t in range(qnt_vetores+1):
        valor = 1/angulo_por_divisao * t
        valor_final = np.pi * valor
        cosseno = np.cos(valor_final)
        lista_cos.add(cosseno)

    lista_vetores = set()

    for cos in lista_cos:
        cateto_oposto_1 = raio * math.sqrt(1 - cos**2)
        cateto_oposto_2 = - cateto_oposto_1

        cateto_adjacente_1 = math.sqrt(raio**2 - cateto_oposto_1**2)
        cateto_adjacente_2 = - cateto_adjacente_1

        # melhorando os valores para serem postos na lista

        cat_op_1 = round(cateto_oposto_1, 3)
        cat_op_2 = round(cateto_oposto_2, 3)
        cat_ad_1 = round(cateto_adjacente_1, 3)
        cat_ad_2 = round(cateto_adjacente_2, 3)

        vet_1 = (cat_ad_1, cat_op_1)
        vet_2 = (cat_ad_1, cat_op_2)
        vet_3 = (cat_ad_2, cat_op_1)
        vet_4 = (cat_ad_2, cat_op_2)

        lista_vetores.add(vet_1)
        lista_vetores.add(vet_2)
        lista_vetores.add(vet_3)
        lista_vetores.add(vet_4)

    return lista_vetores


def gerar_pontos(ponto_inicial, lista_vetores, distancia):
    ponto_inicial_x = ponto_inicial[0]
    ponto_inicial_y = ponto_inicial[1]

    lista_pontos = []

    for vetor in lista_vetores:

        vetor_diretor_x = vetor[0]
        vetor_diretor_y = vetor[1]

        pos_final_x = ponto_inicial_x + vetor_diretor_x * distancia
        pos_final_y = ponto_inicial_y + vetor_diretor_y * distancia

        ponto_final = (int(pos_final_x), int(pos_final_y))

        lista_pontos.append(ponto_final)

    return lista_pontos


# IMPORTANTE
def gerar_lista_pontos_obstrucao(matriz):

    lista_pontos = set()

    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            ponto = (x, y)
            if matriz[y][x] == 0 or matriz[y][x] == 3:
                lista_pontos.add(ponto)

    return lista_pontos


# IMPORTANTE
def gerar_lista_area_obstrucoes(lista_pontos_obstrucao, cell_size):

    lista_area_obstrucoes = set()

    for ponto in lista_pontos_obstrucao:

        ponto_x_inicio = ponto[0] * cell_size
        ponto_x_limite = ponto[0] * cell_size + cell_size
        intervalo_x = (ponto_x_inicio, ponto_x_limite)

        ponto_y_inicio = ponto[1] * cell_size
        ponto_y_limite = ponto[1] * cell_size + cell_size
        intervalo_y = (ponto_y_inicio, ponto_y_limite)

        area_total = (intervalo_x, intervalo_y)
        lista_area_obstrucoes.add(area_total)

    return lista_area_obstrucoes


# IMPORTANTE
def checar_saida_grid(ponto_analisado, width, height):

    ponto_analisado_x = ponto_analisado[0]
    ponto_analisado_y = ponto_analisado[1]


    # resultado para saber como o vetor saiu do grid
    # 0 - n saiu / 1 - saiu

    if ponto_analisado_x < 0 or ponto_analisado_x > width:
        resultado_x = 1
    else:
        resultado_x = 0

    if ponto_analisado_y < 0 or ponto_analisado_y > height:
        resultado_y = 1
    else:
        resultado_y = 0

    resultado_final = (resultado_x, resultado_y)
    return resultado_final


# IMPORTANTE
def gerar_vetores_finais(ponto_inicial, lista_vetores, lista_area_obstrucoes, cell_size, width, height):

    # um vetor eh basicamente formado por dois pontos: o seu ponto inicial e seu ponto final
    # como o ponto inicial sera sempre o ponto do agente, devemos so procurar pelo seu ponto final

    lista_pontos = set()

    ponto_inicial_x = ponto_inicial[0]
    ponto_inicial_y = ponto_inicial[1]

    for vetor in lista_vetores:

        achou_obst = False
        saiu_grid = False

        vetor_diretor_x = vetor[0]
        vetor_diretor_y = vetor[1]

        # agora devemos ir aumentando o vetor ate q ele saia do grid ou encontre um obstaculo

        t = -1

        while achou_obst is False and saiu_grid is False:

            t += 1 * cell_size

            ponto_final_x = ponto_inicial_x + int(vetor_diretor_x * t)
            ponto_final_y = ponto_inicial_y + int(vetor_diretor_y * t)

            # Neste caso o vetor esta fora do grid
            if (ponto_final_x < 0 or ponto_final_x > width) or (ponto_final_y < 0 or ponto_final_y > height):

                saiu_grid = True

                if ponto_final_x < 0:
                    ponto_final_x = 0

                if ponto_final_x > width:
                    ponto_final_x = width

                if ponto_final_y < 0:
                    ponto_final_y = 0

                if ponto_final_y > height:
                    ponto_final_y = height

                ponto_final = (ponto_final_x, ponto_final_y)
                lista_pontos.add(ponto_final)

            else:

                # Checando se o vetor encontrou algum obstaculo
                for area in lista_area_obstrucoes:

                    intervalo_x = area[0]
                    intervalo_y = area[1]

                    obst_x_inicio = intervalo_x[0]
                    obst_x_limite = intervalo_x[1]

                    obst_y_inicio = intervalo_y[0]
                    obst_y_limite = intervalo_y[1]

                    if ponto_final_x > obst_x_inicio and ponto_final_x < obst_x_limite:
                        if ponto_final_y > obst_y_inicio and ponto_final_y < obst_y_limite:
                            ponto_final = (ponto_final_x, ponto_final_y)
                            lista_pontos.add(ponto_final)
                            achou_obst = True

    return lista_pontos


def obter_ponto_borda_r1(p0, p1, height, width):
    dx = abs(p1[0] - p0[0])
    dy = abs(p1[1] - p0[0])

    tg = dy/dx

    dis_borda_hor = width - p1[0]
    dis_borda_ver = height - p1[1]

    min_dis_borda = min(dis_borda_hor, dis_borda_ver)

    if min_dis_borda == dis_borda_hor:
        x = width
        y = p0[0] - (width - p0[0]) * tg
        p2 = (x, y)
        return p2


def obter_ponto_borda_r3(p0, p1, height, width):
    dx = abs(p1[0] - p0[0])
    dy = abs(p1[1] - p0[0])

    tg = dy / dx

    dis_borda_hor = width - p1[0]
    dis_borda_ver = height - p1[1]

    min_dis_borda = min(dis_borda_hor, dis_borda_ver)

    if min_dis_borda == dis_borda_hor:
        x = width - 1
        y = p0[0] - (width - p0[0]) * tg + 1
        p2 = (x, y)
        return p2


def obter_ponto_grid_r1(p, cell_size):
    px = p[0] * cell_size
    py = p[1] * cell_size
    p_final = (px, py)
    return p_final


def obter_ponto_grid_r3(p, cell_size):
    px = p[0] * cell_size + cell_size
    py = p[1] * cell_size + cell_size
    p_final = (px, py)
    return p_final


# fim das funcoes isovistas final
def grid_isovistas_v3(matriz, y0, x0, height, width):

    fov = set()
    sombras = set()

    total = []

    ctrl_sombra_cima = False

    # primeiro temos que achar as sombras

    # achando as sombras nas partes de cima

    for j in range(height):
        nova_cell = (y0 - j, x0)
        if y0 - j == 0 and ctrl_sombra_cima == False:
            fov.add(nova_cell)
            break
        else:
            if matriz[y0-j][x0] == 1 and ctrl_sombra_cima == False:
                fov.add(nova_cell)
            if matriz[y0-j][x0] == 0:
                ctrl_sombra_cima = True
                for s in range(height):
                    nova_cell = (y0 - j - s, x0)
                    if y0-j-s == 0:
                        sombras.add(nova_cell)
                        break
                    else:
                        sombras.add(nova_cell)

    total.append(fov)
    total.append(sombras)

    return total


def gravar_memoria_agente_arquivo(memoria_agente):
    arquivo = open('memoria_agente.txt', 'r')
    locais_para_arquivo = arquivo.readlines()
    arquivo.close()

    for local in memoria_agente:
        local_temp = ''
        cont = 0
        for key, value in local.items():
            cont += 1
            if cont == 3:
                local_temp += str('{}\t{}\n'.format(key, value))
            else:
                local_temp += str('{}\t{}\t'.format(key, value))

        if local_temp not in locais_para_arquivo:
            locais_para_arquivo.append(local_temp)

    arquivo = open('memoria_agente.txt', 'w')

    for local in locais_para_arquivo:
        arquivo.write(local)

    arquivo.close()


def resgatar_memoria_agente_aquivo(nome_aqruivo):

    arquivo = open(nome_aqruivo, 'r')

    locais = arquivo.readlines()
    locais_temp = []
    locais_final = []

    for local in locais:
        a = local.strip('\n')
        b = a.split('\t')
        locais_temp.append(b)

    for local in locais_temp:
        local_final = {}
        for k in range(len(local)//2):
            local_final[local[k*2]] = local[k*2+1]

        local_final['local'] = eval(local_final['local'])
        local_final['cor'] = eval(local_final['cor'])

        locais_final.append(local_final)

    arquivo.close()

    return locais_final


def limpar_memoria_agente():

    arquivo = open('memoria_agente.txt', 'w')

    arquivo.close()


# obsoleto
def obter_grid(nome_arquivo):

    arquivo = open(nome_arquivo)

    matriz = arquivo.readlines()

    arquivo.close()

    grid = []

    for x in range(1000):
        coluna = [0]*1000
        grid.append(coluna)

    matriz_temp = []

    for linha in matriz:
        a = linha.strip('\n')
        b = a.split('\t')
        for n in range(len(b)):
            b[n] = int(b[n])
        matriz_temp.append(b)

    for cell in matriz_temp:
        x = cell[0]
        y = cell[1]
        valor = cell[2]
        grid[y][x] = valor

    return grid


def obter_grid_manual(linhas, colunas):
    grid = []

    for y in range(linhas):
        linha = [0]*colunas
        grid.append(linha)

    return grid


def editar_grid_manual(matriz):
    escolhas = [0, 1]

    for y in range(len(matriz)):
        for x in range(len(matriz[0])):
            matriz[y][x] = random.choice(escolhas)

    return matriz


def obter_grid_randomico(qnt_linhas, qnt_colunas, pesos=(90, 10)):

    matriz = []

    escolhas = [0, 1]

    for y in range(qnt_linhas):
        linha = random.choices(escolhas, weights=pesos, k=qnt_colunas)
        matriz.append(linha)

    return matriz


# funcoes para A*
def obter_nodulo_menor_f(lista):
    menor_f = lista[0].f
    menor_h = lista[0].h
    nodulo_menor_f = lista[0]

    for nodulo in lista:
        if nodulo.f < menor_f:
            menor_f = nodulo.f
            menor_h = nodulo.h
            nodulo_menor_f = nodulo

        elif nodulo.f == menor_f and nodulo.h < menor_h:
            menor_f = nodulo.f
            menor_h = nodulo.h
            nodulo_menor_f = nodulo

    return nodulo_menor_f


def get_abs_dis(pos_1, pos_2):
    d = abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])
    return d


def obter_vizinhos(matriz, coordenada, aceitavel):
    x = coordenada[0]
    y = coordenada[1]

    qnt_linhas = len(matriz)
    qnt_colunas = len(matriz[0])

    lista_vizinhos = []

    for i in range(-1, 2):
        for j in range(-1, 2):

            coord_analisada = (x + j, y + i)

            if coord_analisada == coordenada:
                continue
            else:
                if 0 <= coord_analisada[0] <= qnt_colunas - 1:
                    if 0 <= coord_analisada[1] <= qnt_linhas - 1:
                        if matriz[y+i][x+j] == aceitavel:
                            lista_vizinhos.append(coord_analisada)
    return lista_vizinhos


def icarai():

    arquivo = open('Icarai_uso_cores.txt', 'r')
    legenda_cores = arquivo.readlines()
    arquivo.close()

    legenda_final = []

    for item in legenda_cores:
        a = item.strip('\n')
        b = a.split('\t')
        c = {'valor': b[0], 'cor': b[1]}
        legenda_final.append(c)

    arquivo_1 = open('Icarai_Uso.txt', 'r')
    lista_uso_solo = arquivo_1.readlines()
    arquivo_1.close()

    lista_uso_final = []

    for item in lista_uso_solo:
        a = item.strip('\n')
        b = a.split('\t')
        c = {'x': b[0], 'y': b[1], 'valor': b[2]}
        lista_uso_final.append(c)

    for coord in lista_uso_final:
        for item in legenda_final:

            if coord['valor'] == item['valor']:

                coord['cor'] = item['cor']

    arquivo_final = open('Icarai_uso_final.txt', 'w')

    for item in lista_uso_final:
        item_final = '{}\t{}\t{}\t{}\n'.format(item['x'], item['y'], item['valor'], item['cor'])
        arquivo_final.write(item_final)

    arquivo_final.close()


def resgatar_uso_solo_arquivo(arquivo):

    arquivo_novo = open(arquivo, 'r')
    lista = arquivo_novo.readlines()

    lista_nova = []

    for item in lista:
        a = item.strip('\n')
        b = a.split('\t')
        c = {'x': b[0], 'y': b[1], 'valor': b[2], 'cor': b[3]}
        lista_nova.append(c)

    return lista_nova


def obter_legenda_cores(nome_arquivo):

    arquivo = open(nome_arquivo, 'r')
    lista  = arquivo.readlines()

    lista_final = []

    for item in lista:
        a = item.strip('\n')
        b = a.split('\t')
        b[1] = b[1].strip('(')
        b[1] = b[1].strip(')')
        b[1] = b[1].split(',')
        c = {'valor': int(b[0]), 'cor': tuple(map(int, b[1]))}
        lista_final.append(c)

    return lista_final


def init_celulas_v2(nome_arquivo):

    arquivo = open(nome_arquivo, "r")
    lista_celulas = arquivo.readlines()

    nova_lista = []

    for celula in lista_celulas:
        a = celula.strip("\n")
        b = a.split("\t")
        c = {"x": b[0], "y": b[1], }


def arquivo_csv_para_lista(nome_arquivo):
    arquivo = open(nome_arquivo, "r")
    lista_arquivo = arquivo.readlines()
    arquivo.close()

    lista_temp = [item.strip("\n").split("\t") for item in lista_arquivo]
    #lista_temp = lista_temp[0] ------ talvez continue, se for retornar só a lista
    print(f'\nLISTA_TEMP: {lista_temp}\n')
    lista_final = [list(map(eval, i)) for i in lista_temp]

    return lista_final


def lista_para_arquivo_csv(lista_origem, nome_arquivo_destino, tipo_operacao="w"):

    lista_temp = [list(map(str, i)) for i in lista_origem]
    lista_temp_2 = ["\t".join(i) for i in lista_temp]
    lista_final = ["{}\n".format(i) for i in lista_temp_2]

    arquivo_destino = open(nome_arquivo_destino, tipo_operacao)

    for linha in lista_final:
        arquivo_destino.write(linha)

    arquivo_destino.close()


def transformar_duas_listas_em_dict(lista_chaves, lista_valores):
    dicionario = {chave: valor for chave, valor in zip(lista_chaves, lista_valores)}
    return dicionario


def matriz_para_lista_dicionarios(lista_chaves, lista_valores):
    lista_dict = [{key: value for key, value in zip(lista_chaves, i)} for i in lista_valores]
    return lista_dict


def lista_dicionarios_para_matriz(lista_dicionarios):
    matriz_final = [list(i.values()) for i in lista_dicionarios]
    return matriz_final


def obter_arquivo_final(nome_arquivo_matriz, nome_arquivo_cores, nome_arquivo_final):
    lista_arquivo_matriz = arquivo_csv_para_lista(nome_arquivo_matriz)
    parametros_matriz = ["x", "y", "valor"]
    lista_dict_matriz = matriz_para_lista_dicionarios(parametros_matriz, lista_arquivo_matriz)

    lista_arquivo_cores = arquivo_csv_para_lista(nome_arquivo_cores)
    parametros_cores = ["valor", "cor"]
    lista_dict_cores = matriz_para_lista_dicionarios(parametros_cores, lista_arquivo_cores)

    lista_final = []

    for ponto in lista_dict_matriz:
        for item in lista_dict_cores:
            if ponto["valor"] == item["valor"]:
                novo_dict = {"x": ponto["x"], "y": ponto["y"], "valor": ponto["valor"], "cor": item["cor"]}
                lista_final.append(novo_dict)

    for linha in lista_final:
        print(linha)

    matriz_final = lista_dicionarios_para_matriz(lista_final)
    lista_para_arquivo_csv(matriz_final, nome_arquivo_final)


def transformar_lista_em_matriz(lista_original, qnt_linhas, qnt_colunas):

    matriz_final = []

    for i in range(qnt_linhas):
        linha_temp = []
        for j in range(qnt_colunas):
            n = i * qnt_colunas + j
            linha_temp.append(lista_original[n])
        matriz_final.append(linha_temp)

    return matriz_final


def distancia_pitagorica(ponto_inicial, ponto_final):

    x_inicial = ponto_inicial[0]
    x_final = ponto_final[0]

    y_inicial = ponto_inicial[1]
    y_final = ponto_final[1]

    distancia = math.sqrt((x_final - x_inicial)**2 + (y_final - y_inicial)**2)

    return distancia


def distancia_sebastiana(custo_menor_mov, custo_maior_mov, pos_grid_inicial, pos_grid_final):

    dx = abs(pos_grid_final[0] - pos_grid_inicial[0])
    dy = abs(pos_grid_final[1] - pos_grid_inicial[1])

    if dx > dy:
        distancia = custo_maior_mov * dy + custo_menor_mov * (dx - dy)
    else:
        distancia = custo_maior_mov * dx + custo_menor_mov * (dy - dx)

    return distancia


def obter_distancia_manhattan(coordenada1, coordenada2):
    distancia_eixo_x = abs(coordenada1[0] - coordenada2[0])
    distancia_eixo_y = abs(coordenada1[1] - coordenada2[1])

    distancia_total = distancia_eixo_x + distancia_eixo_y
    return distancia_total


def converter_pos_para_coordenada_grid(tupla_pos, tamanho_celula):
    pos_grid = tuple(map(lambda x: int(x / tamanho_celula), tupla_pos))
    return pos_grid


def encontrar_celulas_principais(lugar1, lugar2):

    # funcao defina a "celula principal" dos dois lugares
    # assim, as celulas principais podem ser usadas no A* para achar a menor distancia entre os dois lugares

    menor_distancia = None
    par_de_celulas = (0, 0)

    for celula1 in lugar1.lista_celulas_grid:
        for celula2 in lugar2.lista_celulas_grid:

            par_celulas_atual = (celula1, celula2)
            distancia_atual = distancia_sebastiana(10, 14, celula1.pos_grid, celula2.pos_grid)

            if menor_distancia is None:
                menor_distancia = distancia_atual
                par_de_celulas = par_celulas_atual

            else:
                if distancia_atual < menor_distancia:
                    menor_distancia = distancia_atual
                    par_de_celulas = par_celulas_atual

    lugar1.celula_principal = par_de_celulas[0]
    lugar2.celula_principal = par_de_celulas[1]
    lugar1.celula_principal.eh_a_celula_principal = lugar2.celula_principal.eh_a_celula_principal = True


def fatorial_recursivo(n):

    if n == 1:
        return 1
    else:
        return n * fatorial_recursivo(n - 1)


def fatorial(n):
    if n == 0:
        return 1
    else:
        num_atual = n
        resultado = n

        while num_atual != 1:
            num_atual -= 1
            resultado *= num_atual

        return resultado


def combinacao(n, r):
    resultado = int(fatorial(n) / (fatorial(r) * fatorial(n-r)))
    return resultado


def porcentagem_relativa(valor_total, valor_analisado):
    porcentagem = (valor_analisado * 100) / valor_total
    return porcentagem

# obsoleto, a "funcao obter_dict_contagem_elementos_repetidos" eh mais rapida e simples
def lista_contagem_elementos_repetidos(lista_com_elementos_repetidos):

    set_elementos = set()

    for elemento in lista_com_elementos_repetidos:
        a = elemento
        b = lista_com_elementos_repetidos.count(elemento)
        c = (a, b)
        set_elementos.add(c)

    lista_elementos_repetidos_contados = list(set_elementos)
    lista_elementos_repetidos_contados.sort()

    return lista_elementos_repetidos_contados


def obter_dict_contagem_elementos_repetidos(lista_com_elementos_repetidos):
    dicionario_contagem_repeticoes = {i: lista_com_elementos_repetidos.count(i) for i in lista_com_elementos_repetidos}
    return dicionario_contagem_repeticoes


def obter_dict_contagem_elementos_repetidos_v2(lista_com_elementos_repetidos):
    set_elementos = set(lista_com_elementos_repetidos)
    dicionario_contagem_repeticoes = {i: lista_com_elementos_repetidos.count(i) for i in set_elementos}
    return dicionario_contagem_repeticoes


def obter_lista_com_elementos_repetidos(dict_contagem_elementos_repetidos):

    lista_com_elementos_repetidos = []

    for key, value in dict_contagem_elementos_repetidos.items():
        for i in range(value):
            lista_com_elementos_repetidos.append(key)

    return lista_com_elementos_repetidos


def obter_arquivo_final_2(nome_arquivo_lugares_base, nome_arquivo_cores, nome_arquivo_lugares_final):
    lista_cores_temp = arquivo_csv_para_lista(nome_arquivo_cores)
    lista_chaves_cores = ["uso", "cor"]
    lista_cores_final = matriz_para_lista_dicionarios(lista_chaves_cores, lista_cores_temp)

    lista_lugares_temp = arquivo_csv_para_lista(nome_arquivo_lugares_base)
    lista_chaves_lugares = ["x", "y", "uso", "id"]
    lista_lugares_temp_2 = matriz_para_lista_dicionarios(lista_chaves_lugares, lista_lugares_temp)

    lista_orientacoes = list(range(0, 1100, 100))
    lista_ids = []
    lista_lugares_final = []

    for celula in lista_lugares_temp_2:

        if celula["id"] == 1:
            continue

        if celula["id"] not in lista_ids:
            lista_ids.append(celula["id"])
            orientacao_selecionada = random.choice(lista_orientacoes)
            coordenada_inicial = (celula["x"], celula["y"])
            cor_selecionada = (255, 255, 255)

            for dict_cores in lista_cores_final:
                if celula["uso"] == dict_cores["uso"]:
                    cor_selecionada = dict_cores["cor"]

            novo_lugar = {"id": celula["id"], "lista_coordenadas": [coordenada_inicial], "cor": cor_selecionada,
                          "orientacao": orientacao_selecionada}

            lista_lugares_final.append(novo_lugar)

        else:
            nova_coordenada = (celula["x"], celula["y"])
            for lugar in lista_lugares_final:
                if celula["id"] == lugar["id"]:
                    lugar["lista_coordenadas"].append(nova_coordenada)

    matriz_lugares = lista_dicionarios_para_matriz(lista_lugares_final)
    lista_para_arquivo_csv(matriz_lugares, nome_arquivo_lugares_final)


def escolher_lugar_menor_e(agente, lista_lugares):

    diferenca_orientacao_inicial = abs(agente.orientacao_latente - lista_lugares[0].orientacao)
    coordenada_principal_inicial = lista_lugares[0].achar_coordenada_principal(agente.pos_grid)
    distancia_inicial = round(distancia_pitagorica(agente.pos_grid, coordenada_principal_inicial))

    menor_e = (diferenca_orientacao_inicial + 100) * distancia_inicial
    lugar_menor_e = lista_lugares[0]

    for lugar in lista_lugares:

        diferenca_orientacao_analisada = abs(agente.orientacao_latente - lugar.orientacao)
        coordenada_principal_analisada = lugar.achar_coordenada_principal(agente.pos_grid)
        distancia_analisada = round(distancia_pitagorica(agente.pos_grid, coordenada_principal_analisada))

        menor_e_analisado = (diferenca_orientacao_analisada + 100) * distancia_analisada

        if menor_e_analisado < menor_e:
            menor_e = menor_e_analisado
            lugar_menor_e = lugar

    return lugar_menor_e


def escolher_menor_e_v2(peso_alpha, peso_beta):
    pass
    # base = 2.7182
    # expoente = (dif orientacao latente) + peso_sigma(distancia)
    # menor_e = base ** expoente
    # probabilidade_e = 1/menor_e (?)


# obsoleto, funcional
def converter_orientacao_para_cor(orientacao):
    cor_r = 0
    cor_g = 0
    cor_b = 0

    contador = 0

    while contador <= orientacao:

        if contador < 256:
            cor_b = contador
        elif contador < 512:
            cor_g = contador - 255
        else:
            cor_r = contador - 510

        contador += 1

    cor_final = (cor_r, cor_g, cor_b)
    return cor_final


# obsoleto, n funcional
def converter_orientacao_para_cor_v2(indice):

    cor_r = 1
    cor_g = 1
    cor_b = 1

    while (cor_r*cor_g*cor_b) <= indice:

        if cor_b < 256:
            cor_b += 10
        else:
            cor_b = 1
            if cor_g < 256:
                if cor_b < 256:
                    cor_b += 10
                else:
                    cor_g += 10
                    cor_b = 1
            else:
                cor_b = 1
                cor_g = 1
                if cor_r < 256:
                    if cor_g < 256:
                        if cor_b < 256:
                            cor_b += 10
                        else:
                            cor_g += 10
                            cor_b = 1
                    else:
                        cor_r += 10
                else:
                    return 1

    cor_final = (cor_r, cor_g, cor_b)
    return cor_final


def converter_orientacao_para_cor_v3(qnt_orientacoes):
    numero_total_cores = 256 * 256 * 256

    faixa = numero_total_cores // qnt_orientacoes
    # print(faixa)

    dict_orientacao_cores = {}

    for n in range(1, qnt_orientacoes + 1):

        orientacao = n * 100 - 100

        indice_cor = n * faixa
        # print("indice cor = ", indice_cor)

        cor_r = indice_cor // (256 * 256)
        # print("cor r = ", cor_r)

        cor_g = (indice_cor % (256 * 256)) // 256
        # print("cor g = ", cor_g)

        cor_b = (indice_cor % (256 * 256)) % 256
        # print("cor b = ", cor_b)

        cor_final = (cor_r, cor_g, cor_b)
        # print("cor final = ", cor_final)

        # print("orientação = {} / cor = {}".format(orientacao, cor_final))

        dict_orientacao_cores[str(orientacao)] = cor_final

        # print("--------------------\n")

    return dict_orientacao_cores


def update_orientacao_cor(dict_orientacoes_cores, orientacao_analisada, qnt_orientacoes=11):
    numero_total_cores = 256 * 256 * 256
    faixa = numero_total_cores // qnt_orientacoes

    menor_diferanca_orientacao = None
    orientacao_escolhida = None

    for orientacao, cor in dict_orientacoes_cores.items():
        orientacao_int = int(orientacao)
        diferenca_orientacao = orientacao_int - orientacao_analisada

        if menor_diferanca_orientacao is None:
            menor_diferanca_orientacao = diferenca_orientacao
            orientacao_escolhida = orientacao_int
        else:
            if abs(diferenca_orientacao) < abs(menor_diferanca_orientacao):
                menor_diferanca_orientacao = diferenca_orientacao
                orientacao_escolhida = orientacao_int

    if str(orientacao_escolhida) in dict_orientacoes_cores:
        cor_final = dict_orientacoes_cores[str(orientacao_escolhida)]
        return cor_final
    else:
        n = (orientacao_escolhida + 100) // 100
        indice_cor = n * faixa + menor_diferanca_orientacao

        cor_r = indice_cor // (256 * 256)
        cor_g = (indice_cor % (256 * 256)) // 256
        cor_b = (indice_cor % (256 * 256)) % 256

        cor_final = (cor_r, cor_g, cor_b)
        return cor_final


def converter_seg_para_min(tempo_segundos):
    minutos = tempo_segundos // 60
    segundos = tempo_segundos % 60
    print("{} minuto(s) e {} segundo(s)!".format(minutos, segundos))


def converter_seg_para_horas(tempo_segundos):
    horas = tempo_segundos // 3600
    minutos = (tempo_segundos % 3600) // 60
    segundos = ((tempo_segundos % 3600) % 60) % 60
    print("{} hora(s), {} minuto(s) e {} segundo(s)!".format(horas, minutos, segundos))


def plotar_grafico_linhas(eixo_x, eixo_y, nome_eixo_x="eixo x", nome_eixo_y="eixo y", nome_grafico="grafico"):
    plt.plot(eixo_x, eixo_y)
    plt.xlabel(nome_eixo_x)
    plt.ylabel(nome_eixo_y)
    plt.title(nome_grafico)
    plt.show()


def plotar_grafico_barras(eixo_x, eixo_y, nome_eixo_x="eixo x", nome_eixo_y="eixo y", nome_grafico="grafico"):
    plt.bar(eixo_x, eixo_y)
    plt.xlabel(nome_eixo_x)
    plt.ylabel(nome_eixo_y)
    plt.title(nome_grafico)
    plt.show()


def plotar_grafico_bolinhas(eixo_x, eixo_y, nome_eixo_x="eixo x", nome_eixo_y="eixo y", nome_grafico="grafico"):
    plt.scatter(eixo_x, eixo_y)
    plt.xlabel(nome_eixo_x)
    plt.ylabel(nome_eixo_y)
    plt.title(nome_grafico)
    plt.show()


def plotar_grafico_multiplas_linhas(matriz_linhas_eixo_y, lista_cores_linhas,
                                    nome_eixo_x="eixo x", nome_eixo_y="eixo y", nome_grafico="grafico"):

    for i in range(len(matriz_linhas_eixo_y)):
        plt.plot(matriz_linhas_eixo_y[i], color=lista_cores_linhas[i])

    plt.xlabel(nome_eixo_x)
    plt.ylabel(nome_eixo_y)
    plt.title(nome_grafico)
    plt.show()


def plotar_grafico_torta(valores_fatias_torta, nomes_das_fatias):
    total = sum(valores_fatias_torta)
    valores_fatias_torta_em_porcentagem = [porcentagem_relativa(total, i) for i in valores_fatias_torta]

    maior_fatia = max(valores_fatias_torta_em_porcentagem)
    lista_explode = []

    for fatia in valores_fatias_torta_em_porcentagem:
        if fatia == maior_fatia:
            lista_explode.append(0.1)
        else:
            lista_explode.append(0)

    plt.pie(valores_fatias_torta, explode=lista_explode, labels=nomes_das_fatias, autopct='%1.1f%%', shadow=True)
    plt.axis('equal')
    plt.show()


# obsoleto, funcao "transformar_pesos_em_cor_rgb_matplotlib" funciona para todos os pesos, n so de 0 a 10
def transformar_tupla_em_cor_rgb_matplotlib(tupla):
    cor = tuple(round(i/10, 1) for i in tupla)
    return cor


def transformar_pesos_em_cor_rgb_matplotlibt(tupla):
    maior_peso = max(tupla)
    cor_rgb = tuple(i/maior_peso for i in tupla)
    return cor_rgb


def gerar_nome_arquivo_lugares(nome_arquivo_matriz):
    nome_temp = nome_arquivo_matriz.strip(".txt")
    nome_final = nome_temp + "_lugares.txt"
    return nome_final


def gerar_nome_arquivo_caminhos(nome_arquivo_base):
    nome_temp = nome_arquivo_base.strip(".txt")
    nome_final = nome_temp + "_caminhos.txt"
    return nome_final


def correcao_arquivo_invertido(nome_arquivo_original, nome_novo_arquivo):
    lista_arquivo = arquivo_csv_para_lista(nome_arquivo_original)

    for lista in lista_arquivo:
        if lista[2] == 0:
            lista[2] = 1
        else:
            lista[2] = 0

    lista_para_arquivo_csv(lista_arquivo, nome_novo_arquivo)


def gerar_arquivo_lugares_com_id(nome_arquivo_original, nome_arquivo_lugares):
    # gera um arquivo lugares a partir de uma arquivo matriz
    # tem info sobre os id de cada coordenada, ou seja, ids dos lugares
    # os lugares sao salvos na forma = [id, lista coordenadas, cor, orientação]

    lista_lugares_temp = arquivo_csv_para_lista(nome_arquivo_original)
    lista_chaves = ["x", "y", "id"]
    lista_lugares_temp_2 = matriz_para_lista_dicionarios(lista_chaves, lista_lugares_temp)

    lista_dicts_orientacoes_cores = converter_orientacao_para_cor_v3(11)

    lista_orientacoes = list(range(0, 1100, 100))
    lista_ids = []
    lista_lugares_final = []

    for dicionario in lista_lugares_temp_2:

        if dicionario["id"] == 1:
            continue
        else:

            nova_coordenada = (dicionario["x"], dicionario["y"])

            if dicionario["id"] not in lista_ids:
                lista_ids.append(dicionario["id"])
                orientacao_escolhida = random.choice(lista_orientacoes)
                cor_escolhida = (0, 0, 0)

                for dicionario_2 in lista_dicts_orientacoes_cores:
                    if orientacao_escolhida == dicionario_2["orientacao"]:
                        cor_escolhida = dicionario_2["cor"]

                novo_lugar = {"id": dicionario["id"], "lista_coordenadas": [nova_coordenada], "cor": cor_escolhida,
                              "orientacao": orientacao_escolhida}

                lista_lugares_final.append(novo_lugar)

            else:
                for lugar in lista_lugares_final:
                    if dicionario["id"] == lugar["id"]:
                        lugar["lista_coordenadas"].append(nova_coordenada)

    matriz_lugares = lista_dicionarios_para_matriz(lista_lugares_final)
    lista_para_arquivo_csv(matriz_lugares, nome_arquivo_lugares)


def checar_existencia_arquivo(nome_arquivo):
    resultado = os.path.isfile(nome_arquivo)
    return resultado


def transformar_duas_listas_em_set(lista_1, lista_2):
    set_1 = set(lista_1)
    set_2 = set(lista_2)
    set_final = set_1.union(set_2)
    return set_final


def obter_media_aritimetica_simples(lista):
    media = sum(lista) / len(lista)
    return media


def obter_moda(lista):
    dict_contagem = obter_dict_contagem_elementos_repetidos_v2(lista)

    maior_ocorrencia = 0
    elemento_maior_ocorrencia = 0

    for key, value in dict_contagem.items():
        if value > maior_ocorrencia:
            maior_ocorrencia = value
            elemento_maior_ocorrencia = key

    return elemento_maior_ocorrencia


def obter_mediana(lista):
    lista.sort()
    # print("lista ordenada: ", lista)
    indice_meio = len(lista) // 2
    elemento_meio_lista = lista[indice_meio]
    return elemento_meio_lista


def sorteio_com_pesos(lista_possibilidades, lista_pesos, qnt_elementos_sorteados=1):
    lista_elementos_sorteados = random.choices(lista_possibilidades, weights=lista_pesos, k=qnt_elementos_sorteados)
    return lista_elementos_sorteados