from Modelo_fast.simulacao_fast2 import simulacao_fast2
from Modelo_fast.ClasseGridV2Fast import GridV2Fast
import Modelo_5.funcoes_arquivos as func_arq
import Modelo_fast.funcoes_fast as fst
import Modelo_fast.gerar_graficos as gg
import pandas as pd


def simulacao_com_arquivo(nome_arquivo_base, pesos=(1, 1, 1), pesos_escolha_lugar=(0.1, 0.1), qnt_agentes=100,
                          qnt_time_steps=30, usar_e_salvar_caminhos=False, salvar_resultados=False, num_sim_atual=0,
                          distancia_importa=True, mostrar_grafico_entropia=False, retornar_resultados_ts=False,
                          salvar_lugares_modificados=False, nome_arquivo_lugares_modificado=None):

    qnt_linhas, qnt_colunas = func_arq.obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base)
    grid = GridV2Fast(qnt_linhas, qnt_colunas)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base)
    path_arquivos_lugares = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares"
    nome_arquivo_lugares_com_path = fst.obter_path_completo_arquivo(path_arquivos_lugares, nome_arquivo_lugares)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares_com_path)

    grid.gerar_agentes_aleatorios_v3(qnt_agentes)

    if usar_e_salvar_caminhos is True:

        nome_arquivo_caminhos = func_arq.gerar_nome_arquivo_caminhos(nome_arquivo_base)
        path_arquivo_caminhos = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_caminhos"
        nome_arquivo_caminhos_com_path = fst.obter_path_completo_arquivo(path_arquivo_caminhos, nome_arquivo_caminhos)
        existencia_arquivo_caminhos = fst.checar_existencia_arquivo(nome_arquivo_caminhos_com_path)

        if existencia_arquivo_caminhos is True:
            grid.resgatar_caminhos_arquivo(nome_arquivo_caminhos_com_path)
            grid.restaurar_caminhos_entre_lugares()

        resultados = simulacao_fast2(grid, pesos=pesos, pesos_escolha_lugar=pesos_escolha_lugar,
                                     numero_da_simulacao=num_sim_atual, qnt_time_steps=qnt_time_steps,
                                     salvar_caminhos_arquivo=True, nome_arquivo_base=nome_arquivo_base,
                                     distancia_importa=distancia_importa)
    else:
        resultados = simulacao_fast2(grid, pesos=pesos, pesos_escolha_lugar=pesos_escolha_lugar,
                                     numero_da_simulacao=num_sim_atual, qnt_time_steps=qnt_time_steps,
                                     salvar_caminhos_arquivo=False, nome_arquivo_base=nome_arquivo_base,
                                     distancia_importa=distancia_importa)

    resultados_staticos = resultados["resultados_staticos"]
    resultados_ts = resultados["resultados_ts"]

    if salvar_resultados is True:

        nome_arq_resultados_staticos = func_arq.gerar_nome_arquivo_resultados(nome_arquivo_base)
        path_resultados_staticos = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_resultados"
        fst.criar_ou_atualizar_arquivo_resultados(path_resultados_staticos, nome_arq_resultados_staticos,
                                                  resultados_staticos)

        nome_arq_resultados_ts = func_arq.gerar_nome_arquivo_resultados_ts(nome_arquivo_base, num_sim=num_sim_atual)
        path_resultados_ts = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_resultados_ts"
        fst.criar_ou_atualizar_arquivo_resultados(path_resultados_ts, nome_arq_resultados_ts, resultados_ts)

    if mostrar_grafico_entropia is True:

        df = pd.DataFrame(resultados_ts)
        lista_entropia = gg.obter_lista_entropias(df)
        lista_entropia_media = gg.obter_lista_entropias_media(lista_entropia)
        eixo_x = list(range(0, qnt_time_steps+1))
        gg.obter_grafico_evolucao_entropia_media(lista_entropia_media, eixo_x)

    if retornar_resultados_ts is True:
        df = pd.DataFrame(resultados_ts)
        return df

    if salvar_lugares_modificados is True:
        path_arquivos_lugares = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares"
        nome_novo_arquivo_lugares_com_path = fst.obter_path_completo_arquivo(path_arquivos_lugares, nome_arquivo_lugares_modificado)
        grid.salvar_lugares_arquivo(nome_novo_arquivo_lugares_com_path)


if __name__ == '__main__':

    lista_arquivos_base = ["new_york_ID(1000x1000)[tipo_2].txt",  # 0
                           "SaoPaulo_6-7v2(1000x1000)[tipo_1].txt"  # 1
                           ]

    nome_arquivo_base_utilizado = lista_arquivos_base[0]
    nome_arquivo_lugares_temp = func_arq.gerar_nome_arquivo_lugares(nome_arquivo_base_utilizado)
    nome_arquivo_lugares_temp = nome_arquivo_lugares_temp.strip(".txt")
    nome_arquivo_lugares_final = nome_arquivo_lugares_temp + "v2.txt"

    path_arquivos_lugares = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_lugares"
    nome_arquivo_lugares_final_com_path = fst.obter_path_completo_arquivo(path_arquivos_lugares,
                                                                          nome_arquivo_lugares_final)

    simulacao_com_arquivo(nome_arquivo_base_utilizado, salvar_lugares_modificados=True,
                          nome_arquivo_lugares_modificado=nome_arquivo_lugares_final)
