import pygame as pg
import cores


def simulacao2(pesos, grid, qnt_time_steps=30):
    pg.init()
    janela = pg.display.set_mode(grid.tamanho_tela)
    titulo = "testes modelo 5"
    pg.display.set_caption(titulo)

    comecar = False
    time_step = 0

    # deixando todos os lugares pretos para ver a mudanca de cores
    # for lugar in grid.lista_lugares:
    #     lugar.cor = cores.preto

    mainloop = True

    while mainloop is True:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                mainloop = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if comecar is False:
                        comecar = True
                    else:
                        comecar = False

                if event.key == pg.K_t:
                    grid.atualizar_cor_lugares()

        if comecar is True:

            print("inicio do time step ", time_step)

            for agente in grid.lista_agentes:
                lugar_escolido = agente.escolher_lugar_v5(grid.lista_lugares)
                coordenada_principal = lugar_escolido.achar_coordenada_principal_v2(agente.pos_grid)
                agente.atualizar_pos_grid(grid, coordenada_principal)
                agente.celula_grid.lugar = lugar_escolido
                lugar_escolido.lista_agentes_presentes.append(agente)
                agente.contaminacao_agente(grid, lugar_escolido.orientacao, pesos)

            for lugar in grid.lista_lugares:
                if len(lugar.lista_agentes_presentes) > 0:
                    lugar.contaminacao_lugar(grid=grid)
                    print("o lugar {} mudou de cor".format(lugar.id))
                lugar.lista_agentes_presentes.clear()

            if time_step == qnt_time_steps:

                for agente in grid.lista_agentes:
                    agente.resgatar_estado_inicial()

                for lugar in grid.lista_lugares:
                    lugar.resgatar_estado_inicial()

                mainloop = False

            else:
                time_step += 1

        grid.update_grid(janela)
        pg.display.update()
