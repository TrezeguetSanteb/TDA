import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
from tercera_parte import BatallaNaval, leer_ejemplo
import numpy as np
from VAproximacion import aproximacion_barcos, calcular_demanda_cumplida

archivos_catedra = [
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\3_3_2.txt",        
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\5_5_6.txt", 
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\8_7_10.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\10_3_3.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\10_10_10.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\12_12_21.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\15_10_15.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\20_20_20.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\20_25_30.txt",  
    r"C:\Users\mateo\OneDrive\Escritorio\FACU\TDA\TDA\Tercera Parte\pruebas_parte3\30_25_25.txt"
]

def aprox(archivos, funcion):
    resultados = []
    tiempos = []
    for archivo in archivos:
        n, m, barcos, restricciones_filas, restricciones_columnas = leer_ejemplo(archivo)
        matriz = [[0] * m for _ in range(n)]
        start = time.time()
        resultado = funcion(matriz, restricciones_filas, restricciones_columnas, barcos)
        end = time.time()
        tiempos.append(end-start)
        resultados.append(calcular_demanda_cumplida(resultado))

    return resultados

def bt(archivos):
    resultados = []
    tiempos = []
    for archivo in archivos:
        n, m, barcos, restricciones_filas, restricciones_columnas = leer_ejemplo(archivo)
        start = time.time()
        batalla_naval = BatallaNaval(n, m, restricciones_filas, restricciones_columnas, barcos, time_limit=180)
        batalla_naval.resolver()
        resultado = batalla_naval.mejor_demanda_cumplida
        end = time.time()
        tiempos.append(end-start)
        resultados.append(resultado)

    return resultados

def dimensiones(archivo):
    n, m, barcos, restricciones_filas, restricciones_columnas = leer_ejemplo(archivo)

    return f'{n}x{m}_{len(barcos)}'

def graficar_diferencia_tiempos(aprox_results, bt_results, archivos_catedra):
    # Calcular diferencias
    diferencias = np.array(aprox_results) / np.array(bt_results)
    
    # Obtener nombres de archivos más limpios (sin la ruta completa)
    nombres = [dimensiones(archivo) for archivo in archivos_catedra]
    
    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    
    # Crear barras
    bars = plt.bar(nombres, diferencias)
    
    # Personalizar el gráfico
    plt.title('Diferencia de tiempos (BT - Aproximación)', pad=20)
    plt.xlabel('Archivos')
    plt.ylabel('Diferencia de tiempo')
    
    # Rotar etiquetas del eje x para mejor legibilidad
    plt.xticks(rotation=45, ha='right')
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Agregar valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Mostrar el gráfico
    plt.show()

aprox_results = aprox(archivos_catedra, aproximacion_barcos)
bt_results = bt(archivos_catedra)
graficar_diferencia_tiempos(aprox_results, bt_results, archivos_catedra)