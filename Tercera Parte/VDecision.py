def es_batalla_navala(rec_fil, rec_col, matriz):
    cont = 0
    i=0
    j=0
    rec_col_finales = [0]*len(rec_col)

    for fila in matriz:
        for celda in fila:
            if celda == 1:
                rec_col_finales[j] += 1
                cont += 1
            j += 1
        
        if cont <= rec_fil[i]:
            return False
        
        i += 1
        cont=0
        j=0

    for i in range(len(rec_col)):
        if rec_col[i] < rec_col_finales[i]:
            return False
    
    return True

matriz = [[0, 0, 0]
            ,[1, 1, 1]
            ,[0, 0, 1]]
        
rec_fil = [0, 3, 1]
rec_col = [1, 1, 1]

print(es_batalla_navala(rec_fil, rec_col, matriz)) # True