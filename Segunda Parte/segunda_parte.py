import sys

def juego_programacion_dinamica(monedas):
    n = len(monedas)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if i == j:
                dp[i][j] = monedas[i]
            else:
                # Si Sophia elige la moneda en la posición i
                if monedas[i + 1] >= monedas[j]:
                    pick_i = monedas[i] + dp[i + 2][j] if i + 2 <= j else monedas[i]
                else:
                    pick_i = monedas[i] + dp[i + 1][j - 1] if i + 1 <= j - 1 else monedas[i]

                # Si Sophia elige la moneda en la posición j
                if monedas[i] >= monedas[j - 1]:
                    pick_j = monedas[j] + dp[i + 1][j - 1] if i + 1 <= j - 1 else monedas[j]
                else:
                    pick_j = monedas[j] + dp[i][j - 2] if i <= j - 2 else monedas[j]

                dp[i][j] = max(pick_i, pick_j)
    return dp[0][n - 1]

def parsear_archivo(archivo):
    with open(archivo, 'r') as archivo:
        for linea in archivo:
            if linea[0] != '#':
                arr = [int(num) for num in linea.split(';') if num.strip().isdigit()]
    return arr

if __name__ == "__main__":
    archivo = sys.argv[1]
    print("Ganancia Sophia:", juego_programacion_dinamica(parsear_archivo(archivo)))