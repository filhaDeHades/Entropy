# Modelos para Medição da Entropia em Cidades Simuladas
Esse projeto tem como objetivo observar como o grau de entropia de uma cidade muda com o passar do tempo, para isso utilizamos diferentes modelos de simulação e analisamos os resultados.

## Modelo 5
Modelo de simulação 2D com representação gráfica.

### -> `apresentacoes_fast.py`

### -> `apresentacoes.py`

### -> `ClasseAgenteV2.py`

### -> `ClasseCelulaGridV2.py`

### -> `ClasseGridV2.py`

### -> `ClasseHeapCelulasGrid.py`

### -> `ClasseLugarV2.py`

### -> `funcoes_arquivos.py`

### -> `funcoes2.py`

### -> `Modelo_5_testes.py`

### -> `simulacao_fast.py`

### -> `simulacao.py`

### -> `simulacao2.py`



## Modelo Fast
Modelo de simulação 2D com resultados rápidos, sem representação gráfica.

### -> `__init__.py`

### -> `apresentacoes_fast2.py`

### -> `ClasseAgenteV2Fast.py`
1. **Classe AgenteV2Fast:**
    Representa os agentes da simulação 2D Fast.
    Importa:

        - Modelo_fast.funcoes_fast as fst
        - numpy as np
        - math
        - random

    **qnt_agentes**: Quantidade de agentes criados para a simulação - _int_.

    - `__init__(self, grid, grid_x, grid_y, orientacao_latente=0, orientacao_atual=0, id_agente=None):`
        Inicializa o agente, adicionando seu id, sua orientação latente, sua orientação atual, o grid e sua posição no grid.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

        **grid_x**: Posição X do agente no grid. - _int_.

        **grid_y**: Posição Y do agente no grid. - _int_.

        **orientacao_latente**: Contém o valor da orientação latente do agente. - _int_.

        **orientacao_atual**: Contém o valor da orientação atual do agente. - _int_.

        **id_agente**: Número de identificação do agente. - _int_.

    - `atualizar_celula_grid(self, grid, x, y):`
        Atualiza a celula do grid em que o agente se encontra.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

        **x**: Posição X do agente no grid. - _int_.

        **y**: Posição Y do agente no grid. - _int_.

    - `atualizar_posicao_grid(self, grid, pos_nova_grid):`
        Atualiza a posição do grid que o agente se encontra.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

        **pos_nova_grid**: Lista contendo a nova posição no grid. - _list_.

    - `contaminacao_agente(self, orientacao_do_lugar, pesos):`
        Calcula a nova orientação latente do agente depois da contaminação pelo lugar onde ele se encontra na simulação.

        **self**: Presente em todas as classes, representa a si mesmo.

        **orientacao_do_lugar**: Contém a orientação do lugar onde o agente se encontra no momento. - _int_.

        **pesos**: Lista contendo os pesos a serem usados no cálculo da contaminação. - _list_.

    - `sortear_nova_orientacao(self):`
        Sorteia uma nova orientação atual para o agente.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `escolher_lugar_v4(self, grid):`
        Versão 4. Escolhe um lugar para onde o agente deve se movimentar.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

    - `escolher_lugar_v5(self, lista_lugares, lista_pesos=(0.1, 0.1), modelo_fabiano=False):`
        Versão 5. Escolhe um lugar para onde o agente deve se movimentar.

        **self**: Presente em todas as classes, representa a si mesmo.

        **lista_lugares**: Lista contendo todos os lugares a possíveis de escolhas. - _list_.

        **lista_pesos**: Lista contendo os pesos que a diferença de orientação e a distância terão durante o sorteio. Valor padrão: (0.1, 0.1). - _tupla_.

        **modelo_fabiano**: Define se a orientação a ser utilizada é a orientação latente (True) ou a atual (False). Valor padrão: False. - _bool_.

    - `sorteioComPesos(listaPossibilidades, listaPesos, qntElementosSorteados=1):`
        Método estático. Sorteia um determinado número de elementos utilizando pesos na decisão.

        **listaPossibilidades**: Lista contendo os elementos possíveis de serem sorteados. - _list_.

        **listaPesos**: Lista contendo o pesos a ser levado em conta para os elementos a serem sorteados. - _list_.

        **qntElementosSorteados**: Define quantos elementos devem ser sorteados pela função. Valor padrão: 1. - _int_.-

    - `escolher_lugar(self, listaLugares, pesos):`
        Método importado do modelo 1D e adaptado para o modelo 2D.  Define o peso dos lugares e com essa informação define o próximo lugar que o agente deve escolher com um sorteio. Retorna o lugar escolhido.

        **self**: Presente em todas as classes, representa a si mesmo.

        **listaLugares**: Lista contendo todos os lugares presentes na simulação. - _list_.

        **pesos**: Lista contendo os pesos que a orientação e a distancia, respectivamente, terão na escolha do lugar. - _list_.

    - `resgatar_estado_inicial(self):`
        Resgata as configurações iniciais do grid, orientação latente e orientação atual e reseta o agente.

        **self**: Presente em todas as classes, representa a si mesmo.

### -> `ClasseCelulaGridV2Fast.py`
1. **Classe CelulaGridV2Fast:** 
    Representa os as células do grid.
    Importa:

        - Modelo_fast.funcoes_fast as fst

    - `__init__(self, grid_x, grid_y, andavel=True, parente=None):`
        Inicializa a célula do grid.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid_x**: Posição X da célula no grid. - _int_.

        **grid_y**: Posição Y da célula no grid. - _int_.

        **andavel**: Determina se a célula é andável ou não. Valor padrão: True. - _bool_.

        **parente**: Valor padrão: None.

    - `atualizar_g(self):` Faz o calculo de 'g', um dos fatores utilizados para o calculo do método A* (A-estrela ou A-star). O 'g' representa a distancia entre a célula atual e o início do caminho.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `atualizar_h(self, pos_grid_final):` Faz o calculo de 'h', um dos fatores utilizados para o calculo do método A* (A-estrela ou A-star). O 'h' representa a distancia entre a célula atual e o destino final.

        **self**: Presente em todas as classes, representa a si mesmo.

        **pos_grid_final**: Representa a posição no grid ao qual se deseja descobrir um caminho.

    - `atualizar_f(self):` Faz o calculo de 'f', um dos fatores utilizados para o calculo do método A* (A-estrela ou A-star). O 'f' representa a soma de 'g' e 'h', sendo assim o valor total da célula para o algoritmo.

        **self**: Presente em todas as classes, representa a si mesmo.

### -> `ClasseGridV2Fast.py`
1. **Classe GridV2Fast:** 
    Representa o grid onde ocorre a simulação.
    Importa:

        -  Modelo_fast.ClasseCelulaGridV2Fast import CelulaGridV2Fast
        - Modelo_fast.ClasseAgenteV2Fast import AgenteV2Fast
        - Modelo_fast.ClasseLugarV2Fast import LugarV2Fast
        - Modelo_fast.funcoes_fast as fst
        - pandas as pd
        - numpy as np
        - random
        - math
        - cores

    - `__init__(self, qnt_linhas, qnt_colunas, qnt_agentes, qnt_lugares, matriz_layout=None, qnt_orientacoes=11, range_possiveis_orientacoes=(0, 1100, 100)):`

        **self**: Presente em todas as classes, representa a si mesmo.

        **qnt_linhas**:

        **qnt_colunas**:

        **qnt_agentes**:

        **qnt_lugares**:

        **matriz_layout**: Valor padrão: None.

        **qnt_orientacoes**: Valor padrão: 11. - _int_

        **range_possiveis_orientacoes**: Valor padrão:(0, 1100, 100). - _list_

    - `obter_dict_orientacoes_cores(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `obter_array_celulas_grid_manual(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `obter_array_celulas_grid_definido(self, matriz_layout):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **matriz_layout**:

    - `obter_celula_array_grid(self, x, y):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **x**:

        **y**:

    - `gerar_agentes_aleatorios_v3(self, qnt_agentes):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **qnt_agentes**:

    - `gerar_lugares_aleatorios_v2(self, qnt_lugares, ajustar_tam_lugar=True, fracao_espaco_vazio=0.5, tamanho_max_lugar=5, sem_cor_repetida=False, sem_orientacao_repetida=False):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **qnt_lugares**:

        **ajustar_tam_lugar**: Valor padrão: True. - _bool_.

        **fracao_espaco_vazio**: Valor padrão: 0.5. - _float_.

        **tamanho_max_lugar**: Valor padrão: 5. - _int_.

        **sem_cor_repetida**: Valor padrão: False. - _bool_.

        **sem_orientacao_repetida**: Valor padrão: False. - _bool_.

    - `gerar_lugares_aleatorios_v3(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `gerar_lugares_aleatorios_v4(self, qnt_lugares, ajustar_tam_lugar=True, fracao_espaco_vazio=0.5, tamanho_max_lugar=5, sem_cor_repetida=False, sem_orientacao_repetida=False):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **qnt_lugares**:

        **ajustar_tam_lugar**: Valor padrão: True. - _bool_.

        **fracao_espaco_vazio**: Valor padrão: 0.5. - _float_.

        **tamanho_max_lugar**: Valor padrão: 5. - _int_.

        **sem_cor_repetida**: Valor padrão: False. - _bool_.

        **sem_orientacao_repetida**: Valor padrão: False. - _bool_.

    - `teste_lugares_certo(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `atualizar_status_andavel_celula(self, x, y, status):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **x**:

        **y**:

        **status**:

    - `obter_lugar_pelo_id(self, num_id):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **num_id**:

    - `resgatar_lugares_arquivo(self, nome_arquivo_lugares):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo_lugares**:

    - `resgatar_caminhos_arquivo(self, nome_arquivo_caminhos):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo_caminhos**:

    - `restaurar_caminhos_entre_lugares(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `mostrar_qnt_caminhos_lugares(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `criar_arquivo_caminhos(self, nome_arquivo):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo**:

    - `salvar_novos_caminhos_arquivo(self, nome_arquivo):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo**:

    - `criar_ou_atualizar_arquivo_caminhos(self, nome_arquivo_caminhos):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo_caminhos**:

    - `obter_dict_ocorrencia_orientacoes(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

    - `calcular_entropia_agentes(self):`
        Calcula a entropia dos agentes da simulação.

        **self**:Presente em todas as classes, representa a si mesmo.
    
    - `calcular_entropia_lugares(self):`
        Calcula a entropia dos lugares da simulação.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `calcular_entropia_geral(self):`
        Calcula a entropia geral da simulação.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `obter_nodulos_vizinhos(self, celula, excluir_obstaculos=True, excluir_diagonais=False):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **celula**:

        **excluir_obstaculos**: Valor padrão: True. - _bool_.

        **excluir_diagonais**: Valor padrão: False. - _bool_.

    - `a_star_lugar(self, nodulo_inicial, lugar, retornar_procura_caminho=False):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nodulo_inicial**:

        **lugar**:

        **retornar_procura_caminho**: Valor padrão: False. - _bool_.

    - `a_star_lugar_v2(self, lugar1, lugar2, retornar_procura_caminho=False):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **lugar1**:

        **lugar2**:

        **retornar_procura_caminho**: Valor padrão: False. - _bool_.

    - `encontrar_celulas_principais(lugar1, lugar2):`
        Método estático.

        **lugar1**:

        **lugar2**:

    - `restaurar_mudancas_feitas_pelo_a_star(self, lista_celulas, lugar1=None, lugar2=None):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **lista_celulas**:

        **lugar1**: Valor padrão: None.

        **lugar2**: Valor padrão: None.

    - `restaurar_estado_inicial_celulas_v2(lista_celulas):`
        Método estático.

        **lista_celulas**:

    - `add_caminho_lista_caminhos_grid_v2(self, lugar_1_id, lugar_2_id, possui_caminho, caminho=None):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **lugar_1_id**:

        **lugar_2_id**:

        **possui_caminho**:

        **caminho**: Valor padrão: None.

    - `salvar_lugares_arquivo(self, nome_arquivo):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo**:

    - `salvar_agentes_arquivo(self, nome_arquivo):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo**:

    - `resgatar_agentes_arquivo(self, nome_arquivo_agentes_staticos):`
        **self**: Presente em todas as classes, representa a si mesmo.

        **nome_arquivo_agentes_staticos**:


### -> `ClasseLugarV2Fast.py`
1. **Classe LugarV2Fast:** 
    Representa os lugares da simulação.
    Importa:

        - Modelo_fast.funcoes_fast as fst
        - numpy as np
        - cores

    - `__init__(self, grid, veio_de_arquivo=False, lista_arquivo=None, lista_coordenadas=None, orientacao=0, cor=cores.verde):`
        Inicializa um lugar para a simulação.

        **self**: Presente em todas as classes, representa a si mesmo.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

        **veio_de_arquivo**: Indica se o lugar foi tirado de um arquivo. O Valor padrão: False. - _bool_.

        **lista_arquivo**: Lista que contém os dados do lugar retirados do arquivo. Valor padrão: None. _list_.

        **lista_coordenadas**: ... Valor padrão: None.

        **orientação**: Orientação a ser atribuida ao lugar. Valor padrão: 0. - _int_.

        **cor**: Contém a cor do lugar. A cor faz referencia a orientação do lugar. Valor padrão: `cores.verde`. - _cores_.

    - `init_array_celulas_grid(self, grid):`

        **self**: Presente em todas as classes, representa a si mesmo.


        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_.

    - `achar_coordenada_principal(self, ponto_referencia):`
        Encontra a coordenada principal apartir da menor distância. Retorna a coordenada principal.

        **self**: Presente em todas as classes, representa a si mesmo.

        **ponto_referencia**:

    - `contaminacao_lugar(self, pesos_contaminacao=(1, 1), mudar_cor=False, grid=None):`
        Calcula a contaminação que o lugar terá apartir da orientação dos agentes que estão presentes nele.

        **self**: Presente em todas as classes, representa a si mesmo.

        **pesos_contaminacao**: Pesos que a orientação do lugar e dos agentes terão, respectivamente. Valor padrão: (1, 1). - _tupla_.

        **mudar_cor**: Define se a cor atual do lugar mudará para acompanhar a mudança de orientação. Valor padrão: False. - _bool_.

        **grid**: Instância da Classe GridV2Fast onde a simulação ocorre. - _GridV2Fast_. Valor padrão: None.

    - `resgatar_estado_inicial(self):`
        Restaura a condição inicial do lugar ao resgatar sua orientação inicial.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `tornar_lugar_andavel(self):`
        Torna o lugar andável.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `tornar_lugar_n_andavel(self):`
        Torna o lugar não andável.
        **self**: Presente em todas as classes, representa a si mesmo.

    - `resetar_coordenada_principal(self):`
        Reseta a coordenada principal.

        **self**: Presente em todas as classes, representa a si mesmo.

    - `restaurar_mudancas_a_star(self):`
        
        **self**: Presente em todas as classes, representa a si mesmo.

    - `add_caminho_lugar_v2(self, lugar_destino, possui_caminho, caminho=None):`
        Adiciona o caminho do lugar a lista de caminhos.

        **self**: Presente em todas as classes, representa a si mesmo.

        **lugar_destino**:

        **possui_caminho**: Indica se há caminho para o lugar de destino. _bool_.

        **caminho**: Valor padrão: None.

### -> `funcoes_fast.py`
1. 
    Contém as funções importantes para que a simulação ocorra.
        Importa:

        - pandas as pd
        - random
        - math
        - os
    
    - `obter_distancia(pos_grid_inicial, pos_grid_final, custo_menor_mov=10, custo_maior_mov=14):`
        **pos_grid_inicial**:

        **pos_grid_final**:

        **custo_menor_mov**: Valor padrão: 10. - _int_.

        **custo_maior_mov**: Valor padrão: 14. - _int_.

    - `arquivo_csv_para_lista(nome_arquivo, separador="\t"):`
        **nome_arquivo**:

        **separador**: Valor padrão: "\t". - _string_.

    - `lista_para_arquivo_csv(lista_origem, nome_arquivo_destino, separador="\t", tipo_operacao="w"):`
        **lista_origem**:

        **nome_arquivo_destino**:

        **separador**: Valor padrão: "\t". - _string_.

        **tipo_operacao**: Valor padrão: "w". - _string_.

    - `obter_distancia_euclidiana(ponto_inicial, ponto_final):`
        **ponto_inicial**:

        **ponto_final**:

    - `obter_distancia_manhattan(coordenada1, coordenada2):`
        **coordenada1**:

        **coordenada2**:

    - `obter_grid_manual(linhas, colunas):`
        **linhas**:

        **colunas**:

    - `escolher_lugar_menor_e(agente, lista_lugares):`
        **agente**:

        **lista_lugares**:

    - `escolher_lugar_mais_parecido(agente, lista_lugares):`
        **agente**:

        **lista_lugares**:

    - `escolher_lugar_mais_parecido_v2(agente, lista_lugares):`
        **agente**:

        **lista_lugares**:

    - `obter_lista_com_elementos_repetidos(dict_contagem_elementos_repetidos):`
        **dict_contagem_elementos_repetidos**:

    - `obter_dict_contagem_elementos_repetidos_v2(lista_com_elementos_repetidos):`
        **lista_com_elementos_repetidos**:

    - `contagem_ocorrencia_elementos_com_referencial(lista_analisada, lista_referencial):`
        **lista_analisada**:

        **lista_referencial**:

    - `obter_media(lista):`
        **lista**:

    - `obter_moda(lista):`
        **lista**:

    - `obter_mediana(lista):`
        **lista**:
    
    - `checar_existencia_arquivo(nome_arquivo):`
        **nome_arquivo**:

    - `transformar_duas_listas_em_dict(lista_chaves, lista_valores):`
        **lista_chaves**:

        **lista_valores**:

    - `obter_path_completo_arquivo(path, nome_arquivo):`
        **path**:

        **nome_arquivo**:

    - `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo):`
        **nome_arquivo**:

        **tipo_arquivo**:

    - `obter_path_arquivos_base():`

    - `obter_path_arquivos_lugares():`

    - `obter_path_arquivos_caminhos():`

    - `obter_path_arquivos_resultados():`

    - `obter_path_arquivos_resultados_ts():`

    - `transformar_duas_listas_em_set(lista_1, lista_2):`
        **lista1**:

        **lista2**:

    - `transformar_lista_em_matriz(lista_original, qnt_linhas, qnt_colunas):`
        **lista_original**:

        **qnt_linhas**:

        **qnt_colunas**:

    - `transformar_matriz_em_lista(matriz):`
        **matriz**:

    - `contar_linhas_e_colunas_matriz(matriz):`
        **matriz**:

    - `matriz_para_lista_dicionarios(lista_chaves, lista_valores):`
        **lista_chaves**:

        **lista_valores**:

    - `converter_orientacao_para_cor_v3(qnt_orientacoes):`
        **qnt_orientacoes**:

    - `converter_orientacao_para_cor_v4(orientacao):`
        **orientacao**:

    - `lista_dicionarios_para_matriz(lista_dicionarios):`
        **lista_dicionarios**:

    - `transformar_resultado_em_linha_csv(dict_resultado, nome_arquivo_destino):`
        **dict_resultado**:

        **nome_arquivo_destino**:

    - `criar_ou_atualizar_arquivo_resultados(path, nome_arquivo_resultados, dict_resultado):`
        **path**:

        **nome_arquivo_resultados**:

        **dict_resultado**:

    - `sorteio_com_pesos(lista_possibilidades, lista_pesos, qnt_elementos_sorteados=1):`
        **lista_possibilidades**:

        **lista_pesos**:

        **qnt_elementos_sorteados**: Valor padrão: 1. - _int_.

    - `obter_lista_media(lista_original):`
        **lista_original**:

    - `update_orientacao_cor(dict_orientacoes_cores, orientacao_analisada, qnt_orientacoes=11):`
        **dict_orientacoes_cores**:

        **orientacao_analisada**:

        **qnt_orientacoes**: Valor padrão: 11. - _int_.

    - `descobir_dif_media(lista):`
        **lista**:

    - `descobrir_num_casa_decimais(n):`
        **n**:


### -> `gerar_graficos.py`

### -> `graficos_matploty.py`

### -> `multiplos_testes.py`

### -> `simulacao_fast2.py`

### -> `simulacao_fast3.py`

### -> `simulacao_fast4.py`

### -> `teste_simples.py`

### -> `testes_fast.py`



## Modelo 1D
Modelo de simulação 1D.

### -> `Agente1D.py`
1. **Classe Agente1D:**
    Representa os agentes da cidade.
    Importa:

        - math
        - random

    **qnt_agentes**: Quantidade de agentes criados para a simulação - _int_.

    - `__init__(self, orientacaoLatente, orientacaoAtual, posicao, id_agente=None):`
        Inicia o agente, adicionando seu id, sua orientação latente e sua orientação atual.

        **self**: Presente em todas as classes, representa a si mesmo.

        **orientacaoLatente**:

        **orientacaoAtual**:

        **posicao**: Posição do agente dentro do espaço da simulação

        **id_agente**: Número de identificação do agente. Valor padrão: None - _int_.

    - `sortearNovaOrientacao(self, listaPossiveisOrientacoes):`
        Sorteia a nova orientação do agente para o próximo timestep.

        **self**: Presente em todas as classes, representa a si mesmo.

        **listaPossiveisOrientacoes**: Lista contendo todas as orientações possiveis para o agente.

    - `sortear_nova_posicao(self, qnt_novas_posicoes):`
        Sorteia a nova posição do agente para o próximo timestep.

        **self**: Presente em todas as classes, representa a si mesmo

        **qnt_novas_posicoes**: Lista contendo todas as possiveis posições para o agente.

    - `sorteioComPesos(listaPossibilidades, listaPesos, qntElementosSorteados=1):`
        Método estático. Escolhe valores levando em consideração o peso de cada valor para o sorteio. Retorna uma lista com os elementos sorteados.

        **listaPossibilidades**:Lista contendo as possibilidades a serem sorteadas. - _list_

        **listaPesos**: Lista contendo o peso de cada possibilidade dentro da "listaPossibilidades". - _list_

        **qntElementosSorteados**: Quantos elementos devem ser sorteados. Valor padrão: 1 - _int_.

    - `escolherLugar(self, listaLugares, pesos)`
        Define o peso dos lugares e com essa informação define o próximo lugar que o agente deve escolher com um sorteio. Retorna o lugar escolhido.

        **self**: Presente em todas as classes, representa a si mesmo.

        **listaLugares**: Lista contendo todos os lugares presentes na simulação. - _list_.

        **pesos**: Lista contendo os pesos que a orientação e a distancia, respectivamente, terão na escolha do lugar. - _list_.
    
    - `escolher_lugar_v2(self, listaLugares, pesos)`
        Segunda versão. Define o peso dos lugares e com essa informação define o próximo lugar que o agente deve escolher com um sorteio. Retorna o lugar escolhido.

        **self**: Presente em todas as classes, representa a si mesmo.

        **listaLugares**: Lista contendo todos os lugares presentes na simulação. - _list_.

        **pesos**: Lista contendo os pesos que a orientação e a distancia, respectivamente, terão na escolha do lugar. - _list_.

    - `contaminacaoAgente(self, lugar, pesos)`
        Define a nova orientação latente do agente a partir da antiga orientação do agente e da orientação do lugar onde o agente se encontra.

        **self**: Presente em todas as classes, representa a si mesmo.

        **lugar**: Instância da classe Lugar1D.

        **pesos**: Lista contendo os pesos que a orientação latente do agente, a orientação atual do agente e a orientação do lugar, respectivamente, terão na contaminação do lugar. - _list_.

    - `contaminacao_agente_v2(self, lugar, pesos=(1, 0.1))`
        Segunda versão. Define a nova orientação latente do agente a partir da antiga orientação latente do agente e da orientação do lugar onde o agente se encontra.

        **self**: Presente em todas as classes, representa a si mesmo.

        **lugar**: Instância da classe Lugar1D.

        **pesos**: Lista contendo os pesos que a orientação latente do agente e a orientação do lugar, respectivamente, terão na contaminação do lugar. Valor padrão: (1, 0.1) _list_.

    - `resgatarEstadoInicial(self)`
        Resgata as configurações iniciais de orientação latente e orientação atual e reseta o agente.

        **self**: Presente em todas as classes, representa a si mesmo.

### -> `cidade-1D_mod.py`
1. Representa os agentes da cidade.
        Importa:

            - numpy as np
            - pandas as pd
            - matplotlib.pyplot as plt
            - random as rd
            - scipy.stats as st
            - math
            - mode from statistics
            - random
            - os
            - curve_fit from scipy.optimize
            - minimize from scipy.optimize
            - stats from scipy
            - entropy from scipy.stats
            - figure, show, output_file, save from bokeh.plotting
            - output_notebook from bokeh.io
            - gridplot from bokeh.layouts
            - gray from bokeh.palettes
            - viridis from bokeh.palettes
            - export_png from bokeh.io
        
    **qntAgentes**:

    **tamanhoCidade**:

    **densidadeEspaco**:

    **qntLugares**:

    **qntOrientacoes**:

    **a**:

    **b**:

    **alfa**:

    **theta**:

    **timeSteps**:
    

### -> `cidade-1D.py`

### -> `funcoes1D.py`
- `obterListaMedia(listaOriginal):`
    **listaOriginal**:

### -> `graficos.py`

### -> `Grid1D.py`
1. **Classe Grid1D:**
    Representa o grid.
        Importa:
        
            - math
            - random
            - Agente1D
            - Lugar1D
            - numpy as np
    
    - `__init__(self, tamGrid, qntAgentes, qntLugares, rangePossiveisOrientacoes=(0, 1100, 100), agentes_aleatorios=False, lugares_aleatorios=False):`
    **tamGrid**:
    **qntAgentes**:
    **qntLugares**:
    **rangePossiveisOrientacoes**: Valor padrão: (0, 1100, 100). - _list_.
    **agentes_aleatorios**: Valor padrão: False. - _bool_.
    **lugares_aleatorios**: Valor padrão: False. - _bool_.

    - `obterListaDeOrientacoes(self, rangeOrientacoes):`
    **self**: Presente em todas as classes, representa a si mesmo.
    **rangeOrientacoes**:

    - `criar_agentes(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `criarAgentesAleatorios(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `criar_lugares(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `criarLugaresAleatorios(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `obterDictContagemElementosLista(listaElementos):`
    Método estático.
    **listaElementos**:

    - `obterDictContagemElementosComReferenial(listaElementos, listaReferencial):`
    Método estático.
    **listaElementos**:
    **listaReferencial**:

    - `obterDictOcorrenciaOrientacoesAgentes(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `obterDictOcorrenciaOrientacoesAgentes_v2(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `calcularEntropia(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `calcular_entropia_v2(self):`
    Segunda versão.
    **self**: Presente em todas as classes, representa a si mesmo.

    - `calcular_entropia_lugares(self):`
    **self**: Presente em todas as classes, representa a si mesmo.

    - `calcular_entropia_geral(self):`
    **self**: Presente em todas as classes, representa a si mesmo.


### -> `Lugar1D.py`
1. **Classe Lugar1D:**
    Representa os lugares da cidade.
        Importa:
        
            - random
    
    **qnt_lugares**:
    - `__init__(self, orientacao, posicao, id_lugar=None):`
    **self**: Presente em todas as classes, representa a si mesmo.
    **orientacao**:
    **posicao**:
    **id_lugar**: Valor padrão: None.

    - `sortearNovaOrientacao(self, listaPossiveisOrientacoes):`
    **self**: Presente em todas as classes, representa a si mesmo.
    **listaPossiveisOrientacoes**:

    - `contaminacaoLugar(self, pesos=(1, 0.1)):`
    **self**: Presente em todas as classes, representa a si mesmo.
    **pesos**:

    - `resgatarEstadoInicial(self):`
    Resgata as configurações iniciais de orientação latente e orientação atual e reseta o agente.

        **self**: Presente em todas as classes, representa a si mesmo.


### -> `simulacao1D.py`

### -> `testes_parametros.py`

### -> `testes.py`

### -> `testesPesos.py`