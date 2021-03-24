import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rd
import math
from statistics import mode
import random
import os

from scipy.optimize import curve_fit
from scipy.optimize import minimize
import scipy.stats as st
from scipy import stats
from scipy.stats import entropy

from bokeh.plotting import figure, show, output_file, save
from bokeh.io import output_notebook
from bokeh.layouts import gridplot
from bokeh.palettes import gray
from bokeh.palettes import viridis
from bokeh.io import export_png

qntAgentes = 50
tamanhoCidade = qntAgentes
densidadeEspaco = 1.0
qntLugares = int(densidadeEspaco * qntAgentes)
qntOrientacoes = 100

a = 0.2 # constante dif orientacao
b = 1.0 # costante distancia

# pesos contaminação (testar varios valores)
alfa = 0.2
theta = 1.0

timeSteps = 1000