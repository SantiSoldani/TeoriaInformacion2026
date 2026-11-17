'''
1. Codificar una función booleana en Python que reciba como parámetros: una lista con la
distribución de probabilidades de una fuente, otra lista con palabras código para la
extensión de orden N y el valor de N, y verifique si el código cumple con el Primer Teorema
de Shannon.
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


# Primer Teorema de Shannon (Teorema de codificación de fuente):
#   H_r(S) <= L_n / n < H_r(S) + 1/n
# Para n=1: H_r(S) <= L < H_r(S) + 1

def primerTeoremaShannon(probabilidades: list, palabras_codigo: list, N: int = 1) -> bool:
    """
    Verifica si un código cumple con el Primer Teorema de Shannon:
        H_r(S) <= L_n / N < H_r(S) + 1/N

    Parámetros:
        probabilidades: Lista con la distribución de probabilidades (de la fuente S o de la extensión S^N).
        palabras_codigo: Lista con las palabras código para la extensión de orden N.
        N: Orden de la extensión (por defecto 1).

    Retorna:
        True si cumple el teorema, False en caso contrario.
    """
    if not palabras_codigo or not probabilidades or N <= 0:
        return False

    # 1. Obtenemos r (cantidad de símbolos distintos en el alfabeto código)
    r = len(alfabeto_codigo(palabras_codigo))
    if r < 2:
        return False

    # 2. Manejo de probabilidades: si se pasó la fuente base S y las palabras código
    # corresponden a la extensión de orden N, generamos las probabilidades de la extensión.
    if len(probabilidades) != len(palabras_codigo) and N > 1:
        probs_n = probabilidades_extension(probabilidades, N)
        H = entropia(probabilidades, r)
    elif len(probabilidades) == len(palabras_codigo) and N > 1:
        probs_n = probabilidades
        # Si ya se pasaron las probabilidades de S^N: H(S^N) = N * H(S) => H(S) = H(S^N) / N
        H = entropia(probabilidades, r) / N
    else:
        probs_n = probabilidades
        H = entropia(probabilidades, r)

    # 3. Calculamos la longitud media L_n del código para la extensión de orden N
    Ln = longMedia(palabras_codigo, probs_n)

    # 4. Longitud media por símbolo de fuente original: L_simbolo = Ln / N
    L_simbolo = Ln / N

    # 5. Verificamos la cota: H_r(S) <= L_n / N < H_r(S) + 1/N
    # (usamos math.isclose por posibles imprecisiones de coma flotante en el extremo inferior)
    cumple_cota_inferior = (L_simbolo >= H) or math.isclose(L_simbolo, H, abs_tol=1e-9)
    cumple_cota_superior = (L_simbolo < H + (1 / N))
    print(f"n = {N} | H_r(S) = {H:.2f} | L_{N} = {Ln} | L_{N}/{N} = {L_simbolo} | Cota Sup = {H + 1/N:.2f}")

    return cumple_cota_inferior and cumple_cota_superior


if __name__ == "__main__":
    # IMPORTANTE: Definir como listas [ ] y NO como sets { }, ya que los sets en Python
    # no garantizan orden y alteran la correspondencia entre probabilidades y palabras código.
    P = [0.5, 0.2, 0.3]
    C1 = ["11", "010", "00"]
    C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]

    print("=== Ejercicio 3 ===")
    print("Primer teorema de Shannon C1 (n=1):", primerTeoremaShannon(P, C1, N=1))
    print("Primer teorema de Shannon C2 (n=2):", primerTeoremaShannon(P, C2, N=2))
