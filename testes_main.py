import numpy as np

a = np.array([(0, 1), (1, 2)])
b = np.array([(0, 1), (2, 3)])

for i in a:
    for j in b:

        if i[0] == j[0] and i[1] == j[1]:
            print(i)