import pygame as pg
import cores
import funcoes


class CelulaGridV2:

    def __init__(self, grid_x, grid_y, cell_size, g=0, h=0, f=0, andavel=True, cor=cores.branco, parente=None,
                 mudar_cor=True):

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_grid = (grid_x, grid_y)
        self.cell_size = cell_size
        self.andavel = andavel
        self.parente = parente
        self.ja_foi_visitado = False
        self.ja_foi_analisado = False
        self.g = g
        self.h = h
        self.f = f
        self.cor = cor
        self.display_cor_de_calor = False
        self.cor_de_calor = cor

        self.lugar = None
        self.eh_a_celula_principal = False
        self.cor_celula_principal = cores.vermelho
        self.lista_agentes_presentes = []

        self.visitas = 0
        self.pode_mudar_cor = mudar_cor

    def draw(self, janela: pg.display):

        if self.lugar is None:

            cor_mostrada = self.cor

            if self.display_cor_de_calor is True:
                cor_mostrada = self.cor_de_calor

            pg.draw.rect(janela, cor_mostrada, (self.grid_x * self.cell_size, self.grid_y * self.cell_size,
                                                self.cell_size, self.cell_size))
        else:
            pg.draw.rect(janela, self.lugar.cor, (self.grid_x * self.cell_size, self.grid_y * self.cell_size,
                                                  self.cell_size, self.cell_size))

    def mudar_estado(self):

        if self.andavel is True:
            self.andavel = False
            self.cor = cores.preto
        else:
            self.andavel = True
            self.cor = cores.branco

    def atualizar_g(self, custo_menor_mov, custo_maior_mov):
        self.g = self.parente.g + \
                 funcoes.distancia_sebastiana(custo_menor_mov, custo_maior_mov, self.parente.pos_grid, self.pos_grid)

    def atualizar_h(self, custo_menor_mov, custo_maior_mov, pos_grid_final):
        self.h = funcoes.distancia_sebastiana(custo_menor_mov, custo_maior_mov, self.pos_grid, pos_grid_final)

    def atualizar_f(self):
        self.f = self.g + self.h

    def mudar_cor(self, nova_cor):
        self.cor = nova_cor

    def update_cor_de_calor(self):
        if self.pode_mudar_cor is True:
            cor_r = 255
            cor_g = 255
            cor_b = 255

            if self.visitas <= 255:
                cor_r -= self.visitas
                cor_g -= self.visitas
            elif 255 < self.visitas < 511:
                cor_r = self.visitas - 255
                cor_g = 0
            elif self.visitas > 511:
                cor_g = 0
                cor_b = 255 - (self.visitas - 511)
                if cor_b < 0:
                    cor_b = 0

            nova_cor = (cor_r, cor_g, cor_b)
            self.cor_de_calor = nova_cor
