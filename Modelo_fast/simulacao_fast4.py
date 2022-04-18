import Testes.src.funcoes_geracao_nomes as fgn
import pandas as pd


# simulacao ja aceita por padrao que eh o modelo fabiano
def simulacao_fast4(grid, pesosContaminacaoAgente=(1, 0.1), pesosContaminacaoLugar=(1, 0.1), 
                pesosEscolhaLugar=(0.1, 0.1), qntTimeSteps=30):

    # data frame da simulacao com info que n muda ao longo do tempo
    resultadosStaticos = {  "tamGrid" :                     [(grid.qnt_linhas, grid.qnt_colunas)],
                            "pesosContaminacaoAgente" :     [pesosContaminacaoAgente],
                            "pesosContaminacaoLugar" :      [pesosContaminacaoLugar],
                            "pesosEscolhaLugar" :           [pesosEscolhaLugar],
                            "qntAgentes" :                  [grid.qnt_agentes],
                            "qntLugares" :                  [grid.qnt_lugares],
                            "qntTimeSteps" :                [qntTimeSteps]
                        }

    resultados_entropia = {
                            "entropia_agentes": [],
                            "entropia_lugares": [],
                            "entropia_geral": []
    }

    df_agentes = pd.DataFrame()
    df_lugares = pd.DataFrame()

    for timeStep in range(qntTimeSteps):

        # print("\n-------------------------------------------------------\n")
        print("TIME STEP ", timeStep)
        # print("\n-------------------------------------------------------\n")

        dict_agentes = {}

        for agente in grid.array_agentes:

            # print("AGENTE {}:".format(agente.id))
            # print("pos: ", agente.pos_grid)
            # print("orientacao: ", agente.orientacao_latente)

            lugarEscolhido = agente.escolher_lugar(grid.array_lugares, pesosEscolhaLugar)
            # print("o agente {} de orientacao {} escolheu o lugar {} de orientacao {}".format(agente.id, agente.orientacao_latente, lugarEscolhido.id, lugarEscolhido.orientacao))

            lugarEscolhido.lista_agentes_presentes.append(agente)
            lista_agentes_presentes_id = [i.id for i in lugarEscolhido.lista_agentes_presentes]
            # print("o Lugar {} agr tem os agentes: {}".format(lugarEscolhido.id, lista_agentes_presentes_id))

            agente.contaminacao_agente(grid, lugarEscolhido.orientacao, pesosContaminacaoAgente)
            # print("o agente agr tem orientacao: {}".format(agente.orientacao_latente))

            dict_agentes["agente_{}".format(agente.id)] = round(agente.orientacao_latente)

            # print("-------------------------------------------------------")

        df_agentes = df_agentes.append(dict_agentes, ignore_index=True)

        dict_lugares = {}

        for lugar in grid.array_lugares:

            # print("LUGAR {}:".format(lugar.id))
            # print("pos: ", lugar.array_coordenadas)
            # print("orientacao: ", lugar.orientacao)

            if len(lugar.lista_agentes_presentes) > 0:
                # print("qnt agentes no lugar: ", len(lugar.lista_agentes_presentes))
                lugar.contaminacao_lugar(pesosContaminacaoLugar)
                # print("orientacao pos contaminacao: ", lugar.orientacao)
                lugar.lista_agentes_presentes.clear()

            dict_lugares["lugar_{}".format(lugar.id)] = round(lugar.orientacao)

            # print("-------------------------------------------------------")

        df_lugares = df_lugares.append(dict_lugares, ignore_index=True)

        entropia_agentes = grid.calcular_entropia_agentes()
        resultados_entropia["entropia_agentes"].append(entropia_agentes)

        entropia_lugares = grid.calcular_entropia_lugares()
        resultados_entropia["entropia_lugares"].append(entropia_lugares)

        entropia_geral = grid.calcular_entropia_geral()
        resultados_entropia["entropia_geral"].append(entropia_geral)

    for agente in grid.array_agentes:
        agente.resgatar_estado_inicial()
    
    for lugar in grid.array_lugares:
        lugar.resgatar_estado_inicial()

    df_agentes = fgn.ordenar_colunas_df_por_id(df_agentes, "agente_")
    df_lugares = fgn.ordenar_colunas_df_por_id(df_lugares, "lugar_")

    
    
    df_resultados_staticos = pd.DataFrame(resultadosStaticos)
    df_resultados_entropia = pd.DataFrame(resultados_entropia)

    resultados_finais = {"resultados_staticos": df_resultados_staticos,
                         "resultados_agentes": df_agentes,
                         "resultados_lugares": df_lugares,
                         "resultados_entropia": df_resultados_entropia
                         }

    return resultados_finais
    
