'''7. Realizar funciones en Python que reciban como parámetros: una lista con las
probabilidades a priori y la matriz de probabilidades condicionales del canal, y devuelvan:
a. Una lista con las probabilidades de los símbolos de salida
b. Una matriz con las probabilidades a posteriori del canal
c. Una matriz con las probabilidades de los eventos simultáneos
''' 

def calcular_probabilidad_salida(p_x, p_y_dado_x):
    """
    Calcula P(Y) = sum_x P(X) * P(Y|X)
    """
    num_salidas = len(p_y_dado_x[0])
    num_entradas = len(p_x)
    p_y = [0.0] * num_salidas

    for j in range(num_salidas):  # columna (salida)
        for i in range(num_entradas):  # fila (entrada)
            p_y[j] += p_x[i] * p_y_dado_x[i][j]
    return p_y


def calcular_probabilidad_conjunta(p_x, p_y_dado_x):
    """
    Calcula P(X,Y) = P(X) * P(Y|X)
    """
    num_entradas = len(p_x)
    num_salidas = len(p_y_dado_x[0])
    p_xy = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]

    for i in range(num_entradas):
        for j in range(num_salidas):
            p_xy[i][j] = p_x[i] * p_y_dado_x[i][j]
    return p_xy


def calcular_probabilidad_a_posteriori(p_x, p_y_dado_x):
    """
    Calcula P(X|Y) usando la regla de Bayes:
    P(X|Y) = [P(Y|X) * P(X)] / P(Y)
    """
    p_y = calcular_probabilidad_salida(p_x, p_y_dado_x)
    num_entradas = len(p_x)
    num_salidas = len(p_y_dado_x[0])
    p_x_dado_y = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]

    for j in range(num_salidas):
        for i in range(num_entradas):
            if p_y[j] > 0:
                p_x_dado_y[i][j] = (p_y_dado_x[i][j] * p_x[i]) / p_y[j]
    return p_x_dado_y


# Aliases para compatibilidad con nombres directos
probabilidad_salida = calcular_probabilidad_salida
probabilidad_conjunta = calcular_probabilidad_conjunta
probabilidad_a_posteriori = calcular_probabilidad_a_posteriori


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 6 del TP6:
    p_x = [0.3, 0.3, 0.4]
    canal = [
        [0.4, 0.4, 0.2],
        [0.3, 0.2, 0.5],
        [0.3, 0.4, 0.3]
    ]

    p_y = calcular_probabilidad_salida(p_x, canal)
    p_xy = calcular_probabilidad_conjunta(p_x, canal)
    p_x_dado_y = calcular_probabilidad_a_posteriori(p_x, canal)

    print("=== Ejercicio 6 TP6 ===")
    print("P(Y):", [round(x, 4) for x in p_y])
    print("P(X, Y):")
    for r in p_xy:
        print(" ", [round(x, 4) for x in r])
    print("P(X|Y):")
    for r in p_x_dado_y:
        print(" ", [round(x, 4) for x in r])
