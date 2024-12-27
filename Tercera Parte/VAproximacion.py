import sys
import time

def verificar_adyacentes(matriz, fila, columna, barco, es_vertical):
    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0])

    if es_vertical:
        inicio_fila = max(0, fila - 1)
        fin_fila = min(cantidad_filas, fila + barco + 1)
        inicio_columna = max(0, columna - 1)
        fin_columna = min(cantidad_columnas, columna + 2)
    else:
        inicio_fila = max(0, fila - 1)
        fin_fila = min(cantidad_filas, fila + 2)
        inicio_columna = max(0, columna - 1)
        fin_columna = min(cantidad_columnas, columna + barco + 1)

    for i in range(inicio_fila, fin_fila):
        for j in range(inicio_columna, fin_columna):
            if i < cantidad_filas and j < cantidad_columnas and matriz[i][j] == 1:
                return False
    return True

def colocar_vertical(matriz, fila, columna, barco, restriccion_columnas, restriccion_filas):
    if fila + barco > len(matriz):
        return False

    if restriccion_filas[columna] < barco:
        return False

    for i in range(fila, fila + barco):
        if restriccion_columnas[i] <= 0:
            return False

    if verificar_adyacentes(matriz, fila, columna, barco, True):
        for i in range(fila, fila + barco):
            matriz[i][columna] = 1
            restriccion_columnas[i] -= 1
        restriccion_filas[columna] -= barco
        return True
    return False

def colocar_horizontal(matriz, fila, columna, barco, restriccion_columnas, restriccion_filas):
    if columna + barco > len(matriz[0]):
        return False

    if restriccion_columnas[fila] < barco:
        return False

    for i in range(columna, columna + barco):
        if restriccion_filas[i] <= 0:
            return False

    if verificar_adyacentes(matriz, fila, columna, barco, False):
        for i in range(columna, columna + barco):
            matriz[fila][i] = 1
            restriccion_filas[i] -= 1
        restriccion_columnas[fila] -= barco
        return True
    return False

def aproximacion_barcos(matriz, restriccion_columnas, restriccion_filas, barcos):
    barcos = sorted(barcos, reverse=True)

    while barcos:
        barco_actual = barcos[0]
        colocado = False

        copia_restriccion_columnas = restriccion_columnas.copy()
        copia_restriccion_filas = restriccion_filas.copy()

        while max(max(copia_restriccion_columnas), max(copia_restriccion_filas)) > 0:
            max_columna = max(copia_restriccion_columnas)
            max_fila = max(copia_restriccion_filas)

            if max_columna >= max_fila:
                fila_max = copia_restriccion_columnas.index(max_columna)
                for columna in range(len(matriz[0])):
                    if colocar_horizontal(matriz, fila_max, columna, barco_actual, restriccion_columnas, restriccion_filas):
                        colocado = True
                        break
                copia_restriccion_columnas[fila_max] = 0
            else:
                columna_max = copia_restriccion_filas.index(max_fila)
                for fila in range(len(matriz)):
                    if colocar_vertical(matriz, fila, columna_max, barco_actual, restriccion_columnas, restriccion_filas):
                        colocado = True
                        break
                copia_restriccion_filas[columna_max] = 0

            if colocado:
                break

        barcos.pop(0)

    return matriz

def leer_datos(archivo):
    with open(archivo, 'r') as f:
        lineas = f.read().strip().split('\n')

    lineas = [linea for linea in lineas if not linea.startswith('#')]

    restricciones_filas = []
    i = 0
    while lineas[i] != '':
        restricciones_filas.append(int(lineas[i]))
        i += 1

    i += 1
    restricciones_columnas = []
    while lineas[i] != '':
        restricciones_columnas.append(int(lineas[i]))
        i += 1

    i += 1
    barcos = []
    while i < len(lineas):
        barcos.append(int(lineas[i]))
        i += 1

    n = len(restricciones_filas)
    m = len(restricciones_columnas)

    return n, m, barcos, restricciones_filas, restricciones_columnas

def calcular_demanda_cumplida(matriz):
    contador = 0
    for fila in matriz:
        for columna in fila:
            if columna == 1:
                contador += 2
    return contador

def calcular_demanda_total(filas, columnas):
    return sum(filas) + sum(columnas)

def imprimir_matriz(matriz, total):
    for fila in matriz:
        print(' '.join(map(str, fila)))
    print(f"Demanda cumplida: {calcular_demanda_cumplida(matriz)}")
    print(f"Demanda total: {total}")

if __name__ == "__main__":
    archivo = sys.argv[1]
    n, m, barcos, filas, columnas = leer_datos(archivo)
    total = calcular_demanda_total(filas, columnas)
    matriz = [[0] * m for _ in range(n)]
    solucion = aproximacion_barcos(matriz, filas, columnas, barcos)
    imprimir_matriz(solucion, total)
