'''
14. Dada una matriz de transición (lista de listas), implementar funciones en Python que
resuelvan lo siguiente:
a. generar una lista que represente el vector estacionario de la fuente.
b. calcular la entropía de la fuente (utilizar la función anterior).
'''

import math


def _validar_matriz_transicion(matriz):
    """Comprueba que sea cuadrada y que cada fila sea una distribución."""
    n = len(matriz)
    if n == 0:
        raise ValueError("La matriz de transición no puede estar vacía.")

    for fila in matriz:
        if len(fila) != n:
            raise ValueError("La matriz de transición debe ser cuadrada.")
        if any(probabilidad < 0 or probabilidad > 1 for probabilidad in fila):
            raise ValueError("Las probabilidades deben estar entre 0 y 1.")
        if not math.isclose(sum(fila), 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError("Cada fila de la matriz debe sumar 1.")


def entropia(probabilidades, r=2):
    """Calcula la entropía de una distribución de probabilidades."""
    if r <= 0 or r == 1:
        raise ValueError("La base del logaritmo debe ser positiva y distinta de 1.")
    if any(probabilidad < 0 or probabilidad > 1 for probabilidad in probabilidades):
        raise ValueError("Las probabilidades deben estar entre 0 y 1.")

    return -sum(
        probabilidad * math.log(probabilidad, r)
        for probabilidad in probabilidades
        if probabilidad > 0
    )


def vectorEstacionario(matriz, decimales=None, tolerancia=1e-12, max_iter=10000):
    """
    Calcula el vector estacionario por iteración.

    Convención: matriz[i][j] es la probabilidad de pasar del símbolo i al j.
    Usa una iteración suavizada para evitar oscilaciones en cadenas periódicas;
    sus puntos fijos son los vectores que cumplen pi[j] = sum_i pi[i] * matriz[i][j].
    """
    _validar_matriz_transicion(matriz)
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser positiva.")
    if max_iter <= 0:
        raise ValueError("max_iter debe ser positivo.")

    n = len(matriz)
    pi = [1 / n] * n

    for _ in range(max_iter):
        siguiente = [0.0] * n
        for i in range(n):
            for j in range(n):
                siguiente[j] += pi[i] * matriz[i][j]

        # Promediar pi con pi*P conserva los estacionarios y ayuda a converger
        # cuando la cadena es periódica.
        nuevo_pi = [(pi[j] + siguiente[j]) / 2 for j in range(n)]

        diferencia = sum(abs(nuevo_pi[k] - pi[k]) for k in range(n))
        pi = nuevo_pi
        if diferencia < tolerancia:
            break
    else:
        raise RuntimeError(
            "La iteración no convergió dentro de max_iter; aumentá max_iter o revisá la matriz."
        )

    suma = sum(pi)
    pi = [probabilidad / suma for probabilidad in pi]
    if decimales is not None:
        return [round(probabilidad, decimales) for probabilidad in pi]
    return pi


# Alias para compatibilidad con código anterior.
vectorEstaconario = vectorEstacionario


def entropiaFuenteMarkov(matriz, vector_estacionario=None):
    """
    Calcula la entropía por símbolo de la fuente de Markov:
    H = sum_i pi_i * H(fila_i).
    """
    _validar_matriz_transicion(matriz)
    if vector_estacionario is None:
        vector_estacionario = vectorEstacionario(matriz)

    if len(vector_estacionario) != len(matriz):
        raise ValueError("El vector estacionario debe tener una entrada por estado.")
    if any(probabilidad < 0 or probabilidad > 1 for probabilidad in vector_estacionario):
        raise ValueError("Las probabilidades del vector deben estar entre 0 y 1.")
    if not math.isclose(sum(vector_estacionario), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("El vector estacionario debe sumar 1.")

    return sum(
        vector_estacionario[i] * entropia(matriz[i], r=2)
        for i in range(len(matriz))
    )


if __name__ == '__main__':
    matriz = [[1 / 2, 1 / 2],
              [1 / 3, 2 / 3]]
    vector = vectorEstacionario(matriz)
    print("Vector estacionario:", [round(probabilidad, 4) for probabilidad in vector])
    print("Entropía de la fuente de Markov:", round(entropiaFuenteMarkov(matriz), 6), "bits")
