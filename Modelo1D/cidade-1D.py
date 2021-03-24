
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import igraph
import random as rd
#import networkx as nx
import math
from scipy.optimize import curve_fit

import scipy.stats as st
#import statsmodels as sm
from numpy import inf

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.layouts import gridplot


from scipy import stats

from statistics import mode
from scipy.optimize import minimize
import random
from random import randint

from bokeh.io import export_png

from bokeh.plotting import figure, output_file, save
import os


# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rd
import os

import bokeh
from bokeh.layouts import column
from bokeh.layouts import row

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.layouts import gridplot
#from bokeh.io import output_file, show, vplot

from scipy.optimize import curve_fit
output_notebook()

from bokeh.plotting import figure, output_file, show


from scipy.stats import entropy


#from scipy.optimize import curve_fit
#import networkx as nx
#import math
#import igraph


# In[3]:


from bokeh.palettes import gray
from bokeh.palettes import viridis




# In[107]:


N = 50           #50 ou 100 / number of citizens
L = N         
rho = 1.0        # density = 1 / densidade de espacos (?)
P = int(rho*N)   # number of public spaces (numero de lugares)
Nchar = 100      #number of possible characters inside the population (o que é isso?)

c1 = 0.2   #   0.5  constante da diferenca de characteristica
c2 = 1.0    #  entre 0 e 1 -- constante da distancia  -- / constante  c2=0 => T infinito (espaco nao importa)


eta = 0.5   # 0.5   # passo do agente
theta = 0.1   #0.1  #passo do espaco


tmax = 1000     #15000


# In[120]:


v_sigma =  Nchar*np.random.rand(N)  # array de 50 elementos entre 0 e 100 / orientacao dos agentes?
v_space =  Nchar*np.random.rand(P)  # array de 50 elementos entre 0 e 100 / orientacao dos lugares?
v_space_new =  np.zeros(P)          # array de 50 zeros 
v_space_x  =   list(range(0,L,int(1/rho)))      #np.random.randint(L, size=P)    #       rand (P, L ) / lista de o ate L-1, com step de 1/rho - o q representa?
v_entropy_space = []
v_entropy_ind = []  
M_sigma_t =  np.zeros([N,tmax])     # matriz de zeros de dimensão N x Tmax (50x1000) / o que representa?
M_space_t =  np.zeros([P,tmax])     # matriz de zeros de dimensão P x Tmax (50x1000) / o que representa?

for t in range(tmax):
    
    #print('t=%d'%t)
    
    v_space_new = v_space
    
    for k in range(P):
        M_space_t[k,t] = v_space[k] # o que ta fazendo aqui?
    
    for i in range(N):
    
        M_sigma_t[i,t] = v_sigma[i] # o que ta fazendo aqui?
    
        # sorteio para interacao 

        v_prob =  np.zeros(P)  
        norma = 0
        for k in range(P):
            
            #menor = min( v_sigma[i], v_space[k])
            #maior = max( v_sigma[i], v_space[k])
            #dist1 =  min(  abs(v_sigma[i] -  v_space[k])   ,   menor + Nchar -maior)
            
            dist1 =  abs(v_sigma[i] -  v_space[k]) # diferenca entre orientacao agentes e lugar
            
            
            menor = min(i,v_space_x[k]) # procurando o menor de que?
            maior = max(i,v_space_x[k]) # procurando o maior de que?
            dist2 = min( abs(i - v_space_x[k] )  ,  (menor + L - maior)   ) # distancia?

            #print(dist1,dist2)
            
            
            E =  c1*dist1 + c2*dist2    # expoente da formula

            v_prob[k] = np.exp(-E)      # "e" elevado pelo expoente acima

            norma = norma + v_prob[k]    # adicionando a probabilidade à norma / o que é a norma?
        

        v_prob = v_prob/norma
        kchoose = list(np.random.choice(range(P), 1, p=v_prob))[0]
    
        v_space_new[kchoose] = (v_space_new[kchoose] + theta* v_sigma[i])/(1+theta)
        v_sigma[i] = (v_sigma[i] + eta*v_space[kchoose])/(1+eta)  
    

    v_space = v_space_new
    
    #####
    #calculo da entropia 
    ######
    
    Freq,binEdges = np.histogram(v_space,bins= Nchar)
    freq = Freq/P   #  sum(Freq)
    v_entropy_space.append(entropy(freq, base=2))
    
    Freq,binEdges = np.histogram(v_sigma,bins= Nchar)
    freq = Freq/N   #  sum(Freq)
    v_entropy_ind.append(entropy(freq, base=2))
    


# In[121]:


#M_sigma_t


# In[122]:


#M_sigma_t[0]


# In[123]:


p1 = figure(title=" red: individuos ,  blue: espacos publicos", x_axis_label='time step', y_axis_label= 'character') #, x_axis_type="log", y_axis_type="log"   )

for i in range(N):
    p1.line( range(tmax) , M_sigma_t[i]  ,  line_width=1, color = 'red')  #legend="individuos",  

    

for k in range(P):
    p1.line( range(tmax) , M_space_t[k]  ,    line_width=1, color = 'blue') #legend="spaces",
    

    
p1.legend.location = "top_left" 


show(p1)








# In[124]:


p1 = figure(title=" Entropia", x_axis_label='time step', y_axis_label= 'Entropia') #, x_axis_type="log", y_axis_type="log"   )
p1.line( range(tmax) , v_entropy_space,  line_width=1, color = 'blue', legend="espacos publicos")  
p1.line( range(tmax) , v_entropy_ind,  line_width=1, color = 'red', legend="individuos")  
p1.legend.location = "top_right" # "top_left" 


show(p1)


# In[125]:



plt.figure(4)
imgplot = plt.imshow( M_sigma_t , aspect='auto' )
imgplot.set_cmap('rainbow') # gray  hot
imgplot.set_clim(0.0,Nchar)
plt.colorbar()
plt.title("Cores: caracteristica do individuo")
plt.xlabel("time")
plt.ylabel("Posicao do individuo")
#plt.imshow(aspect='auto')
plt.axis([0, tmax, 0, N])
plt.savefig('saida.png', bbox_inches=0)







# In[126]:



plt.figure(4)
imgplot = plt.imshow( M_space_t , aspect='auto' )
imgplot.set_cmap('rainbow') # gray  hot
imgplot.set_clim(0.0,Nchar)
plt.colorbar()
plt.title("Cores: caracteristica do espaco publico")
plt.xlabel("time")
plt.ylabel("Posicao do espaco publico")
#plt.imshow(aspect='auto')
plt.axis([0, tmax, 0, N])
plt.savefig('saida2.png', bbox_inches=0)



# In[127]:


y,binEdges = np.histogram( v_space,bins= Nchar)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

plt.figure(2)
plt.plot(bincenters,y,'-')
plt.ylabel("Frequency")
plt.xlabel("Space chararacter")
#plt.yscale('log')
#plt.xscale('log')
plt.title('Histogram')
plt.show()


# In[128]:


v_colors = viridis(N)

p1 = figure(title="Cores representam a posicao dos individuos", 
            x_axis_label='time step', y_axis_label= 'Caracteristica do individuo') #, x_axis_type="log", y_axis_type="log"   )

for i in range(N):
    p1.line( range(tmax) , M_sigma_t[i]  ,  line_width=2, color = v_colors[i])



show(p1)


# In[129]:


v_colors = viridis(P)

p1 = figure(title="Cores representam a posicao do espaco ",
            x_axis_label='time step', y_axis_label= 'Caracteristica do espaco') #, x_axis_type="log", y_axis_type="log"   )

for k in range(P):
    p1.line( range(tmax) , M_space_t[k]  ,  line_width=2, color = v_colors[k])



show(p1)


# In[ ]:





# In[130]:




y,binEdges = np.histogram( v_space,bins=100)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

plt.figure(2)
plt.plot(bincenters,y,'-')
plt.ylabel("Frequency")
plt.xlabel("Space chararacter")
#plt.yscale('log')
#plt.xscale('log')
plt.title('Histogram')
plt.show()



# In[131]:



#


# # Rascunho

# In[ ]:


print(random.random())


# In[ ]:


np.zeros(shape=(N))


# In[ ]:


list(np.zeros(4))


# In[ ]:



for k in range(10):
    print(lis = random.randint(0,N-1))


# In[ ]:


np.random.randint(4, size=10)


# In[ ]:


10*np.random.rand(10)


# In[ ]:


min(2,5)


# In[ ]:


max(2,5)


# In[ ]:


max(5,5)


# In[ ]:


abs(3-5)


# In[ ]:


D0 = np.array([np.cos(2*np.pi*f*time), np.sin(2*np.pi*f*time), np.ones(time.size)]).T
print(D0)


# In[ ]:


np.array([1,2,3], [2,2,2]) 


# In[ ]:


time = np.array([0, 1, 2, 3])


# In[ ]:


np.array(time+ time)


# In[ ]:


np.concatenate([time,time])   #, axis=1) 


# In[ ]:


np.concatenate(time,time)


# In[ ]:


M = np.zeros([2,3])


# In[ ]:


M[1,1] = 5


# In[ ]:


print(M)


# In[ ]:


p1 = figure(title=" ", x_axis_label='Population (N)', y_axis_label= 'PIB', x_axis_type="log", y_axis_type="log"   )
#p1.line(  ,  line_width=2, color = 'red')

p1.xaxis.axis_label_text_font_size = "20pt"
p1.yaxis.axis_label_text_font_size = "20pt"    
p1.xaxis.major_label_text_font_size = "14pt"
p1.yaxis.major_label_text_font_size = "14pt"
p1.title.text_font_size = '13pt'



p1.circle( popu, pib, size = 10) #, legend="N=%d"%N)   #color = 'red',    
#p1.legend.location = "top_left" 

p1.line(X_teo,  Y_teo,       line_width=2, color = 'red', 
        legend="Expoente:%.2f+- %0.2f"%(result.x[1], 1.96*simples.stderr   )  )

p1.legend.location = "top_left" 

show(p1)


# In[ ]:


np.random.choice(4, 10, p=[0.1, 0.2, 0.3, 0.4])


# In[ ]:


Numero = list(np.random.choice([0.2,4.1,6], 1, p=[0.1, 0.8, 0.1]))[0]


# In[ ]:


Numero


# In[315]:


all_palettes['Viridis'][4]


# In[316]:





# In[320]:


v_colors

