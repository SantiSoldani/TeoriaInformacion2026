'''
6. Realizar una función en Python que reciba como parámetros: dos listas paralelas con la
distribución de probabilidades de una fuente y su codificación, y calcule el rendimiento y la
redundancia del código.
'''

import math


def informacion(probabilidades, r=2):
    '''
        Información es todo evento con cierto grado de incertidumbre
        Es inversamente proporcional a la probabilidad del evento, ya que 
        a mayor probabilidad de ocurrencia de un evento, menor la cantidad de información
        que nos da.
    '''

    # Caso 1: Probabilidad individual (int o float)
    if isinstance(probabilidades, (int, float)):
        if probabilidades > 0 and probabilidades <= 1:
            return math.log(1 / probabilidades, r)
        else: 
            return None
    # Caso 2: Lista o tupla de probabilidades
    return [math.log(1 / prob, r) for prob in probabilidades if prob > 0 and prob <= 1]


def entropia(probabilidades : list, r=2) -> float:
    '''
        Es una cualidad de la fuente, no individual de cada evento.
        El valor medio de la información por símbolo suministrada por la fuente o el valor medio de
        la incertidumbre de un observador antes de conocer la salida de la fuente.
        Se calcula como: 
        La sumatoria de las probabilidades de los eventos posibles multiplicadas
        por la cantidad de información que nos da cada uno de ellos.
    '''

    return sum(prob * informacion(prob, r) for prob in probabilidades if prob > 0 and prob <= 1)


def longMedia(codigo, probabilidades) -> float:
    """Calcula la longitud media del código."""
    return sum(probabilidad * len(palabra)
               for palabra, probabilidad in zip(codigo, probabilidades))


def alfabeto_codigo(codigo) -> str:
    """Devuelve los símbolos distintos que aparecen en las palabras código."""
    return "".join(sorted(set("".join(codigo))))


def probabilidades_extension(probabilidades: list, N: int) -> list:
    """Calcula las probabilidades de la extensión de orden N para una fuente de memoria nula."""
    if N <= 1:
        return list(probabilidades)
    sub_probs = probabilidades_extension(probabilidades, N - 1)
    return [p_prev * p for p_prev in sub_probs for p in probabilidades]


def rendimiento_redundancia(probabilidades: list, codigo: list) -> tuple:
    """
    Calcula el rendimiento (eta = H_r / L) y la redundancia (1 - eta) de un código.
    Espera dos listas paralelas (misma cantidad de elementos):
      - probabilidades: distribución de probabilidad de los símbolos (fuente o extensión).
      - codigo: palabras código correspondientes a cada símbolo.
    """
    if not codigo or not probabilidades or len(codigo) != len(probabilidades):
        raise ValueError("Las listas de probabilidades y código deben tener la misma longitud y no estar vacías.")

    # Base r a partir de los símbolos únicos del código
    r = len(alfabeto_codigo(codigo))
    if r < 2:
        r = 2

    # Ojo con el orden de parámetros: longmedia(codigo, probabilidades)
    L = longMedia(codigo, probabilidades)
    H = entropia(probabilidades, r)

    if L == 0:
        return 0.0, 1.0

    rendimiento = round(H / L, 4)
    redundancia = round(1 - rendimiento, 4)

    return rendimiento, redundancia


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 8
    probs = [0.2, 0.15, 0.1, 0.3, 0.25]
    codigos = {
        "Código 1": ['01', '111', '110', '101', '100'],
        "Código 2": ['00', '01', '10', '110', '111'],
        "Código 3": ['0110', '010', '0111', '1', '00'],
        "Código 4": ['11', '001', '000', '10', '01']
    }

    print("=== Prueba de Rendimiento y Redundancia (Ej 8) ===")
    for nombre, c in codigos.items():
        rend, redun = rendimiento_redundancia(probs, c)
        print(f"{nombre}: Rendimiento = {rend:.4f} ({rend*100:.2f}%) | Redundancia = {redun:.4f} ({redun*100:.2f}%)")