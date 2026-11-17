'''20. Implementar una función en Python que reciba como parámetros las matrices de dos
canales y genere la matriz del canal compuesto por los canales en serie.
'''

def get_matriz_compuesta(canal1: list[list[float]], canal2: list[list[float]]) -> list[list[float]]:
    """
    Calcula la matriz compuesta de dos canales (multiplicación de matrices).

    canal1: matriz de tamaño (n x m)
    canal2: matriz de tamaño (m x p)

    Retorna la matriz resultante (n x p).
    """
    
    # Dimensiones
    filas_1 = len(canal1)
    columnas_1 = len(canal1[0])
    filas_2 = len(canal2)
    columnas_2 = len(canal2[0])

    # Validación mínima
    if columnas_1 != filas_2:
        raise ValueError("Las dimensiones no son compatibles para la multiplicación.")

    # Crear matriz resultado con ceros
    resultado = [[0 for _ in range(columnas_2)] for _ in range(filas_1)]

    # Multiplicación matricial
    for i in range(filas_1):
        for j in range(columnas_2):
            suma = 0
            for k in range(columnas_1):  
                suma += canal1[i][k] * canal2[k][j]
            resultado[i][j] = round(suma, 4)

    return resultado


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 19 del TP6:
    canal1 = [
        [0.7, 0.0, 0.3, 0.0],
        [0.2, 0.6, 0.0, 0.2]
    ]
    canal2 = [
        [0.9, 0.0, 0.1],
        [0.0, 1.0, 0.0],
        [0.1, 0.1, 0.8],
        [0.0, 0.5, 0.5]
    ]

    compuesto = get_matriz_compuesta(canal1, canal2)
    print("=== Canal Compuesto en Serie (Ej 19 TP6) ===")
    for fila in compuesto:
        print(" ", fila)
    # Esperado:
    # [0.66, 0.03, 0.31]
    # [0.18, 0.70, 0.12]
