# import matplotlib.pyplot as plt
import numpy as np

# a = np.random.rand(71, 71)

# fig, ax1 = plt.subplots()
# grafico1 = ax1.pcolor(a, cmap="OrRd", vmin=0)
# fig.colorbar(grafico1, ax=ax1)

# # eixo x
# ax1.set_xticks(np.linspace(1, 71, 5))
# eixo_x = np.linspace(0.1, 1.50, 5)
# eixo_x = [round(i, 2) for i in eixo_x]
# ax1.set_xticklabels(eixo_x)
# ax1.set_xlabel("valores de B")


# # eixo y
# ax1.set_yticks(np.linspace(1, 71, 5))
# eixo_y = eixo_x
# ax1.set_yticklabels(eixo_y)
# ax1.set_ylabel("valores de A")

# ax1.set_title("entropia agentes / contaminação (1, 0.1) X pesos (a, b)")
# plt.show()

# peso_contaminacao_agente = np.linspace(0.1, 0.001, 5)
# peso_contaminacao_agente = [round(i, 3) for i in peso_contaminacao_agente]
# peso_contaminacao_lugar = np.linspace(0.1, 0.001, 5)

# print(peso_contaminacao_agente)

a = np.array([(0, 1), (1, 2)])
b = np.array([(0, 1), (2, 3)])

for i in a:
    for j in b:

        if i[0] == j[0] and i[1] == j[1]:
            print(i)