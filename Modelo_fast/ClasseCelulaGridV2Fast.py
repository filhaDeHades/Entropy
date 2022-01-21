import Modelo_fast.funcoes_fast as fst


class CelulaGridV2Fast:

    def __init__(self, grid_x, grid_y, andavel=True, parente=None):
        """Função inicializadora da classe 'CelulaGridV2Fast'

        Args:
            grid_x (int): Valor X da coordenada referente a posição da célula no grid.
            grid_y (int): Valor y da coordenada referente a posição da célula no grid.
            andavel (bool, optional): Indica se é uma célula vazia ou se representa um lugar. Defaults to True.
            parente (CelulaGridV2Fast, optional): Indica a célula-pai durante o cálculo do algoritmo A*. Defaults to None.
        """

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_grid = (grid_x, grid_y)

        self.andavel = andavel
        self.parente = parente

        self.ja_foi_visitado = False
        self.ja_foi_analisado = False

        self.g = 0
        self.h = 0
        self.f = 0

        self.lugar = None
        self.lista_agentes_presentes = []

    def atualizar_g(self):
        """'G' é a variável que representa o custo da célula anterior até essa célula.
        """

        self.g = self.parente.g + fst.obter_distancia(self.parente.pos_grid, self.pos_grid)


    def atualizar_h(self, pos_grid_final):
        """'H' é a variável que representa a distância estimada entre essa célula e a célula destino.

        Args:
            pos_grid_final ([type]): [description]
        """

        self.h = fst.obter_distancia(self.pos_grid, pos_grid_final)


    def atualizar_f(self):
        """'F' é a variável que representa o custo total da célula, ele é calculado através da soma de 'G' e 'H'
        """

        self.f = self.g + self.h
