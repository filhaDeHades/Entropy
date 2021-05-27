from Testes.src import funcoes_geracao_nomes as fgn
import pandas as pd
import numpy as np

arq = "..\\arquivos\\arquivos_lugares_dinamicos\\new_york_ID(1000x1000)[tipo_2]_info_lugares_dinamicos.txt"
df = pd.read_csv(arq)

colunas = df.columns.tolist()

dict_colunas = {coluna: fgn.string_to_id(coluna) for coluna in colunas}
# print(dict_colunas)

colunas_int = [fgn.string_to_id(coluna) for coluna in colunas]
colunas_int.sort()
# print(colunas_int)

colunas_novas = [fgn.id_to_string("lugar_", i) for i in colunas_int]
# print(colunas_novas)

df = df[colunas_novas]
df.to_csv(arq, index=False)


a = np.arange(0.1, 1.0, 0.1)
print(a)
