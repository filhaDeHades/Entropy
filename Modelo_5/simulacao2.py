import Modelo_5.funcoes_arquivos as func_arq
from Modelo_5.ClasseGridV2 import GridV2
from Modelo_5.simulacao import simulacao
import Modelo_5.apresentacoes as apr
import pygame as pg
import cores
import time


path_base_projeto = "Arquivos\\"

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

def simulacao_utiliza_arquivo(nome_arquivo_base, pesos=(1, 1, 1), pesos_escolha_lugar=(0.1, 0.1), peso_cont_agente=(1, 1), peso_cont_lugar=(1, 1),
                          qnt_time_steps=30, usar_e_salvar_caminhos=False, salvar_resultados=False, num_sim_atual=0,
                          distancia_importa=True, mostrar_grafico_entropia=False, retornar_resultados_ts=False,
                          salvar_lugares_modificados=False, nome_arquivo_lugares_modificado=None):
    
    qnt_linhas, qnt_colunas = func_arq.obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base)
    nome = func_arq.obter_path_completo_arquivo_base(nome_arquivo_base)
    matriz_layout = func_arq.criar_matriz_layout(nome)
    grid = GridV2(qnt_linhas, qnt_colunas, 10, matriz_layout, qnt_orientacoes=1000)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base)
    path_arquivos_lugares = f"Arquivos\\Arquivos_lugares\\"
    nome_arquivo_lugares_com_path = func_arq.obter_path_completo_arquivo(path_arquivos_lugares, nome_arquivo_lugares)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_com_path)
    print("RESGATOU")
    time.sleep(5)
    
    grid.gerar_agentes_aleatorios_v2(sem_cor_repetida=True)

    if usar_e_salvar_caminhos is True:

        nome_arquivo_caminhos = func_arq.gerar_nome_arquivo_caminhos(nome_arquivo_base)
        path_arquivo_caminhos =f"Arquivos_caminhos\\{nome_arquivo_caminhos}"
        nome_arquivo_caminhos_com_path = func_arq.obter_path_completo_arquivo( path_arquivo_caminhos)
        existencia_arquivo_caminhos = func_arq.checar_existencia_arquivo(nome_arquivo_caminhos_com_path)

        if existencia_arquivo_caminhos is True:
            grid.resgatar_caminhos_arquivo(nome_arquivo_caminhos_com_path)
            grid.restaurar_caminhos_entre_lugares()

        resultados = simulacao([pesos_escolha_lugar, peso_cont_agente, peso_cont_lugar], grid, qnt_time_steps, 1, nome_arquivo_base)
        #resultados = simulacao2([pesos_escolha_lugar, peso_cont_agente, peso_cont_lugar], grid, qnt_time_steps)
    else:
        resultados = simulacao([pesos_escolha_lugar, peso_cont_agente, peso_cont_lugar], grid, qnt_time_steps, 1, nome_arquivo_base)
        #resultados = simulacao2([pesos_escolha_lugar, peso_cont_agente, peso_cont_lugar], grid, qnt_time_steps)
        
    #resultados_staticos = resultados["resultados_staticos"]

    if salvar_resultados is True:
        pass
        # nome_arq_resultados_staticos = func_arq.gerar_nome_arquivo_resultados(nome_arquivo_base)
        # path_resultados_staticos = path_base_projeto + "Arquivos_resultados"
        # func_arq.criar_ou_atualizar_arquivo_resultados(path_resultados_staticos, nome_arq_resultados_staticos,)


    if salvar_lugares_modificados is True:
        path_arquivos_lugares = path_base_projeto + "Arquivos_lugares"
        nome_novo_arquivo_lugares_com_path = func_arq.obter_path_completo_arquivo(path_arquivos_lugares, nome_arquivo_lugares_modificado)
        grid.salvar_lugares_arquivo(nome_novo_arquivo_lugares_com_path)


    #tem resultado

    return resultados