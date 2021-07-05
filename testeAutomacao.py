def lerArquivo(arquivo):
    file = open(arquivo, 'r')
    
    importData = False
    listInformation = []

    for line in file:
        line = line.strip('\n') #Retira das strings o \n (enter)

        #Verificação dos HEADER -----------------------------------
        if line == 'IMPORT':
            importData = True
            continue
        elif line == 'IMPORTEND':
            importData = False
            continue
        #----------------------------------------------------------
        
        if importData == True:
            line = line.split()

            #Import comum
            if line[0] == '0':
                if len(line) != 2:
                    print('ERRO AO LER ARQUIVO. String de importação do tipo 0 com tamanho diferente de 2.')
                    return
                listInformation.append(f'import {line[1]}')


            #Import as
            elif line[0] == '1':
                if len(line) != 3:
                    print('ERRO AO LER ARQUIVO. String de importação do tipo 1 com tamanho diferente de 3.')
                    return
                listInformation.append(f'import {line[1]} as {line[2]}')

            #Import from
            elif line[0] == '2':
                if len(line) != 3:
                    print('ERRO AO LER ARQUIVO. String de importação do tipo 2 com tamanho diferente de 3.')
                    return
                listInformation.append(f'from {line[1]} import {line[2]}')

    file.close()
    return listInformation


nomeArquivo = input('Digite o caminho para o arquivo: ')
resultadoLeitura = lerArquivo(nomeArquivo)
print('Resultado da leitura:\n-------------------------')
for i in resultadoLeitura:
    print(i)