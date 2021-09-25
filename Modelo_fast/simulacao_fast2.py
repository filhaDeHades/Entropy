
import Modelo_5.funcoes_arquivos as func_arq
import Modelo_fast.funcoes_fast as fst
import Testes.src.funcoes_geracao_nomes as fgn
import pandas as pd


def simulacao_fast2(grid, pesos=(1, 1, 1), numero_da_simulacao=0, qnt_time_steps=30, time_step_atual=0,
                    pesos_escolha_lugar=(0.1, 0.1), salvar_caminhos_arquivo=False, nome_arquivo_base=None,
                    distancia_importa=True, retornar_info_lugares=False, retornar_info_agentes=False,
                    salvar_dados_lugares=False, nome_arquivo_lugares=None, nome_arquivo_lugares_dinamicos=None,
                    salvar_dados_agentes=False, nome_arquivo_agentes=None):

    df_agentes_arquivo = None

    if salvar_dados_agentes is True:
        if nome_arquivo_agentes is None:
            df_agentes_arquivo = pd.DataFrame()
        else:
            df_agentes_arquivo = pd.read_csv(nome_arquivo_agentes)

    df_lugares_arquivo = None

    if salvar_dados_lugares is True:
        if nome_arquivo_lugares_dinamicos is None:
            df_lugares_arquivo = pd.DataFrame()
        else:
            df_lugares_arquivo = pd.read_csv(nome_arquivo_lugares_dinamicos)

    resultados_staticos = {"qnt_linhas": [grid.qnt_linhas],
                           "qnt_colunas": [grid.qnt_colunas],
                           "peso_a": [pesos[0]],
                           "peso_b": [pesos[1]],
                           "peso_c": [pesos[2]],
                           "qnt_agentes": [len(grid.array_agentes)],
                           "qnt_lugares": [len(grid.array_lugares)],
                           "qnt_time_steps": [qnt_time_steps],
                           }
    
    

    if nome_arquivo_base is not None:
        nome_arquivo_resultado_ts = func_arq.gerar_nome_arquivo_resultados_ts(nome_arquivo_base, numero_da_simulacao)
        resultados_staticos["res_time_steps"] = [nome_arquivo_resultado_ts]

    resultados_ts = {"0": [],
                     "100": [],
                     "200": [],
                     "300": [],
                     "400": [],
                     "500": [],
                     "600": [],
                     "700": [],
                     "800": [],
                     "900": [],
                     "1000": [],
                     "lista_ent": []
                     }

    dict_inicial_agentes = {str(i): [] for i in range(qnt_time_steps)}
    df_agentes = pd.DataFrame(dict_inicial_agentes)
    lista_colunas_df_agentes = list(df_agentes.columns)

    dict_inicial_lugares = {str(i): [] for i in range(qnt_time_steps)}
    df_lugares = pd.DataFrame(dict_inicial_lugares)
    lista_colunas_df_lugares = list(df_lugares.columns)

    for time_step in range(time_step_atual, time_step_atual+qnt_time_steps):

        # if time_step == 0:
        #     pass
        #     print('INICIO DA SIMULACAO {} / PESOS = {}'.format(numero_da_simulacao, pesos))
        #     print("\n")
        #     # print("AGENTES NO INICIO DA SIMULACAO {}:".format(numero_da_simulacao))
        #     # for agente in grid.array_agentes:
        #     #     print("agente ", agente.id)
        #     #     print("orientacao latente: ", agente.orientacao_latente)
        #     #     print("orientacao atual: ", agente.orientacao_atual)
        #     #     print("-------------------------------------------")
        #
        print('TIME STEP {}'.format(time_step))
        print('\n')

        for agente in grid.array_agentes:
            # print("o agente {} vai escolher um lugar".format(agente.id))
            if salvar_caminhos_arquivo is True:
                lugar_escolhido = agente.escolher_lugar_v4(grid)
            else:
                if distancia_importa is True:
                    lugar_escolhido = agente.escolher_lugar_v5(grid.array_lugares, lista_pesos=pesos_escolha_lugar)
                    # lugar_escolhido = fst.escolher_lugar_menor_e(agente, grid.array_lugares)
                else:
                    lugar_escolhido = fst.escolher_lugar_mais_parecido_v2(agente, grid.array_lugares)
                    # lugar_escolhido = fst.escolher_lugar_mais_parecido(agente, grid.array_lugares)

            agente.celula_grid.lugar = lugar_escolhido
            agente.celula_grid = lugar_escolhido.array_celulas_grid[0]

            # print("o agente {} ({}) escolheu o lugar {} ({})".format(agente.id, agente.orientacao_atual,
            #                                                          lugar_escolhido.id, lugar_escolhido.orientacao))

            # coordenada_escolhida = lugar_escolhido.achar_coordenada_principal(agente.pos_grid)
            # print("distancia: ", fst.obter_distancia_manhattan(agente.pos_grid, coordenada_escolhida))

            lugar_escolhido.lista_agentes_presentes.append(agente)
            agente.contaminacao_agente(lugar_escolhido.orientacao, pesos)
            agente.sortear_nova_orientacao()

            coluna_atual = lista_colunas_df_agentes[time_step]
            df_agentes.loc[agente.id, coluna_atual] = agente.orientacao_latente

        if salvar_dados_agentes is True:
            nome_coluna = "time_step_" + str(time_step)
            orientacoes_atuais_agentes = [i.orientacao_atual for i in grid.array_agentes]
            df_agentes_arquivo[nome_coluna] = orientacoes_atuais_agentes

        for lugar in grid.array_lugares:

            if len(lugar.lista_agentes_presentes) > 0:
                lugar.contaminacao_lugar(mudar_cor=True, grid=grid)
                lugar.lista_agentes_presentes.clear()

            coluna_atual = lista_colunas_df_lugares[time_step]
            df_lugares.loc[lugar.id, coluna_atual] = lugar.orientacao
            # print("o lugar {} tem orientacao de {}".format(lugar.id, lugar.orientacao))

        if salvar_dados_lugares is True:
            nome_coluna = "time_step_" + str(time_step)
            orientacoes_lugares = [i.orientacao for i in grid.array_lugares]
            df_lugares_arquivo[nome_coluna] = orientacoes_lugares

        # print(df_lugares[lista_colunas_df_lugares[time_step]])
        # print("---------------------------------------------")

            # if len(grid.lista_caminhos) == 0:
        #     print("n ha caminhos salvos na lista do grid")
        # else:
        #     for dicionario in grid.lista_caminhos:
        #         print(dicionario)

        entropia_atual = grid.calcular_entropia_geral()
        # print("a entropia foi de: ", entropia_atual)
        resultados_ts["lista_ent"].append(entropia_atual)

        ocorrencia_orientacoes = grid.obter_dict_ocorrencia_orientacoes()

        for orientacao in resultados_ts:
            for key, value in ocorrencia_orientacoes.items():
                if orientacao == key:
                    resultados_ts[key].append(value)

        # print("orientacoes do time step {}: ".format(time_step))
        # for key, value in ocorrencia_orientacoes.items():
        #     print("{}: {} vezes".format(key, value))
        #
        # print("FIM DO TIME STEP: {}\n".format(time_step))

    if salvar_dados_lugares is True:
        grid.salvar_lugares_arquivo(nome_arquivo_lugares)

        nome_arquivo_lugares_ts = nome_arquivo_lugares_dinamicos

        if nome_arquivo_lugares_ts is None:
            nome_arquivo_lugares_ts = fgn.gerar_nome_arquivo_info_lugares_dinamicos(nome_arquivo_lugares)

        df_lugares_arquivo.to_csv(nome_arquivo_lugares_ts, index=False)

    if salvar_dados_agentes is True:
        df_agentes_arquivo.to_csv(nome_arquivo_agentes, index=False)

    for agente in grid.array_agentes:
        agente.resgatar_estado_inicial()

    for lugar in grid.array_lugares:
        lugar.resgatar_estado_inicial()

    if salvar_caminhos_arquivo is True:
        nome_arquivo_caminhos = func_arq.gerar_nome_arquivo_caminhos(nome_arquivo_base)
        path_arquivos_caminhos = "C:\\Users\\lucas\\PycharmProjects\\Pratica_IC\\Arquivos_caminhos"
        nome_arquivo_caminhos_com_path = fst.obter_path_completo_arquivo(path_arquivos_caminhos, nome_arquivo_caminhos)
        grid.criar_ou_atualizar_arquivo_caminhos(nome_arquivo_caminhos_com_path)

    # print("AGENTES NO FINAL DA SIMULACAO:")
    # for agente in grid.array_agentes:
    #     print("agente ", agente.id)
    #     print("orientacao latente: ", agente.orientacao_latente)
    #     print("orientacao atual: ", agente.orientacao_atual)
    #     print("-------------------------------------------")

    # print("-- FIM DA SIMULACAO {} -- / PESOS: {}".format(numero_da_simulacao, pesos))

    # print("RESULTADOS STATICOS: ")
    # for key, value in resultados_staticos.items():
    #     print("{}: {}".format(key, value))
    #
    # print("----------------")
    #
    # print("RESULTADOS TIME STEPS: ")
    # for key, value in resultados_ts.items():
    #     print("{}: {}".format(key, value))

    resultados_finais = {"resultados_staticos": resultados_staticos, "resultados_ts": resultados_ts}

    if retornar_info_agentes is True:
        resultados_finais["resultados_agentes"] = df_agentes

    if retornar_info_lugares is True:
        resultados_finais["resultados_lugares"] = df_lugares

    return resultados_finais

