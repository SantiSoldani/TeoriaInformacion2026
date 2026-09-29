'''
Archivo con todas las funciones necesarias para el parcial, que comprende
las unidades 1, 2 y 3 de Teoría de la Información.
'''

import math
import random

def alfabeto(cadena):
    return sorted(set(cadena))

def imprimirmatriz(matriz):
    for fila in matriz:
        print(fila)

# Unidad 2: ejercicio 1
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

    return sum(prob * informacion(prob,r) for prob in probabilidades if prob > 0 and prob <= 1)

# Unidad 2: ejercicio 2
def alfabeto_y_probabilidades(cadena):
    # Devuelve el alfabeto y las probabilidades de los simbolos, ordenados de manera ascendente.
    alfabeto = sorted(set(cadena))
    probabilidades = [cadena.count(simbolo)/len(cadena) for simbolo in alfabeto]
    return alfabeto, probabilidades

def generacion_cadena(N, alfabeto, probabilidades) -> str:
    probabilidades_acumuladas = [sum(probabilidades[:i+1]) for i in range(len(probabilidades))]
    cadena = ""
    for _ in range(N):
        r = random.random()
        for i in range(len(alfabeto)):
            if r <= probabilidades_acumuladas[i]:
                cadena += alfabeto[i]
                break

    return cadena

# Unidad 2: ejercicio 8
def entropia_fuente_binaria(prob, r = 2):
    """
    Recibe el parámetro p (probabilidad de uno de los símbolos) de una fuente binaria
    de memoria nula y, utilizando la función entropia_fuente del ejercicio 1, calcula su entropía.
    """
    probabilidades = [prob, 1 - prob]
    return entropia(probabilidades, r)

# Unidad 2: ejercicio 10
def extension(alfabeto, probabilidades, N):
    if N <= 0:
        return [], []
    if N == 1:
        return list(alfabeto), list(probabilidades)

    # Obtenemos recursivamente la extensión de orden N - 1
    sub_alf, sub_prob = extension(alfabeto, probabilidades, N - 1)

    nueva_ext = []
    nuevas_prob = []
    for palabra, prob in zip(sub_alf, sub_prob):
        for simbolo, p in zip(alfabeto, probabilidades):
            nueva_ext.append(palabra + simbolo)
            nuevas_prob.append(prob * p)

    return nueva_ext, nuevas_prob

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
    return mat

# Unidad 2: ejercicio 14
def vectorEstacionario(matriz, tolerancia=0.001, max_iter=1000):
    """
    Utiliza un método númerico para calcular el vector estacionario de la matriz de transición.
    Partimos de una distribucion inicial equiprobable, y vamos a
    iterar haciendo la multiplicacion de la distribucion actual por la matriz de transición.
    De esta manera, conseguimos una nueva distribucion. Luego, vemos la diferencia más grande entre 
    la nueva distribucion y la anterior, y si es menor a la tolerancia, detenemos el proceso. Si no, 
    actualizamos la distribucion con la nueva y repetimos el proceso.
    """
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser positiva.")
    if max_iter <= 0:
        raise ValueError("max_iter debe ser positivo.")

    n = len(matriz) 
    vector_estacionario = [1 / n] * n    
    
    for _ in range(max_iter):   
        nuevo_vector_estacionario = [0] * n   
        for i in range(n):  
            for j in range(n):  
                nuevo_vector_estacionario[i] += vector_estacionario[j] * matriz[i][j]
                    
        diferencia = max([abs(nuevo_vector_estacionario[k] - vector_estacionario[k]) for k in range(n)])

        if diferencia < tolerancia:
            break
        else: vector_estacionario = nuevo_vector_estacionario

    else:
        raise RuntimeError(
            "La iteración no convergió dentro de max_iter; aumentá max_iter o revisá la matriz."
        )

    return nuevo_vector_estacionario


def entropiaFuenteMarkov(matriz, vector_estacionario=None):
    """
    Calcula la entropía por símbolo de una fuente de Markov.

    Convención: matriz[i][j] = P(siguiente=i | actual=j), así que cada
    columna j es la distribución de transición condicionada al estado j.
    H = sum_j pi_j * H(columna_j).
    """
    n = len(matriz)

    if vector_estacionario is None:
        vector_estacionario = vectorEstacionario(matriz)
    return sum(
        vector_estacionario[j] * entropia([matriz[i][j] for i in range(n)], r=2)
        for j in range(n)
    )

# Unidad 2: ejercicio 15
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
    return mat

def alfabeto_y_matriz_transicion(cadena):
    return alfabeto(cadena), matrizTransicion(cadena)

def esMemoriaNula(matriz, tolerancia=0.05):
    """
    Determina si una fuente es de memoria nula.
    Para cada fila (símbolo actual), calcula la distancia máxima entre pares
    (max(fila) - min(fila)). Luego toma la mayor de esas distancias y la compara
    con la tolerancia. Si es menor o igual, la fuente es de memoria nula.
    """
    if not matriz or not matriz[0]:
        return True

    distancias_maximas = [max(fila) - min(fila) for fila in matriz]
    max_distancia = max(distancias_maximas)
    return max_distancia <= tolerancia


# Unidad 3: propiedades de los códigos

# Unidad 3: ejercicio 5
def esNoSingular(codigo) -> bool:
    """
    Se denomina códigos no singulares a los códigos bloque cuyas palabras código son distintas.
    En mi caso lo calculo a partir de comparar las longitudes del conjunto de palabras unicos
    del alfabeto código, y el conjunto de palabras totales del codigo. Si son iguales, significa que
    todas las palabras son unicas.
    """
    return len(set(codigo)) == len(codigo)


def esInstantaneo(codigo) -> bool:
    """Indica si el código es prefijo: ninguna palabra inicia otra."""
    if not esNoSingular(codigo) or any(not palabra for palabra in codigo):
        return False

    for i, palabra in enumerate(codigo):
        for j, otra in enumerate(codigo):
            if i != j and otra.startswith(palabra):
                return False
    return True


def esUnivoco(codigo) -> bool:
    '''
    Un código se dice univoco o univocamente decodificable a aquellos codigos bloque no singulares
    que puedan asegurar que su extención de orden N es no singular para cualquier valor finito de N.
    Es decir, podemos 
    Aplicando el algoritmo de Sardinas-Patterson.
    '''
    if not esNoSingular(codigo) or any(not palabra for palabra in codigo):
        return False

    palabras = set(codigo)
    residuos = set()
    for prefijo in palabras:
        for palabra in palabras:
            if palabra.startswith(prefijo) and len(palabra) > len(prefijo):
                residuos.add(palabra[len(prefijo):])

    vistos = set()
    while residuos:
        if residuos & palabras:
            return False

        estado = frozenset(residuos)
        if estado in vistos:
            return True
        vistos.add(estado)

        nuevos_residuos = set()
        for residuo in residuos:
            for palabra in palabras:
                if palabra.startswith(residuo):
                    nuevos_residuos.add(palabra[len(residuo):])
                elif residuo.startswith(palabra):
                    nuevos_residuos.add(residuo[len(palabra):])
        residuos = nuevos_residuos

    return True

def clasificarCodigo(codigo) -> str:
    if esInstantaneo(codigo):
        return "Instantaneo"
    elif esUnivoco(codigo):
        return "Univoco"
    elif esNoSingular(codigo):
        return "No Singular"
    else:
        return "Bloque"

# Unidad 3: ejercicio 9
# a
def alfabeto_codigo(codigo) -> str:
    """Devuelve los símbolos distintos que aparecen en las palabras código."""
    return "".join(sorted(set("".join(codigo))))

# b
def longitudes_palabras(codigo) -> list:
    """Devuelve la longitud de cada palabra código."""
    return [len(palabra) for palabra in codigo]

# c
def Kraft(codigo) -> float:
    """Calcula la sumatoria de Kraft usando el alfabeto código observado."""
    if not codigo:
        return 0.0

    r = len(alfabeto_codigo(codigo))

    return sum(r ** (-longitud) for longitud in longitudes_palabras(codigo))


# Unidad 3: ejercicio 11
# a (entropia a partir de probabilidades)
# b
def longmedia(codigo, probabilidades) -> float:
    """Calcula la longitud media del código."""
    return sum(probabilidad * len(palabra)
               for palabra, probabilidad in zip(codigo, probabilidades))


# Unidad 3: ejercicio 14
def esCompacto(palabras_codigo, probabilidades) -> bool:
    """Comprueba instantaneidad y el máximo ceil(I_r(s)) para cada palabra."""
    if len(palabras_codigo) != len(probabilidades):
        raise ValueError("Código y probabilidades deben tener la misma longitud.")

    if not esInstantaneo(palabras_codigo):
        return False

    r = len(alfabeto_codigo(palabras_codigo))
    if r < 2:
        return False

    for palabra, probabilidad in zip(palabras_codigo, probabilidades):
        if probabilidad > 0:
            max_longitud = math.ceil(informacion(probabilidad, r))
            if len(palabra) > max_longitud:
                return False
    return True


def generaMensaje(N, palabras_codigo, probabilidades) -> list:
    """Genera N palabras código, sorteadas según la distribución de la fuente."""
    return random.choices(palabras_codigo, weights=probabilidades, k=N)

if __name__ == "__main__":
    mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"
    alf, prob = alfabeto_y_probabilidades(mensaje)
    matriz = matrizTransicion(mensaje)
    imprimirmatriz(matriz)
    esNula = esMemoriaNula(matriz)
    print (alf, prob)
    print ("ees nula: ", esNula)
    h = entropia(prob)
    print(h)
    ext, probs = extension(alf, prob, 2)
    print(ext, probs)
    h_ext = entropia(probs)
    print(h_ext)
    


    print()