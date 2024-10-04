import sys
def sofiaa(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if(p>u):
        vec.pop(0)
        return p
    else:
        vec.pop(len(vec)-1)
        return u
    
def mateoo(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if(p<u):
        vec.pop(0)
        return p
    else:
        vec.pop(len(vec)-1)
        return u
    
    
def juego_greedy(vec):
    
    v_sofia = [] * (len(vec)//2)
    v_mateo = [] * (len(vec)//2)

    for i in range(0, len(vec)):
        if (i%2==0 or i==0):
            v_sofia.append(sofiaa(vec))

        else:
            v_mateo.append(mateoo(vec))

    return sum(v_sofia)

def ParsearArchivo(archivo):
    with open(archivo, 'r') as archivo:
        contenido = archivo.read()
        arr = [int(num) for num in contenido.split(';') if num.strip().isdigit()]
    return arr

if __name__ == "__main__":
    archivo = sys.argv[1]
    print(juego_greedy(ParsearArchivo(archivo)))