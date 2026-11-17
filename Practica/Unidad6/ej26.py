'''26. Realizar una función en Python que reciba como parámetros: la matriz de un canal binario
y un valor de paso, y estime la capacidad del canal mediante el cálculo de la información
mutua para un conjunto de probabilidades a priori distribuidas uniformemente según el
paso especificado. La función debe retornar el valor de capacidad estimado, junto con su
probabilidad asociada.
'''

import math


def entropia(fila: list[float]) -> float:
    """Calcula la entropía H de una distribución."""
    H = 0.0
    for p in fila:
        if p > 0:
            H -= p * math.log2(p)
    return H


def distribucion_salida(p_apriori: list[float], canal: list[list[float]]) -> list[float]:
    """Calcula la distribución de salida P(Y)."""
    salida = []
    num_filas = len(canal)
    num_columnas = len(canal[0])

    for y in range(num_columnas):
        prob = 0.0
        for x in range(num_filas):
            prob += p_apriori[x] * canal[x][y]
        salida.append(prob)

    return salida


def informacion_mutua(p_apriori: list[float], canal: list[list[float]]) -> float:
    """
    Calcula I(X; Y) = H(Y) - H(Y|X)
    """
    # H(Y)
    p_salida = distribucion_salida(p_apriori, canal)
    Hy = entropia(p_salida)

    # H(Y|X) = sum_x P(X=x) * H(Y|X=x)
    Hy_dado_x = 0.0
    for x in range(len(canal)):
        Hy_dado_x += p_apriori[x] * entropia(canal[x])

    return Hy - Hy_dado_x


def maximizar_informacion_mutua(canal: list[list[float]], h: float) -> tuple[float, float]:
    """
    Estima la capacidad del canal binario mediante barrido de la probabilidad a priori omega en [0, 1]
    con paso h.

    Retorna:
        tuple[float, float]: (probabilidad_asociada_optima, capacidad_estimada)
    """
    capacidad = -1.0
    prob_optima = 0.0

    omega = 0.0
    while omega <= 1.0000001:
        p_apriori = [omega, 1.0 - omega]
        info = informacion_mutua(p_apriori, canal)

        if info > capacidad:
            capacidad = info
            prob_optima = omega

        omega += h

    return round(prob_optima, 4), round(capacidad, 4)


if __name__ == "__main__":
    # Prueba con canal binario simétrico BSC con p=0.1
    # Capacidad teórica BSC: 1 - H(0.1) = 1 - 0.4690 = 0.5310 con p_optima = 0.5
    bsc = [
        [0.9, 0.1],
        [0.1, 0.9]
    ]

    p_opt, cap = maximizar_informacion_mutua(bsc, h=0.01)
    print("=== Estimación de Capacidad (Canal BSC p=0.1) ===")
    print(f"Probabilidad óptima estimada: {p_opt} (esperado 0.50)")
    print(f"Capacidad estimada          : {cap} bits (esperado ~0.5310)")
