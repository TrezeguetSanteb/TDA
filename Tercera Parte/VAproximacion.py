def chequeo_fil(req_fil, col, barco):
    for i in range(col-barco, col):
        if req_fil[i] == 0:
            return False
        
    for i in range(col-barco, col):
        req_fil[i] -= 1
    return True

def chequeo_col(req_col, fil, barco):
    for i in range(fil-barco, fil):
        if req_col[i] == 0:
            return False
        
    for i in range(fil-barco, fil):
        req_col[i] -= 1
    return True

def poner_barco_vertical(matriz, max, barco, req_col, req_fil):
    cont = 0
    for col in range(len(matriz)):
        if cont == barco:
            if chequeo_fil(req_fil, col, barco)== True:
                for i in range(col-barco, col):
                    matriz[i][max] = 1
                req_col[max] -= barco
                break
            cont=0
        else:
            if matriz[col][max] == 0:
                cont += 1
            else:
                cont = 0

def poner_barco_horizontal(matriz, max, barco, req_col, req_fil):
    cont = 0
    for fil in range(len(matriz[max])):
        if cont == barco:
            if chequeo_col(req_col, fil, barco)== True:
                for i in range(fil-barco, fil):
                    matriz[max][i] = 1
                req_fil[max] -= barco
                break
            cont=0
        else:
            if matriz[max][fil] == 0:
                cont += 1
            else:
                cont = 0    

def aproximacion(matriz, req_col, req_fil, barcos):
    barcos = sorted(barcos, reverse=True)

    for i in range(len(barcos)):
        barco = barcos[i]
        if (max(req_col) > max(req_fil)):
            if max(req_col) < barco:
                continue
            maximo = req_col.index(max(req_col))
            poner_barco_vertical(matriz, maximo, barco, req_col, req_fil)
              
        else:
            if max(req_fil) < barco:
                continue
            maximo = req_fil.index(max(req_fil))
            poner_barco_horizontal(matriz, maximo, barco, req_col, req_fil)

    return matriz

matriz_inicial = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
demanda_filas = [3, 2, 2, 1]
demanda_columnas = [2, 2, 2, 2]
barcos = [ 2, 3, 2]

matriz_final = aproximacion(matriz_inicial, demanda_columnas, demanda_filas, barcos)
print("Matriz final:")
for fila in matriz_final:
    print(fila)
