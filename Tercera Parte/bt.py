import copy

class Juego:
    def __init__(self, restricciones_filas, restricciones_columnas, barcos):
        """
        Initialize the game board with row and column constraints and ship sizes.
        
        :param restricciones_filas: List of ship constraints for each row
        :param restricciones_columnas: List of ship constraints for each column
        :param barcos: List of ship sizes to place
        """
        self.restricciones = {
            'filas': restricciones_filas.copy(), 
            'columnas': restricciones_columnas.copy()
        }
        self.tablero = [["-"] * len(restricciones_columnas) for _ in range(len(restricciones_filas))]
        
        # Track ship placements
        self.tamanios_barcos = {}
        self.tamanios_barcos_sacados = {}
        
        # Organize ships by size
        for indice, tam in enumerate(barcos):
            if tam not in self.tamanios_barcos:
                self.tamanios_barcos[tam] = [indice]
                self.tamanios_barcos_sacados[tam] = []
            else:
                self.tamanios_barcos[tam].append(indice)
        
        # Total demand calculation
        self.demanda_total = sum(restricciones_columnas) + sum(restricciones_filas)
        self.casillas_ya_ocupadas = 0
        
        # Trackable ships that can be placed
        self.tamanios_barcos_colocables = copy.deepcopy(self.tamanios_barcos)

    def puede_colocar_barco_horizontal(self, tamanio_barco, posicion):
        """
        Check if a ship can be placed horizontally at the given position.
        
        :param tamanio_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        :return: Boolean indicating if ship can be placed
        """
        fila, columna = posicion['fila'], posicion['columna']

        # Check if ship size is available
        if (tamanio_barco not in self.tamanios_barcos_colocables or 
            not self.tamanios_barcos_colocables[tamanio_barco]):
            return False

        # Check board boundaries
        if columna + tamanio_barco > len(self.tablero[0]):
            return False

        # Check row constraints
        if self.restricciones['filas'][fila] < tamanio_barco:
            return False

        # Check column and adjacent cell availability
        for c in range(columna, columna + tamanio_barco):
            if self.restricciones['columnas'][c] < 1:
                return False
            if not self.es_posicion_disponible({'fila': fila, 'columna': c}):
                return False

        return True
    
    def colocar_barco_horizontal(self, tam_barco, posicion):
        """
        Place a ship horizontally on the board.
        
        :param tam_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        """
        fila = posicion['fila']
        columna_inicial = posicion['columna']
        
        # Remove ship from available ships
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos_sacados[tam_barco].append(barco)
        
        # Place ship on board
        for columna in range(columna_inicial, columna_inicial + tam_barco):
            if columna < len(self.tablero[fila]):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas += 1
                self.restricciones['columnas'][columna] -= 1
        
        # Update row constraint
        self.restricciones['filas'][fila] -= tam_barco

        # Update position for next placement
        if columna + tam_barco >= len(self.tablero[0]) - 1:
            if posicion['fila'] == len(self.tablero) - 1:
                posicion['fila'] = len(self.tablero) - 1
                posicion['columna'] = len(self.tablero[0]) - 1
            else:
                posicion['fila'] += 1
                posicion['columna'] = 0
        else:
            posicion['columna'] += tam_barco + 1
    
    def colocar_barco_vertical(self, tam_barco, posicion):
        """
        Place a ship vertically on the board.
        
        :param tam_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        """
        fila_inicial = posicion['fila']
        columna = posicion['columna']
        
        # Remove ship from available ships
        barco = self.tamanios_barcos[tam_barco].pop()
        self.tamanios_barcos_sacados[tam_barco].append(barco)
        
        # Place ship on board
        for fila in range(fila_inicial, fila_inicial + tam_barco):
            if fila < len(self.tablero):
                self.tablero[fila][columna] = barco
                self.casillas_ya_ocupadas += 1
                self.restricciones['filas'][fila] -= 1
        
        # Update column constraint
        self.restricciones['columnas'][columna] -= tam_barco

        # Update position for next placement
        if posicion['columna'] >= len(self.tablero[0]) - 2:
            if posicion['fila'] == len(self.tablero) - 1:
                posicion['fila'] = len(self.tablero) - 1
                posicion['columna'] = len(self.tablero[0]) - 1
            else:
                posicion['fila'] += 1
                posicion['columna'] = 0
        else:
            posicion['columna'] += 2
    
    def sacar_barco_horizontal(self, tam_barco, posicion):
        """
        Remove a horizontally placed ship from the board.
        
        :param tam_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        """
        fila = posicion['fila']
        columna_inicial = posicion['columna']
        
        # Return ship to available ships
        barco = self.tamanios_barcos_sacados[tam_barco].pop()
        self.tamanios_barcos[tam_barco].append(barco)
        
        # Remove ship from board
        for columna in range(columna_inicial, columna_inicial + tam_barco):
            if columna < len(self.tablero[fila]):
                self.tablero[fila][columna] = '-'
                self.casillas_ya_ocupadas -= 1
                self.restricciones['columnas'][columna] += 1
        
        # Update row constraint
        self.restricciones['filas'][fila] += tam_barco
    
    def sacar_barco_vertical(self, tam_barco, posicion):
        """
        Remove a vertically placed ship from the board.
        
        :param tam_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        """
        fila_inicial = posicion['fila']
        columna = posicion['columna']
        
        # Return ship to available ships
        barco = self.tamanios_barcos_sacados[tam_barco].pop()
        self.tamanios_barcos[tam_barco].append(barco)
        
        # Remove ship from board
        for fila in range(fila_inicial, fila_inicial + tam_barco):
            if fila < len(self.tablero):
                self.tablero[fila][columna] = '-'
                self.casillas_ya_ocupadas -= 1
                self.restricciones['filas'][fila] += 1
        
        # Update column constraint
        self.restricciones['columnas'][columna] += tam_barco
    
    def es_posicion_disponible(self, posicion):
        """
        Check if a position is available for ship placement.
        
        :param posicion: Dictionary with 'fila' and 'columna' keys
        :return: Boolean indicating if position is available
        """
        fila = posicion['fila']
        columna = posicion['columna']
        
        # Check adjacent cells for ship conflicts
        checks = [
            (columna != 0, self.tablero[fila][columna - 1] != '-'),  # Left
            (fila != 0, self.tablero[fila - 1][columna] != '-'),  # Top
            (columna != len(self.tablero[0]) - 1, self.tablero[fila][columna + 1] != '-'),  # Right
            (fila != len(self.tablero) - 1, self.tablero[fila + 1][columna] != '-'),  # Bottom
            (self.tablero[fila][columna] != '-'),  # Current cell
            (columna != 0 and fila != 0, self.tablero[fila - 1][columna - 1] != '-'),  # Top-left diagonal
            (columna != len(self.tablero[0]) - 1 and fila != 0, self.tablero[fila - 1][columna + 1] != '-'),  # Top-right diagonal
            (columna != 0 and fila != len(self.tablero) - 1, self.tablero[fila + 1][columna - 1] != '-'),  # Bottom-left diagonal
            (columna != len(self.tablero[0]) - 1 and fila != len(self.tablero) - 1, self.tablero[fila + 1][columna + 1] != '-')  # Bottom-right diagonal
        ]
        
        #return not any(condition and cell_occupied for condition, cell_occupied in checks)

    def puede_colocar_barco_vertical(self, tamanio_barco, posicion):
        """
        Check if a ship can be placed vertically at the given position.
        
        :param tamanio_barco: Size of the ship
        :param posicion: Dictionary with 'fila' and 'columna' keys
        :return: Boolean indicating if ship can be placed
        """
        fila, columna = posicion['fila'], posicion['columna']

        # Check if ship size is available
        if (tamanio_barco not in self.tamanios_barcos_colocables or 
            not self.tamanios_barcos_colocables[tamanio_barco]):
            return False

        # Check board boundaries
        if fila + tamanio_barco > len(self.tablero):
            return False

        # Check column constraints
        if self.restricciones['columnas'][columna] < tamanio_barco:
            return False

        # Check row and adjacent cell availability
        for f in range(fila, fila + tamanio_barco):
            if self.restricciones['filas'][f] < 1:
                return False
            if not self.es_posicion_disponible({'fila': f, 'columna': columna}):
                return False

        return True

def llenar_juego_optimizado(juego_inicial):
    """
    Optimize board placement using backtracking algorithm.
    
    :param juego_inicial: Initial game board
    :return: Tuple of best board configuration and best demand
    """
    mejor_demanda = [0]  # Use list to allow modification in nested function
    mejor_tablero = [None]

    def backtrack(juego, demanda_actual=0):
        # Update best solution if current is better
        if demanda_actual > mejor_demanda[0]:
            mejor_demanda[0] = demanda_actual
            mejor_tablero[0] = copy.deepcopy(juego.tablero)

        # Try different ship placements
        for tam_barco in sorted(juego.tamanios_barcos.keys(), reverse=True):
            for fila in range(len(juego.tablero)):
                for columna in range(len(juego.tablero[0])):
                    pos = {'fila': fila, 'columna': columna}
                    
                    # Try horizontal placement
                    if juego.puede_colocar_barco_horizontal(tam_barco, pos):
                        juego.colocar_barco_horizontal(tam_barco, pos)
                        backtrack(juego, demanda_actual + tam_barco * 2)
                        juego.sacar_barco_horizontal(tam_barco, pos)

                    # Try vertical placement
                    if tam_barco > 1 and juego.puede_colocar_barco_vertical(tam_barco, pos):
                        juego.colocar_barco_vertical(tam_barco, pos)
                        backtrack(juego, demanda_actual + tam_barco * 2)
                        juego.sacar_barco_vertical(tam_barco, pos)

        return mejor_demanda[0]

    backtrack(juego_inicial)
    return mejor_tablero[0], mejor_demanda[0]

def resolver_tablero(restricciones_filas, restricciones_columnas, barcos):
    """
    Solve the board placement problem.
    
    :param restricciones_filas: Row constraints
    :param restricciones_columnas: Column constraints
    :param barcos: List of ship sizes
    :return: Best board configuration and demand
    """
    juego = Juego(restricciones_filas, restricciones_columnas, barcos)
    return llenar_juego_optimizado(juego)

def parsear_archivo_con_arrays(archivo):
    """
    Parse input file with row, column, and ship constraints.
    
    :param archivo: Path to input file
    :return: Tuple of row constraints, column constraints, and ship sizes
    """
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

# Example usage
def main():
    try:
        restricciones_filas, restricciones_columnas, barcos = parsear_archivo_con_arrays(r"tda2/tpTDA/Tercera Parte/pruebas_parte3/10_10_10.txt")
        mejor_tablero, mejor_demanda = resolver_tablero(restricciones_filas, restricciones_columnas, barcos)
        
        print("Tablero resultante:")
        for fila in mejor_tablero:
            print(" ".join(map(str, fila)))

        print(f"\nMejor demanda: {mejor_demanda}")
        print(f"Demanda total: {sum(restricciones_columnas) + sum(restricciones_filas)}")
    
    except FileNotFoundError:
        print("Error: Archivo de entrada no encontrado.")

main()