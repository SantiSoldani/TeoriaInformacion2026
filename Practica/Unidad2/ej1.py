
'''
1. Dada una lista que representa una distribución de probabilidades de una fuente de
memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:
a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
comprensión de listas).
b. obtener la entropía de la fuente (utilizar la función anterior).
'''

import math

def informacion(probabilidad_evento, r = 2):
    """Calcula la cantidad de información de un evento/símbolo individual."""
    if probabilidad_evento <= 0:
        return float('inf')
    return math.log(1 / probabilidad_evento, r)

def entropia(probabilidad_evento, r = 2):
    """Calcula el aporte a la entropía de un evento: p * I(p). Si p == 0, devuelve 0."""
    if probabilidad_evento <= 0:
        return 0.0
    return probabilidad_evento * informacion(probabilidad_evento, r)

def cantidades_informacion(probabilidades, r = 2):
    """
    1.a Genera una lista con la cantidad de información en bits de cada símbolo
    a partir de una lista de probabilidades (utiliza comprensión de listas).
    """
    return [informacion(p, r) for p in probabilidades]

def entropia_fuente(probabilidades, r = 2):
    """
    1.b Obtiene la entropía de la fuente utilizando la función anterior (cantidades_informacion).
    H(S) = sum(p_i * I(s_i))
    """
    infos = cantidades_informacion(probabilidades, r)
    return sum(p * info for p, info in zip(probabilidades, infos) if p > 0)

def entropia_fuenteBinaria(probabilidad, r = 2):
    probs = [probabilidad, 1 - probabilidad]
    return entropia_fuente(probs, r)

if __name__ == '__main__':
    probabilidades = [0.3, 0.5, 0.15, 0.05]
    cantidad_informacion = cantidades_informacion(probabilidades)
    print("Cantidad de informacion: ", cantidad_informacion)
    print("Entropia de la fuente: ", entropia_fuente(probabilidades))