'''
15. Codificar funciones en Python que resuelvan los siguiente:
a. Dada una cadena de caracteres que representa un mensaje emitido por una fuente,
devolver una lista con su alfabeto y su matriz de transición.
b. Dada una lista que contenga el alfabeto de una fuente y su matriz de transición,
simular la generación de una cadena de caracteres emitida por esa fuente.
c. Dada una matriz de transición y una tolerancia máxima, determinar si se trata de
una fuente de memoria nula o una fuente con memoria.
'''

import random

def matrizTransicion(cadena):
    '''
    Genera la matriz de transición a partir de una cadena. La convencion es la siguiente: 
    M[i][j] = P(sale i | antes salió j).
    Se cuentan los pares de simbolos consecutivos del mensaje, se coloca el valor contado en la posicion
    de la matriz siguiendo la convención. Luego, se divide cada celda por la cantidad de apariciones del simbolo
    de la columna.
    '''
    alfabeto = sorted(set(cadena))
    n = len(alfabeto)

    mat = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(len(cadena)-1):
        anterior = cadena[i]
        siguiente = cadena[i+1]
        mat[alfabeto.index(siguiente)][alfabeto.index(anterior)] += 1

    for j in range(n):
        total_col = sum(mat[i][j] for i in range(n))
        for i in range(n):
            mat[i][j] = mat[i][j] / total_col if total_col > 0 else 0.0
    return alfabeto, mat

def matriz_transicion_catedra(cadena):
    """
    Matriz de transición en el formato de la cátedra (por COLUMNAS):
    M[i][j] = P(sale i | antes salió j).
    Se cuentan los pares de símbolos consecutivos del mensaje y cada columna se
    divide por la cantidad de veces que ese símbolo fue seguido de otro, así cada
    columna suma 1.
    """
    alfabeto = sorted(set(cadena))
    n = len(alfabeto)
    indice = {s: k for k, s in enumerate(alfabeto)}
    conteos = [[0] * n for _ in range(n)]
    for anterior, siguiente in zip(cadena, cadena[1:]):
        conteos[indice[siguiente]][indice[anterior]] += 1
    M = [[0.0] * n for _ in range(n)]
    for j in range(n):
        total_col = sum(conteos[i][j] for i in range(n))
        for i in range(n):
            M[i][j] = conteos[i][j] / total_col if total_col > 0 else 0.0
    return alfabeto, conteos, M
# INTERPRETACIÓN:
#   Formato cátedra (Unidad 2): M[i][j] = P(sale i | antes salió j). Cada COLUMNA
#   suma 1: Σ_j P(j|i) = 1.
#   - Se cuentan los pares (anterior, siguiente) del mensaje y cada columna se divide
#     por la cantidad de veces que ese símbolo fue seguido de otro. No se divide por
#     el total de pares, y el último símbolo del mensaje no tiene siguiente.
#   - Memoria nula <=> cada FILA tiene todos sus valores (casi) iguales: la
#     probabilidad de que salga i es la misma sin importar cuál salió antes.
#   EN EL PARCIAL: explicar cómo se armó (qué es fila, qué es columna y por qué se divide).

def simularMensaje(alfabeto, mat, longitud):
    cadena = []
    estado = random.choice(alfabeto)
    cadena.append(estado)
    for _ in range(longitud-1):
        idx = alfabeto.index(estado)
        pesos = [mat[i][idx] for i in range(len(alfabeto))]
        estado = random.choices(alfabeto, weights=pesos)[0]
        cadena.append(estado)
    return ''.join(cadena)


def esMemoriaNula(matriz, tolerancia=0.05):
    if not matriz or not matriz[0]:
        return True

    distancias_maximas = [max(fila) - min(fila) for fila in matriz]
    max_distancia = max(distancias_maximas)
    return max_distancia <= tolerancia


if __name__ == '__main__':
    # Prueba:
    cadena = "abracadabra"
    alfabeto, matriz = matrizTransicion(cadena)
    print("Alfabeto:", alfabeto)
    print("Matriz de transición:")
    for fila in matriz:
        print(" ", fila)
    print("Mensaje simulado:", simularMensaje(alfabeto, matriz, len(cadena)))
    print("¿Es memoria nula?:", esMemoriaNula(matriz, 0.1))