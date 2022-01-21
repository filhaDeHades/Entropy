import Modelo_5.funcoes_arquivos as func_arq
import Modelo_fast.funcoes_fast as fst
import Testes.src.funcoes_geracao_nomes as fgn
import pandas as pd


def simulacao_fast3(grid, pesos=(1, 1, 1), numero_da_simulacao=0, qnt_time_steps=30, time_step_atual=0,
                    pesos_escolha_lugar=(0.1, 0.1), modelo_fabiano=False, salvar_dados_agentes=False,
                    nome_arquivo_agentes=None, atualizar_agentes=False, salvar_dados_lugares=False,
                    nome_arquivo_lugares=None, atualizar_lugares=False):

    # DATA FRAME AGENTES (colunas: id agentes / linhas: time steps / valores: orientação do agente no time step
    df_agentes = None

    if salvar_dados_agentes is True:
        if nome_arquivo_agentes is not None:

            df_agentes = pd.read_csv(nome_arquivo_agentes)

            # caso seja a primeira vez que o arquivo estaja sendo usado, tirando a linha e coluna desnecessárias
            # isso acontece q o pandas não aceita ler um arquivo vazio e transformar em um DataFrame vazio
            if "teste" in df_agentes.columns:
                df_agentes.drop(columns="teste", inplace=True)
                df_agentes.drop([0], inplace=True)

            # atualizando a orientacao latente do ultimo time step salvo (que foi guardado em arquivo)
            if atualizar_agentes is True:
                qnt_linhas_agentes, qnt_colunas_agentes = df_agentes.shape
                ultima_linha_agentes = list(df_agentes.iloc[qnt_linhas_agentes-1])

                for agente, orientacao in zip(grid.array_agentes, ultima_linha_agentes):
                    agente.orientacao_latente = orientacao

    # DATA FRAME LUGARES (colunas: id lugares / linhas: time steps / valores: orientação do lugar no time step
    df_lugares = None

    if salvar_dados_lugares is True:
        if nome_arquivo_lugares is not None:

            df_lugares = pd.read_csv(nome_arquivo_lugares)

            # removendo lixo / ver explicação da linha 20  21
            if "teste" in df_lugares.columns:
                df_lugares.drop(columns="teste", inplace=True)
                df_lugares.drop([0], inplace=True)

            # atualizando a oirnetação dos lugares do ultimo time step salvo (que foi guardado em arquivo)
            if atualizar_lugares is True:
                qnt_linhas_lugares, qnt_colunas_lugares = df_lugares.shape
                ultima_linha_lugares = list(df_lugares.iloc[qnt_linhas_lugares-1])

                for lugar, orientacao in zip(grid.array_lugares, ultima_linha_lugares):
                    lugar.orientacao = orientacao


    # DATA FRAME ENTROPIA (colunas: entropia de agentes, lugares e ambos / linhas: time steps / valores: entropia em
    # um time step
    resultados_entropia = {
                            "entropia_agentes": [],
                            "entropia_lugares": [],
                            "entropia_geral":   []
    }

    for time_step in range(time_step_atual, qnt_time_steps):

        print("time step {}".format(time_step))

        dict_agentes = {}

        for agente in grid.array_agentes:

            lugar_escolhido = agente.escolher_lugar_v5(grid.array_lugares, lista_pesos=pesos_escolha_lugar,
                                                       modelo_fabiano=modelo_fabiano)

            lugar_escolhido.lista_agentes_presentes.append(agente)
            agente.contaminacao_agente(lugar_escolhido.orientacao, pesos_escolha_lugar, modelo_fabiano=modelo_fabiano)

            dict_agentes["agente_{}".format(agente.id)] = round(agente.orientacao_latente)

            if modelo_fabiano is False:
                agente.atualizar_posicao_grid(grid, lugar_escolhido.array_coordenadas[0])
                agente.sortear_nova_orientacao()

        df_agentes = df_agentes.append(dict_agentes, ignore_index=True)

        dict_lugares = {}

        for lugar in grid.array_lugares:

            if len(lugar.lista_agentes_presentes) > 0:
                lugar.contaminacao_lugar(pesos_escolha_lugar)
                lugar.lista_agentes_presentes.clear()

            dict_lugares["lugar_{}".format(lugar.id)] = round(lugar.orientacao)

        df_lugares = df_lugares.append(dict_lugares, ignore_index=True)

        entropia_agentes = grid.calcular_entropia()
        resultados_entropia["entropia_agentes"].append(entropia_agentes)

        entropia_lugares = grid.calcular_entropia_lugares()
        resultados_entropia["entropia_lugares"].append(entropia_lugares)

        entropia_geral = grid.calcular_entropia_geral()
        resultados_entropia["entropia_geral"].append(entropia_geral)

    if salvar_dados_agentes is True:
        if nome_arquivo_agentes is not None:
            df_agentes.to_csv(nome_arquivo_agentes, index=False)

    if salvar_dados_lugares is True:
        if nome_arquivo_lugares is not None:
            df_lugares.to_csv(nome_arquivo_lugares, index=False)

    df_entropias = pd.DataFrame(resultados_entropia)

    resultados_finais = {"resultados_agentes": df_agentes, "resultados_lugares": df_lugares,
                         "resultados_entropia": df_entropias}

    return resultados_finais
