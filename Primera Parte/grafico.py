# Imports necesarios para el notebook
from random import seed

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from util import time_algorithm

# Siempre seteamos la seed de aleatoridad para que los # resultados sean reproducibles
seed(12345)
np.random.seed(12345)

sns.set_theme()

def get_random_array(size: int):
    return np.random.randint(0, 100.000, size)

def sofiaa(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if p > u:
        vec = vec[1:]
        return p
    else:
        vec = vec[:-1]
        return u

def mateoo(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if p < u:
        vec = vec[1:]
        return p
    else:
        vec = vec[:-1]
        return u


def juego_greedy(vec):

    v_sofia = [] * (len(vec)//2)
    v_mateo = [] * (len(vec)//2)

    for i in range(0, len(vec)):
        if (i%2==0 or i==0):
            v_sofia.append(sofiaa(vec))

        else:
            v_mateo.append(mateoo(vec))

    return v_sofia, v_mateo

x = np.linspace(100, 100_000, 20).astype(int)
results = time_algorithm(juego_greedy, x, lambda s: [get_random_array(s)])


#funcion lineal
f_n = lambda n, c1, c2: c1 * n + c2

## Para ajustar la funcion
c_n, _ = sp.optimize.curve_fit(f_n, x, [results[n] for n in x])

ax: plt.Axes
fig, ax = plt.subplots()
ax.plot(x, [results[n] for n in x], label="Medición")
ax.plot(x, [f_n(n, c_n[0], c_n[1]) for n in x], 'r--', label="Ajuste $o(n)$")
ax.set_title('Tiempo de ejecución del algoritmo')
ax.set_xlabel('Tamaño del array')
ax.set_ylabel('Tiempo de ejecución (s)')
ax.legend()
None

errors_n = [np.abs(c_n[0] * n + c_n[1] - results[n]) for n in x]

ax: plt.Axes
fig, ax = plt.subplots()
ax.plot(x, errors_n, label="Ajuste $O(n)$")
ax.set_title('Error de ajuste')
ax.set_xlabel('Tamaño del array')
ax.set_ylabel('Error absoluto (s)')
ax.legend()
None

plt.show()
