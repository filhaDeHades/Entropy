import Modelo_5.funcoes_arquivos as func_arq
import Modelo_fast.funcoes_fast as fst
from Modelo_fast.ClasseGridV2Fast import GridV2Fast

nome = "SaoPaulo_6-7v2.txt"
# nome_com_path = func_arq.obter_path_completo_arquivo_base(nome)

matriz_layout_temp = fst.arquivo_csv_para_lista(nome)
print("primeira transformacao: ")
fst.contar_linhas_e_colunas_matriz(matriz_layout_temp)

matriz_layout_temp2 = [i[2] for i in matriz_layout_temp]
print(" qnt elementos lista: ", len(matriz_layout_temp2))


qnt_linhas = 1000
qnt_colunas = 1000

matriz_layout_final = fst.transformar_lista_em_matriz(matriz_layout_temp2, qnt_linhas, qnt_colunas)
print("terceira transformacao: ")
fst.contar_linhas_e_colunas_matriz(matriz_layout_final)
