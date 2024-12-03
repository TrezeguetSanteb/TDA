import numpy as np
from typing import List, Tuple
import time
import itertools

def demandas_validas(tablero: np.ndarray, demandas_filas: List[int], demandas_columnas: List[int]) -> bool:
    # Verificar filas
    for i, demanda in enumerate(demandas_filas):
        if demanda < 0 or np.sum(tablero[i, :]) > demanda:
            return False
    # Verificar columnas
    for j, demanda in enumerate(demandas_columnas):
        if demanda < 0 or np.sum(tablero[:, j]) > demanda:
            return False
    return True


def es_valido(tablero: np.ndarray, fila: int, columna: int, barco: int, orientacion: str) -> bool:
    n, m = tablero.shape
    largo = barco

    if orientacion == 'H':
        if columna + largo > m:
            return False
        return np.all(tablero[fila, columna:columna+largo] == 0)
    else:
        if fila + largo > n:
            return False
        return np.all(tablero[fila:fila+largo, columna] == 0)

def colocar_barco(tablero: np.ndarray, fila: int, columna: int, barco: int, orientacion: str):
    largo = barco
    if orientacion == 'H':
        tablero[fila, columna:columna+largo] = 1
    else:
        tablero[fila:fila+largo, columna] = 1

def quitar_barco(tablero: np.ndarray, fila: int, columna: int, barco: int, orientacion: str):
    largo = barco
    if orientacion == 'H':
        tablero[fila, columna:columna+largo] = 0
    else:
        tablero[fila:fila+largo, columna] = 0

def calcular_demanda_cumplida(tablero: np.ndarray, demandas_filas: List[int], demandas_columnas: List[int]) -> int:
    demanda_cumplida = 0
    demanda_cumplida += sum(min(demanda, np.sum(tablero[i,:])) for i, demanda in enumerate(demandas_filas))
    demanda_cumplida += sum(min(demanda, np.sum(tablero[:,j])) for j, demanda in enumerate(demandas_columnas))
    return demanda_cumplida

def backtracking(
    tablero: np.ndarray, 
    barcos: List[int], 
    demandas_filas: List[int], 
    demandas_columnas: List[int], 
    index: int, 
    posiciones: List[Tuple[int, int, str]], 
    mejor_solucion: List, 
    tiempo_inicio: float,
    tiempo_limite: float
) -> bool:
    # Tiempo de ejecución
    if time.time() - tiempo_inicio > tiempo_limite:
        return False

    if index == len(barcos):
        demanda_cumplida = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)
        if demanda_cumplida > mejor_solucion[0]:
            mejor_solucion[0] = demanda_cumplida
            mejor_solucion[1] = tablero.copy()
            mejor_solucion[2] = posiciones.copy()
        return True

    barco = barcos[index]
    n, m = tablero.shape
    encontrado = False

    # Intentar colocar el barco
    for fila in range(n):
        for columna in range(m):
            for orientacion in ['H', 'V']:
                if es_valido(tablero, fila, columna, barco, orientacion):
                    # Crear copias para no modificar el estado original
                    tablero_temp = tablero.copy()
                    colocar_barco(tablero_temp, fila, columna, barco, orientacion)
                    
                    # Validar demandas actuales
                    if demandas_validas(tablero_temp, demandas_filas, demandas_columnas):
                        posiciones.append((fila, columna, orientacion))
                        
                        # Llamada recursiva
                        resultado = backtracking(
                            tablero_temp, barcos, demandas_filas, demandas_columnas, 
                            index + 1, posiciones, mejor_solucion, tiempo_inicio, tiempo_limite
                        )
                        
                        posiciones.pop()
                        
                        if resultado:
                            encontrado = True

    # Intentar omitir este barco
    resultado = backtracking(
        tablero, barcos, demandas_filas, demandas_columnas, 
        index + 1, posiciones, mejor_solucion, tiempo_inicio, tiempo_limite
    )
    
    return encontrado or resultado


def resolver_batalla_naval(
    n: int, m: int, 
    barcos: List[int], 
    demandas_filas: List[int], 
    demandas_columnas: List[int], 
    tiempo_limite: float = 60.0
) -> Tuple[np.ndarray, List[Tuple[int, int, str]], int, int]:
    # Inicialización con NumPy para eficiencia
    tablero = np.zeros((n, m), dtype=int)
    posiciones = []
    mejor_solucion = [0, None, None]
    
    # Iniciar conteo de tiempo
    tiempo_inicio = time.time()
    
    # Ejecutar backtracking
    backtracking(
        tablero, barcos, demandas_filas, demandas_columnas, 
        0, posiciones, mejor_solucion, tiempo_inicio, tiempo_limite
    )
    
    # Calcular demanda total
    demanda_total = sum(demandas_filas) + sum(demandas_columnas)
    
    return (
        mejor_solucion[1], 
        mejor_solucion[2], 
        mejor_solucion[0], 
        demanda_total
    )

def parsear_archivo_con_arrays(archivo: str) -> List[List[int]]:
    with open(archivo, 'r') as f:
        res = []
        fi_co_bar = []
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                if fi_co_bar:
                    res.append(fi_co_bar)
                    fi_co_bar = []
            else:
                fi_co_bar.append(int(linea))
        if fi_co_bar:
            res.append(fi_co_bar)
    return res

def main(archivo_prueba: str):
    # Leer datos del archivo
    datos = parsear_archivo_con_arrays(archivo_prueba)
    demandas_filas = datos[0]
    demandas_columnas = datos[1]
    barcos = datos[2]

    # Dimensiones del tablero
    n = len(demandas_filas)
    m = len(demandas_columnas)

    # Resolver batalla naval con un límite de tiempo
    try:
        tablero, posiciones, demanda_cumplida, demanda_total = resolver_batalla_naval(
            n, m, barcos, demandas_filas, demandas_columnas, tiempo_limite=60.0
        )
        
        if tablero is not None:
            print("Posiciones:")
            for i, pos in enumerate(posiciones):
                print(f"{i}: {pos}")
            print(f"Demanda cumplida: {demanda_cumplida}")
            print(f"Demanda total: {demanda_total}")
            
            # Imprimir tablero de forma legible
            print("\nTablero:")
            for fila in tablero:
                print(' '.join(map(str, fila)))
        else:
            print("No se encontró solución dentro del tiempo límite")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    archivo_prueba = r'ejemplo.txt'
    main(archivo_prueba)