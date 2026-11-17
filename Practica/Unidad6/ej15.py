'''15. Implementar funciones en Python que reciban como parámetros: una lista con las
probabilidades a priori y la matriz de probabilidades condicionales del canal, y calculen por
definición (es decir, a partir de las probabilidades, no de sus relaciones):
a. La equivocación o ruido
b. La pérdida
c. La entropía afín
d. La información mutua'''

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


def probabilidad_conjunta(p_x: list[float], canal: list[list[float]]) -> list[list[float]]:
    """Calcula P(X, Y) = P(X) * P(Y|X)."""
    num_entradas = len(p_x)
    num_salidas = len(canal[0])
    p_xy = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]
    for i in range(num_entradas):
        for j in range(num_salidas):
            p_xy[i][j] = p_x[i] * canal[i][j]
    return p_xy


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


def ruido(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    a. Calcula la equivocación o ruido H(A/B) POR DEFINICIÓN:
       H(A/B) = sum_i sum_j P(a_i, b_j) * log2(1 / P(a_i/b_j))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    p_post = probabilidad_a_posteriori(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(probs_condicionales[0])):
            if p_xy[i][j] > 0 and p_post[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / p_post[i][j])
    return round(val, 4)


def perdida(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    b. Calcula la pérdida H(B/A) POR DEFINICIÓN:
       H(B/A) = sum_i sum_j P(a_i, b_j) * log2(1 / P(b_j/a_i))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(probs_condicionales[0])):
            if p_xy[i][j] > 0 and probs_condicionales[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / probs_condicionales[i][j])
    return round(val, 4)


def entropia_afin(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    c. Calcula la entropía afín H(A, B) POR DEFINICIÓN:
       H(A, B) = sum_i sum_j P(a_i, b_j) * log2(1 / P(a_i, b_j))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(probs_condicionales[0])):
            if p_xy[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / p_xy[i][j])
    return round(val, 4)


def informacion_mutua(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    d. Calcula la información mutua I(A, B) POR DEFINICIÓN:
       I(A, B) = sum_i sum_j P(a_i, b_j) * log2(P(a_i, b_j) / (P(a_i) * P(b_j)))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    p_y = probabilidad_salida(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(p_y)):
            if p_xy[i][j] > 0:
                denominador = probs_a_priori[i] * p_y[j]
                if denominador > 0:
                    val += p_xy[i][j] * math.log2(p_xy[i][j] / denominador)
    return round(val, 4)


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 14 (Canal 1) del TP6:
    # P = { 0.70, 0.30 }, canal = [[0.7, 0.3], [0.4, 0.6]]
    # Resultados oficiales del TP6:
    #   Ruido H(A/B)     = 0.8247
    #   Pérdida H(B/A)   = 0.9082
    #   Entropía afín    = 1.7895
    #   Inf. mutua       = 0.0566
    p_x = [0.70, 0.30]
    canal = [[0.7, 0.3], [0.4, 0.6]]

    r = ruido(p_x, canal)
    p = perdida(p_x, canal)
    e = entropia_afin(p_x, canal)
    i = informacion_mutua(p_x, canal)

    print("=== Ejercicio 14 (Canal 1) TP6 - Cálculos por Definición ===")
    print(f"Ruido H(A/B)         : {r} (esperado 0.8247)")
    print(f"Pérdida H(B/A)       : {p} (esperado 0.9082)")
    print(f"Entropía afín H(A, B): {e} (esperado 1.7895)")
    print(f"Información mutua I  : {i} (esperado 0.0566)")
