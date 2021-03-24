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


def ordenar_colunas_df_por_id(df, string_coluna):
    lista_colunas = list(df.columns)
    lista_colunas_int = [string_to_id(coluna) for coluna in lista_colunas]
    lista_colunas_int.sort()
    lista_colunas_novas = [id_to_string(string_coluna, i) for i in lista_colunas_int]
    df = df[lista_colunas_novas]
    return df


