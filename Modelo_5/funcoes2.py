def obter_distancia(pos_grid_inicial, pos_grid_final, custo_menor_mov=10, custo_maior_mov=14):

    dx = abs(pos_grid_final[0] - pos_grid_inicial[0])
    dy = abs(pos_grid_final[1] - pos_grid_inicial[1])

    if dx > dy:
        distancia = custo_maior_mov * dy + custo_menor_mov * (dx - dy)
    else:
        distancia = custo_maior_mov * dx + custo_menor_mov * (dy - dx)

    return distancia
