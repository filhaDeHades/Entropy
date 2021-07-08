## Colocando as informações de Import:

**IMPORT** -> Inicio da seção de importações - Linha própria

**IMPORTEND** -> Fim da seção de importações - Linha própria

        X primeiraSeção segundaSeção
        |       |            └── Parte opcional a ser adicionada no final.
        |       └─────────────── Aquilo que deve ser importado.
        └─────────────────────── Número que indica o tipo de importação.
    
- 0 - **Import comum**
- 1 - **Import as**
- 2 - **Import from**

*obs: As informações de cada linha devem ser separadas por espaços.

exemplos de uso:

        1 smtplib sl
        0 os

## Colocando informações do Grid:

**GRID** -> Inicio da seção do grid - Linha própria

**GRIDEND** -> Fim da seção do grid - Linha própria

        linha 0: w x y z
                 | | | └── Quantidade de Lugares
                 | | └──── Quantidade de Agentes
                 | └────── Quantidade de Colunas
                 └──────── Quantidade de Linhas
        linha 1: layout
                    └───── Layout da Matriz
        linha 2: A B C D
                 | | | └── Passo entre cada orientação
                 | | └──── Maior orientação possível
                 | └────── Menor orientação possível
                 └──────── Quantidade de Orientações

Quando for usar os valores padrões da função adicione "**base**" no lugar correspondente.

- 0 - **linha 0**
- 1 - **linha 1**
- 2 - **linha 2**