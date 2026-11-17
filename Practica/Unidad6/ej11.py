'''11. Desarrollar una función en Python que reciba como parámetros: una lista con las
probabilidades a priori y la matriz de probabilidades condicionales del canal, y retorne una
lista con las entropías a posteriori.'''

import math


def probabilidad_salida(p_x: list[float], canal: list[list[float]]) -> list[float]:
    """Calcula P(Y) = sum_x P(X) * P(Y|X)."""
    num_salidas = len(canal[0])
    num_entradas = len(p_x)
    p_y = [0.0] * num_salidas
    for j in range(num_salidas):
        for i in range(num_entradas):
            p_y[j] += p_x[i] * canal[i][j]
    return p_y


def probabilidad_a_posteriori(p_x: list[float], canal: list[list[float]]) -> list[list[float]]:
    """Calcula P(X|Y) = [P(Y|X) * P(X)] / P(Y)."""
    p_y = probabilidad_salida(p_x, canal)
    num_entradas = len(p_x)
    num_salidas = len(canal[0])
    p_x_dado_y = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]
    for j in range(num_salidas):
        for i in range(num_entradas):
            if p_y[j] > 0:
                p_x_dado_y[i][j] = (canal[i][j] * p_x[i]) / p_y[j]
    return p_x_dado_y


def entropias_a_posteriori(p_x: list[float], p_y_dado_x: list[list[float]]) -> list[float]:
    """
    Devuelve una lista con H(A|b_j) para cada símbolo de salida b_j:
      H(A|b_j) = sum_i P(a_i|b_j) * log2(1 / P(a_i|b_j))
    """
    p_x_dado_y = probabilidad_a_posteriori(p_x, p_y_dado_x)
    num_salidas = len(p_y_dado_x[0])
    h_posteriori = []

    for j in range(num_salidas):
        h = 0.0
        for i in range(len(p_x_dado_y)):
            p = p_x_dado_y[i][j]
            if p > 0:
                h -= p * math.log2(p)
        h_posteriori.append(round(h, 4))

    return h_posteriori


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 10 (Canal 1 del Ejercicio 14) del TP6:
    # P(A) = [0.70, 0.30]
    # Canal = [[0.7, 0.3], [0.4, 0.6]]
    # P(Y=0) = 0.7*0.7 + 0.3*0.4 = 0.61, P(Y=1) = 0.39
    # P(X=0|Y=0) = 0.49/0.61 = 0.8033, P(X=1|Y=0) = 0.12/0.61 = 0.1967 -> H(A/b1) = 0.7148
    p_x = [0.70, 0.30]
    canal = [[0.7, 0.3], [0.4, 0.6]]
    h_post = entropias_a_posteriori(p_x, canal)
    print("Entropías a posteriori H(A|b_j):", h_post)
