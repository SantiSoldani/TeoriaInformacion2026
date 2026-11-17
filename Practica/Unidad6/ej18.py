'''18. Realizar funciones booleanas en Python que reciban como parámetro la matriz de un canal
y verifiquen si se trata de:
a. Un canal sin ruido
b. Un canal determinante'''

def es_canal_sin_ruido(matriz_canal: list[list[float]]) -> bool:
    """
    a. Devuelve True si cada columna de la matriz tiene a lo sumo o exactamente un valor distinto de 0.
    """
    filas = len(matriz_canal)
    columnas = len(matriz_canal[0]) if filas > 0 else 0

    for j in range(columnas):
        contador_no_cero = 0
        for i in range(filas):
            if matriz_canal[i][j] != 0:
                contador_no_cero += 1
            if contador_no_cero > 1:
                return False
        if contador_no_cero != 1:
            return False

    return True


def es_canal_determinante(matriz_canal: list[list[float]]) -> bool:
    """
    b. Devuelve True si cada fila tiene exactamente un valor distinto de 0.
    """
    for fila in matriz_canal:
        contador_no_cero = 0
        for v in fila:
            if v != 0:
                contador_no_cero += 1
            if contador_no_cero > 1:
                return False
        if contador_no_cero != 1:
            return False

    return True


if __name__ == "__main__":
    # Prueba con canales del Ejercicio 17 del TP6:
    # Canal 1 (Determinante):
    # [[0, 1, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]] (4 entradas x 3 salidas) -> cada fila tiene un 1
    c_det = [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0]
    ]

    # Canal 2 (Sin ruido):
    # [[1, 0, 0, 0], [0, 0.2, 0, 0.8], [0, 0, 1, 0]] (3 entradas x 4 salidas) -> cada columna tiene un solo no nulo
    c_sin_ruido = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.0, 0.8],
        [0.0, 0.0, 1.0, 0.0]
    ]

    print("Canal 1 - ¿Sin ruido?   :", es_canal_sin_ruido(c_det), "(esperado False)")
    print("Canal 1 - ¿Determinante?:", es_canal_determinante(c_det), "(esperado True)")
    print("Canal 2 - ¿Sin ruido?   :", es_canal_sin_ruido(c_sin_ruido), "(esperado True)")
    print("Canal 2 - ¿Determinante?:", es_canal_determinante(c_sin_ruido), "(esperado False)")
