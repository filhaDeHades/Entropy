from Modelo_fast.apresentacoes_fast2 import simulacao_com_arquivo
import Modelo_fast.gerar_graficos as gg

lista_arquivos_base = ["modelo1(42x42)[tipo_1].txt",    # 0
                       "modelo2(42x42)[tipo_1].txt",    # 1
                       "modelo4(42x42)[tipo_1].txt",    # 2
                       "modelo5(42x42)[tipo_1].txt",    # 3
                       "modelo6(42x42)[tipo_1].txt"]    # 4


arquivo_usado = lista_arquivos_base[1]

pesos_a = [2, 4]
pesos_b = [2, 4]
pesos_c = [2, 4]

qnt_time_steps_teste = 30

multiplo_inicial = gg.descobrir_multiplo_incial_cores(pesos_a, pesos_b, pesos_c)

matriz_entropias_medias = []
lista_cores = []

num_sim = 0

for a in pesos_a:
    for b in pesos_b:
        for c in pesos_c:

            pesos_atual = (a, b, c)
            cor_linha = gg.descobir_cor_rgb(multiplo_inicial, a, b, c)
            lista_cores.append(cor_linha)

            df = simulacao_com_arquivo(arquivo_usado, pesos=pesos_atual, qnt_agentes=10,
                                       qnt_time_steps=qnt_time_steps_teste, salvar_resultados=False,
                                       num_sim_atual=num_sim, retornar_resultados_ts=True)

            lista_entropias_normal = gg.obter_lista_entropias(df)
            lista_entropias_medias = gg.obter_lista_entropias_media(lista_entropias_normal)
            matriz_entropias_medias.append(lista_entropias_medias)

            num_sim += 1
            print("arquivo {} / simulacao {} finalizada!".format(arquivo_usado, num_sim))

eixo_x = list(range(0, qnt_time_steps_teste+1))

gg.gerar_grafico_multiplas_linhas(eixo_x, matriz_entropias_medias, lista_cores)
