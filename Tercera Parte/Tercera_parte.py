import copy

class Juego:
    restricciones = {'filas': [], 'columnas': []}
    tablero = []
    posicion_actual = { 'fila':0, 'columna':0 }
    casillas_ya_ocupadas_x_fila = []
    casillas_ya_ocupadas_x_columna = []
    tamanios_barcos = {}

    def __init__(self, *args):
        if len(args) == 3:
            restricciones_filas, restricciones_columnas, barcos = args
            self.restricciones['filas'] = restricciones_filas
            self.restricciones['columnas'] = restricciones_columnas
            self.tablero = [["-"] * len(restricciones_columnas) for _ in range(len(restricciones_filas))]
            self.casillas_ya_ocupadas_x_fila = [0] * len(restricciones_filas)
            self.casillas_ya_ocupadas_x_columna = [0] * len(restricciones_columnas)
            for indice in range(len(barcos)):
                if barcos[indice] not in self.tamanios_barcos:
                    self.tamanios_barcos[barcos[indice]] = [indice]
                else:
                    self.tamanios_barcos[barcos[indice]].append(indice)
        elif len(args) == 6:
            restricciones, tablero, posicion_actual, casillas_ya_ocupadas_x_fila, casillas_ya_ocupadas_x_columna, tamanios_barcos = args
            self.restricciones = restricciones
            self.tablero = tablero
            self.posicion_actual = posicion_actual
            self.casillas_ya_ocupadas_x_fila = casillas_ya_ocupadas_x_fila
            self.casillas_ya_ocupadas_x_columna = casillas_ya_ocupadas_x_columna
            self.tamanios_barcos = tamanios_barcos
        self.filtrar_barcos_por_colocables()
    
    def copiar(self):
        return Juego(copy.deepcopy(self.restricciones), copy.deepcopy(self.tablero), copy.deepcopy(self.posicion_actual), copy.deepcopy(self.casillas_ya_ocupadas_x_fila), copy.deepcopy(self.casillas_ya_ocupadas_x_columna), copy.deepcopy(self.tamanios_barcos))
    
    def puede_colocar_barco_horizontal(self, tamanio_barco, posicion, es_prueba):
        if tamanio_barco not in self.tamanios_barcos.keys():
            return False
        fila = posicion['fila']
        columna = posicion['columna']

        if len(self.tablero[0]) < columna + tamanio_barco: 
            return False

        if self.casillas_ya_ocupadas_x_fila[fila] + tamanio_barco > self.restricciones['filas'][fila]: return False
        for indice_columna in range(columna, columna + tamanio_barco):
            if self.restricciones['columnas'][indice_columna] < self.casillas_ya_ocupadas_x_columna[indice_columna] + 1: return False
        
        for indice in range(0, tamanio_barco):
            if not self.es_posicion_disponible({'fila':fila, 'columna':columna + indice}):
                return False
            
        if not es_prueba:
            self.colocar_barco_horizontal(tamanio_barco, fila, columna)
            if columna + tamanio_barco >= len(self.tablero[0]) - 1:
                if posicion['fila'] == len(self.tablero) - 1:
                    posicion['fila'] = len(self.tablero) - 1
                    posicion['columna'] = len(self.tablero[0]) - 1
                else:
                    posicion['fila'] = posicion['fila'] + 1
                    posicion['columna'] = 0
            else: posicion['columna'] = posicion['columna'] + tamanio_barco + 1
        return True
    
    def puede_colocar_barco_vertical(self, tamanio_barco, posicion, es_prueba):
        fila = posicion['fila']
        columna = posicion['columna']
        if len(self.tablero) < fila + tamanio_barco: 
            return False

        if self.casillas_ya_ocupadas_x_columna[columna] + tamanio_barco > self.restricciones['columnas'][columna]: return False
        for indice_fila in range(fila, fila + tamanio_barco):
            if self.restricciones['filas'][indice_fila] < self.casillas_ya_ocupadas_x_fila[indice_fila] + 1: return False
        
        for indice in range(0, tamanio_barco):
            if not self.es_posicion_disponible({'fila':fila + indice, 'columna':columna}):
                return False
                    
        if not es_prueba:
            self.colocar_barco_vertical(tamanio_barco, fila, columna)
            if columna >= len(self.tablero[0]) - 2:
                if posicion['fila'] == len(self.tablero) - 1:
                    posicion['fila'] = len(self.tablero) - 1
                    posicion['columna'] = len(self.tablero[0]) - 1
                else:
                    posicion['fila'] = posicion['fila'] + 1
                    posicion['columna'] = 0
            else: posicion['columna'] = posicion['columna'] + 2
        return True

    #Se le pasa la 1ra columna que debe ocupar el barco y de ahi se rellena hacia la derecha por su tamaño
    def colocar_barco_horizontal(self, tam_barco, fila, columna_inicial):
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos = {clave: valor for clave, valor in self.tamanios_barcos.items() if valor != []}
        for columna in range(columna_inicial, columna_inicial + tam_barco):
            if columna < len(self.tablero[fila]):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas_x_fila[fila] = self.casillas_ya_ocupadas_x_fila[fila] + 1
                self.casillas_ya_ocupadas_x_columna[columna] = self.casillas_ya_ocupadas_x_columna[columna] + 1
    
    #Se le pasa la 1ra fila que debe ocupar el barco y de ahi se rellena hacia abajo por su tamaño
    def colocar_barco_vertical(self, tam_barco, fila_inicial, columna):
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos = {clave: valor for clave, valor in self.tamanios_barcos.items() if valor != []}
        for fila in range(fila_inicial, (fila_inicial + tam_barco)):
            if fila < len(self.tablero):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas_x_fila[fila] = self.casillas_ya_ocupadas_x_fila[fila] + 1
                self.casillas_ya_ocupadas_x_columna[columna] = self.casillas_ya_ocupadas_x_columna[columna] + 1
    
    def obtener_tamanios_barcos(self):
        self.tamanios_barcos = {clave: valor for clave, valor in self.tamanios_barcos.items() if valor != []}
        return self.tamanios_barcos
    
    def obtener_tablero(self):
        return copy.deepcopy(self.tablero)
    
    def obtener_demanda_cumplida(self):
        devolucion = 0
        if (len(self.casillas_ya_ocupadas_x_fila) != 0): devolucion = sum(self.casillas_ya_ocupadas_x_fila) * 2
        return devolucion
    
    def mostrar_tablero(self):
        for fila in self.tablero:
            for columna in fila:
                print(columna, end=" ")
            print('\n')
    
    def mostrar_demanda_total(self):
        print('Demanda total:', end=' ')
        print(sum(restricciones_columnas) + sum(restricciones_filas))

    def mostrar_demanda_cumplida(self):
        devolucion = 0
        if (len(self.casillas_ya_ocupadas_x_fila) != 0): devolucion = sum(self.casillas_ya_ocupadas_x_fila) * 2
        print('Demanda cumplida:', end=' ')
        print(devolucion)

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
                tam_minimo_barco = 1
                if list(self.obtener_tamanios_barcos().keys()) != []: tam_minimo_barco = min(self.obtener_tamanios_barcos().keys())
                if self.es_posicion_disponible(posicion2) and self.puede_colocar_barco_horizontal(tam_minimo_barco, posicion2, True) or self.puede_colocar_barco_vertical(tam_minimo_barco, posicion2, True):
                    posicion['fila'] = indice_fila
                    posicion['columna'] = indice_columna
                    return True
            columna_inicial = 0
        return False
    
    def obtener_mayor_demanda_posible(self):
        posiciones_restantes = 0
        for fila in range(self.posicion_actual['fila'], len(self.tablero)):
            if fila == self.posicion_actual['fila']: columna_inicial = self.posicion_actual['columna']
            else: columna_inicial = 0
            for columna in range(columna_inicial, len(self.tablero[0])):
                posicion = {'fila':fila, 'columna':columna}
                tam_minimo_barco = 1
                if list(self.obtener_tamanios_barcos().keys()) != []: tam_minimo_barco = min(self.obtener_tamanios_barcos().keys())
                if self.es_posicion_disponible(posicion) and self.puede_colocar_barco_horizontal(tam_minimo_barco, posicion, True) or self.puede_colocar_barco_vertical(tam_minimo_barco, posicion, True):
                    posiciones_restantes = posiciones_restantes + 1
        
        barcos_restantes = 0
        for tam_barco in self.tamanios_barcos.keys():
            barcos_restantes = barcos_restantes + (len(self.tamanios_barcos[tam_barco]) * tam_barco)

        demanda_ya_cumplida = sum(self.casillas_ya_ocupadas_x_fila) * 2

        maxima_capacidad_fila_restante = 0
        for i in range(len(self.casillas_ya_ocupadas_x_fila)):
            maxima_capacidad_fila_restante = maxima_capacidad_fila_restante + self.restricciones['filas'][i] - self.casillas_ya_ocupadas_x_fila[i]

        maxima_capacidad_columna_restante = 0
        for i in range(len(self.casillas_ya_ocupadas_x_columna)):
            maxima_capacidad_columna_restante = maxima_capacidad_columna_restante + self.restricciones['columnas'][i] - self.casillas_ya_ocupadas_x_columna[i]

        #print('( ', demanda_ya_cumplida, ', ', maxima_capacidad_fila_restante, ', ', maxima_capacidad_columna_restante, ', ', barcos_restantes, ', ', posiciones_restantes, ' )')
        return demanda_ya_cumplida + min(maxima_capacidad_fila_restante, maxima_capacidad_columna_restante, barcos_restantes, posiciones_restantes) * 2
    
    

    def filtrar_barcos_por_colocables(self):
        seguir = True
        for tam_barco in sorted(self.tamanios_barcos.keys(), reverse=True):
            if seguir:
                capacidad_fila_restante = []
                for i in range(len(self.casillas_ya_ocupadas_x_fila)):
                    capacidad_fila_restante.append(self.restricciones['filas'][i] - self.casillas_ya_ocupadas_x_fila[i])

                capacidad_columna_restante = []
                for i in range(len(self.casillas_ya_ocupadas_x_columna)):
                    capacidad_columna_restante.append(self.restricciones['columnas'][i] - self.casillas_ya_ocupadas_x_columna[i])

                if max(capacidad_fila_restante) < tam_barco and max(capacidad_columna_restante) < tam_barco:
                    del self.tamanios_barcos[tam_barco]
                    continue
                
                no_puede_colocarlo = True
                if no_puede_colocarlo and max(capacidad_fila_restante) >= tam_barco:
                    for indice_fila in range(self.posicion_actual['fila'], len(self.restricciones['filas'])):
                        if capacidad_fila_restante[indice_fila] >= tam_barco:
                            if indice_fila == self.posicion_actual['fila']: columna_inicial = self.posicion_actual['columna']
                            else: columna_inicial = 0
                            for indice_columna in range(columna_inicial, len(self.restricciones['columnas'])):
                                posicion = {'fila':indice_fila, 'columna':indice_columna}
                                puede_colocarlo = self.puede_colocar_barco_horizontal(tam_barco, posicion, True)
                                if puede_colocarlo:
                                    no_puede_colocarlo = False
                                    break
                
                if no_puede_colocarlo and max(capacidad_columna_restante) >= tam_barco:
                    for indice_columna in range(0, len(self.restricciones['columnas'])):
                        if capacidad_columna_restante[indice_columna] >= tam_barco:
                            for indice_fila in range(self.posicion_actual['fila'], len(self.restricciones['filas'])):
                                posicion = {'fila':indice_fila, 'columna':indice_columna}
                                puede_colocarlo = self.puede_colocar_barco_vertical(tam_barco, posicion, True)
                                if puede_colocarlo:
                                    no_puede_colocarlo = False
                                    break
                
                if no_puede_colocarlo: del self.tamanios_barcos[tam_barco]
                else: seguir = False
    
    def podar(self, mejor_solucion):
        if isinstance(mejor_solucion, Juego):
            barcos_restantes = 0
            for tam_barco in self.tamanios_barcos.keys():
                barcos_restantes = barcos_restantes + len(self.tamanios_barcos[tam_barco]) * tam_barco * 2

            if barcos_restantes == 0:
                return False

            if self.obtener_mayor_demanda_posible() <= mejor_solucion.obtener_demanda_cumplida():
                return False

            if self.obtener_demanda_cumplida() + barcos_restantes <= mejor_solucion.obtener_demanda_cumplida():
                return False
            
            if mejor_solucion.obtener_demanda_cumplida() == sum(self.restricciones['filas']) + sum(self.restricciones['columnas']):
                return False

            return True
    
    def obtener_restricciones_restantes(self):
        restantes_filas = [a - b for a, b in zip(restricciones_filas, self.casillas_ya_ocupadas_x_fila)]
        restantes_columnas = [a - b for a, b in zip(restricciones_columnas, self.casillas_ya_ocupadas_x_columna)]
        return restantes_filas, restantes_columnas

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

def llenar_juego(juego_inicial, posicion_inicial, mejor_solucion, nro_copia):
    if isinstance(juego_inicial, Juego) and isinstance(mejor_solucion, Juego):
        if not juego_inicial.es_posicion_disponible(posicion_inicial):
            juego_inicial.obtener_siguiente_posicion_disponible(posicion_inicial)
        seguir = juego_inicial.podar(mejor_solucion)
        while seguir:
            for barco_tamanio in sorted(juego_inicial.obtener_tamanios_barcos().keys(), reverse=True):
                copia_juego_horizontal = juego_inicial.copiar()
                copia_juego_vertical = juego_inicial.copiar()
                copia_posicion_horizontal = posicion_inicial.copy()
                copia_posicion_vertical = posicion_inicial.copy()
                posible_solucion_horizontal = None
                posible_solucion_vertical = None
                if copia_juego_horizontal.puede_colocar_barco_horizontal(barco_tamanio, copia_posicion_horizontal, False):
                    posible_solucion_horizontal = llenar_juego(copia_juego_horizontal, copia_posicion_horizontal, mejor_solucion, nro_copia)
                #barco_tamanio != 1 and ESTO EN EL IF DE ABAJO DEBERIA AGILIZAR, PERO SI LO HAGO NO FUNCIONA NOSE PORQUE
                if copia_juego_vertical.puede_colocar_barco_vertical(barco_tamanio, copia_posicion_vertical, False):
                    posible_solucion_vertical = llenar_juego(copia_posicion_vertical, copia_posicion_vertical, mejor_solucion, nro_copia)
                if posible_solucion_horizontal == None: posible_solucion_horizontal = copia_juego_horizontal
                if posible_solucion_vertical == None: posible_solucion_vertical = copia_juego_vertical
                soluciones = [mejor_solucion.obtener_demanda_cumplida(), posible_solucion_horizontal.obtener_demanda_cumplida(), posible_solucion_vertical.obtener_demanda_cumplida()]
                maximo = max(soluciones)
                indice_maximo = soluciones.index(maximo)
                if indice_maximo == 1: mejor_solucion = posible_solucion_horizontal
                elif indice_maximo == 2: mejor_solucion = posible_solucion_vertical
            seguir = juego_inicial.obtener_siguiente_posicion_disponible(posicion_inicial)
        return mejor_solucion
    
def _llenar_juego(restricciones_filas, restricciones_columnas, barcos):
    nuevo = Juego(restricciones_filas, restricciones_columnas, barcos)
    #print(nuevo.obtener_siguiente_posicion_disponible({ 'fila':4, 'columna':4 }))
    return llenar_juego(nuevo, { 'fila':0, 'columna':0 }, nuevo, 0)

restricciones_filas, restricciones_columnas, barcos = parsear_archivo_con_arrays(r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\pruebas\TP3\10_10_10.txt")
mejor_juego = _llenar_juego(restricciones_filas, restricciones_columnas, barcos)
if isinstance(mejor_juego, Juego):
    mejor_juego.mostrar_tablero()
    mejor_juego.mostrar_demanda_cumplida()
    mejor_juego.mostrar_demanda_total()