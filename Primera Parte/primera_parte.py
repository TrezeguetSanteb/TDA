import sys
import numpy as np

def sofiaa(vec):
    p = vec[0]
    u = vec[-1]

    if p > u:
        vec = vec[1:]
        return p, vec, "primera"
    else:
        vec = vec[:-1]
        return u, vec, "ultima"

def mateoo(vec):
    p = vec[0]
    u = vec[-1]

    if p < u:
        vec = vec[1:]
        return p, vec, "primera"
    else:
        vec = vec[:-1]
        return u, vec, "ultima"

def juego_greedy(vec):
    v_sofia = []
    v_mateo = []

    for i in range(len(vec)):
        if i % 2 == 0:
            moneda, vec, posicion = sofiaa(vec)
            v_sofia.append((moneda, posicion))
        else:
            moneda, vec, posicion = mateoo(vec)
            v_mateo.append((moneda, posicion))

    return v_sofia, v_mateo

if __name__ == "__main__":
    archivo = sys.argv[1]
    vec = np.loadtxt(archivo, delimiter=';', dtype=int)
    v_sofia, v_mateo = juego_greedy(list(vec))
    ganancia_sophia = sum([moneda for moneda, _ in v_sofia])
    ganancia_mateo = sum([moneda for moneda, _ in v_mateo])

    if ganancia_sophia <= ganancia_mateo:
        print("Mateo gana")
    else:
        for i in range(len(v_sofia)):
            moneda, posicion = v_sofia[i]
            print(f"{posicion} moneda para Sophia({moneda})", end=", ")

            if i < len(v_mateo):
                moneda, posicion = v_mateo[i]
            print(f"{posicion} moneda para Mateo({moneda})", end=", ")
            print() 
    
        print(f"Ganancia de Sophia: {ganancia_sophia}")