import copy
import sys

class Juego:
    restricciones = {'filas': [], 'columnas': []}
    tablero = []
    tamanios_barcos = {}
    tamanios_barcos_colocables = {}
    tamanios_barcos_sacados = {}
    posiciones_restantes = 0
    casillas_ya_ocupadas = 0
    demanda_total = 0

    def __init__(self, *args):
        if len(args) == 3:
            restricciones_filas, restricciones_columnas, barcos = args
            self.restricciones['filas'] = restricciones_filas
            self.restricciones['columnas'] = restricciones_columnas
            self.tablero = [["-"] * len(restricciones_columnas) for _ in range(len(restricciones_filas))]
            for indice in range(len(barcos)):
                if barcos[indice] not in self.tamanios_barcos:
                    self.tamanios_barcos[barcos[indice]] = [indice]
                    self.tamanios_barcos_sacados[barcos[indice]] = []
                else:
                    self.tamanios_barcos[barcos[indice]].append(indice)
            self.demanda_total = sum(restricciones_columnas) + sum(restricciones_filas)
        elif len(args) == 6:
            restricciones, tablero, tamanios_barcos, tamanios_barcos_sacados, posiciones_restantes, casillas_ya_ocupadas, demanda_total = args
            self.restricciones = restricciones
            self.tablero = tablero
            self.tamanios_barcos = tamanios_barcos
            self.tamanios_barcos_sacados = tamanios_barcos_sacados
            self.posiciones_restantes = posiciones_restantes
            self.casillas_ya_ocupadas = casillas_ya_ocupadas
            self.demanda_total = demanda_total
        #self.obtener_posiciones_restantes()
        self.resetear_barcos_colocables()
        #self.filtrar_barcos_colocables()

    def resetear_barcos_colocables(self):
        self.tamanios_barcos_colocables = copy.deepcopy(self.tamanios_barcos)
    
    def copiar(self):
        return Juego(copy.deepcopy(self.restricciones), copy.deepcopy(self.tablero), copy.deepcopy(self.tamanios_barcos), copy.deepcopy(self.tamanios_barcos_sacados), self.posiciones_restantes, self.casillas_ya_ocupadas, self.demanda_total)
    
    def puede_colocar_barco_horizontal(self, tamanio_barco, posicion):
        fila = posicion['fila']
        columna = posicion['columna']

        if tamanio_barco not in self.tamanios_barcos_colocables.keys() or self.tamanios_barcos[tamanio_barco] == []:
            return False
    
        if len(self.tablero[0]) < columna + tamanio_barco: 
            return False

        if self.restricciones['filas'][fila] - tamanio_barco < 0: return False
        for indice_columna in range(columna, columna + tamanio_barco):
            if self.restricciones['columnas'][indice_columna] - 1 < 0: return False
        
        for indice in range(0, tamanio_barco):
            if not self.es_posicion_disponible({'fila':fila, 'columna':columna + indice}):
                return False
            
        return True
    
    def puede_colocar_barco_vertical(self, tamanio_barco, posicion):
        fila = posicion['fila']
        columna = posicion['columna']

        if tamanio_barco not in self.tamanios_barcos_colocables.keys() or self.tamanios_barcos[tamanio_barco] == []:
            return False

        if len(self.tablero) < fila + tamanio_barco: 
            return False

        if self.restricciones['columnas'][columna] - tamanio_barco < 0: return False
        for indice_fila in range(fila, fila + tamanio_barco):
            if self.restricciones['filas'][indice_fila] - 1 < 0: return False
        
        for indice in range(0, tamanio_barco):
            if not self.es_posicion_disponible({'fila':fila + indice, 'columna':columna}):
                return False
                    
        return True

    #Se le pasa la 1ra columna que debe ocupar el barco y de ahi se rellena hacia la derecha por su tamaño
    def colocar_barco_horizontal(self, tam_barco, posicion):
        fila = posicion['fila']
        columna_inicial = posicion['columna']
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos_sacados[tam_barco].append(barco)
        for columna in range(columna_inicial, columna_inicial + tam_barco):
            if columna < len(self.tablero[fila]):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas = self.casillas_ya_ocupadas + 1
                self.restricciones['columnas'][columna] = self.restricciones['columnas'][columna] - 1
        self.restricciones['filas'][fila] = self.restricciones['filas'][fila] - tam_barco

        if columna + tam_barco >= len(self.tablero[0]) - 1:
            if posicion['fila'] == len(self.tablero) - 1:
                posicion['fila'] = len(self.tablero) - 1
                posicion['columna'] = len(self.tablero[0]) - 1
            else:
                posicion['fila'] = posicion['fila'] + 1
                posicion['columna'] = 0
        else: posicion['columna'] = posicion['columna'] + tam_barco + 1
    
    #Se le pasa la 1ra fila que debe ocupar el barco y de ahi se rellena hacia abajo por su tamaño
    def colocar_barco_vertical(self, tam_barco, posicion):
        fila_inicial = posicion['fila']
        columna = posicion['columna']
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos_sacados[tam_barco].append(barco)
        for fila in range(fila_inicial, (fila_inicial + tam_barco)):
            if fila < len(self.tablero):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas = self.casillas_ya_ocupadas + 1
                self.restricciones['filas'][fila] = self.restricciones['filas'][fila] - 1
        self.restricciones['columnas'][columna] = self.restricciones['columnas'][columna] - tam_barco

        if posicion['columna'] >= len(self.tablero[0]) - 2:
            if posicion['fila'] == len(self.tablero) - 1:
                posicion['fila'] = len(self.tablero) - 1
                posicion['columna'] = len(self.tablero[0]) - 1
            else:
                posicion['fila'] = posicion['fila'] + 1
                posicion['columna'] = 0
        else: posicion['columna'] = posicion['columna'] + 2
    
    def sacar_barco_horizontal(self, tam_barco, posicion):
        fila = posicion['fila']
        columna_inicial = posicion['columna']
        barco = self.tamanios_barcos_sacados[tam_barco].pop()
        self.tamanios_barcos[tam_barco].append(barco)
        for columna in range(columna_inicial, columna_inicial + tam_barco):
            if columna < len(self.tablero[fila]):
                self.tablero[fila][columna] = '-'
                self.casillas_ya_ocupadas = self.casillas_ya_ocupadas - 1
                self.restricciones['columnas'][columna] = self.restricciones['columnas'][columna] + 1
        self.restricciones['filas'][fila] = self.restricciones['filas'][fila] + tam_barco

    def sacar_barco_vertical(self, tam_barco, posicion):
        fila_inicial = posicion['fila']
        columna = posicion['columna']
        barco = self.tamanios_barcos_sacados[tam_barco].pop()
        self.tamanios_barcos[tam_barco].append(barco)
        for fila in range(fila_inicial, (fila_inicial + tam_barco)):
            if fila < len(self.tablero):
                self.tablero[fila][columna] = '-'
                self.casillas_ya_ocupadas = self.casillas_ya_ocupadas - 1
                self.restricciones['filas'][fila] = self.restricciones['filas'][fila] + 1
        self.restricciones['columnas'][columna] = self.restricciones['columnas'][columna] + tam_barco

    def obtener_tamanios_barcos(self):
        #x = {clave: valor for clave, valor in self.tamanios_barcos.items() if valor != []}
        return copy.deepcopy(self.tamanios_barcos_colocables)
    
    def obtener_demanda_cumplida(self):
        return self.casillas_ya_ocupadas * 2

    def es_posicion_disponible(self, posicion):
        fila = posicion['fila']
        columna = posicion['columna']
        if ((columna != 0 and self.tablero[fila][columna - 1] != '-')
        or (fila != 0 and self.tablero[fila - 1][columna] != '-')
        or (columna != len(self.tablero[0]) - 1 and self.tablero[fila][columna + 1] != '-')
        or (fila != len(self.tablero) - 1 and self.tablero[fila + 1][columna] != '-')
        or self.tablero[fila][columna] != '-'
        or (columna != 0 and fila != 0 and self.tablero[fila - 1][columna - 1] != '-')
        or (columna != len(self.tablero[0]) - 1 and fila != 0 and self.tablero[fila - 1][columna + 1] != '-')
        or (columna != 0 and fila != len(self.tablero) - 1 and self.tablero[fila + 1][columna - 1] != '-')
        or (columna != len(self.tablero[0]) - 1 and fila != len(self.tablero) - 1 and self.tablero[fila + 1][columna + 1] != '-')):
            return False
        return True
    
    def obtener_siguiente_posicion_disponible(self, posicion):
        if posicion['columna'] == len(self.tablero[0]) - 1:
            if posicion['fila'] == len(self.tablero) - 1:
                return False
            fila_inicial = posicion['fila'] + 1
            columna_inicial = 0
        else:
            fila_inicial = posicion['fila']
            columna_inicial = posicion['columna'] + 1
        for indice_fila in range(fila_inicial, len(self.tablero)):
            for indice_columna in range(columna_inicial, len(self.tablero[0])):
                posicion2 = {'fila':indice_fila, 'columna':indice_columna}
                if list(self.tamanios_barcos_colocables.keys()) == []: return False
                else: tam_minimo_barco = min(self.tamanios_barcos_colocables.keys())
                if self.es_posicion_disponible(posicion2) and self.puede_colocar_barco_horizontal(tam_minimo_barco, posicion2) or self.puede_colocar_barco_vertical(tam_minimo_barco, posicion2):
                    posicion['fila'] = indice_fila
                    posicion['columna'] = indice_columna
                    return True
            columna_inicial = 0
        return False
    
    def obtener_mayor_demanda_posible(self, posicion):
        barcos_restantes = sum(len(self.tamanios_barcos[tam_barco]) * tam_barco for tam_barco in self.tamanios_barcos_colocables.keys())
        
        demanda_ya_cumplida = self.casillas_ya_ocupadas * 2
        
        # Estimar la máxima demanda potencial de manera más precisa
        max_posible = demanda_ya_cumplida + min(
            max(self.restricciones['filas']), 
            max(self.restricciones['columnas']), 
            barcos_restantes
        ) * 2
    
        return max_posible
    
    def podar(self, mejor_demanda_cumplida, posicion):
        # Calcular la demanda potencial de manera más agresiva
        demanda_actual = self.obtener_demanda_cumplida()
        
        # Calcular los barcos restantes de manera más eficiente
        barcos_restantes = sum(len(barcos) * tam for tam, barcos in self.tamanios_barcos.items())
        
        # Estimación más pesimista de la demanda máxima potencial
        demanda_potencial_maxima = demanda_actual + min(
            max(self.restricciones['filas']), 
            max(self.restricciones['columnas']), 
            barcos_restantes
        ) * 2
        
        # Poda más estricta
        if demanda_potencial_maxima <= mejor_demanda_cumplida:
            return False
        
        # Poda adicional basada en espacio disponible
        espacio_disponible_filas = sum(self.restricciones['filas'])
        espacio_disponible_columnas = sum(self.restricciones['columnas'])
        
        if espacio_disponible_filas + espacio_disponible_columnas <= mejor_demanda_cumplida // 2:
            return False
        
        return True

    def filtrar_barcos_colocables(self, posicion):
        # Filtrado más simple y eficiente
        nuevos_barcos_colocables = {}
        for tam_barco, barcos in self.tamanios_barcos_colocables.items():
            # Verificar si el tamaño del barco es viable en alguna dimensión
            if (max(self.restricciones['filas']) >= tam_barco or 
                max(self.restricciones['columnas']) >= tam_barco):
                # Verificar si quedan barcos de este tamaño
                if barcos:
                    nuevos_barcos_colocables[tam_barco] = barcos
        
        self.tamanios_barcos_colocables = nuevos_barcos_colocables
    
    def obtener_tablero(self):
        return copy.deepcopy(self.tablero)

def llenar_juego(juego_inicial, posicion_inicial, mejor_tablero, mejor_demanda_cumplida):
    if isinstance(juego_inicial, Juego):
        # Verificar y actualizar la posición inicial
        if not juego_inicial.es_posicion_disponible(posicion_inicial):
            if not juego_inicial.obtener_siguiente_posicion_disponible(posicion_inicial):
                # Si no hay más posiciones disponibles, retornar el estado actual
                return [mejor_tablero, mejor_demanda_cumplida]

        juego_inicial.filtrar_barcos_colocables(posicion_inicial)
        
        # Verificar si se puede podar
        seguir = juego_inicial.podar(mejor_demanda_cumplida, posicion_inicial)
        
        # Actualizar mejor demanda y tablero si es necesario
        demanda_actual = juego_inicial.obtener_demanda_cumplida()
        if demanda_actual > mejor_demanda_cumplida:
            mejor_demanda_cumplida = demanda_actual
            mejor_tablero = juego_inicial.obtener_tablero()

        # Si no se puede continuar, retornar
        if not seguir:
            return [mejor_tablero, mejor_demanda_cumplida]

        # Intentar colocar barcos en diferentes orientaciones
        for barco_tamanio in sorted(list(juego_inicial.obtener_tamanios_barcos().keys()), reverse=True):
            if juego_inicial.obtener_tamanios_barcos()[barco_tamanio] == []:
                continue

            # Intento horizontal
            copia_posicion_h = posicion_inicial.copy()
            if juego_inicial.puede_colocar_barco_horizontal(barco_tamanio, copia_posicion_h):
                juego_inicial.colocar_barco_horizontal(barco_tamanio, copia_posicion_h)
                posible_solucion_h = llenar_juego(juego_inicial, copia_posicion_h, mejor_tablero, mejor_demanda_cumplida)
                
                if posible_solucion_h[1] > mejor_demanda_cumplida:
                    mejor_demanda_cumplida = posible_solucion_h[1]
                    mejor_tablero = posible_solucion_h[0]
                
                juego_inicial.sacar_barco_horizontal(barco_tamanio, posicion_inicial)

            # Intento vertical (si no es 1)
            if barco_tamanio != 1:
                copia_posicion_v = posicion_inicial.copy()
                if juego_inicial.puede_colocar_barco_vertical(barco_tamanio, copia_posicion_v):
                    juego_inicial.colocar_barco_vertical(barco_tamanio, copia_posicion_v)
                    posible_solucion_v = llenar_juego(juego_inicial, copia_posicion_v, mejor_tablero, mejor_demanda_cumplida)
                    
                    if posible_solucion_v[1] > mejor_demanda_cumplida:
                        mejor_demanda_cumplida = posible_solucion_v[1]
                        mejor_tablero = posible_solucion_v[0]
                    
                    juego_inicial.sacar_barco_vertical(barco_tamanio, posicion_inicial)

        # Intentar avanzar a la siguiente posición
        copia_posicion = posicion_inicial.copy()
        if juego_inicial.obtener_siguiente_posicion_disponible(copia_posicion):
            posible_solucion_sin_colocar = llenar_juego(juego_inicial, copia_posicion, mejor_tablero, mejor_demanda_cumplida)
            
            if posible_solucion_sin_colocar[1] > mejor_demanda_cumplida:
                mejor_demanda_cumplida = posible_solucion_sin_colocar[1]
                mejor_tablero = posible_solucion_sin_colocar[0]

        juego_inicial.resetear_barcos_colocables()
        return [mejor_tablero, mejor_demanda_cumplida]
    
def _llenar_juego(restricciones_filas, restricciones_columnas, barcos):
    nuevo = Juego(restricciones_filas, restricciones_columnas, barcos)
    return llenar_juego(nuevo, { 'fila':0, 'columna':0 }, nuevo.obtener_tablero(), nuevo.obtener_demanda_cumplida())

def parsear_archivo_con_arrays(archivo):
    with open(archivo, 'r') as archivo:
        res = []
        fi_co_bar = []
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                if fi_co_bar:
                    res.append(fi_co_bar)
                    fi_co_bar = []
                continue
            fi_co_bar.append(int(linea))
        if fi_co_bar:
            res.append(fi_co_bar)
    return res[0], res[1], res[2]

def mostrar_tablero(tablero):
        for fila in tablero:
            for columna in fila:
                print(columna, end=" ")
            print('\n')
    
def mostrar_demanda_total(demanda_total):
    print('Demanda total:', end=' ')
    print(demanda_total)

def mostrar_demanda_cumplida(demanda_cumplida):
    print('Demanda cumplida:', end=' ')
    print(demanda_cumplida)

if __name__ == "__main__":
    archivo = sys.argv[1]
    restricciones_filas, restricciones_columnas, barcos = parsear_archivo_con_arrays(archivo)
    demanda_total = sum(restricciones_columnas) + sum(restricciones_filas)
    mejor_tablero, mejor_demanda_cumplida = _llenar_juego(restricciones_filas, restricciones_columnas, barcos)
    mostrar_tablero(mejor_tablero)
    mostrar_demanda_cumplida(mejor_demanda_cumplida)
    mostrar_demanda_total(demanda_total)
    # mejor_juego.mostrar_tablero()
    # mejor_juego.mostrar_demanda_cumplida()
    # mejor_juego.mostrar_demanda_total()