# Documentação do Projeto
Documentação do projeto para simulação de cidades e avaliação da entropia com o passar do tempo.

Voltar para o [ReadMe](README.md).

Modelos propostos pelo projeto:

* [Modelo 5](#modelo-5)
* [Modelo Fast](#modelo-fast)
* [Modelo 1D](#modelo-1d)


## Modelo 5
Modelo de simulação 2D com representação gráfica.

* [Classes](#classes-modelo-5)
    - [Classe Agente Modelo 5](#classe-agente-v2)
    - [Classe Celula Grid Modelo 5](#classe-celula-grid-v2)
    - [Classe Grid Modelo 5](#classe-grid-v2)
    - [Classe Head Celulas Grid Modelo 5](#classe-head-celulas-grid)
    - [Classe Lugar Modelo 5](#classe-lugar-v2)

### -> `apresentacoes_fast.py`

### -> `apresentacoes.py`

### **Classes Modelo 5**

#### Classe Agente V2
-> `ClasseAgenteV2.py`

#### Classe Celula Grid V2
-> `ClasseCelulaGridV2.py`

#### Classe Grid V2
-> `ClasseGridV2.py`

#### Classe Head Celulas Grid
-> `ClasseHeapCelulasGrid.py`

#### Classe Lugar V2
-> `ClasseLugarV2.py`

### **Funções Modelo 5**

#### -> `funcoes_arquivos.py`
1. **Funções para Arquivos:**
    Contém as funções importantes para que a simulação ocorra.
        Importa:

        - GridV2Fast from Modelo_fast.ClasseGridV2Fast
        - LugarV2Fast from Modelo_fast.ClasseLugarV2Fast
        - Modelo_fast.funcoes_fast as fst
        - numpy as np
        - random
        - cores
        - os
    
    - `gerar_nome_arquivo_lugares(nome_arquivo_base):`
        Atualiza o nome de arquivos contendo lugares que serão usados na simulação para que fiquem de acordo com o padrão estipulado. **Retorna o arquivo renomeado**.

        **nome_arquivo_base**: Nome do arquivo que deve ser renomeado. - _string_.

    - `obter_path_completo_arquivo_lugares(nome_arquivo_lugares):`
        Sabendo o nome do arquivo contendo os lugares que serão usados na simulação, **retorna o caminho completo até o arquivo**.

        **nome_arquivo_lugares**: Nome do arquivo que contém os lugares. - _string_.

    - `gerar_nome_arquivo_caminhos(nome_arquivo_base):`
        Atualiza o nome de arquivos contendo os caminhos entre os lugares usados na simulação para que fiquem de acordo com o padrão estipulado. **Retorna o arquivo renomeado**.

        **nome_arquivo_base**: Nome do arquico que deve ser renomeado. - _string_.

    - `obter_path_completo_arquivo_caminhos(nome_arquivo_caminhos):`
        Sabendo o nome do arquivo contendo os caminhos enre os lugares usados na simulação, **retorna o caminho completo até o arquivo**.

        **nome_arquivo_caminhos**: Nome do arquivo contendo os caminhos entre os lugares. - _string_.

    - `gerar_nome_arquivo_resultados(nome_arquivo_base):`
        Atualiza o nome de arquivos contendo os resultados da simulação para que fiquem de acordo com o padrão estipulado. **Retorna o arquivo renomeado**.

        **nome_arquivo_base**: Nome do arquivo que deve ser renomeado. - _string_.

    - `obter_path_completo_arquivo_resultados(nome_arquivo_resultados):`
        Sabendo o nome do arquivo contendo resultados da simulação, **retorna o caminho completo até o arquivo**.

        **nome_arquivo_resultados**: Nome do arquivo contendo os resultados. - _string_.

    - `gerar_nome_arquivo_resultados_ts(nome_arquivo_base, num_sim):`

        **nome_arquivo_base**:. - _string_.

        **num_sim**:

    - `gerar_nome_arquivos_agentes_ts(nome_arquivo_agentes, time_step_atual):`

        **nome_arquivo_agentes**:. - _string_.

        **time_step_atual**:

    - `atualizar_nome_arquivo_lugares_ts(nome_arquivo_lugares, time_step_atual):`
        Função sem conteúdo.

        **nome_arquivo_lugares**:. - _string_.

        **time_step_atual**:

    - `atualizar_nome_arquivo_agentes_ts(nome_arquivo_agentes, time_step_atual):`
        Função sem conteúdo.

        **nome_arquivo_agentes**:. - _string_.

        **time_step_atual**:

    - `criar_arquivo_lugares_tipo_1(nome_arquivo_base, qnt_linhas, qnt_colunas, path_arquivos_base=None, path_arquivos_lugares=None):`
        Cria um arquivo de lugares do tipo 1 (contem somente matriz binaria (0 ou 1)).

        **nome_arquivo_base**: Nome do arquivo do qual as informações devem ser retiradas. - _string_.

        **qnt_linhas**: Quantidade de linhas que a matriz dos lugares deve ter. - _int_.

        **qnt_colunas**: Quantidade de colunas que a matriz dos lugares deve ter. - _int_.

        **path_arquivos_base**: Caminho para os arquivos base. Valor Padrão: None. - _string_.

        **path_arquivos_lugares**: Caminho para os arquivos de lugares. Valor Padrão: None. - _string_.

    - `criar_arquivo_lugares_tipo_1_v2(nome_arquivo_base, qnt_linhas, qnt_colunas):`
        Função obsoleta.

        **nome_arquivo_base**:

        **qnt_linhas**:

        **qnt_colunas**:

    - `criar_arquivo_lugares_tipo_2(nome_arquivo_base, path_arquivos_base=None, path_arquivos_lugares=None):`
        Cria um arquivo de lugares do tipo 2 (contem info sobre o id dos lugares (podem ser quantos ids forem necessarios)).

        **nome_arquivo_base**: Nome do arquivo do qual as informações devem ser retiradas. - _string_.

        **path_arquivos_base**: Caminho para os arquivos base. Valor Padrão: None. - _string_.

        **path_arquivos_lugares**: Caminho para os arquivos de lugares. Valor Padrão: None. - _string_.

    - `obter_tam_grid_pelo_nome_arquivo(nome_arquivo_base):`
        Sabendo que o nome do arquivo contém o tamanho do grid, obtém e **retorna uma lista contendo a quantidade de linhas e colunas**.

        **nome_arquivo_base**: Nome do arquivo do qual as informações devem ser retiradas. - _string_.

    - `gerar_nome_arquivo_com_info_tamanho(nome_arquivo_original, qnt_linhas, qnt_colunas):`
        Gera um arquivo cujo nome contém a o tamanho do grid. **Retorna o nome atualizado do arquivo**.

        **nome_arquivo_original**: Nome do arquivo que deve ser renomeado. - _string_.

        **qnt_linhas**: Quantidade de linhas do grid. - _int_.

        **qnt_colunas**: Quantidade de colunas do grid. - _int_.

    - `obter_tipo_grid_pelo_nome_arquivo(nome_arquivo_base):`
        Obter o tipo (1, 2, ou 3) do arquivo a partir do nome. **Retorna o tipo do arquivo**.

        **nome_arquivo_base**:  Nome do arquivo do qual as informações devem ser retiradas. - _string_.

    - `gerar_nome_arquivo_com_info_tipo(nome_arquivo_original, numero_tipo):`
        Gera um arquivo cujo nome contém a o tipo de informação encontrada. **Retorna o nome atualizado do arquivo**.

        **nome_arquivo_original**: Nome do arquivo que deve ser renomeado. - _string_.

        **numero_tipo**: O número correspondente ao tipo do arquivo. - _int_.

    - `copiar_e_renomear_arquivo(nome_arquivo_original, nome_arquivo_final):`
        Copia um arquivo para um arquivo de nome diferente.

        **nome_arquivo_original**: Nome do arquivo que deve ser copiado. - _string_.

        **nome_arquivo_final**: Nome do arquivo que receberá os dados copiados. - _string_.

    - `gerar_nome_arquivo_base(nome_arquivo_original, qnt_linhas, qnt_colunas, numero_tipo):`
        Gera um arquivo cujo nome contém a o tamanho do grid e o tipo de informações encontradas no arquivo. **Retorna o nome atualizado do arquivo**.

        **nome_arquivo_original**: Nome do arquivo que deve ser renomeado. - _string_.

        **qnt_linhas**: Quantidade de linhas do grid. - _int_.

        **qnt_colunas**: Quantidade de colnas do grid. - _int_.

        **numero_tipo**: O número correspondente ao tipo do arquivo. - _int_.

    - `obter_path_completo_arquivo_base(nome_arquivo_base):`
        Sabendo o nome do arquivo base, **retorna o caminho completo até o arquivo**.

        **nome_arquivo_base**:  Nome do arquivo base. - _string_.

    - `criar_arquivo_base(nome_arquivo_original, nome_arquivo_base):`
        Tendo como base um arquivo e definindo um nome, a função cria um arquivo base.

        **nome_arquivo_original**: Nome do arquivo original. - _string_.

        **nome_arquivo_base**: Nome do arquivo base. - _string_.

    - `criar_arquivo_lugares(nome_arquivo_base, path_arquivos_base=None, path_arquivos_lugares=None):`
        Cria um arquivo de lugares a partir de um arquivo base.

        **nome_arquivo_base**: Nome do arquivo base para a criação de um arquivo de lugares. - _string_.

        **path_arquivos_base**: Caminho a ser percorrido até o arquivo base. Valor padrão: None. - _string_.

        **path_arquivos_lugares**: Caminho a ser percorrido até o arquivo de lugares. Valor padrão: None. - _string_.

    - `corrigir_arquivo_invertido(nome_arquivo_invertido, nome_arquivo_certo):`
        Corrige um arquivo com valores invertidos.

        **nome_arquivo_invertido**: Nome do arquivo cujos valores estão invertidos. - _string_.

        **nome_arquivo_certo**: Nome do arquivo que receberá os valores corretos. - _string_.

    - `contar_qnt_linhas_arq(nome_arq):`
        Conta quantas linhas um arquivo tem.

        **nome_arq**: Nome do arquivo cujas linhas sweão contadas. - _string_.

    - `recebimento_arquivo_original(nome_arquivo_original, qnt_linhas, qnt_colunas, numero_tipo):`
        Ao receber o arquivo original, cria um arquivo de lugares.

        **nome_arquivo_original**: Nome do arquivo original. - _string_.

        **qnt_linhas**: Quantidade de linhas que devem ser criadas. - _int_.

        **qnt_colunas**: Quantidade de colunas que devem ser criadas. - _int_.

        **numero_tipo**: Número correspondente ao tipo do arquivo que será criado. - _int_.

#### -> `funcoes2.py`

### -> `Modelo_5_testes.py`

### -> `simulacao_fast.py`

### -> `simulacao.py`

### -> `simulacao2.py`



## Modelo Fast
Modelo de simulação 2D com resultados rápidos, sem representação gráfica.

* [Classes](#classes-modelo-fast)
    - [Classe Agente Modelo Fast](#classe-agente-modelo-fast)
    - [Classe Celula Grid Modelo Fast](#classe-celula-grid-modelo-fast)
    - [Classe Grid Modelo Fast](#classe-grid-modelo-fast)
    - [Classe Lugar Modelo Fast](#classe-lugar-modelo-fast)
* [Funções](#funções-do-modelo-fast)
* [Gráficos](#trabalhando-com-gráficos)
    - [Gerar Gráficos](#gerar-gráficos)
    - [Gráficos do Matplotlib](#gráficos-do-matplotlib)
* [Simulações](#simulações-modelo-fast)
    - [Simulação 2](#simulação-2-modelo-fast)
    - [Simulação 3](#simulação-3-modelo-fast)
    - [Simulação 4](#simulação-4-modelo-fast)
* [Testes](#testes-modelo-fast)
    - [Múltiplos Testes](#múltiplos-testes-modelo-fast)
    - [Teste Simples](#teste-simples)
    - [Testes Fast](#testes-fast)


### -> `__init__.py`

### -> `apresentacoes_fast2.py`

### Classes Modelo Fast

#### Classe Agente Modelo Fast
-> `ClasseAgenteV2Fast.py`

1. **Classe AgenteV2Fast:**
    Representa os agentes da simulação 2D Fast.
    Importa:

        - Modelo_fast.funcoes_fast as fst
        - numpy as np
        - math
        - random

    **qnt_agentes**: Quantidade de agentes criados para a simulação - _int_.

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

#### Classe Celula Grid Modelo Fast
-> `ClasseCelulaGridV2Fast.py`

1. **Classe CelulaGridV2Fast:** 
    Representa os as células do grid.
    Importa:

        - Modelo_fast.funcoes_fast as fst

    - `__init__(self, grid_x, grid_y, andavel=True, parente=None):`
        Inicializa a célula do grid, informa se a célula é andável ou não (importante para o algoritmo A*).

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

#### Classe Grid Modelo Fast
-> `ClasseGridV2Fast.py`

1. **Classe GridV2Fast:** 
    Representa o grid onde ocorre a simulação.
    Importa:

        - CelulaGridV2Fast from Modelo_fast.ClasseCelulaGridV2Fast
        - AgenteV2Fast from Modelo_fast.ClasseAgenteV2Fast
        - LugarV2Fast from Modelo_fast.ClasseLugarV2Fast
        - Modelo_fast.funcoes_fast as fst
        - pandas as pd
        - numpy as np
        - random
        - math
        - cores

    - `__init__(self, qnt_linhas, qnt_colunas, qnt_agentes, qnt_lugares, matriz_layout=None, qnt_orientacoes=11, range_possiveis_orientacoes=(0, 1100, 100)):`Inicializa o grid, adicionando a quantidade de linhas, colunas, agentes e lugares que o mesmo terá, além do layout da matriz, a quantidade de orientações e o quanto as orientações podem variar.

        **self**: Presente em todas as classes, representa a si mesmo.

        **qnt_linhas**: Define a quantidade de linhas que o grid terá. - _int_.

        **qnt_colunas**:Define a quantidade de colunas que o grid terá. - _int_.

        **qnt_agentes**:Define a quantidade de agentes que o grid terá. - _int_.

        **qnt_lugares**:Define a quantidade de lugares que o grid terá. - _int_.

        **matriz_layout**: Valor padrão: None.

        **qnt_orientacoes**: Valor padrão: 11. - _int_.

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

    - `gerar_lugares_aleatorios_v3(self):`
        **self**: Presente em todas as classes, representa a si mesmo.

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


#### Classe Lugar Modelo Fast
-> `ClasseLugarV2Fast.py`

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

### Funções do Modelo Fast
-> `funcoes_fast.py`

1. **Funções Fast:**
    Contém as funções importantes para que a simulação ocorra.
        Importa:

        - pandas as pd
        - random
        - math
        - os
    
    - `obter_distancia(pos_grid_inicial, pos_grid_final, custo_menor_mov=10, custo_maior_mov=14):` Faz o cálculo da distância entre 2 células do grid. Esse cálculo é importante para o uso do algoritmo A* (A star / A estrela). **Retorna a distância entre as 2 células.**

        **pos_grid_inicial**: A posição da primeira célula do grid a qual se quer calcular a distância. - _list_.

        **pos_grid_final**: A posição da segunda célula do grid a qual se quer calcular a distância. - _list_.

        **custo_menor_mov**: Contém o valor do menor custo unitário de movimentação. Valor padrão: 10. - _int_.

        **custo_maior_mov**: Contém o valor do maior custo unitário de movimentação. Valor padrão: 14. - _int_.

    - `arquivo_csv_para_lista(nome_arquivo, separador="\t"):`
        Transfere as informações de um arquivo .csv para uma lista. **Retorna uma lista com o conteúdo do arquivo.**

        **nome_arquivo**: String contendo o nome do arquivo a ser analisado. - _string_.

        **separador**: Carácter a ser usado como separador do arquivo. Valor padrão: "\t". - _string_.

    - `lista_para_arquivo_csv(lista_origem, nome_arquivo_destino, separador="\t", tipo_operacao="w"):`
        Transfere as informações de uma lista para um arquivo .csv.

        **lista_origem**: A lista que contém as informações a serem transferidas. - _list_.

        **nome_arquivo_destino**: O nome do arquivo de destino (caso não exista um arquivo com esse nome, será criado um). - _string_.

        **separador**: Carácter a ser usado como separador do arquivo. Valor padrão: "\t". - _string_.

        **tipo_operacao**: Carácter que representa a operação a ser feita no arquivo(escrita ou leitura). Valor padrão: "w". - _string_.

    - `obter_distancia_euclidiana(ponto_inicial, ponto_final):`
        Obtém a distância entre 2 pontos a partir do teorema de pitágoras (a^2 = b^2 + c^2) e **retorna essa distância**.

        **ponto_inicial**: Lista contendo as coordenadas do ponto inicial. - _list_.

        **ponto_final**: Lista contendo as coordenadas do ponto final. - _list_.

    - `obter_distancia_manhattan(coordenada1, coordenada2):`
        Obtém a distância total entre 2 pontos e **retorna essa distância.

        **coordenada1**: Lista contendo as primeiras coordenadas. - _list_.

        **coordenada2**: Lista contendo as segundas coordenadas. - _list_.

    - `obter_grid_manual(linhas, colunas):`
        Cria um grid com o número de linhas e colunas informados. **Retorna o grid**.

        **linhas**: Número de linhas do grid. - _int_.

        **colunas**: Número de colunas do grid. - _int_.

    - `escolher_lugar_menor_e(agente, lista_lugares):`
        Escolhe o lugar a partir da menor distância euclidiana. **Retorna o lugar com a menor distância euclidiana**.

        **agente**: Instância da Classe AgenteV2Fast. - _AgenteV2Fast_.


        **lista_lugares**: Lista contendo as opções de lugares que o agente pode escolher. - _list_.

    - `escolher_lugar_mais_parecido(agente, lista_lugares):`
        Um agente escolhe um lugar para ir baseado apenas na diferença entre suas orientações. Assume que apenas um lugar terá a orientação mais próxima do agente. **Retorna o lugar com a menor diferença de orientação**.

        **agente**: Instância da Classe AgenteV2Fast. - _AgenteV2Fast_.

        **lista_lugares**: Lista contendo as opções de lugares que o agente pode escolher. - _list_.

    - `escolher_lugar_mais_parecido_v2(agente, lista_lugares):`
        Segunda versão. Um agente escolhe um lugar para ir baseado apenas na diferença entre suas orientações. Assume a possibilidade de mais de um lugar ter a orientação mais próxima do agente e caso isso aconteça escolhe um deles de forma aleatória. **Retorna o lugar com a menor diferença de orientação**.

        **agente**:  Instância da Classe AgenteV2Fast. - _AgenteV2Fast_.

        **lista_lugares**: Lista contendo as opções de lugares que o agente pode escolher. - _list_.

    - `obter_lista_com_elementos_repetidos(dict_contagem_elementos_repetidos):`
        A partir de um dicionário contendo a contagem de elementos repetidos a função cria uma lista contendo esses elementos. **Retorna uma lista contendo os elementos repetidos**.

        **dict_contagem_elementos_repetidos**: Dicionário contendo a contagem dos elementos repetidos. - _dict_.

    - `obter_dict_contagem_elementos_repetidos_v2(lista_com_elementos_repetidos):`
        Obtém um dicionário contendo os elementos repetidos e sua contagem a partir de uma lista contendo todos os elementos repetidos. **Retorna um dicionário contendo a contagem dos elementos repetidos.

        **lista_com_elementos_repetidos**: Lista contendo todos os elementos repetidos. - _list_.

    - `contagem_ocorrencia_elementos_com_referencial(lista_analisada, lista_referencial):`
        A partir de uma lista referencial com os valores cuja ocorrência deve ser contada é criada um dicionário com os elementos e seu número de ocorrências. **Retorna um dicionário contendo os elementos e seu número de ocorrências**.

        **lista_analisada**: Lista contendo os valores a serem analisados. - _list_.

        **lista_referencial**: Lista contendo os valores a serem usados como referenciais. - _list_.

    - `obter_media(lista):`
        Obtém a média dos valores de uma lista. **Retorna a média dos valores de uma lista**.

        **lista**: Lista contendo os valores dos quais será obtida a média. - _list_.

    - `obter_moda(lista):`
        Obtém a moda (valor que mais se repete) entre os valores de uma lista. **Retorna o a moda entre os valores de uma lista**.

        **lista**: Lista contendo os valores dos quais será obtida a moda. - _list_.

    - `obter_mediana(lista):`
        Obtém a mediana entre os valores de uma lista. **Retorna a mediana entre os valores de uma lista**.

        **lista**:Lista contendo os valores dos quais será obtida a mediana. - _list_.
    
    - `checar_existencia_arquivo(nome_arquivo):`
        Checa se um determinado arquivo existe. **Retorna um valor booleano indicando a existência ou não do arquivo analisado**.

        **nome_arquivo**: Nome do arquivo a ser analisado. - _string_.

    - `transformar_duas_listas_em_dict(lista_chaves, lista_valores):`
        Obtém um dicionário a partir de 2 listas, uma contendo os valores chaves e outra contendo os valores por si só. **Retorna um dicionário com o conteúdo das 2 listas iniciais**.

        **lista_chaves**: Lista contendo os valores chaves. - _list_.

        **lista_valores**: Lista contendo os valores em si. - _list_.

    - `obter_path_completo_arquivo(path, nome_arquivo):`
        Obtém a partir de um path parcial(caminho parcial) e o nome de um arquivo o path completo (caminho completo) para um arquivo. **Retorna o path completo para um arquivo**.

        **path**: String contendo o caminho parcial até o arquivo a ser analisado. - _string_.

        **nome_arquivo**: String contendo o nome do arquivo a ser analisado. - _string_.

    - `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo):`
        Segunda versão. Obtém a partir do nome do arquivo e do tipo de arquivo o path completo (caminho completo). **Retorna o path completo para um arquivo**.

        **nome_arquivo**: String contendo o nome do arquivo a ser analisado. - _string_.

        **tipo_arquivo**: String contendo o tipo do arquivo (base, lugares, caminhos, resultados, resultados_ts). - _string_.

    - `obter_path_arquivos_base():`
        Utilizada na função `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo)`. Determina parte do caminho para arquivos do tipo base. **Retorna parte do caminho para um arquivo do tipo base**.

    - `obter_path_arquivos_lugares():`
        Utilizada na função `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo)`. Determina parte do caminho para arquivos do tipo lugares. **Retorna parte do caminho para um arquivo do tipo lugares**.

    - `obter_path_arquivos_caminhos():`
        Utilizada na função `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo)`. Determina parte do caminho para arquivos do tipo caminhos. **Retorna parte do caminho para um arquivo do tipo caminhos**.

    - `obter_path_arquivos_resultados():`
        Utilizada na função `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo)`. Determina parte do caminho para arquivos do tipo resultados. **Retorna parte do caminho para um arquivo do tipo resultados**.

    - `obter_path_arquivos_resultados_ts():`
        Utilizada na função `obter_path_completo_arquivo_v2(nome_arquivo, tipo_arquivo)`. Determina parte do caminho para arquivos do tipo resultados_ts. **Retorna parte do caminho para um arquivo do tipo resultados_ts**.

    - `transformar_duas_listas_em_set(lista_1, lista_2):`
        Concatena 2 listas separadas em um mesmo set. **Retorna um set com o conteúdo das 2 listas iniciais**.

        **lista1**: Primeira lista contendo os valores a serem concatenados no set. - _list_.

        **lista2**: Segunda lista contendo os valores a serem concatenados no set. - _list_.

    - `transformar_lista_em_matriz(lista_original, qnt_linhas, qnt_colunas):`
        Transforma uma lista em uma matriz. **Retorna uma matriz com as quantidades de linhas e colunas determinadas na chamada da função**.

        **lista_original**: Lista contendo os valores a serem adicionados a nova matriz. - _list_.

        **qnt_linhas**: Inteiro representando a quantidade de linhas que a nova matriz deverá ter. - _int_.

        **qnt_colunas**: Inteiro representando a quantidade de colunas que a nova matriz deverá ter. - _int_.

    - `transformar_matriz_em_lista(matriz):`
        Transforma uma matriz em uma lista. **Retorna uma lista contendo todos os valores da matriz**.

        **matriz**: Matriz contendo todos os valores a serem transferidos para a lista. - _matriz_.

    - `contar_linhas_e_colunas_matriz(matriz):`
        Conta quantas linhas e colunas a matriz tem e printa o resultado.

        **matriz**: Matriz da qual será feita a contagem das linhas e colunas. - _matriz_.

    - `matriz_para_lista_dicionarios(lista_chaves, lista_valores):`
        Transforma duas lista uma lista que contém um dicionário. **Retorna uma lista que contém um dicionário**.

        **lista_chaves**: Lista contendo os valores chaves do dicionário. - _list_.

        **lista_valores**: Lista contendo os valores em si do dicionário. - _list_.

    - `converter_orientacao_para_cor_v3(qnt_orientacoes):`
        Avaliando quantas orientações diferentes há na simulação a função determina quais as cores serão atribuidas a cada uma delas. **Retorna um dicionário com as cores correspondentes a cada orientação**.

        **qnt_orientacoes**: Inteiro que indica quantas são as orientações da simulação. - _int_.

    - `converter_orientacao_para_cor_v4(orientacao):`
        Determina 1 cor a partir de 1 orientação. **Retorna uma tupla contendo a cor correspondente a orientação indicada**.

        **orientacao**: Inteiro contendo o valor que representa a orientação. - _int_.

    - `lista_dicionarios_para_matriz(lista_dicionarios):`
        A partir de uma lista que contém um dicionário, a função obtem os valores desse dicionário e **retorna uma matriz**.

        **lista_dicionarios**:  Uma lista contendo um ou mais dicionários. - _list_.

    - `transformar_resultado_em_linha_csv(dict_resultado, nome_arquivo_destino):`
        Pega os resultados que estão em um dicionário, os formata e adiciona a um arquivo .csv.

        **dict_resultado**: Dicionário contendo as informações a serem transferidas. - _dict_.

        **nome_arquivo_destino**: Nome do arquivo .csv cujas informações serão colocadas. Caso o arquivo não exista será criado um arquivo com o nome informado. - _string_.

    - `criar_ou_atualizar_arquivo_resultados(path, nome_arquivo_resultados, dict_resultado):`
        Verifica se existe um arquivo para os resultados, caso exista, atualiza os dados do arquivo, caso contrário, cria um arquivo e insere as informações.

        **path**: Caminho para encontrar o arquivo. - _string_.

        **nome_arquivo_resultados**: Nome do arquivo que contém os resultados. - _string_.

        **dict_resultado**: Dicionário contendo o resultado da simulação. - _dict_.

    - `sorteio_com_pesos(lista_possibilidades, lista_pesos, qnt_elementos_sorteados=1):`
        Sorteia elementos levando em consideração o peso de cada elemento para o sorteio. **Retorna uma lista com os elementos sorteados**.

        **lista_possibilidades**: Lista contendo os elementos a serem sorteados. - _list_.

        **lista_pesos**: Lista contendo o peso de cada elemento. - _list_.

        **qnt_elementos_sorteados**: A quantidade de elementos que devem ser sorteados. Valor padrão: 1. - _int_.

    - `obter_lista_media(lista_original):`
        **Retorna uma lista contendo a media dos valores obtidos através de recortes da lista original**.

        **lista_original**: Lista contendo os valores dos quais a média deve ser retirada. - _list_.

    - `update_orientacao_cor(dict_orientacoes_cores, orientacao_analisada, qnt_orientacoes=11):`
        Atualiza a cor do elemento de acordo com a sua orientação. **Retorna a cor atualizada**.

        **dict_orientacoes_cores**: Dicionário contendo as cores atribuidas a cada orientação. - _dict_.

        **orientacao_analisada**: A orientação cuja cor deve ser atualizada. - _int_.

        **qnt_orientacoes**: A quantidade de orientações que estão sendo utilizadas na simulação. Valor padrão: 11. - _int_.

    - `descobir_dif_media(lista):`
        Descobre a média entre as diferenças. **Retorna a lista contendo as diferenças**.

        **lista**: Lista contendo os valores dos quais deve ser verificada a diferença. - _list_.

    - `descobrir_num_casa_decimais(n):`
        Descobre o numero de casas decimais de que um float tem. **Retorna o número de casas decimais de um float**.

        **n**: Float do qual se quer saber o número de casas decimais. - _float_.


### Trabalhando com Gráficos

#### Gerar Gráficos
-> `gerar_graficos.py`

#### Gráficos do Matplotlib
-> `graficos_matploty.py`

### Simulações Modelo Fast

#### Simulação 2 Modelo Fast
-> `simulacao_fast2.py`

#### Simulação 3 Modelo Fast
-> `simulacao_fast3.py`

#### Simulação 4 Modelo Fast
-> `simulacao_fast4.py`

### Testes Modelo Fast

#### Múltiplos Testes Modelo Fast
-> `multiplos_testes.py`

#### Teste Simples
-> `teste_simples.py`

#### Testes Fast
-> `testes_fast.py`


## Modelo 1D
Modelo de simulação 1D.

* [Classes](#classes-modelo-1d)
    - [Classe Agente Modelo 1D](#classe-agente-modelo-1d)
    - [Classe Grid Modelo 1D](#classe-grid-modelo-1d)
    - [Classe Lugar V2](#classe-lugar-modelo-1d)

### Classes Modelo 1D

#### Classe Agente Modelo 1D
-> `Agente1D.py`

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

#### Classe Grid Modelo 1D
-> `Grid1D.py`

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

#### Classe Lugar Modelo 1D
-> `Lugar1D.py`

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

### -> `simulacao1D.py`

### -> `testes_parametros.py`

### -> `testes.py`

### -> `testesPesos.py`

## Fim
Voltar para o [início](#documentação-do-projeto).