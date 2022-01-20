from Modelo_fast.simulacao_fast3 import simulacao_fast3
from Modelo_fast.ClasseGridV2Fast import GridV2Fast
import Modelo_5.funcoes_arquivos as func_arq
import Testes.src.funcoes_geracao_nomes as fgn
import os

lista_arquivos_base = ["new_york_ID(1000x1000)[tipo_2].txt"]


# escolhendo o arquivo base e criando o grid
arquivo_base_escolhido = lista_arquivos_base[0]
qnt_linhas, qnt_colunas = func_arq.obter_tam_grid_pelo_nome_arquivo(arquivo_base_escolhido)
grid = GridV2Fast(qnt_linhas, qnt_colunas)


# recuperando os lugares (staticos) do arquivo
nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(arquivo_base_escolhido)
nome_dir_arq_lugares = "..\\arquivos\\arquivos_lugares"
path_arq_lugares = os.path.abspath(nome_dir_arq_lugares)
nome_arquivo_lugares_completo = os.path.join(path_arq_lugares, nome_arquivo_lugares)
grid.resgatar_lugares_arquivo(nome_arquivo_lugares_completo)


# recuperando os agentes (staticos) do arquivo
nome_arq_agentes_staticos = fgn.gear_nome_arquivo_info_agentes_staticos(arquivo_base_escolhido)
nome_dir_arq_agentes_staticos = "..\\arquivos\\arquivos_agentes_staticos"
path_arq_agentes_staticos = os.path.abspath(nome_dir_arq_agentes_staticos)
nome_arq_agentes_staticos_completo = os.path.join(path_arq_agentes_staticos, nome_arq_agentes_staticos)
grid.resgatar_agentes_arquivo(nome_arq_agentes_staticos_completo)


# recuperando o arquivo de lugares (dinamicos)
nome_arq_lugares_dinamicos = fgn.gerar_nome_arquivo_info_lugares_dinamicos(arquivo_base_escolhido)
nome_dir_lugares_dinamicos = "..\\arquivos\\arquivos_lugares_dinamicos"
path_arq_lugares_dinamicos = os.path.abspath(nome_dir_lugares_dinamicos)
nome_arq_lugares_dinamicos_completo = os.path.join(path_arq_lugares_dinamicos, nome_arq_lugares_dinamicos)


# recuperando o arquivo de agentes (dinamicos)
nome_arq_agentes_dinamicos = fgn.gerar_nome_arquivo_info_agentes_dinamicos(arquivo_base_escolhido)
nome_dir_agentes_dinamicos = "..\\arquivos\\arquivos_agentes_dinamicos"
path_arq_agentes_dinamicos = os.path.abspath(nome_dir_agentes_dinamicos)
nome_arq_agentes_dinamicos_completo = os.path.join(path_arq_agentes_dinamicos, nome_arq_agentes_dinamicos)


# parametros para a simulacao
qnt_time_steps = 4
pesos_contaminacao = (1, 1, 1)
pesos_escolha_lugar = (0.1, 0.1)
modelo_fabiano = False


# executando a simulacao e obtendo resultados

resultados = simulacao_fast3(grid, pesos=pesos_contaminacao, qnt_time_steps=qnt_time_steps,
                             pesos_escolha_lugar=pesos_escolha_lugar, modelo_fabiano=modelo_fabiano,
                             salvar_dados_agentes=True, nome_arquivo_agentes=nome_arq_agentes_dinamicos_completo,
                             atualizar_agentes=True, salvar_dados_lugares=True,
                             nome_arquivo_lugares=nome_arq_lugares_dinamicos_completo, atualizar_lugares=True)
