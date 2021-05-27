from Modelo_5.simulacao_fast import simulacao_fast
from Modelo_5.ClasseGridV2 import GridV2
import Modelo_5.funcoes_arquivos as func_arq
import funcoes


def simulacao_com_arquivo(nome_arquivo):
    nome_arquivo_base_1 = nome_arquivo

    arquivo_base_utilizado = nome_arquivo_base_1

    qnt_linhas_teste, qnt_colunas_teste = func_arq.obter_tam_grid_pelo_nome_arquivo(arquivo_base_utilizado)
    matriz_layout = funcoes.obter_grid_manual(qnt_linhas_teste, qnt_colunas_teste)
    tamanho_celula_inutil = 1
    grid = GridV2(qnt_linhas_teste, qnt_colunas_teste, tamanho_celula_inutil, matriz_layout)

    nome_arquivo_lugares = func_arq.gerar_nome_arquivo_lugares(arquivo_base_utilizado)
    print("o nome do arquivo lugares eh: ", nome_arquivo_lugares)
    grid.resgatar_lugares_arquivo(nome_arquivo_lugares)
    print("foram resgatados {} lugares".format(len(grid.lista_lugares)))

    qnt_agentes = 100
    grid.gerar_agentes_aleatorios_v2(qnt_agentes)
    print("foram gerados {} agentes aleatorios".format(qnt_agentes))

    nome_arquivo_caminhos = func_arq.gerar_nome_arquivo_caminhos(arquivo_base_utilizado)
    grid.resgatar_caminhos_arquivo_v2(nome_arquivo_caminhos)

    pesos_teste = (1, 1, 1)
    numero_simulacao_teste = 1
    qnt_time_steps_teste = 30

    salvar_caminhos = False

    if salvar_caminhos is True:
        resultados = simulacao_fast(pesos_teste, grid, numero_simulacao_teste, qnt_time_steps_teste,
                                    salvar_caminhos_arquivo=True, nome_arquivo_base=arquivo_base_utilizado)
    else:
        resultados = simulacao_fast(pesos_teste, grid, numero_simulacao_teste, qnt_time_steps_teste,
                                    salvar_caminhos_arquivo=False)


if __name__ == '__main__':
    simulacao_com_arquivo("modelo1(42x42)[tipo_1].txt")
