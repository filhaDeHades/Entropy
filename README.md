# Modelos para Medição da Entropia em Cidades Simuladas
Esse projeto tem como objetivo observar como o grau de entropia de uma cidade muda com o passar do tempo, para isso utilizamos diferentes modelos de simulação e analisamos os resultados.

## **Primeiros passos:**

Para criar uma simulação a primeira coisa que você precisa decidir é qual modelo você irá usar, atualmente o projeto tem 3 modelos de simulação:

**Simulação 1D:**

O modelo 1D tem como objetivo a simulação de uma cidade em um ambiente 1D (uma linha). O programa roda inteiramente pelo terminal.

**Simulação 2D Fast:**

O modelo 2D fast tem como objetivo a simulação de uma cidade em um ambiente 2D. O programa roda inteiramente pelo terminal.

**Simulação 2D com Visualização:**

O modelo 2D com Visualização também tem como objetivo a simulação de uma cidade em um ambiente 2D, porém esse modelo permite a visualização dos passos do sistema atráves de uma interface gráfica.

## **Rodando o programa:**
Para conseguir utilizar o programa no seu computador será necessário fazer alguns passos:

1. **Fazer o Download do Repositório**

2. **Criar um Ambiente Virtual**

    É necessário que o você crie um ambiente virtual (é aconselhavel que você o adicione dentro da pasta do programa).

3. **Configurar seu ambiente virtual**

    É necessário que você garanta que seu ambiente virtual tem instalado as seguintes linguagens/bibliotecas:
    - **python 3.9** ou superior
    - biblioteca **matplotlib**
    - biblioteca **numpy**
    - biblioteca **pandas**
    - biblioteca **pygame**

4. **...**

## **Documentação**
Para ver a documentação do projeto basta clicar [nesse link](Documentation.md).

## **Utilizando o programa**
Aqui estão alguns exemplos de uso que podem ser úteis.

- **Preparar um arquivo para simulação**

Esse script roda automaticamente quando o arquivo que recebeu sua importação
é executado, logo, basta apenas que as pastas sejam configuradas e as importações sejam feitas como demonstrado abaixo para que seja feita a utilização no código.

- Importações necessárias:
    ```python
    import Testes.main.recebe_arquivo_original
    ```
- Configuração das pastas:

    ```
    ├── Entropy
    │   ├── Arquivos
    │   │   ├── Arquivos_base
    │   │   ├── Arquivos_caminhos
    │   │   ├── Arquivos_lugares
    │   │   ├── Arquivos_originais
    │   │   ├── Arquivos_resultados
    │   │   └── Arquivos_resultados_ts
    │   ...
    ...
    ```
- Exemplos de Inputs:

    1. Arquivo do tipo 1 com matriz de 25x25:
    ```
    Digite o nome, nº de linhas, nº de colunas e tipo do arquivo:
    cidadeTal.txt 25 25 1
    ```
    2. Arquivo do tipo 2 com matriz de 100x100:
    ```
    Digite o nome, nº de linhas, nº de colunas e tipo do arquivo:
    outraCidade.txt 100 100 2
    ```

## **Organização dos Arquivos**

1. **Nomeando Elementos**
    Definições comuns a todos os nomes:
    * Utilizar nomes que indiquem facilmente a finalidade da variável, função, classe ou arquivo.
    * O uso de números (como enumeração) deve ser feito ao final do nome.
    * Não utilizar caracteres especiais ou acentos ortográficos.
    * Nenhum nome deve conter espaços entre as palavras.

    **Nomenclatura das variáveis (Em andamento):**
    - Separação das palavras por "_".
    - Utilização apenas de letras minúsculas.
    - Caso a variável seja uma tupla, lista, matriz, dicionário ou set a primeira palavra do nome deve ser respectivamente, tupl, list, mtrx, dict ou set.
    - Exemplo:
        - nome_da_variavel
        - variavel_2
        - tupl_outra_variavel

    **Nomenclatura das funções (Em andamento):**
    - Separação das palavras por "_".
    - Capitalização das palavras, exceto pela primeira palavra. (A primeira letra de cada palavra deve ser maiúscula e todas as outras minúsculas).
    - Exemplo:
        - nome_Da_Funcao
        - funcao_1

    **Nomenclatura das Classes (Em andamento):**
    - Separação das palavras por **Camelcase**.
    - Primeira palavra inicia com letra maiúscula.
    - Exemplo:
        - ClasseExemplo
        - ExemploDeClasse3
        - Classe4

    **Nomenclatura dos Arquivos (Em andamento):**
    - A primeira palavra deve indicar que tipo de arquivo é:
        - Arquivo de Classes: **"Classe"**.
        - Arquivo de Funções: **"funcoes"**.
        - Arquivo de configuração de Gráficos: **"graficos"**.
        - Arquivo de configuração de Simulações: **"simulacao"**.
        - Arquivo de Testes: **"teste"/"testes"**.
        
        