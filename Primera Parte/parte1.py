import sys
import numpy as np
def sofiaa(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if p > u:
        vec = vec[1:]
        return p, vec
    else:
        vec = vec[:-1]
        return u, vec

def mateoo(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if p < u:
        vec = vec[1:]
        return p , vec
    else:
        vec = vec[:-1]
        return u, vec
    
def juego_greedy(vec):
    
    v_sofia = [] * (len(vec)//2)
    v_mateo = [] * (len(vec)//2)

    for i in range(0, len(vec)):
        if (i%2==0 or i==0):
            resultado, vec = sofiaa(vec) 
            v_sofia.append(resultado)
        else:
            resultado, vec = mateoo(vec) 
            v_mateo.append(resultado)
    return sum(v_sofia)

def ParsearArchivo(archivo):
    with open(archivo, 'r') as archivo:
        contenido = archivo.read()
        arr = [int(num) for num in contenido.split(';') if num.strip().isdigit()]
    return arr

if __name__ == "__main__":
    archivo = sys.argv[1]
    print(juego_greedy(ParsearArchivo(archivo)))