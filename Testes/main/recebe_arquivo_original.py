import Modelo_5.funcoes_arquivos as func_arq
import os

def recebe_Arquivo(nome_arquivo, tamanho_x, tamanho_y, tipo):
    #path_arquivos_originis = "..\\arquivos\\arquivos_originais"
    #arquivo_original = os.path.join(path_arquivos_originais, nome_arquivo)

    nome_arquivo_base = func_arq.recebimento_arquivo_original(nome_arquivo, tamanho_x, tamanho_y, tipo)
    path_arquivos_base = "Arquivos\\Arquivos_base"
    #nome_arquivo_base_com_path = os.path.join(path_arquivos_base, nome_arquivo_base)

    path_arquivos_lugares = "Arquivos\\Arquivos_lugares"
    func_arq.criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=path_arquivos_base,
                                    path_arquivos_lugares=path_arquivos_lugares)
    
info = input('Digite o nome, nº de linhas, nº de colunas e tipo do arquivo: ')
list_info = info.split()

recebe_Arquivo(list_info[0], int(list_info[1]), int(list_info[2]), int(list_info[3]))