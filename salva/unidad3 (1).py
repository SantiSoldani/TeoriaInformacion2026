import math
import random





#identificar alfabeto codigo

def cantidad_info(s, base):
    """
    Calcula la cantidad de información (autoinformación) que aporta la ocurrencia
    de un símbolo dada su probabilidad, utilizando la base logarítmica especificada:
    I(s) = log_base(1 / s).

    CONTRATO:
    - PRE: 's' es un float en el rango (0, 1] que representa la probabilidad del símbolo.
           'base' es un número (int o float) > 1 para el logaritmo (e.g., 2 para bits/shannons).
    - POST: Retorna un float correspondiente a la cantidad de información aportada por el símbolo en dicha base logarítmica.

    EJEMPLO DE USO:
    >>> cantidad_info(0.5, 2)
    1.0
    >>> cantidad_info(0.25, 2)
    2.0
    """
    res = math.log(1/s, base)
    return res

def get_alfabeto_codigo(palabras_codigo):
    """
    Obtiene la lista de símbolos elementales (alfabeto del código) utilizados para
    construir el conjunto de palabras código.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de strings (list[str]) con las secuencias del código.
    - POST: Retorna una lista de strings (list[str]) con los caracteres únicos presentes en las palabras código.

    EJEMPLO DE USO:
    >>> get_alfabeto_codigo(["0", "10", "110"])
    ['0', '1']
    >>> get_alfabeto_codigo(["A", "BC", "CA"])
    ['A', 'B', 'C']
    """
    alfabeto = []
    for palabra in palabras_codigo:
        for letra in palabra:
            if letra not in alfabeto:
                alfabeto.append(letra)
    return alfabeto

#entropia de la fuente

def entropia_from_palabras_codigo(palabras_codigo, probs):
    """
    Calcula la entropía de la fuente en base 'r' (H_r(S)), donde 'r' es la cardinalidad
    del alfabeto del código: H_r(S) = sum(p_i * log_r(1 / p_i)).
    Representa la cota inferior teórica de Shannon para la longitud media de cualquier
    código unívocamente decodificable.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de strings (list[str]) a partir de la cual se obtiene
           el tamaño del alfabeto código 'r' (r >= 2). 'probs' es una lista de floats (list[float])
           con las probabilidades de los símbolos (sum(probs) == 1.0 y p_i > 0), con igual longitud
           que 'palabras_codigo'.
    - POST: Retorna un float con la entropía de la fuente calculada en base 'r'.

    EJEMPLO DE USO:
    >>> entropia_from_palabras_codigo(["0", "10", "11"], [0.5, 0.25, 0.25])
    1.5
    """
    r = len(get_alfabeto_codigo(palabras_codigo))
    return sum([prob * math.log(1/prob, r) for prob in probs])


#longitud media del codigo
def generate_longs(palabras_codigo):
    """
    Genera la lista con las longitudes asociadas a cada una de las palabras código del conjunto.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de strings (list[str]).
    - POST: Retorna una lista de enteros (list[int]) que contiene la longitud de cada palabra código en la misma posición.

    EJEMPLO DE USO:
    >>> generate_longs(["0", "10", "110"])
    [1, 2, 3]
    """
    return [len(palabra) for palabra in palabras_codigo]

def longitud_media(palabras_codigo, probs):
    """
    Calcula la longitud media esperada (L_barra) de las palabras código ponderada
    por sus probabilidades asociadas: L_barra = sum(p_i * l_i).

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de strings (list[str]) con las palabras del código.
           'probs' es una lista de floats (list[float]) con las probabilidades correspondientes
           (misma longitud que 'palabras_codigo' y sum(probs) == 1.0).
    - POST: Retorna un float correspondiente a la longitud media esperada del código.

    EJEMPLO DE USO:
    >>> longitud_media(["0", "10", "11"], [0.5, 0.25, 0.25])
    1.5
    >>> longitud_media(["00", "01", "10", "11"], [0.25, 0.25, 0.25, 0.25])
    2.0
    """
    longitudes = generate_longs(palabras_codigo)
    return sum([prob * longitud for prob, longitud in zip(probs, longitudes)])


#propiedades

def es_no_singlular(palabras_codigo):
    """
    Determina si un código es no singular comprobando que no existan palabras código repetidas
    (es decir, cada símbolo de la fuente tiene asignada una secuencia binaria/alfabética única).

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista o iterable de cadenas de texto (list[str]).
    - POST: Retorna un boolean: True si todas las palabras código son distintas entre sí
            (no singular), o False si existe al menos una palabra código repetida (singular).

    EJEMPLO DE USO:
    >>> es_no_singlular(["0", "10", "110"])
    True
    >>> es_no_singlular(["0", "10", "0"])
    False
    """
    lista_auxiliar = []

    for palabra in palabras_codigo:
        if palabra in lista_auxiliar:
            return False
        lista_auxiliar.append(palabra)
    return True


def es_instantaneo(palabras_codigo):
    """
    Verifica si un código es instantáneo (código prefijo), garantizando que ninguna
    palabra código sea prefijo de otra dentro del mismo conjunto.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de cadenas de texto (list[str]) con las palabras del código.
    - POST: Retorna un boolean: True si ninguna palabra código es prefijo de otra (es instantáneo),
            o False en caso contrario.

    EJEMPLO DE USO:
    >>> es_instantaneo(["0", "10", "110"])
    True
    >>> es_instantaneo(["0", "01", "11"])
    False
    """
    for palabra in palabras_codigo:
        for aux in palabras_codigo:
            if palabra is not aux and aux.startswith(palabra):
                return False
    return True


def es_univoco(palabras_codigo, verbose = True):
    """
    Determina si un código es unívocamente decodificable aplicando el algoritmo de Sardinas-Patterson
    mediante la generación e inspección iterativa de conjuntos de sufijos colgantes.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de cadenas de texto (list[str]) que representan el código.
    - POST: Retorna un boolean: True si el código es unívocamente decodificable, o False si existe ambigüedad
            (algún sufijo coincide con una palabra código original).

    EJEMPLO DE USO:
    >>> es_univoco(["0", "10", "110"])
    True
    >>> es_univoco(["0", "01", "011"])
    False
    """
    conjunto_inicial = set(palabras_codigo)
    conjuntos = []

    while True:
        conjunto_auxiliar = set()
        if verbose:
            print("VALORES DE CADA ITERACION DEL ALGORITMO SARDINAS-PATTERSON")
            print(f"valor del conjunto auxiliar {conjunto_auxiliar}")
            print(f"valor del conjunto inicial {conjunto_inicial}")
            print(f"conjuntos: {conjuntos}")
        for palabra in palabras_codigo:
            for item in conjunto_inicial:

                if palabra != item and palabra.startswith(item):
                    sufijo = palabra[len(item):]

                    if sufijo in palabras_codigo:
                        return False
                    conjunto_auxiliar.add(sufijo)

        if not conjunto_auxiliar:
            return True

        if conjunto_auxiliar in conjuntos:
            return True

        conjuntos.append(conjunto_auxiliar.copy())
        conjunto_inicial = conjunto_auxiliar


#es compacto

def es_compacto(palabras_codigo, probs):
    """ve
    Evalúa si un código es compacto/óptimo verificando si su longitud media alcanza
    la cota mínima entera superior de la entropía: L_barra == ceil(H_r(S)).

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista de strings (list[str]) y 'probs' es una lista
           de floats (list[float]) con las probabilidades asociadas (sum(probs) == 1.0).
    - POST: Retorna un boolean: True si la longitud media coincide con el entero techo
            de la entropía en base 'r' (ceil(H)), o False en caso contrario.

    EJEMPLO DE USO:
    >>> es_compacto(["0", "1"], [0.5, 0.5])
    True
    >>> es_compacto(["0", "10", "11"], [0.5, 0.25, 0.25])
    False
    """
    r = len(get_alfabeto_codigo(palabras_codigo))
    L = generate_longs(palabras_codigo)
    H = [cantidad_info(prob,r) for prob in probs]

    resultado = [li <= math.ceil(hi) for li,hi in zip(L,H)]
    #L = longitud_media(palabras_codigo, probs)
    #H = entropia_from_palabras_codigo(palabras_codigo, probs)
    return False not in resultado
#inecuacion de kraft

def sum_kraft(palabras_codigo):
    """
    Calcula la sumatoria de la desigualdad de Kraft-McMillan sum(r^(-l_i)) para verificar
    si un conjunto de longitudes de palabras código satisface la condición necesaria y suficiente
    de decodificabilidad unívoca / instantaneidad.

    CONTRATO:
    - PRE: 'palabras_codigo' es una lista no vacía de strings (list[str]) con las palabras código.
    - POST: Retorna un float correspondiente al valor de la sumatoria sum(r^(-l_i)), donde 'r' es el tamaño
            del alfabeto código y 'l_i' son las longitudes de cada palabra.

    EJEMPLO DE USO:
    >>> sum_kraft(["0", "10", "110", "111"])
    1.0
    """
    r = len(get_alfabeto_codigo(palabras_codigo))
    longitudes = generate_longs(palabras_codigo)

    return sum([r**(-l) for l in longitudes])


def run_pipeline(codigos, probs):
    alfabeto_codigo = get_alfabeto_codigo(codigos)
    entropia = entropia_from_palabras_codigo(codigos, probs)
    long = longitud_media(codigos,probs)
    cumple_inecuacion = sum_kraft(codigos)
    no_singular = es_no_singlular(codigos)
    if(no_singular):
        univoco = es_univoco(codigos)
        if univoco:
            instantaneo = es_instantaneo(codigos)
            if instantaneo:
                compacto = es_compacto(codigos, probs)
            else:
                compacto = False
        else:
            instantaneo = False
            compacto = False
    else:
        univoco = False
        instantaneo = False
        compacto = False


    print(f"el alfabeto codigo es: {alfabeto_codigo}")
    print(f"la entropia de la fuente es: {entropia}")
    print(f"la longitud media es: {long}")
    print(f"cumple la inecuacion de kraft: {cumple_inecuacion}")
    print(f"es univoco: {univoco}")
    print(f"es no singular: {no_singular}")
    print(f"es instantaneo: {instantaneo}")
    print(f"es compacto: {compacto}")

#run_pipeline(["0", "1", "20", "21","22"],[0.40, 0.30, 0.15, 0.10, 0.05])
