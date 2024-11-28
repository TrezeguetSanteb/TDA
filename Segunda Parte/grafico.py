# Imports necesarios para el notebook
from random import seed
from segunda_parte import juego_programacion_dinamica
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

x = np.linspace(100, 5_000, 10).astype(int)
results = time_algorithm(juego_programacion_dinamica, x, lambda s: [get_random_array(s)])


#funcion Cuadratica
f_n = lambda n, c1, c2, c3: c1 * n**2 + c2 * n + c3

## Para ajustar la funcion
c_n, _ = sp.optimize.curve_fit(f_n, x, [results[n] for n in x])

ax: plt.Axes
fig, ax = plt.subplots()
ax.plot(x, [results[n] for n in x], label="Medición")
ax.plot(x, [f_n(n, c_n[0], c_n[1], c_n[2]) for n in x], 'r--', label="Ajuste $O(n^2)$")
ax.set_title('Tiempo de ejecución del algoritmo')
ax.set_xlabel('Tamaño del array')
ax.set_ylabel('Tiempo de ejecución (s)')
ax.legend()
None

errors_n = [np.abs(f_n(n, *c_n) - results[n]) for n in x]

ax: plt.Axes
fig, ax = plt.subplots()
ax.plot(x, errors_n, label="Ajuste $O(n)$")
ax.set_title('Error de ajuste')
ax.set_xlabel('Tamaño del array')
ax.set_ylabel('Error absoluto (s)')
ax.legend()
None

plt.show()
