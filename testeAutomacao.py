from os import close


def ler_Arquivo(arquivo):
    import_data = False
    grid_data = False
    pass_grid = False


    list_information = []
    dict_grid = {
        'qnt_linhas' : None,
        'qnt_colunas' : None,
        'qnt_agentes' : None,
        'qnt_lugares' : None,
        'matriz_layout' : None,
        'qnt_orientacoes' : None,
        'possiveis_orientacoes' : [None, None, None] #necessário implementar
    }

    file = open(arquivo, 'r')

    for line in file:
        line = line.strip('\n') #Retira das strings o \n (enter)

        if line == '':
            continue

        #Verificação dos HEADER -----------------------------------
        if line == 'IMPORT':
            import_data = True
            continue
        elif line == 'IMPORTEND':
            import_data = False
            continue

        if line == 'GRID':
            grid_data = True
            continue
        if line == 'GRIDEND':
            grid_data = False
        #----------------------------------------------------------
        
        if import_data == True: #lê e escreve as informações de import
            result_imports = lendo_Imports(line)
            for content in result_imports:
                list_information.append(content)
        
        elif grid_data == True: #obtem as informações do grid
            lendo_Grid(line, dict_grid)
            pass_grid = True


        if grid_data == False and pass_grid == True:
            #forma a linha após ter as informações completas
            result_grid = escrevendo_Grid(dict_grid, 'fast')
            list_information.append(result_grid)
            pass_grid = False

    file.close()
    return list_information


def lendo_Imports(line):
    list_imports = []
    line = line.split()

    #Import comum
    if line[0] == '0':
        if len(line) != 2:
            print('ERRO AO LER ARQUIVO. [IMPORT] String de importação do tipo 0 com tamanho diferente de 2.')
            close()
        list_imports.append(f'import {line[1]}')

    #Import as
    elif line[0] == '1':
        if len(line) != 3:
            print('ERRO AO LER ARQUIVO. [IMPORT] String de importação do tipo 1 com tamanho diferente de 3.')
            close()
        list_imports.append(f'import {line[1]} as {line[2]}')

    #Import from
    elif line[0] == '2':
        if len(line) != 3:
            print('ERRO AO LER ARQUIVO. [IMPORT] String de importação do tipo 2 com tamanho diferente de 3.')
            close()
        list_imports.append(f'from {line[1]} import {line[2]}')
    
    else:
        print('ERRO AO LER ARQUIVO. [IMPORT] String de importação do tipo INVÁLIDO.')
        close()

    return list_imports


def lendo_Grid(line, dict_grid):
    line = line.split()
    print(f'linha do tipo = {line[0]}')

    if (line[0] == '0'):
        if (len(line) != 5):
            print('ERRO AO LER ARQUIVO. [GRID] String de importação do tipo 0 com tamanho diferente de 5.')
            close(1)
        if line[1] != 'base': dict_grid['qnt_linhas'] = line[1]
        if line[2] != 'base': dict_grid['qnt_colunas'] = line[2]
        if line[3] != 'base': dict_grid['qnt_agentes'] = line[3]
        if line[4] != 'base': dict_grid['qnt_lugares'] = line[4]

    elif (line[0] == '1'):
        if (len(line) != 2):
            print('ERRO AO LER ARQUIVO. [GRID] String de importação do tipo 1 com tamanho diferente de 2.')
            close(1)
        if line[1] != 'base': dict_grid['matriz_layout'] = line[1]

    elif (line[0] == '2'):
        if (len(line) != 5):
            print('ERRO AO LER ARQUIVO. [GRID] String de importação do tipo 2 com tamanho diferente de 5.')
            close(1)
        if line[1] != 'base': dict_grid['qnt_orientacoes'] = line[1]
        #Implementar range orientações
        if line[2] != 'base' and line[3] != 'base' and line[4] != 'base':
            dict_grid['possiveis_orientacoes'] = [line[2], line[3], line[4]]
    else:
        print('ERRO AO LER ARQUIVO. [GRID] String de importação do tipo INVÁLIDO.')
        close(1)


def escrevendo_Grid(dict_grid_information, tipo_simulacao):
    grid_line = ''
    if dict_grid_information['qnt_linhas'] == None:
        print('ERRO AO LER ARQUIVO. [GRID] Informação "qnt_linhas" nula.')
        close()
    if dict_grid_information['qnt_colunas'] == None:
        print('ERRO AO LER ARQUIVO. [GRID] Informação "qnt_colunas" nula.')
        close()
    if dict_grid_information['qnt_agentes'] == None:
        print('ERRO AO LER ARQUIVO. [GRID] Informação "qnt_agentes" nula.')
        close()
    if dict_grid_information['qnt_lugares'] == None:
        print('ERRO AO LER ARQUIVO. [GRID] Informação "qnt_lugares" nula.')
        close()
    
    if tipo_simulacao == 'fast':
        grid_line += f"grid = GridV2Fast({dict_grid_information['qnt_linhas']}, "
        grid_line += f"{dict_grid_information['qnt_colunas']}, "
        grid_line += f"{dict_grid_information['qnt_agentes']}, "
        grid_line += f"{dict_grid_information['qnt_lugares']}"
    
    if dict_grid_information['matriz_layout'] != None:
        grid_line += f", matriz_layout={dict_grid_information['matriz_layout']}"
    if dict_grid_information['qnt_orientacoes'] != None:
        grid_line += f", qnt_orientacoes={dict_grid_information['qnt_orientacoes']}"
    if (dict_grid_information['possiveis_orientacoes'][0] != None) and (dict_grid_information['possiveis_orientacoes'][1]) and (dict_grid_information['possiveis_orientacoes'][3]):
        grid_line += f", possiveis_orientacoes= ({dict_grid_information['possiveis_orientacoes'][0]},{dict_grid_information['possiveis_orientacoes'][1]}, {dict_grid_information['possiveis_orientacoes'][3]})"
    grid_line += ')'

    return grid_line
    

nome_arquivo = input('Digite o caminho para o arquivo: ')
resultado_leitura = ler_Arquivo(nome_arquivo)
print('Resultado da leitura:\n-------------------------')
for i in resultado_leitura:
    print(i)
print('\n-------------------------')