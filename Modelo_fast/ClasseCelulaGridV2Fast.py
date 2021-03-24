import Modelo_fast.funcoes_fast as fst


class CelulaGridV2Fast:

    def __init__(self, grid_x, grid_y, andavel=True, parente=None):
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
        self.g = self.parente.g + fst.obter_distancia(self.parente.pos_grid, self.pos_grid)

    def atualizar_h(self, pos_grid_final):
        self.h = fst.obter_distancia(self.pos_grid, pos_grid_final)

    def atualizar_f(self):
        self.f = self.g + self.h
