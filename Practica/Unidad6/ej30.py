'''
30. Desarrollar una función en Python que reciba como parámetros: una lista con
probabilidades a priori y la matriz de un canal, y calcule la probabilidad de error utilizando
la regla de decisión de máxima posibilidad.
'''


def prob_error_canal(probs_a_priori: list[float], canal: list[list[float]], condicional: bool = False) -> float:
    """
    Calcula la probabilidad de error del canal según la regla de decisión de máxima posibilidad.

    Convención de Cátedra (Apunte págs. 85-86 y TP6 Ej. 29):
      - Por defecto (condicional=False): "Regla de decisión de máxima posibilidad" (Maximum Likelihood),
        donde para cada símbolo de salida Y=y se elige la entrada X=x que maximiza el elemento de la
        columna de la matriz del canal: max_x P(Y=y | X=x).
      - Si condicional=True: "Regla de máxima posibilidad condicional" (MAP),
        donde se maximiza la probabilidad a posteriori: max_x P(X=x) * P(Y=y | X=x).

    Parámetros:
        probs_a_priori (list[float]): Probabilidades de los símbolos de entrada P(X=x).
        canal (list[list[float]]): Matriz del canal donde canal[x][y] = P(Y=y | X=x).
        condicional (bool): False para Máxima Posibilidad (ML de cátedra), True para MAP.

    Retorna:
        float: Probabilidad de error PE redondeada a 4 decimales.
    """
    filas = len(canal)        # cantidad de valores de entrada X
    columnas = len(canal[0])  # cantidad de valores de salida Y

    p_acierto_total = 0.0

    # Recorremos cada posible símbolo recibido Y = y
    for y in range(columnas):
        if condicional:
            # MAP: maximiza P(X=x, Y=y) = P(X=x) * P(Y=y|X=x)
            criterio = [probs_a_priori[x] * canal[x][y] for x in range(filas)]
        else:
            # Máxima Posibilidad estándar de la cátedra: maximiza P(Y=y | X=x)
            criterio = [canal[x][y] for x in range(filas)]

        # Decisión d(y): índice de la entrada x elegida
        x_decision = criterio.index(max(criterio))

        # Probabilidad de acierto para esta salida: P(X = x_decision, Y = y)
        p_acierto_total += probs_a_priori[x_decision] * canal[x_decision][y]

    # Probabilidad de error total: P(E) = 1 - P(acierto)
    prob_error = 1.0 - p_acierto_total
    return round(prob_error, 4)


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 29 del TP6:
    # Canal:
    #   [0.6, 0.3, 0.1]
    #   [0.1, 0.8, 0.1]
    #   [0.3, 0.3, 0.4]
    canal = [
        [0.6, 0.3, 0.1],
        [0.1, 0.8, 0.1],
        [0.3, 0.3, 0.4]
    ]

    pa = [1/3, 1/3, 1/3]
    pb = [1/8, 3/8, 4/8]
    pc = [4/15, 3/15, 8/15]

    pea = prob_error_canal(pa, canal)
    peb = prob_error_canal(pb, canal)
    pec = prob_error_canal(pc, canal)

    print("=== Probabilidad de Error - Ejercicio 29 TP6 ===")
    print(f"a. P_E = {pea:.4f} (esperado oficial TP6: 0.4000)")
    print(f"b. P_E = {peb:.4f} (esperado oficial TP6: 0.4250)")
    print(f"c. P_E = {pec:.4f} (esperado oficial TP6: 0.4667)")
