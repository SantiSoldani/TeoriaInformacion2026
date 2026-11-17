'''23. Codificar una función en Python que reciba como parámetro la matriz de un canal y,
utilizando las funciones de los ejercicios 20 y 22, realice todas las reducciones suficientes
posibles y devuelva la matriz del canal reducido.'''

import math


def get_matriz_compuesta(canal1: list[list[float]], canal2: list[list[float]]) -> list[list[float]]:
    """Calcula la matriz compuesta de dos canales (multiplicación de matrices)."""
    filas_1 = len(canal1)
    columnas_1 = len(canal1[0])
    filas_2 = len(canal2)
    columnas_2 = len(canal2[0])

    if columnas_1 != filas_2:
        raise ValueError("Las dimensiones no son compatibles para la multiplicación.")

    resultado = [[0.0 for _ in range(columnas_2)] for _ in range(filas_1)]
    for i in range(filas_1):
        for j in range(columnas_2):
            suma = 0.0
            for k in range(columnas_1):
                suma += canal1[i][k] * canal2[k][j]
            resultado[i][j] = round(suma, 4)
    return resultado


def se_pueden_reducir(matriz: list[list[float]], col1: int, col2: int) -> bool:
    """Verifica si dos columnas son proporcionales en todas las filas."""
    filas = len(matriz)
    for i in range(filas):
        for k in range(i + 1, filas):
            prod1 = matriz[i][col1] * matriz[k][col2]
            prod2 = matriz[k][col1] * matriz[i][col2]
            if not math.isclose(prod1, prod2, abs_tol=1e-6):
                return False
    return True


def generar_matriz_determinante(matriz: list[list[float]], col1: int, col2: int) -> list[list[int]]:
    """Genera la matriz determinante para combinar col1 y col2."""
    c_min, c_max = min(col1, col2), max(col1, col2)
    columnas_original = len(matriz[0])
    columnas_nueva = columnas_original - 1

    matriz_det = [[1 if i == j else 0 for j in range(columnas_nueva)]
                  for i in range(columnas_nueva)]

    fila_nueva = [0] * columnas_nueva
    fila_nueva[c_min] = 1
    matriz_det.insert(c_max, fila_nueva)

    return matriz_det


def reducir_matriz(matriz: list[list[float]]) -> list[list[float]]:
    """
    Reduce una matriz de canal combinando columnas proporcionalmente equivalentes
    mediante la multiplicación iterativa por canales determinantes.
    Itera hasta que no queden columnas reducibles.
    """
    matriz_reducida = [fila[:] for fila in matriz]

    hubo_reduccion = True
    while hubo_reduccion:
        hubo_reduccion = False
        n_cols = len(matriz_reducida[0])

        for i in range(n_cols):
            for j in range(i + 1, n_cols):
                if se_pueden_reducir(matriz_reducida, i, j):
                    mat_det = generar_matriz_determinante(matriz_reducida, i, j)
                    matriz_reducida = get_matriz_compuesta(matriz_reducida, mat_det)
                    hubo_reduccion = True
                    break
            if hubo_reduccion:
                break

    return matriz_reducida


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 21 del TP6:
    # Canal original (3 entradas x 4 salidas):
    #   [0.4, 0.6, 0.0, 0.0]
    #   [0.0, 0.0, 0.5, 0.5]
    #   [0.0, 0.0, 0.7, 0.3]
    # Columnas 0 y 1 se combinan (0.4+0.6=1.0)
    # Resultado oficial TP6 (pág. 9):
    #   [1.0, 0.0, 0.0]
    #   [0.0, 0.5, 0.5]
    #   [0.0, 0.7, 0.3]
    canal = [
        [0.4, 0.6, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.7, 0.3]
    ]

    reducido = reducir_matriz(canal)
    print("=== Ejercicio 21 TP6 - Canal Reducido ===")
    for f in reducido:
        print(" ", f)
