from math import sqrt
import pygame as pg
from Modelo_5.ClasseAgenteV2 import AgenteV2
from Modelo_5.ClasseGridV2 import GridV2
from Modelo_5.ClasseLugarV2 import LugarV2
import funcoes
import cores
import pyautogui
import imageio

modelo=2
listaImagem=[]

def simulacao(grid, qnt_time_steps, numero_da_simulacao, pesosEscolhaLugar, pesosContaminacaoAgente, pesosContaminacaoLugar, iniciar_automaticamente=False, mov_randomico_agentes=False,
              nome_arquivo_caminhos_utlizado=None):

    pg.init()
    janela = pg.display.set_mode(grid.tamanho_tela)
    titulo = "testes modelo 5"
    pg.display.set_caption(titulo)
    relogio = pg.time.Clock()

    celula_selecionada = None
    comecar = iniciar_automaticamente
    uma_vez = True
    time_step = 0
    meta = qnt_time_steps
    controle_agentes = 0
    iniciar_time_step = True

    # RESULTADOS

    resultados = {"pesosContaminacaoAgente": pesosContaminacaoAgente,
                  "qnt_time_steps": qnt_time_steps,
                  "dict_ocr_ortcs": {},
                  "media_ortcs": 0,
                  "moda_ortcs": 0,
                  "mediana_ortcs": 0,
                  "lista_ent": [],
                  "lista_ent_med": [],
                  "delta_ent": 0,
                  "lugares_vizitados": []
                  }

    mainloop = True

    while mainloop is True:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                mainloop = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:

                    grid.remover_display_caminhos()

                    if celula_selecionada is not None:
                        if celula_selecionada.lugar is not None:
                            if celula_selecionada.lugar.display_caminhos is True:
                                celula_selecionada.lugar.display_caminhos = False

                            if celula_selecionada.lugar.display_celulas_acessiveis is True:
                                celula_selecionada.lugar.display_celulas_acessiveis = False
                                for celula in celula_selecionada.lugar.lista_celulas_grid_acessiveis:
                                    celula.cor = cores.branco

                    pos_mouse = pg.mouse.get_pos()
                    pos_mouse_grid = funcoes.converter_pos_para_coordenada_grid(pos_mouse, grid.cell_size)
                    celula_selecionada = grid.selecinar_nodulo(pos_mouse_grid)

                    if celula_selecionada.lugar is None:
                        if grid.permissao_criar_lugares_manuais is False:
                            # print("{}, nao ha lugar nessa celula".format(celula_selecionada.pos_grid))
                            if len(celula_selecionada.lista_agentes_presentes) == 0:
                                grid.mudar_estado_celula(celula_selecionada)
                        else:       # esta no modo de criar lugares manuais
                            if celula_selecionada not in grid.lista_coordenadas_lugar_temp:
                                celula_selecionada.mudar_cor(cores.cinza)
                                grid.lista_coordenadas_lugar_temp.append(celula_selecionada)
                            else:
                                celula_selecionada.mudar_cor(cores.branco)
                                grid.lista_coordenadas_lugar_temp.remove(celula_selecionada)
                    else:
                        # print("lugar atual: ", celula_selecionada.lugar.id)
                        # print("cel ocupadas: ", celula_selecionada.lugar.lista_coordenadas)
                        # print("orientacao: ", celula_selecionada.lugar.orientacao)
                        # print("-----------------------------------------------")
                        # celula_selecionada.lugar.display_caminhos = True
                        # if len(celula_selecionada.lugar.lista_celulas_grid_acessiveis) == 0:
                        #     celula_selecionada.lugar.achar_celulas_acessiveis(grid)
                        # celula_selecionada.lugar.display_celulas_acessiveis = True

                        # if len(celula_selecionada.lugar.lista_caminhos) == 0:
                        #     print("nao ha caminhos na lista")
                        # else:
                        print("\n")
                        print("lugar: ", celula_selecionada.lugar.id)
                        print("orientacao: ", celula_selecionada.lugar.orientacao)
                        print("cor: ", celula_selecionada.lugar.cor)
                        print("LISTA DE CAMINHOS: \n")
                        for dicionario in celula_selecionada.lugar.lista_caminhos:
                            print("destino: ", dicionario["destino"].id)
                            print("caminho analisado: ", dicionario["caminho_analisado"])
                            if dicionario["caminho_analisado"] is True:
                                print("possui caminho: ", dicionario["possui_caminho"])
                                if dicionario["possui_caminho"] is True:
                                    print("caminho: ", dicionario["caminho"])
                            print("*****************")

                        # if agente_teste.escolheu_destino is False:
                        #     lugar_atual_agente = None
                        #     if agente_teste.celula_grid.lugar is not None:
                        #         lugar_atual_agente = agente_teste.celula_grid.lugar
                        #     agente_teste.configuracoes_proximo_destino(grid, celula_selecionada.lugar, lugar_atual=lugar_atual_agente)
                        #     print("o agente escolheu o destino: ", agente_teste.destino_atual.id)
                        #     print("o destino esta em: ", agente_teste.destino_atual.lista_coordenadas)

                    if len(celula_selecionada.lista_agentes_presentes) > 0:
                        for agente in celula_selecionada.lista_agentes_presentes:
                            print("esta celula possui o agente: ", agente.id)
                            print("o agente tem orientacao latente: ", agente.orientacao_latente)
                            print("o agente possui orientacao atual: ", agente.orientacao_atual)
                            print("--------------------------------")

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if comecar is False:
                        comecar = True
                    else:
                        comecar = False

                if event.key == pg.K_s:
                    grid.salvar_caminhos_arquivo("arquivo_caminhos_teste_2.txt")
                    print("caminhos salvos")

                if event.key == pg.K_d:
                    grid.gerar_todos_caminhos()
                    print("caminhos gerados")

                if event.key == pg.K_f:
                    grid.resgatar_caminhos_arquivo("arquivo_caminhos_teste_2.txt")
                    grid.restaurar_caminhos_entre_lugares()
                    print("caminhos resgatados e restaurados")

                if event.key == pg.K_c:
                    grid.salvar_lugares_arquivo("arquivo_lugares_teste_3.txt")
                    print("lugares salvos")

                if event.key == pg.K_x:
                    grid.resgatar_lugares_arquivo("arquivo_lugares_teste_3.txt")
                    # grid.init_lista_caminho_lugares()
                    print("lugares resgatados")

                if event.key == pg.K_e:
                    grid.salvar_matriz_arquivo("arquivo_matriz_teste.txt")
                    print("matriz salva")

                if event.key == pg.K_r:
                    grid.resgatar_matriz_arquivo("arquivo_matriz_teste.txt")
                    print("matriz resgatada")

                if event.key == pg.K_m:     # deixando todos os lugares pretos
                    grid.todos_lugares_pretos()

                if event.key == pg.K_n:     # deixando todos os lugares com suas devidas cores
                    grid.restaurar_cor_lugares()

                if event.key == pg.K_p:     # colorindo o lugar escolhido a partir do id
                    grid.achar_lugar()

                if event.key == pg.K_q:
                    print(grid.lista_celulas_ocupadas)

                if event.key == pg.K_l:
                    if grid.permissao_criar_lugares_manuais is False:
                        grid.permissao_criar_lugares_manuais = True
                    else:
                        for celula in grid.lista_coordenadas_lugar_temp:
                            celula.mudar_cor(cores.branco)
                        grid.lista_coordenadas_lugar_temp.clear()
                        grid.permissao_criar_lugares_manuais = False

                if event.key == pg.K_RETURN and grid.permissao_criar_lugares_manuais is True:
                    grid.criar_lugar_manual()

                if event.key == pg.K_a:
                    id_lugar_inicial = int(input("digite o id do lugar inicial: "))
                    lugar_inicial = grid.obter_lugar_pelo_id(id_lugar_inicial)
                    id_lugar_final = int(input("digite o id do lugar final: "))
                    print("a_star_lugar_v2 --> 1")
                    print("a_star_lugar_v3 --> 2")
                    print("a_star_lugar_v4 --> 3")
                    tipo_a_star = int(input("digite o tipo do A*: "))

                    lugar_final = grid.obter_lugar_pelo_id(id_lugar_final)
                    resultado_procura_caminho = True
                    resultado_qnt_comparacoes = True
                    resultado_tempo = True

                    resultados = {}
                    if tipo_a_star == 1:
                        resultados = grid.a_star_lugar_v2(lugar_inicial, lugar_final,
                                                          retornar_procura_caminho=resultado_procura_caminho,
                                                          retornar_tempo=resultado_tempo)

                    elif tipo_a_star == 2:
                        resultados = grid.a_star_lugar_v3(lugar_inicial, lugar_final,
                                                          retornar_procura_caminho=resultado_procura_caminho,
                                                          retornar_qnt_comparacoes=resultado_qnt_comparacoes,
                                                          retornar_tempo=resultado_tempo)
                    elif tipo_a_star == 3:
                        resultados = grid.a_star_lugar_v4(lugar_inicial, lugar_final,
                                                          retornar_procura_caminho=resultado_procura_caminho,
                                                          retornar_qnt_comparacoes=resultado_qnt_comparacoes,
                                                          retornar_tempo=resultado_tempo)

                    if resultados is not None:
                        menor_caminho_agr = resultados["lista_refinada"]
                        grid.lista_menor_caminho_atual = menor_caminho_agr
                        grid.permissao_display_menor_caminho = True

                        if resultado_procura_caminho is True:
                            procura_menor_caminho_agr = resultados["lista_bruta"]
                            print("qnt celulas testadas: ", len(procura_menor_caminho_agr))
                            grid.lista_procura_caminho_atual = procura_menor_caminho_agr
                            grid.permissao_display_procura_caminho = True

                        if tipo_a_star == 2:
                            if resultado_qnt_comparacoes is True:
                                qnt_comparacoes_agr = resultados["qnt_comparacoes"]
                                print("foram feitas {} comparacoes".format(qnt_comparacoes_agr))

                        if resultado_tempo is True:
                            tempo_gasto = resultados["tempo_gasto"]
                            print("foram gastos {} segundos para achar o caminho".format(tempo_gasto))
                    else:
                        print("nenhum caminho foi encontrado")

                if event.key == pg.K_h:
                    for agente in grid.lista_agentes:
                        lugar_escolhido = agente.escolher_lugar_v2(grid)
                        print("o escolhido pelo o agente eh: ", lugar_escolhido.id)

                if event.key == pg.K_t:
                    grid.gerar_todos_caminhos()

                if event.key == pg.K_j:
                    if len(grid.lista_caminhos) == 0:
                        print("n ha caminhos gravados")
                    else:
                        for dicionario in grid.lista_caminhos:
                            print("lugar {} e lugar {}".format(dicionario["lugar_1"], dicionario["lugar_2"]))
                            print("caminho analisado: ", dicionario["caminho_analisado"])
                            if dicionario["caminho_analisado"] is True:
                                print("possui caminho: ", dicionario["possui_caminho"])
                                if dicionario["possui_caminho"] is True:
                                    print("caminho: ", dicionario["caminho"])
                            print("----------------------")
                        print("qnt de caminhos na lista: ", len(grid.lista_caminhos))

        if comecar is True:
            if mov_randomico_agentes is True:

                for agente in grid.lista_agentes:
                    agente.update_posicao_randomica(grid)

            if mov_randomico_agentes is False:
                if time_step == 0 and uma_vez is True:
                    print("-- INICIO DA SIMULACAO {} -- / PESOS = {} \n".format(numero_da_simulacao, pesosEscolhaLugar))
                    uma_vez = False

                if iniciar_time_step is True:
                    print("INICIO DO TIME STEP: {} \n".format(time_step))
                    # for agente in grid.lista_agentes:
                        # print("agente {} tem orientacao: {}".format(agente.id, agente.orientacao_latente))
                    iniciar_time_step = False

                for agente in grid.lista_agentes:
                    if agente.chegou_destino is True:
                        continue

                    if agente.escolheu_destino is False:
                        lugar_atual_agente = None
                        if agente.celula_grid.lugar is not None:
                            lugar_atual_agente = agente.celula_grid.lugar
                        lugar_escolhido = agente.escolher_lugar_v4(grid,pesosEscolhaLugar)
                        agente.atualizar_lugares_vizitados(lugar_escolhido.id)
                        # print("lugar escolhido: ", lugar_escolhido.id)
                        # print("diferenca de orientacao: ", abs(agente.orientacao_latente - lugar_escolhido.orientacao))
                        agente.configuracoes_proximo_destino(grid, lugar_escolhido, lugar_atual=lugar_atual_agente)

                    if agente.escolheu_destino is True:
                        if agente.chegou_destino is False:
                            agente.update_posicao(grid)
                            for coordenada in agente.destino_atual.lista_coordenadas:
                                if agente.pos_grid == coordenada:
                                    agente.contaminacao_agente(grid, agente.destino_atual.orientacao, pesosContaminacaoAgente)
                                    agente.configuracoes_chegou_destino()
                                    controle_agentes += 1
                                    break

                if controle_agentes == AgenteV2.qnt_agentes:
                    for lugar in grid.lista_lugares:
                        if len(lugar.lista_agentes_presentes) > 0:
                            # print("o lugar sofre contaminacao")
                            # print("o lugar tinha uma orientacao de: ", lugar.orientacao)
                            lugar.contaminacao_lugar(pesosContaminacaoLugar,mudar_cor=True, grid=grid)
                            # print("agora o lugar tem um orientacao de: ", lugar.orientacao)
                        lista_agentes_id = [i.id for i in lugar.lista_agentes_presentes]
                        # print("lugar: ", lugar.id)
                        # print("agentes presentes: ", lista_agentes_id)
                        lugar.lista_agentes_presentes.clear()

                    for agente in grid.lista_agentes:
                        agente.chegou_destino = False

                    print("FIM DO TIME STEP: {}".format(time_step))
                    xxx=pyautogui.screenshot(region=(347,42,672,680))
                    passagem="C:\\Users\\julio\\Desktop\\resultados\\modelo{}\\imagem{}.png".format(modelo,time_step)
                    xxx.save(passagem)
                    listaImagem.append(imageio.imread(passagem))
                    time_step += 1
                    controle_agentes = 0
                    iniciar_time_step = True

                    entropia_atual = grid.calcular_entropia()
                    # print("a entropia foi de: ", entropia_atual)
                    resultados["lista_ent"].append(entropia_atual)

                    entropia_media_atual = round(sum(resultados["lista_ent"]) / len(resultados["lista_ent"]), 3)
                    # print("a entropia media eh de: ", entropia_media_atual)
                    resultados["lista_ent_med"].append(entropia_media_atual)

                    dict_orientacoes_ocorrencias_temp = grid.obter_dict_ocorrencia_orientacoes()
                    if len(resultados["dict_ocr_ortcs"]) == 0:
                        resultados["dict_ocr_ortcs"] = dict_orientacoes_ocorrencias_temp
                        # print("lista orientacoes: ", dict_orientacoes_ocorrencias_temp)
                    else:
                        # print("lista orientacoes antiga: ", resultados["dict_ocr_ortcs"])
                        # print("lista orientacoes nova: ", dict_orientacoes_ocorrencias_temp)
                        lista_temp = funcoes.obter_lista_com_elementos_repetidos(resultados["dict_ocr_ortcs"])
                        lista_temp_2 = funcoes.obter_lista_com_elementos_repetidos(dict_orientacoes_ocorrencias_temp)
                        lista_temp.extend(lista_temp_2)
                        dict_orientacoes_ocorrencias_final = funcoes.obter_dict_contagem_elementos_repetidos_v2(lista_temp)
                        # print("lista orientacoes atualizada: ", dict_orientacoes_ocorrencias_final)
                        resultados["dict_ocr_ortcs"] = dict_orientacoes_ocorrencias_final

                if time_step == meta:
                    print("-- FIM DA SIMULACAO {} -- / PESOS: {}".format(numero_da_simulacao, pesosContaminacaoAgente))

                    for agente in grid.lista_agentes:
                        agente.resgatar_estado_inicial()

                    for lugar in grid.lista_lugares:
                        lugar.resgatar_estado_inicial()

                    if nome_arquivo_caminhos_utlizado is not None:
                        grid.salvar_caminhos_arquivo_v2(nome_arquivo_caminhos_utlizado)

                    lista_orientacoes_com_repeticoes = funcoes.obter_lista_com_elementos_repetidos(resultados["dict_ocr_ortcs"])
                    lista_usavel = [int(i) for i in lista_orientacoes_com_repeticoes]
                    resultados["media_ortcs"] = funcoes.obter_media_aritimetica_simples(lista_usavel)
                    resultados["moda_ortcs"] = funcoes.obter_moda(lista_usavel)
                    resultados["mediana_ortcs"] = funcoes.obter_mediana(lista_usavel)
                    resultados["delta_ent"] = round(resultados["lista_ent_med"][-1] - resultados["lista_ent_med"][0], 3)
                    imageio.mimsave("C:\\Users\\julio\\Desktop\\resultados\\modelo{}\\vid.gif".format(modelo), listaImagem, duration=0.1)
                    arq=open("C:\\Users\\julio\\Desktop\\resultados\\modelo{}\\lugaresVizitados.txt".format(modelo),"w")
                    for agente in grid.lista_agentes:
                        #resultados["lugares_vizitados"].append((agente.id,agente.lugares_vizitados))
                        linha=""
                        linha+=str(agente.id)+"#"
                        for lugar in agente.lugares_vizitados:
                            linha+=str(lugar)+"@"
                        arq.write(linha.strip("@"))
                        arq.write("\n")
                    arq.close
                    mainloop = False

        grid.update_grid(janela)
        pg.display.update()
        relogio.tick(60)

    return resultados


