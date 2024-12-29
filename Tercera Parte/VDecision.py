def es_batalla_naval(rec_fil, rec_col, matriz, barcos):
    if not matriz or not matriz[0]:
        return False
    
    filas = len(matriz)
    columnas = len(matriz[0])
    
    # Verificar restricciones de filas
    for i in range(filas):
        casillas_ocupadas = sum(1 for celda in matriz[i] if celda > 0)
        if casillas_ocupadas > rec_fil[i]:  
            return False
    
    # Verificar restricciones de columnas
    for j in range(columnas):
        casillas_ocupadas = sum(1 for i in range(filas) if matriz[i][j] > 0)
        if casillas_ocupadas > rec_col[j]:  
            return False
    
    # Verificar adyacencia
    def tiene_adyacente(i, j):
        direcciones = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for di, dj in direcciones:
            ni, nj = i + di, j + dj
            if (0 <= ni < filas and 0 <= nj < columnas and 
                matriz[ni][nj] > 0 and matriz[ni][nj] != matriz[i][j]): 
                return True
        return False
    
    # Verificar que no hay barcos diferentes adyacentes
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] > 0 and tiene_adyacente(i, j):
                return False
    
    # Validar longitudes de barcos
    def medir_barco(i, j, id_barco, visitados):
        if (i < 0 or i >= filas or j < 0 or j >= columnas or 
            matriz[i][j] != id_barco or (i,j) in visitados):
            return 0
        visitados.add((i,j))
        return (1 + medir_barco(i, j+1, id_barco, visitados) + 
                   medir_barco(i+1, j, id_barco, visitados))
    
    # Encontrar longitudes de barcos colocados
    barcos_encontrados = {}
    visitados = set()
    
    for i in range(filas):
        for j in range(columnas):
            id_barco = matriz[i][j]
            if id_barco > 0 and (i,j) not in visitados:
                if id_barco in barcos_encontrados:  
                    return False
                longitud = medir_barco(i, j, id_barco, visitados)
                if longitud not in barcos:  
                    return False
                barcos_encontrados[id_barco] = longitud
    
    return True

matriz = [
[0, 0, 0],
[1, 1, 1],
[0, 0, 0]
]
        
rec_fil = [0, 3, 1]
rec_col = [1, 1, 1]
barcos = [3, 1, 1]

print(es_batalla_naval(rec_fil, rec_col, matriz, barcos)) 