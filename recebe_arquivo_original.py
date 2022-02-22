import Modelo_5.funcoes_arquivos as func_arq
import os

def recebe_Arquivo(nome_arquivo, tamanho_x, tamanho_y, tipo):
    """Recebe um arquivo original e renomeia ele de forma a possibilitar
    a utilização do mesmo no programa. O arquivo renomeado é colocado na
    pasta Arquivos/Arquivos_base

    Args:
        nome_arquivo (string): nome do arquivo (adicionar o ".txt" ao final)
        tamanho_x (int): Número de colunas da matriz
        tamanho_y (int): Número de linhas da matriz
        tipo (int): Tipo do arquivo (Quais informações ele contém)
    """

    nome_arquivo_base = func_arq.recebimento_arquivo_original(nome_arquivo, tamanho_x, tamanho_y, tipo)
    path_arquivos_base = "Arquivos\\Arquivos_base"

    path_arquivos_lugares = "Arquivos\\Arquivos_lugares"
    func_arq.criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=path_arquivos_base,
                                    path_arquivos_lugares=path_arquivos_lugares)


if __name__ == "__main__":
    info = input('Digite o nome, nº de linhas, nº de colunas e tipo do arquivo: ')
    list_info = info.split()

    recebe_Arquivo(list_info[0], int(list_info[1]), int(list_info[2]), int(list_info[3]))