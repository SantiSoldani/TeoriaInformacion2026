'''25. Implementar funciones en Python que reciban como parámetro la matriz de un canal y
calculen su capacidad en los siguientes casos:
a. Canal determinante
b. Canal sin ruido
'''

import math


def entropia(fila: list[float]) -> float:
    """Calcula la entropía H de una distribución."""
    H = 0.0
    for p in fila:
        if p > 0:
            H -= p * math.log2(p)
    return H


def es_canal_determinante(matriz: list[list[float]]) -> bool:
    """Canal determinante: cada fila tiene exactamente un valor no nulo (que es 1.0)."""
    for fila in matriz:
        count = sum(1 for v in fila if v != 0)
        if count != 1:
            return False
    return True


def es_canal_sin_ruido(matriz: list[list[float]]) -> bool:
    """Canal sin ruido: cada columna tiene a lo sumo / exactamente un valor distinto de cero."""
    filas = len(matriz)
    columnas = len(matriz[0])
    for j in range(columnas):
        count = sum(1 for i in range(filas) if matriz[i][j] != 0)
        if count != 1:
            return False
    return True


def es_uniforme(matriz: list[list[float]]) -> bool:
    """Canal uniforme: todas las filas son permutaciones de la primera fila."""
    primera = sorted(matriz[0])
    for fila in matriz[1:]:
        if sorted(fila) != primera:
            return False
    return True


def capacidad_canal_determinante(matriz: list[list[float]]) -> float:
    """
    a. Capacidad de un canal determinante:
       C = log2(número de salidas alcanzables) bits.
    """
    columnas = len(matriz[0])
    return round(math.log2(columnas), 4)


def capacidad_canal_sin_ruido(matriz: list[list[float]]) -> float:
    """
    b. Capacidad de un canal sin ruido:
       C = log2(número de entradas) bits.
    """
    filas = len(matriz)
    return round(math.log2(filas), 4)


def capacidad_canal(matriz: list[list[float]]) -> float:
    """
    Calcula la capacidad del canal según su tipo:
      - Determinante: C = log2(columnas)
      - Sin ruido:    C = log2(filas)
      - Uniforme:     C = log2(columnas) - H(fila)
    """
    if es_canal_determinante(matriz):
        return capacidad_canal_determinante(matriz)

    if es_canal_sin_ruido(matriz):
        return capacidad_canal_sin_ruido(matriz)

    if es_uniforme(matriz):
        columnas = len(matriz[0])
        return round(math.log2(columnas) - entropia(matriz[0]), 4)

    raise ValueError("El canal no es determinante, ni sin ruido, ni uniforme.")


if __name__ == "__main__":
    # Canal determinante (4 entradas x 3 salidas):
    c_det = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0]
    ]

    # Canal sin ruido (3 entradas x 4 salidas):
    c_sr = [
        [0.5, 0.5, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

    print("=== Capacidad de Canales Especiales ===")
    print("Capacidad Canal Determinante (3 salidas):", capacidad_canal(c_det), "bits (esperado log2(3) = 1.5850)")
    print("Capacidad Canal Sin Ruido (3 entradas)  :", capacidad_canal(c_sr), "bits (esperado log2(3) = 1.5850)")



if __name__ == "__main__":
    # Canal determinante (4 entradas x 3 salidas):
    c_det = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0]
    ]

    # Canal sin ruido (3 entradas x 4 salidas):
    c_sr = [
        [0.5, 0.5, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

    print("=== Capacidad de Canales Especiales ===")
    print("Capacidad Canal Determinante (3 salidas):", capacidad_canal(c_det), "bits (esperado log2(3) = 1.5850)")
    print("Capacidad Canal Sin Ruido (3 entradas)  :", capacidad_canal(c_sr), "bits (esperado log2(3) = 1.5850)")