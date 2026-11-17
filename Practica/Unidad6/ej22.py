'''22. Desarrollar funciones en Python que reciban como parámetros: la matriz de un canal y los
índices de dos columnas, y realicen lo siguiente:
a. Verificar si las columnas se pueden combinar en una reducción suficiente
b. Generar la matriz del canal determinante necesario para combinar las columnas
'''

import math


def se_pueden_reducir(matriz: list[list[float]], col1: int, col2: int) -> bool:
    """
    a. Verifica si las columnas col1 y col2 pueden combinarse en una reducción suficiente.
    Dos columnas son reducibles si son proporcionales en todas las filas (a_i * b_k == a_k * b_i).
    """
    filas = len(matriz)
    # Comprobación de proporcionalidad cruzada para evitar divisiones por cero
    for i in range(filas):
        for k in range(i + 1, filas):
            prod1 = matriz[i][col1] * matriz[k][col2]
            prod2 = matriz[k][col1] * matriz[i][col2]
            if not math.isclose(prod1, prod2, abs_tol=1e-6):
                return False
    return True


def generar_matriz_determinante(matriz: list[list[float]], col1: int, col2: int) -> list[list[int]]:
    """
    b. Genera la matriz del canal determinante necesaria para combinar las columnas col1 y col2.
    La matriz resultante tiene dimensiones: (columnas_originales) x (columnas_originales - 1).
    """
    c_min, c_max = min(col1, col2), max(col1, col2)
    columnas_original = len(matriz[0])
    columnas_nueva = columnas_original - 1

    # 1. Crear matriz identidad de tamaño (columnas_nueva) x (columnas_nueva)
    matriz_det = [[1 if i == j else 0 for j in range(columnas_nueva)]
                  for i in range(columnas_nueva)]

    # 2. Fila que combina la columna mayor en la menor
    fila_nueva = [0] * columnas_nueva
    fila_nueva[c_min] = 1

    # 3. Insertar la fila nueva en la posición c_max
    matriz_det.insert(c_max, fila_nueva)

    return matriz_det


if __name__ == "__main__":
    # Prueba con datos del Apunte de Cátedra (pág. 82):
    # Canal:
    #   [1/6, 1/3, 1/2, 0]
    #   [1/12, 1/6, 1/4, 1/2]
    # Columnas 0 y 1 son proporcionales (ratio 1:2)
    c_ejemplo = [
        [1/6, 1/3, 1/2, 0],
        [1/12, 1/6, 1/4, 1/2]
    ]

    print("¿Col 0 y 1 son reducibles?:", se_pueden_reducir(c_ejemplo, 0, 1), "(esperado True)")
    print("¿Col 1 y 2 son reducibles?:", se_pueden_reducir(c_ejemplo, 1, 2), "(esperado False)")

    det = generar_matriz_determinante(c_ejemplo, 0, 1)
    print("Matriz determinante generada (4 x 3):")
    for fila in det:
        print(" ", fila)
