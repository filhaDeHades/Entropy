import Testes.src.funcoes_geracao_nomes as fgn
import pandas as pd


def simulacao1D(grid, pesosContaminacaoAgente=(1, 0.1), pesosContaminacaoLugar=(1, 0.1), 
                pesosEscolhaLugar=(0.1, 0.1), qntTimeSteps=30, modelo_fabiano=False):

    # data frame da simulacao com info que n muda ao longo do tempo
    resultadosStaticos = {  "tamGrid" :                     [grid.tamGrid],
                            "pesosContaminacaoAgente" :     [pesosContaminacaoAgente],
                            "pesosContaminacaoLugar" :      [pesosContaminacaoLugar],
                            "pesosEscolhaLugar" :           [pesosEscolhaLugar],
                            "qntAgentes" :                  [grid.qntAgentes],
                            "qntLugares" :                  [grid.qntLugares],
                            "qntTimeSteps" :                [qntTimeSteps]
                        }

    # data frame com info que muda conforme os time steps
    resultadosTimeSteps = {}

    # inicializando o data frame (resultadosTimeSteps) que contem info de ocorrencia de orientacoes e entropias
    for orientacao in grid.listaDeOrientacoes:
        resultadosTimeSteps[str(orientacao)] = []
    resultadosTimeSteps["listaEntropias"] = []

    resultados_entropia = {
                            "entropia_agentes": [],
                            "entropia_lugares": [],
                            "entropia_geral": []
    }

    df_agentes = pd.DataFrame()

    df_lugares = pd.DataFrame()

    for timeStep in range(qntTimeSteps):

        # print("-------------------------------------------------------")
        # print("TIME STEP ", timeStep)
        # print("-------------------------------------------------------")

        dict_agentes = {}

        for agente in grid.arrayAgentes:

            # print("AGENTE {}:".format(agente.id))
            # print("pos: ", agente.posicao)
            # print("orientacao: ", agente.orientacaoLatente)

            if modelo_fabiano is False:
                lugarEscolhido = agente.escolherLugar(grid.arrayLugares, pesosEscolhaLugar)
            else:
                lugarEscolhido = agente.escolher_lugar_v2(grid.arrayLugares, pesosEscolhaLugar)
                # print("escolheu o lugar {} - orientacao {}".format(lugarEscolhido.id, lugarEscolhido.orientacao))

            lugarEscolhido.listaAgentesPresentes.append(agente)

            if modelo_fabiano is False:
                agente.contaminacaoAgente(lugarEscolhido, pesosContaminacaoAgente)
                agente.sortearNovaOrientacao(grid.listaDeOrientacoes)
                agente.sortear_nova_posicao(grid.tamGrid)
            else:
                agente.contaminacao_agente_v2(lugarEscolhido, pesosContaminacaoAgente)
                # print("orientacao pos contaminacao: ", agente.orientacaoLatente)

            dict_agentes["agente_{}".format(agente.id)] = round(agente.orientacaoLatente)

            # print("-------------------------------------------------------")

        df_agentes = df_agentes.append(dict_agentes, ignore_index=True)

        dict_lugares = {}

        for lugar in grid.arrayLugares:

            # print("LUGAR {}:".format(lugar.id))
            # print("pos: ", lugar.posicao)
            # print("orientacao: ", lugar.orientacao)

            if len(lugar.listaAgentesPresentes) > 0:
                # print("qnt agentes no lugar: ", len(lugar.listaAgentesPresentes))
                lugar.contaminacaoLugar(pesos=pesosContaminacaoLugar)
                # print("orientacao pos contaminacao: ", lugar.orientacao)
                lugar.listaAgentesPresentes.clear()

            dict_lugares["lugar_{}".format(lugar.id)] = round(lugar.orientacao)

            # print("-------------------------------------------------------")

        df_lugares = df_lugares.append(dict_lugares, ignore_index=True)

        entropia_agentes = grid.calcular_entropia_v2()
        resultadosTimeSteps["listaEntropias"].append(entropia_agentes)
        resultados_entropia["entropia_agentes"].append(entropia_agentes)

        entropia_lugares = grid.calcular_entropia_lugares()
        resultados_entropia["entropia_lugares"].append(entropia_lugares)

        entropia_geral = grid.calcular_entropia_geral()
        resultados_entropia["entropia_geral"].append(entropia_geral)

        if modelo_fabiano is False:
            ocorrenciaOrientacoes = grid.obterDictOcorrenciaOrientacoesAgentes()
        else:
            ocorrenciaOrientacoes = grid.obterDictOcorrenciaOrientacoesAgentes_v2()

        for orientacao, ocorrencia in ocorrenciaOrientacoes.items():
            resultadosTimeSteps[orientacao].append(ocorrencia)

    for agente in grid.arrayAgentes:
        agente.resgatarEstadoInicial()
    
    for lugar in grid.arrayLugares:
        lugar.resgatarEstadoInicial()

    df_agentes = fgn.ordenar_colunas_df_por_id(df_agentes, "agente_")
    df_lugares = fgn.ordenar_colunas_df_por_id(df_lugares, "lugar_")
    
    df_resultados_staticos = pd.DataFrame(resultadosStaticos)
    df_resultados_time_steps = pd.DataFrame(resultadosTimeSteps)
    df_resultados_entropia = pd.DataFrame(resultados_entropia)

    resultados_finais = {"resultados_staticos": df_resultados_staticos,
                         "resultados_time_steps": df_resultados_time_steps,
                         "resultados_agentes": df_agentes,
                         "resultados_lugares": df_lugares,
                         "resultados_entropia": df_resultados_entropia}

    return resultados_finais



