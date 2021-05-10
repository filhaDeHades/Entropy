import os


def gear_nome_arquivo_info_agentes_staticos(nome_arquivo):
    nome_temp = nome_arquivo.strip(".txt")
    nome_final = nome_temp + "_info_agentes_staticos.txt"
    return nome_final


def gerar_nome_arquivo_info_agentes_dinamicos(nome_arquivo):
    nome_temp = nome_arquivo.strip(".txt")
    nome_final = nome_temp + "_info_agentes_dinamicos.txt"
    return nome_final


def gerar_nome_arquivo_info_lugares_dinamicos(nome_arquivo):
    nome_temp = nome_arquivo.strip(".txt")
    nome_final = nome_temp + "_info_lugares_dinamicos.txt"
    return nome_final


def string_to_id(string):
    num = []
    for i in string:
        if i.isdecimal() is True:
            num.append(i)

    num = int("".join(num))
    return num


def id_to_string(string, n):
    return string + str(n)


def obter_peso_por_nome(nome_arquivo):
    i0 = nome_arquivo.index("(")
    i1 = nome_arquivo.index(")")
    peso = nome_arquivo[i0:i1+1]
    return peso


def nomear_com_peso(nome_base, peso, extensao=".txt"):
    return nome_base + str(peso) + extensao


def ordenar_colunas_df_por_id(df, string_coluna):
    lista_colunas = list(df.columns)
    lista_colunas_int = [string_to_id(coluna) for coluna in lista_colunas]
    lista_colunas_int.sort()
    lista_colunas_novas = [id_to_string(string_coluna, i) for i in lista_colunas_int]
    df = df[lista_colunas_novas]
    return df


def formatar_nomes_arquivos(nome_dir_origem):

    # nao funciona, mas estou mantebdo aqui pela ideia

    lista_nomes_arqs = os.listdir(nome_dir_origem)

    lista_nomes_arqs_renomeados = []

    for nome_arq in lista_nomes_arqs:
        nome_temp = ""

        i0_selecionado = False
        i0 = 0

        i1_selecionado = False
        i1 = 0

        k = 0

        for i in range(len(nome_arq)):
            
            if (i0_selecionado == False and nome_arq[i] == "("):
                i0 = i
            elif (i1_selecionado == False and nome_arq[i] == ")"):
                i1 = i

            if i0_selecionado == True and i1_selecionado == True:
                sub_string = nome_arq[k:i1]
                
                peso = nome_arq[i0:i1+1]
                peso = eval(peso)
                peso_string = "({:.3f}, {:.3f})".format(peso[0], peso[1])

                nome_temp += sub_string
                nome_temp += peso_string

                k = i1 + 1
                i0_selecionado = False
                i1_selecionado = False

            if (i == len(nome_arq) - 1 and (i0_selecionado == False or i1_selecionado == False)):
                sub_string = nome_arq[k:]
                nome_temp += sub_string

        lista_nomes_arqs_renomeados.append(nome_temp) 

    print("nomes antigos:")
    
    for nome_antigo in lista_nomes_arqs:
        print(nome_antigo)

    print("\n------------\n")

    print("nomes novos:")

    for nome_novo in lista_nomes_arqs_renomeados:
        print(nome_novo)


