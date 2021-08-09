import Modelo_5.funcoes_arquivos as func_arq
import os

def cria_Invertido():
    try:
        path_arquivos_base = "Arquivos\\Arquivos_base"
        path_arquivos_originais = "Arquivos\\Arquivos_originais\\"
        path_arquivos_lugares = "Arquivos\\Arquivos_lugares"

        info = input('Digite o nome, nº de linhas, nº de colunas e tipo do arquivo: ')
        list_info = info.split()

        novo_nome = input('Qual deve ser o novo nome do arquivo? ')

        novo_nome = novo_nome + '.txt'

        list_info[0] = path_arquivos_originais + list_info[0]

        func_arq.corrigir_arquivo_invertido(list_info[0], path_arquivos_originais + novo_nome)

        nome_arquivo_base = func_arq.recebimento_arquivo_original(novo_nome, list_info[1], list_info[2], list_info[3])
        print(nome_arquivo_base)

        func_arq.criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=path_arquivos_base, path_arquivos_lugares=path_arquivos_lugares)


    except:
        print("Erro ao inverter arquivo")