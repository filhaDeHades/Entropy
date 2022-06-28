from Modelo_5.simulacao import *
import Modelo_5.simulacao2 as s2
import Modelo_5.funcoes_arquivos as func_arq
import os

path_base_projeto = "Arquivos\\Arquivos_lugares\\"

# info compartilhadas
peso_teste = (1, 1, 1)
qnt_time_steps_teste = 1000
numero_simulacao_teste = 0
iniciar_automaticamente_teste = False


def simulacao_1():
    qnt_linhas = 42
    qnt_colunas = 42
    tamanho_celula = 10
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout)
    grid.permissao_display_linhas_grid = False

    nome_arquivo_base_utilizado = "new_york_ID100x100.txt"
    nome_arquivo_lugares = funcoes.gerar_nome_arquivo_lugares(nome_arquivo_base_utilizado)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares)

    qnt_agentes = 50
    grid.gerar_agentes_aleatorios(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    resultados = simulacao(peso_teste, grid, qnt_time_steps_teste, numero_simulacao_teste,
                               iniciar_automaticamente_teste, mov_randomico_agentes=True)


def simulacao_2():
    qnt_linhas = 350
    qnt_colunas = 350
    tamanho_celula = 2
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout)
    grid.permissao_display_linhas_grid = False

    nome_arquivo_base_utilizado = "new_york_ID350x350.txt"
    nome_arquivo_lugares = funcoes.gerar_nome_arquivo_lugares(nome_arquivo_base_utilizado)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares)

    qnt_agentes = 50
    grid.gerar_agentes_aleatorios(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    resultados = simulacao(peso_teste, grid, qnt_time_steps_teste, numero_simulacao_teste,
                           iniciar_automaticamente_teste, mov_randomico_agentes=True)


def simulacao_3():
    qnt_linhas = 21
    qnt_colunas = 21
    tamanho_celula = 30

    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout)
    grid.permissao_display_linhas_grid = True

    qnt_agentes = 10
    grid.gerar_agentes_aleatorios_v2(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    qnt_lugares = 10
    tamanho_max_lugar = 10
    grid.gerar_lugares_aleatorios_v2(qnt_lugares, tamanho_max_lugar)

    resultados = simulacao(peso_teste, grid, qnt_time_steps_teste, numero_simulacao_teste)


def simulacao_com_arquivo():

    lista_arquivos_base = ["modelo1(42x42)[tipo_1].txt"]

    # lista_arquivos_base = ["new_york_ID(1000x1000)[tipo_2].txt",    # 0
    #                        "SaoPaulo_6-7v2(1000x1000)[tipo_1].txt"  # 1
    #                        ]

    nome_arquivo_base_utilizado = lista_arquivos_base[0]

    tam_grid = func_arq.obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base_utilizado)
    qnt_linhas = tam_grid[0]
    qnt_colunas = tam_grid[1]
    tamanho_celula = 5
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout)

    qnt_agentes = 100
    grid.gerar_agentes_aleatorios_v2(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base_utilizado)
    nome_arquivo_lugares_completo = func_arq.obter_path_completo_arquivo_lugares(nome_arquivo_lugares)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_completo)
    print("foram resgatados {} lugares, vindos do arquivo {}".format(len(grid.lista_lugares), nome_arquivo_base_utilizado))

    resultados = simulacao(peso_teste, grid, qnt_time_steps_teste, numero_simulacao_teste)


def simulacao_manual():
    qnt_linhas = 100
    qnt_colunas = 100
    tamanho_celula = 7

    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout)
    grid.permissao_display_linhas_grid = False

    for linha in grid.matriz_celulas:
        for celula in linha:
            celula.display_cor_de_calor = True

    qnt_agentes = 0
    grid.gerar_agentes_aleatorios_v2(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    qnt_lugares = 100
    tam_lugar = 50

    grid.gerar_lugares_aleatorios_v2(qnt_lugares, tam_lugar)

    resultados = simulacao(peso_teste, grid, qnt_time_steps_teste, numero_simulacao_teste)


def simulacao_com_arquivo_2():

    #lista_arquivos_base = ["modelo6(42x42)[tipo_1].txt"]
    lista_arquivos_base = ["new_york_ID(42x42)[tipo_2].txt"]

    # lista_arquivos_base = ["new_york_ID(1000x1000)[tipo_2].txt",  # 0
    #                        "SaoPaulo_6-7v2(1000x1000)[tipo_1].txt"  # 1
    #                        ]

    nome_arquivo_base_utilizado = lista_arquivos_base[0]

    tam_grid = func_arq.obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base_utilizado)
    qnt_linhas = tam_grid[0]
    qnt_colunas = tam_grid[1]
    print(f'\nQUANTIDADE DE LINHAS: {qnt_linhas}\nQUANTIDADE DE COLUNAS: {qnt_colunas}\n')
    #quit(1)
    tamanho_celula = 10
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas, qnt_colunas)
    grid = GridV2(qnt_linhas, qnt_colunas, tamanho_celula, matriz_layout, display_agentes=False)

    print(f'\nQUANTIDADE DE LINHAS: {grid.largura}\nQUANTIDADE DE COLUNAS: {grid.altura}\n')

    qnt_agentes = 1000
    grid.gerar_agentes_aleatorios_v2(qnt_agentes, sem_cor_repetida=False, sem_orientacao_repetida=False)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base_utilizado)
    # nome_arquivo_lugares_completo = func_arq.obter_path_completo_arquivo_lugares(nome_arquivo_lugares)

    nome_arquivo_lugares_completo = path_base_projeto + nome_arquivo_lugares      #"C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares\\new_york_ID(1000x1000)[tipo_2]_lugaresv2.txt"
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_completo)
    print("foram resgatados {} lugares, vindos do arquivo {}".format(len(grid.lista_lugares),
                                                                     nome_arquivo_base_utilizado))
    s2.simulacao2(peso_teste, grid, qnt_time_steps_teste)


def simulacao_com_arquivo_V(arquivo, timesteps=2000, fQA=2.5, peso_escolha_lugar=(0.1, 0.1), peso_cont_agente=(1,1), peso_cont_lugar=(1,1)):

    qnt_time_steps = timesteps
    pesos_escolha_lugar = peso_escolha_lugar
    pesos_agente = peso_cont_agente
    pesos_lugar = peso_cont_lugar

    resultados = s2.simulacao_utiliza_arquivo(arquivo, pesos_escolha_lugar=pesos_escolha_lugar, peso_cont_agente=pesos_agente,
                                        peso_cont_lugar=pesos_lugar, qnt_time_steps=qnt_time_steps, fQA= fQA,
                                        salvar_resultados=True, mostrar_grafico_entropia=True, retornar_resultados_ts=False)
    
    # info_agentes = resultados["resultados_agentes"]
    # info_lugares = resultados["resultados_lugares"]
    # info_entropia = resultados["resultados_entropia"]

    