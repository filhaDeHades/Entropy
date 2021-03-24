from Modelo_fast.simulacao_fast2 import simulacao_fast2
from Modelo_fast.ClasseGridV2Fast import GridV2Fast
import matplotlib.pyplot as plt
import pandas as pd

qnt_linhas = 100
qnt_colunas = 100

grid = GridV2Fast(qnt_linhas, qnt_colunas)

qnt_agentes = 10
grid.gerar_agentes_aleatorios_v3(qnt_agentes)

qnt_lugares = 10
tamanho_lugar = 10
grid.gerar_lugares_aleatorios_v2(qnt_lugares, tamanho_lugar)

time_steps = 600

resultados = simulacao_fast2(grid, qnt_time_steps=time_steps, retornar_info_agentes=True, retornar_info_lugares=True,
                             pesos_escolha_lugar=(0.2, 1))

df_agentes = resultados["resultados_agentes"]
df_lugares = resultados["resultados_lugares"]

# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(df_agentes)

qnt_linhas, qnt_colunas = df_agentes.shape
eixo_x = list(range(qnt_colunas))

for linha in range(qnt_linhas):

    lista_orientacoes_agente = list(df_agentes.iloc[linha])
    plt.plot(eixo_x, lista_orientacoes_agente, color=(1, 0, 0))

    lista_orientacoes_lugar = list(df_lugares.iloc[linha])
    plt.plot(eixo_x, lista_orientacoes_lugar, color=(0, 0, 1))

plt.grid(True)
plt.show()
