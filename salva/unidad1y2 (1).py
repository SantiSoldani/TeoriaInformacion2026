import math
import random
#FUNCIONES UTILIZADAS PARA LA RESOLUCION DEL PARCIAL

#determinar el alfabeto y las probabilidades de sus simbolos

def get_alfabetoYprobs(mensaje):
    """
        PARAMS:
            mensaje:str --> mensaje emitido por una fuente sin memoria
        POST:
            alfabeto : list[char] -> alfabeto del mensaje
            probs: list[float] --> arreglo paralelo con las probabilidades de aparicion de cada simbolo del alfabeto
    """
    alfabeto = get_alfabeto_from_MSJ(mensaje)
    tamanio = len(mensaje)
    apariciones = {}
    for letra in mensaje:
        apariciones[letra] = apariciones.get(letra,0) + 1
    probs = []
    for aparicion, (letra, conteo) in enumerate(apariciones.items()):
        #print(conteo)
        #print(tama/conteo)
        probs.append(conteo/tamanio)
    #print(tamanio)
    return alfabeto,probs

def get_alfabetoYprobs2(mensaje):

    alfabeto = get_alfabeto_from_MSJ(mensaje)
    tamanio = len(mensaje)
    probs = []

    for letra in alfabeto:
        probs.append(mensaje.count(letra) / tamanio)

    return alfabeto,probs

def get_alfabeto_from_MSJ(mensaje):
    """
    Extrae el conjunto de símbolos únicos (alfabeto) que componen un mensaje
    y los devuelve ordenados alfabéticamente.

    CONTRATO:
    - PRE: 'mensaje' es una string (str) de símbolos generados por la fuente.
    - POST: Retorna una lista ordenada alfabéticamente de strings (list[str]) con los caracteres únicos que conforman dicho alfabeto.

    EJEMPLO DE USO:
    >>> get_alfabeto_from_MSJ("abracadabra")
    ['a', 'b', 'c', 'd', 'r']
    """
    alfabeto = []
    for caracter in mensaje:
        if caracter not in alfabeto:
            alfabeto.append(caracter)

    return sorted(alfabeto)


#PUNTO B


def get_matriz(mensaje):
    """
    Construye la matriz de probabilidades de transición / digramas condicionales para todos
    los pares de símbolos presentes en el alfabeto del mensaje.

    CONTRATO:
    - PRE: 'mensaje' es una string (str) no vacía de símbolos emitidos por la fuente.
    - POST: Retorna una matriz (list[list[float]]) donde cada fila 'i' y columna 'j' representa
            la frecuencia observada del par (simbolo_i, simbolo_j) en el mensaje.

    EJEMPLO DE USO:
    >>> get_matriz("ABA")
    [[0.0, 0.3333333333333333], [0.3333333333333333, 0.0]]
    """
    alfabeto = get_alfabeto_from_MSJ(mensaje)
    matriz = []
    for simboloJ in alfabeto:
        fila = []
        for simboloI in alfabeto:
            fila.append(get_probabilidad_conMemoria(simboloI, simboloJ, mensaje)) #P(simboloJ / simboloI)
        matriz.append(fila)
        print(fila)

    return matriz



def get_probabilidad_conMemoria(letraI, letraS, mensaje):
    """
    Calcula la frecuencia relativa con la que aparece un par ordenado de caracteres consecutivos
    (letraI seguido inmediatamente de letraS) a lo largo de un mensaje.

    CONTRATO:
    - PRE: 'letraI' es un str (carácter inicial), 'letraS' es un str (carácter sucesor),
           y 'mensaje' es un str con longitud >= 2.
    - POST: Retorna un float in [0.0, 1.0] correspondiente a la proporción de apariciones del par consecutivo
            (letraI, letraS) respecto de la cantidad total de caracteres evaluados.

    EJEMPLO DE USO:
    >>> get_probabilidad_conMemoria('A', 'B', "ABABA")
    0.4
    """
    apariciones = 0
    coincidencias = 0
    i = 0
    while(i < len(mensaje)):
        if mensaje[i] == letraI and i!=len(mensaje) - 1:
            apariciones+=1
            if (i+1 < len(mensaje)) and mensaje[i+1] == letraS:
                coincidencias +=1
        i+=1

    return coincidencias / apariciones



#PUNTO C


def es_memoria_nula(matriz, tolerancia):
    """
    Determina si una matriz de transiciones representa una fuente de memoria nula,
    verificando si todas las filas son equivalentes entre sí dentro de un margen de tolerancia.

    CONTRATO:
    - PRE: 'matriz' es una lista de listas de floats (list[list[float]]) y 'tolerancia'
           es un float > 0 que indica la diferencia máxima permitida entre probabilidades.
    - POST: Retorna un boolean: True indicando que las probabilidades transicionales coinciden
            (fuente sin memoria), o False si las probabilidades difieren (fuente con memoria).

    EJEMPLO DE USO:
    >>> es_memoria_nula([[0.5, 0.5], [0.5, 0.5]], 0.01)
    True
    >>> es_memoria_nula([[0.8, 0.2], [0.3, 0.7]], 0.01)
    False
    """
    for i in range(len(matriz)):
        for j in range(len(matriz)-1):
            if(abs(matriz[i][j] - matriz[i][j+1] > tolerancia)):
                return False

    return True
#PUNTO D

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

def entropia_Sin_memoria(fuente, r=2):
    """
    Calcula la entropía media (en bits/símbolo) de una fuente de información discreta
    y sin memoria (de orden cero), a partir de las probabilidades individuales de sus símbolos:
    H(S) = sum(p_i * log2(1 / p_i)).

    CONTRATO:
    - PRE: 'fuente' es una lista de floats (list[float]) donde cada elemento representa
           la probabilidad p_i en (0, 1] de un símbolo de la fuente y la suma total es 1.0.
    - POST: Retorna un float con la entropía media (base 2) esperada de esa fuente asumiendo memoria nula.

    EJEMPLO DE USO:
    >>> entropia_Sin_memoria([0.5, 0.5])
    1.0
    >>> entropia_Sin_memoria([0.5, 0.25, 0.25])
    1.5
    """
    resultado = 0
    for suceso in fuente:
        if suceso > 0:
            i = cantidad_info(suceso, r)
            resultado += suceso * i
    return resultado




def get_vector_estacionario(matriz):

    vector_estacionario = [1/len(matriz)] * len(matriz)
    for i in range(100):
        vector_auxiliar = [0] * len(matriz)
        for j in range(len(matriz)):
            suma = 0
            for k in range(len(matriz)):
                suma += vector_estacionario[k] * matriz[j][k]
            vector_auxiliar[j] = suma
        print(sum(vector_estacionario))
        diff = max([abs(vector_estacionario[k] - vector_auxiliar[k]) for k in range(len(matriz))])
        if(diff < 0.001):
            break
        vector_estacionario = vector_auxiliar.copy()

    return vector_estacionario

def entropia_fuente_markoviana(vector_estacionario, matriz, base):
    """
    Calcula la entropía por símbolo (en bits/símbolo) de una fuente de información markoviana
    estacionaria: H(S) = sum_i P(s_i) * sum_j P(s_j|s_i) * log2(1 / P(s_j|s_i)).

    CONTRATO:
    - PRE: 'vector_estacionario' es una list[float] con las probabilidades del estado estacionario
           y 'matriz' condicional es list[list[float]] con las probabilidades de transición P(s_j|s_i) >= 0.
    - POST: Retorna un float con el valor de la entropía promedio estacionaria total de la fuente con memoria en bits.

    EJEMPLO DE USO:
    >>> vector_est = [0.5, 0.5]
    >>> matriz_trans = [[0.8, 0.2], [0.2, 0.8]]
    >>> entropia_fuente_markoviana(vector_est, matriz_trans)
    0.7219280948873623
    """
    entropia = 0

    for i in range(len(vector_estacionario)):
        for j in range(len(matriz[i])):
            if matriz[j][i] > 0 and vector_estacionario[i] > 0:
                entropia += vector_estacionario[i] * matriz[j][i] * math.log((1 / matriz[j][i]), base)
    return entropia

#PUNTO E

def extension_probs(alfabeto, distribucion, n):
    """
    Calcula la extensión de orden 'n' de una fuente de memoria nula, generando todas las
    combinaciones posibles de palabras de longitud 'n' y sus probabilidades compuestas asociadas.

    CONTRATO:
    - PRE: 'alfabeto' es list[str], 'distribucion' es list[float] de la fuente original (mismo largo que 'alfabeto'),
           y 'n' es int > 0 para el orden de extensión.
    - POST: Retorna una tupla (nuevo_alfabeto, nueva_distribucion) de las listas combinatorias calculadas en orden extensión n.

    EJEMPLO DE USO:
    >>> extension_probs(['A', 'B'], [0.7, 0.3], 2)
    (['AA', 'AB', 'BA', 'BB'], [0.49, 0.21, 0.21, 0.09])
    """
    if n == 1:
        return alfabeto.copy(), distribucion.copy()
    else:
        prox = extension_probs(alfabeto, distribucion, n-1)
        alfabeto_prox = prox[0]
        distribucion_prox = prox[1]
        resAlf = []
        resDist = []
        for item, prob in zip(alfabeto_prox, distribucion_prox):
            for simbolo, dist in zip(alfabeto, distribucion):
                resAlf.append(item + simbolo)
                resDist.append(prob*dist)
        return resAlf, resDist


def entropia_SN_probs(probs, r):
    return sum([prob * math.log(1/prob,r) for prob in probs])

def testcase(mensaje):

    print(f"test del mensaje {mensaje}")
    #a
    call = get_alfabetoYprobs2(mensaje)
    alfabeto = call[0]
    probs = call[1]
    print(f"alfabeto = {alfabeto} \n probs = {probs}\n")

    #b
    matriz = get_matriz(mensaje)
    imprimir_matriz(matriz, alfabeto)

    #c

    if(es_memoria_nula(matriz,0.08)):
        print("es memoria nula")
        print(f"entropia de la funente = {entropia_Sin_memoria(probs)}")
        extension = extension_probs(alfabeto, probs, 2)
        print(f"alfabeto de la extension = {extension[0]}")
        print(f"probabilidades de la extension = {extension[1]}")

        entropia = entropia_SN_probs(extension[1], 2)
        print(f"entro[ia de la extension = {entropia}")
    else:
        print("es memoria no nula")
        vector = get_vector_estacionario(matriz)
        print(f"entropia de la fuente = {entropia_fuente_markoviana(vector, matriz,2)}")
        print(f"vector estacionario = ", [round(valor,2) for valor in vector])


def imprimir_matriz(matriz, alfabeto):

    print(letra for letra in alfabeto)
    columnas = [0] * len(matriz)
    print(str(alfabeto))
    for i in range(len(matriz)):
        print("fila:", [round(elem,2) for elem in matriz[i]])
        for j in range(len(matriz[i])):
            columnas[j] += matriz[i][j]
    print(f"sumas: {columnas}")

#testcase(".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::.")
#testcase(")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])")

#testcase("bcacaacababbabaaaaaabaaccbbaacbabbbcabaabcbacbbbacbbacaacccaaabbcaabccaacababcccbabacacaaabaaaaaabab")
testcase("wxwywxyxwzyyzyxwzyzyzzwyzxwxyzwxwxyyxyxyxwxwxyzxwxzyzwwzyxwx")
