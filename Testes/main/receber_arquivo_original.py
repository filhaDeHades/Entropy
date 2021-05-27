import Modelo_5.funcoes_arquivos as func_arq
import os


# dando infos sobre o arquivo recebido
nome_arquivo_recebido = "new_york_ID.txt"
qnt_linhas = 1000
qnt_colunas = 1000
tipo_do_arquivo = 2

path_arquivos_originis = "..\\arquivos\\arquivos_originais"
arquivo_original = os.path.join(path_arquivos_originis, nome_arquivo_recebido)

nome_arquivo_base = func_arq.gerar_nome_arquivo_base(nome_arquivo_recebido, qnt_linhas, qnt_colunas, tipo_do_arquivo)
path_arquivos_base = "..\\arquivos\\arquivos_base"
nome_arquivo_base_com_path = os.path.join(path_arquivos_base, nome_arquivo_base)

# func_arq.copiar_e_renomear_arquivo(arquivo_original, nome_arquivo_base_com_path)

path_arquivos_lugares = "..\\arquivos\\arquivos_lugares"
func_arq.criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=path_arquivos_base,
                               path_arquivos_lugares=path_arquivos_lugares)


