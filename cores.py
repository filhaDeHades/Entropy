# CORES EM RGB
import random


preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (106, 106, 106)
vermelho = (255, 0, 0)
laranja = (255, 127, 0)
amarelo = (255, 255, 0)
verde = (0, 255, 0)
verde_claro = (0, 255, 127)
verde_escuro = (0, 128, 0)
verde_azeite = (107, 142, 35)
verde_amarronzado = (128, 128, 0)
azul = (0, 0, 255)
azul_cyan = (0, 255, 255)
azul_claro = (0, 191, 255)
azul_escuro = (0, 0, 128)
rosa = (255, 0, 255)
roxo = (128, 0, 128)
roxo_escuro = (139, 0, 139)

lista_cores_completa = [preto, branco, vermelho, laranja, amarelo, verde, azul, roxo]
lista_cores_coloridas = [vermelho, laranja, amarelo, verde, verde_claro, verde_escuro, verde_azeite, verde_amarronzado,
                         azul, azul_cyan, azul_claro, azul_escuro, rosa, roxo, roxo_escuro]

pulo = 50

lista_cores_random = []
for i in range(0, 1000, pulo):
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    z = random.randint(0, 255)
    if (x,y,z) in lista_cores_random:
        i -= 1
        continue
    lista_cores_random.append((x,y,z))
