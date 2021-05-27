class HeapCelulasGrid:

    def __init__(self, exibir_operacoes=False):
        self.lista_heap_celulas = []
        self.qnt_celulas_heap = 0
        self.exibir_operacoes = exibir_operacoes
        self.qnt_comparacoes_ultima_operacao = 0

    def zerar_contagem_comparacoes(self):
        self.qnt_comparacoes_ultima_operacao = 0

    def add_celula_heap(self, celula):
        self.lista_heap_celulas.append(celula)
        self.subir_celula_na_heap(celula)
        self.qnt_celulas_heap += 1

    def remover_primeira_celula_heap(self):
        primeira_celula = self.lista_heap_celulas.pop(0)
        self.qnt_celulas_heap -= 1

        if self.qnt_celulas_heap > 0:
            ultima_celula = self.lista_heap_celulas.pop(-1)
            nova_primeira_celula = ultima_celula
            self.lista_heap_celulas.insert(0, nova_primeira_celula)
            self.descer_celula_na_heap(nova_primeira_celula)

        return primeira_celula

    def obter_celula_pai(self, celula):
        indice_celula = self.lista_heap_celulas.index(celula)

        celula_pai = None

        if indice_celula != 0:
            indice_celula_pai = (indice_celula - 1) // 2
            celula_pai = self.lista_heap_celulas[indice_celula_pai]

        return celula_pai

    def obter_celula_filha_esquerda(self, celula):
        indice_celula_filha_esquerda = self.lista_heap_celulas.index(celula) * 2 + 1

        if indice_celula_filha_esquerda <= self.qnt_celulas_heap - 1:
            celula_filha_esquerda = self.lista_heap_celulas[indice_celula_filha_esquerda]
            return celula_filha_esquerda
        else:
            return None

    def obter_celula_filha_direita(self, celula):
        indice_celula_filha_direita = self.lista_heap_celulas.index(celula) * 2 + 2

        if indice_celula_filha_direita <= self.qnt_celulas_heap - 1:
            celula_filha_direita = self.lista_heap_celulas[indice_celula_filha_direita]
            return celula_filha_direita
        else:
            return None

    @staticmethod
    def comparar_prioridade(celula_1, celula_2):
        if celula_1.f < celula_2.f:
            return celula_1
        elif celula_1.f == celula_2.f and celula_1.h < celula_2.h:
            return celula_1
        else:
            return celula_2

    def trocar_pos_celulas_na_heap(self, celula_1, celula_2):
        indice_celula_1 = self.lista_heap_celulas.index(celula_1)
        indice_celula_2 = self.lista_heap_celulas.index(celula_2)

        self.lista_heap_celulas[indice_celula_1] = celula_2
        self.lista_heap_celulas[indice_celula_2] = celula_1

    def subir_celula_na_heap(self, celula):

        while True:
            celula_pai = self.obter_celula_pai(celula)
            if celula_pai is None:
                break
            else:
                celula_maior_prioridade = self.comparar_prioridade(celula, celula_pai)

                if celula_maior_prioridade == celula:
                    self.trocar_pos_celulas_na_heap(celula, celula_pai)
                else:
                    break

    def descer_celula_na_heap(self, celula):

        while True:
            celula_filha_esquerda = self.obter_celula_filha_esquerda(celula)
            celula_filha_direita = self.obter_celula_filha_direita(celula)

            if celula_filha_esquerda is not None:

                celula_filha_maior_prioridade = celula_filha_esquerda

                if celula_filha_direita is not None:
                    celula_filha_maior_prioridade = self.comparar_prioridade(celula_filha_esquerda, celula_filha_direita)

                celula_maior_prioridade_geral = self.comparar_prioridade(celula, celula_filha_maior_prioridade)

                if celula_maior_prioridade_geral == celula_filha_maior_prioridade:
                    self.trocar_pos_celulas_na_heap(celula, celula_filha_maior_prioridade)
                else:
                    break
            else:
                break
