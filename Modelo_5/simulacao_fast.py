import funcoes
import Modelo_5.funcoes_arquivos as func_arq


def simulacao_fast(pesos, grid, numero_da_simulacao, qnt_time_steps, salvar_caminhos_arquivo=False,
                   nome_arquivo_base=None):

    resultados = {"pesos_sim": pesos,
                  "qnt_time_steps": qnt_time_steps,
                  "dict_ocr_ortcs": {},
                  "media_ortcs": 0,
                  "moda_ortcs": 0,
                  "mediana_ortcs": 0,
                  "lista_ent": [],
                  "lista_ent_med": [],
                  "delta_ent": 0
                  }

    for time_step in range(qnt_time_steps):

        if time_step == 0:
            print('INICIO DA SIMULACAO {} / PESOS = {}'.format(numero_da_simulacao, pesos))
            print("\n")
        print('TIME STEP {}'.format(time_step))
        print('\n')

        for agente in grid.lista_agentes:
            # print("o agente {} vai escolher um lugar".format(agente.id))
            if salvar_caminhos_arquivo is True:
                lugar_escolhido = agente.escolher_lugar_v4(grid)
            else:
                lugar_escolhido = funcoes.escolher_lugar_menor_e(agente, grid.lista_lugares)

            agente.celula_grid = lugar_escolhido.lista_celulas_grid[0]
            print("o agente {} escolheu o lugar {}".format(agente.id, lugar_escolhido.id))
            lugar_escolhido.lista_agentes_presentes.append(agente)
            agente.contaminacao_agente(grid, lugar_escolhido.orientacao, pesos, atualizar_cor=True)
            agente.sortear_nova_orientacao()

        for lugar in grid.lista_lugares:
            if len(lugar.lista_agentes_presentes) > 0:
                lugar.contaminacao_lugar()
                lugar.lista_agentes_presentes.clear()

        if len(grid.lista_caminhos) == 0:
            print("n ha caminhos salvos na lista do grid")
        else:
            for dicionario in grid.lista_caminhos:
                print(dicionario)

        entropia_atual = grid.calcular_entropia()
        print("a entropia foi de: ", entropia_atual)
        resultados["lista_ent"].append(entropia_atual)

        entropia_media_atual = round(sum(resultados["lista_ent"]) / len(resultados["lista_ent"]), 3)
        print("a entropia media eh de: ", entropia_media_atual)
        resultados["lista_ent_med"].append(entropia_media_atual)

        dict_orientacoes_ocorrencias_temp = grid.obter_dict_ocorrencia_orientacoes()
        if len(resultados["dict_ocr_ortcs"]) == 0:
            resultados["dict_ocr_ortcs"] = dict_orientacoes_ocorrencias_temp
        else:
            print("lista orientacoes: ", dict_orientacoes_ocorrencias_temp)
            # print("lista orientacoes antiga: ", resultados["dict_ocr_ortcs"])
            # print("lista orientacoes nova: ", dict_orientacoes_ocorrencias_temp)
            lista_temp = funcoes.obter_lista_com_elementos_repetidos(resultados["dict_ocr_ortcs"])
            lista_temp_2 = funcoes.obter_lista_com_elementos_repetidos(dict_orientacoes_ocorrencias_temp)
            lista_temp.extend(lista_temp_2)
            dict_orientacoes_ocorrencias_final = funcoes.obter_dict_contagem_elementos_repetidos_v2(lista_temp)
            print("lista orientacoes atualizada: ", dict_orientacoes_ocorrencias_final)
            resultados["dict_ocr_ortcs"] = dict_orientacoes_ocorrencias_final

        print("FIM DO TIME STEP: {}\n".format(time_step))

    lista_orientacoes_com_repeticoes = funcoes.obter_lista_com_elementos_repetidos(resultados["dict_ocr_ortcs"])
    lista_usavel = [int(i) for i in lista_orientacoes_com_repeticoes]
    resultados["media_ortcs"] = funcoes.obter_media_aritimetica_simples(lista_usavel)
    resultados["moda_ortcs"] = funcoes.obter_moda(lista_usavel)
    resultados["mediana_ortcs"] = funcoes.obter_mediana(lista_usavel)
    resultados["delta_ent"] = round(resultados["lista_ent_med"][-1] - resultados["lista_ent_med"][0], 3)

    for agente in grid.lista_agentes:
        agente.resgatar_estado_inicial()

    for lugar in grid.lista_lugares:
        lugar.resgatar_estado_inicial()

    if salvar_caminhos_arquivo is True:
        nome_arquivo_caminhos = func_arq.gerar_nome_arquivo_caminhos(nome_arquivo_base)
        grid.salvar_caminhos_arquivo_v2(nome_arquivo_caminhos)

    print("-- FIM DA SIMULACAO {} -- / PESOS: {}".format(numero_da_simulacao, pesos))

    return resultados
