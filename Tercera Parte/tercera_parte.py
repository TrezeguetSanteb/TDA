import time
import sys

class BatallaNaval:
    def __init__(self, n, m, filas, columnas, barcos, time_limit=180):
        self.n = n
        self.m = m
        self.filas = filas
        self.columnas = columnas
        self.barcos = sorted([(barco, i + 1) for i, barco in enumerate(barcos)], reverse=True)
        self.tablero = [[0] * m for _ in range(n)]
        self.mejor_tablero = None
        self.mejor_demanda_cumplida = 0
        self.demanda_total = sum(filas) + sum(columnas)
        self.time_limit = time_limit
        self.start_time = None
        self.timeout_reached = False
        
        # Caches para optimizar cálculos frecuentes
        self.casillas_por_fila = [0] * n  # Cuenta de casillas ocupadas por fila
        self.casillas_por_columna = [0] * m  # Cuenta de casillas ocupadas por columna
        
    def resolver(self):
        self.start_time = time.time()
        self.timeout_reached = False
        self.backtracking()
        if self.mejor_tablero:
            self.tablero = self.mejor_tablero
            return True
        return False

    def check_timeout(self):
        if time.time() - self.start_time > self.time_limit:
            self.timeout_reached = True
            return True
        return False

    def backtracking(self, barco_index=0, demanda_acumulada=0):
        if self.check_timeout():
            return demanda_acumulada
            
        if self.debe_podar(barco_index, demanda_acumulada):
            return demanda_acumulada
            
        if barco_index >= len(self.barcos):
            self._update_best_solution(demanda_acumulada)
            return demanda_acumulada

        barco, id_original = self.barcos[barco_index]
        mejor_demanda = demanda_acumulada
        
        # Obtener y ordenar posiciones válidas una sola vez
        posiciones = self.obtener_posiciones_validas(barco)
        
        for fila, col, orientacion in posiciones:
            if self.check_timeout():
                return mejor_demanda
                
            if not self.es_prometedora(fila, col, barco, orientacion, barco_index, demanda_acumulada):
                continue
                
            demanda_nueva = self.colocar_y_calcular(fila, col, barco, orientacion, id_original)
            nueva_demanda = self.backtracking(barco_index + 1, demanda_acumulada + demanda_nueva)
            self.remover_barco(fila, col, barco, orientacion)
            
            mejor_demanda = max(mejor_demanda, nueva_demanda)
            if mejor_demanda >= self.demanda_total:
                return mejor_demanda

        if self.se_puede_mejorar(barco_index, demanda_acumulada):
            nueva_demanda = self.backtracking(barco_index + 1, demanda_acumulada)
            mejor_demanda = max(mejor_demanda, nueva_demanda)
        
        return mejor_demanda

    def debe_podar(self, barco_index, demanda_acumulada):
        return (demanda_acumulada + 
                sum(barco[0] for barco in self.barcos[barco_index:]) * 2 <= 
                self.mejor_demanda_cumplida)

    def es_prometedora(self, fila, col, barco, orientacion, barco_index, demanda_acumulada):
        demanda_potencial = self.calcular_demanda_potencial(fila, col, barco, orientacion)
        return (demanda_acumulada + demanda_potencial + 
                (sum(b[0] for b in self.barcos[barco_index+1:]) * 2) > 
                self.mejor_demanda_cumplida)

    def se_puede_mejorar(self, barco_index, demanda_acumulada):
        return (demanda_acumulada + 
                sum(b[0] for b in self.barcos[barco_index+1:]) * 2 > 
                self.mejor_demanda_cumplida)

    def colocar_y_calcular(self, fila, col, barco, orientacion, id_original):
        self.colocar_barco(fila, col, barco, orientacion, id_original)
        return self.calcular_demanda_barco(fila, col, barco, orientacion)

    def obtener_posiciones_validas(self, barco):
        posiciones = []
        for i in range(self.n):
            # Skip si la fila ya está llena
            if self.casillas_por_fila[i] >= self.filas[i]:
                continue
                
            for j in range(self.m):
                # Skip si la columna ya está llena
                if self.casillas_por_columna[j] >= self.columnas[j]:
                    continue
                    
                if self.tablero[i][j] != 0:
                    continue
                
                for orientacion in ['H', 'V']:
                    if self.es_valido(i, j, barco, orientacion):
                        score = self.calcular_score_posicion(i, j, barco, orientacion)
                        posiciones.append((score, i, j, orientacion))
        
        # Ordenar por score y devolver solo las coordenadas
        return [(i, j, o) for _, i, j, o in sorted(posiciones, reverse=True)]

    def es_valido(self, fila, col, barco, orientacion):
        if orientacion == 'H':
            if col + barco > self.m:
                return False
            if self.casillas_por_fila[fila] + barco > self.filas[fila]:
                return False
            for j in range(col, col + barco):
                if self.casillas_por_columna[j] >= self.columnas[j] or self.tablero[fila][j] != 0:
                    return False
                
            # Verificar área alrededor del barco
            for i in range(max(0, fila - 1), min(self.n, fila + 2)):
                for j in range(max(0, col - 1), min(self.m, col + barco + 1)):
                    if self.tablero[i][j] != 0:
                        return False
        else:
            if fila + barco > self.n:
                return False
            if self.casillas_por_columna[col] + barco > self.columnas[col]:
                return False
            for i in range(fila, fila + barco):
                if self.casillas_por_fila[i] >= self.filas[i] or self.tablero[i][col] != 0:
                    return False
                
            # Verificar área alrededor del barco
            for i in range(max(0, fila - 1), min(self.n, fila + barco + 1)):
                for j in range(max(0, col - 1), min(self.m, col + 2)):
                    if self.tablero[i][j] != 0:
                        return False
        return True

    def calcular_score_posicion(self, i, j, barco, orientacion):
        score = 0
        # Priorizar posiciones que maximizan el uso de restricciones
        if orientacion == 'H':
            score += (self.filas[i] - self.casillas_por_fila[i]) * 2
            for k in range(j, min(j + barco, self.m)):
                score += self.columnas[k] - self.casillas_por_columna[k]
        else:
            score += (self.columnas[j] - self.casillas_por_columna[j]) * 2
            for k in range(i, min(i + barco, self.n)):
                score += self.filas[k] - self.casillas_por_fila[k]
        
        # Bonus para barcos grandes en los bordes
        if barco > 2:
            if i == 0 or i == self.n-1 or j == 0 or j == self.m-1:
                score += 5
        
        return score

    def colocar_y_calcular(self, fila, col, barco, orientacion, valor):
        if orientacion == 'H':
            for i in range(barco):
                self.tablero[fila][col + i] = valor
                self.casillas_por_fila[fila] += 1
                self.casillas_por_columna[col + i] += 1
        else:
            for i in range(barco):
                self.tablero[fila + i][col] = valor
                self.casillas_por_fila[fila + i] += 1
                self.casillas_por_columna[col] += 1
        
        return self.calcular_demanda_barco(fila, col, barco, orientacion)

    def remover_barco(self, fila, col, barco, orientacion):
        if orientacion == 'H':
            for i in range(barco):
                self.tablero[fila][col + i] = 0
                self.casillas_por_fila[fila] -= 1
                self.casillas_por_columna[col + i] -= 1
        else:
            for i in range(barco):
                self.tablero[fila + i][col] = 0
                self.casillas_por_fila[fila + i] -= 1
                self.casillas_por_columna[col] -= 1

    def calcular_demanda_barco(self, fila, col, barco, orientacion):
        demanda = 0
        if orientacion == 'H':
            if self.casillas_por_fila[fila] <= self.filas[fila]:
                demanda += barco
            for j in range(col, col + barco):
                if self.casillas_por_columna[j] <= self.columnas[j]:
                    demanda += 1
        else:
            if self.casillas_por_columna[col] <= self.columnas[col]:
                demanda += barco
            for i in range(fila, fila + barco):
                if self.casillas_por_fila[i] <= self.filas[i]:
                    demanda += 1
        return demanda

    def calcular_demanda_potencial(self, fila, col, barco, orientacion):
        demanda = 0
        if orientacion == 'H':
            if self.casillas_por_fila[fila] + barco <= self.filas[fila]:
                demanda += barco
            for j in range(col, col + barco):
                if self.casillas_por_columna[j] + 1 <= self.columnas[j]:
                    demanda += 1
        else:
            if self.casillas_por_columna[col] + barco <= self.columnas[col]:
                demanda += barco
            for i in range(fila, fila + barco):
                if self.casillas_por_fila[i] + 1 <= self.filas[i]:
                    demanda += 1
        return demanda

    def _update_best_solution(self, demanda_acumulada):
        if demanda_acumulada > self.mejor_demanda_cumplida:
            self.mejor_demanda_cumplida = demanda_acumulada
            if self.mejor_tablero is None:
                self.mejor_tablero = [fila[:] for fila in self.tablero]
            else:
                for i in range(self.n):
                    self.mejor_tablero[i][:] = self.tablero[i]

    def imprimir_tablero(self):
        for fila in self.tablero:
            print(' '.join(map(str, fila)))
        print(f"Demanda cumplida: {self.mejor_demanda_cumplida}")
        print(f"Demanda total: {self.demanda_total}")
        if self.timeout_reached:
            print(f"¡Tiempo límite de {self.time_limit} segundos alcanzado!")
        print(f"Tiempo total de ejecución: {time.time() - self.start_time:.2f} segundos")

def leer_ejemplo(archivo):
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

if __name__ == "__main__":
    archivo = sys.argv[1]
    n, m, barcos, filas, columnas = leer_ejemplo(archivo)
    juego = BatallaNaval(n, m, filas, columnas, barcos, time_limit=180)
    juego.resolver()
    juego.imprimir_tablero()