"""
Toolkit Integral de Teoría de la Información y la Comunicación (Primer Parcial)
Facultad de Ingeniería - Universidad Nacional de Mar del Plata (UNMdP)

Cubre completamente los contenidos de:
- TP1: Información, entropía de eventos, fuentes sin memoria.
- TP2: Fuentes de memoria nula, extensiones, fuentes de Markov, ergodicidad, entropía markoviana.
- TP3: Propiedades de códigos (bloque, no singular, instantáneo, Sardinas-Patterson),
       Kraft-McMillan, longitud media, eficiencia, codificación de Huffman y códigos compactos.
"""

import math
import random
# Solo math y random: son las únicas librerías permitidas en el parcial.


# ==============================================================================
# SECCIÓN 1: INFORMACIÓN, ENTROPÍA Y FUENTES DE MEMORIA NULA (TP1 y TP2)
# ==============================================================================

def cantidad_informacion(prob, base=2):
    """
    Cantidad de información de un suceso E: I(E) = log_r(1/P(E)).
    Mide cuánta incertidumbre se elimina cuando ocurre E: cuanto menos probable es
    el suceso, más información aporta; un suceso seguro (P = 1) aporta 0.
    Base 2 = bits.
    """
    if prob <= 0:
        return float('inf')
    if prob >= 1.0:
        return 0.0
    return math.log(1.0 / prob, base)
# INTERPRETACIÓN:
#   I(E) = log_r(1/P(E)) (Unidad 1). Para la materia, información es todo evento con
#   cierto grado de INCERTIDUMBRE: mide cuánto se reduce la incertidumbre del receptor
#   cuando ocurre E (no importa el significado del mensaje).
#   - Relación inversa: si P(s1) >= P(s2) entonces I(s1) <= I(s2). Un evento muy
#     seguro aporta poca información y uno sorpresivo aporta mucha.
#   - P = 1 -> I = 0: evento seguro. Si el receptor ya lo conoce con certeza antes de
#     que llegue, no hay incertidumbre que reducir y no aporta información.
#   - P = 1/2 -> I = 1 bit (la unidad): elegir entre dos opciones equiprobables.
#   - No negatividad: I >= 0 siempre, porque 0 <= P <= 1.
#   - Aditividad: I(s1,s2) = I(s1) + I(s2) SOLO si s1 y s2 son independientes.
#   - Unidad según la base: r=2 bits, r=e nats, r=10 hartleys.
#   - bit != binit: el bit es la unidad de información y el binit es un dígito binario
#     en memoria. Ej. dado: I = 2.58 bits, pero hacen falta 3 binits enteros.


def entropia_fuente(probabilidades, base=2):
    """
    Entropía de una fuente de memoria nula: H(S) = Σ P(si)·log_r(1/P(si)).
    Es la información promedio que aporta cada símbolo de la fuente: a la
    información de cada símbolo, I(si) = log_r(1/P(si)), se la multiplica por su
    probabilidad y se suman todas.
    """
    h = 0.0
    for p in probabilidades:
        if p > 0:
            h += p * math.log(1.0 / p, base)
    return h
# INTERPRETACIÓN:
#   H(S) = Σ P(si)·log_r(1/P(si)) (Unidad 2). Se puede interpretar como:
#   - el valor medio de la información por símbolo que suministra la fuente;
#   - el valor medio de la incertidumbre de un observador ANTES de conocer la salida;
#   - la cantidad media de binits necesarios para representar cada símbolo.
#   Propiedades (fuente de memoria nula con n símbolos):
#   - 0 <= H(S) <= log(n).
#   - H(S) = 0 si y solo si un símbolo tiene P = 1 y los demás P = 0 (no hay incertidumbre).
#   - H(S) = log(n) si y solo si todos tienen P = 1/n (máxima incertidumbre).
#   - Es continua y simétrica (no importa el orden de las probabilidades).
#   - No tiene por qué ser un número entero de bits.


def entropia_binaria(w):
    """
    Entropía de una fuente binaria de memoria nula con probabilidades w y 1-w:
    H(w) = w·log2(1/w) + (1-w)·log2(1/(1-w)).
    Vale 1 bit (máximo) en w = 0.5 y 0 bits en w = 0 o w = 1.
    """
    if w < 0 or w > 1:
        raise ValueError("La probabilidad w debe estar en el intervalo [0, 1].")
    if w == 0.0 or w == 1.0:
        return 0.0
    return -(w * math.log2(w) + (1.0 - w) * math.log2(1.0 - w))
# INTERPRETACIÓN:
#   Fuente binaria de memoria nula S = {0,1} con P = {w, 1-w}:
#   H(w) = w·log(1/w) + (1-w)·log(1/(1-w)).
#   - Máximo de 1 bit en w = 0.5: los dos símbolos son equiprobables y no hay forma
#     de predecir cuál sale.
#   - H = 0 en w = 0 o w = 1: siempre sale el mismo símbolo y no hay incertidumbre.
#   - Es simétrica: H(w) = H(1-w). Por eso w = 0.25 y w = 0.75 dan lo mismo (0.81 bits).


def entropia_maxima(n, base=2):
    """
    Entropía máxima de una fuente de n símbolos: H_max = log_r(n).
    Es la entropía que tiene la fuente cuando todos sus símbolos son
    equiprobables (P = 1/n).
    """
    if n <= 0:
        raise ValueError("La cantidad de símbolos n debe ser mayor a 0.")
    return math.log(n, base)
# INTERPRETACIÓN:
#   H_max = log(n): es la cota superior de la entropía de una fuente de n símbolos
#   (propiedad 1: 0 <= H(S) <= log(n)). Se alcanza si y solo si todos los símbolos
#   son equiprobables (P = 1/n). Cuanto más desbalanceadas las probabilidades, más
#   predecible la fuente y más lejos de este máximo. Ej: 4 símbolos -> 2 bits.


def analizar_cadena_fuente(cadena):
    """
    A partir de un mensaje obtiene el alfabeto de la fuente y la probabilidad de
    cada símbolo por frecuencia relativa:
    P(s) = veces que aparece s / cantidad total de símbolos del mensaje.
    """
    total = len(cadena)
    if total == 0:
        raise ValueError("La cadena no puede estar vacía.")
    conteo = {}
    for c in cadena:
        conteo[c] = conteo.get(c, 0) + 1
    alfabeto = sorted(conteo.keys())
    probabilidades = [conteo[c] / total for c in alfabeto]
    return alfabeto, probabilidades
# INTERPRETACIÓN:
#   Estima las probabilidades por FRECUENCIA RELATIVA: P(s) = apariciones de s / largo
#   del mensaje. En el parcial conviene escribirlo con los números (ej. P(A) = 21/50).
#   - Son estimaciones: cuanto más largo el mensaje, más se parecen a las reales.
#   - Siempre suman 1.
#   - El símbolo más frecuente es el que aporta MENOS información al aparecer.


def simular_fuente_memoria_nula(alfabeto, probabilidades, n):
    """
    Genera un mensaje de n símbolos emitido por una fuente de memoria nula: cada
    símbolo se elige según su probabilidad, independientemente de los anteriores.
    """
    return ''.join(random.choices(alfabeto, weights=probabilidades, k=n))
# INTERPRETACIÓN:
#   En una fuente de memoria nula cada símbolo es estadísticamente independiente de
#   los anteriores, así que se elige al azar según su probabilidad sin mirar lo que
#   salió antes. Con N grande, las frecuencias del mensaje generado se parecen a
#   las probabilidades dadas. Cada corrida da un mensaje distinto.


def extension_fuente(alfabeto, probabilidades, orden_n):
    """
    Extensión de orden n de una fuente de memoria nula (S^n).
    Sus símbolos son todas las secuencias de n símbolos de S (q^n en total). La
    probabilidad de cada una es el producto de las probabilidades de los símbolos
    que la forman, porque son independientes. Devuelve también su entropía, que
    cumple H(S^n) = n·H(S).
    """
    palabras = ['']
    for _ in range(orden_n):
        palabras = [pal + s for pal in palabras for s in alfabeto]
    prob_dict = dict(zip(alfabeto, probabilidades))
    
    probs = []
    for pal in palabras:
        p = 1.0
        for ch in pal:
            p *= prob_dict[ch]
        probs.append(p)
    
    entropia_ext = entropia_fuente(probs, base=2)
    return palabras, probs, entropia_ext
# INTERPRETACIÓN:
#   Extensión de orden n (S^n): fuente de memoria nula cuyo alfabeto tiene q^n
#   símbolos, uno por cada secuencia de n símbolos de S (todas las combinaciones).
#   - P(σi) = Pi1·Pi2·...·Pin: se multiplican porque cada símbolo es
#     estadísticamente independiente. Las probabilidades de S^n suman 1.
#   - H(S^n) = n·H(S): cada símbolo de S^n equivale a n símbolos de S, así que lleva
#     n veces la información. Agrupar no crea ni pierde información.


# ==============================================================================
# SECCIÓN 2: FUENTES CON MEMORIA Y CADENAS DE MARKOV (TP2)
# ==============================================================================

def matriz_transicion(cadena):
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


def es_fuente_memoria_nula(matriz_transicion, tolerancia=0.05):
    """
    Decide si la fuente es de memoria nula: lo es si la probabilidad del símbolo
    siguiente no depende del anterior, es decir, si en cada fila de la matriz de
    transición (formato cátedra) todos los valores son iguales dentro de una
    tolerancia: máximo - mínimo <= tolerancia.
    """
    for fila in matriz_transicion:
        if max(fila) - min(fila) > tolerancia:
            return False
    return True
# INTERPRETACIÓN:
#   Memoria nula = cada símbolo es estadísticamente independiente de los anteriores,
#   o sea que P(si | anterior) no depende del anterior. En la matriz de la cátedra
#   eso se ve en que cada FILA tiene todos sus valores iguales. Como la matriz sale de un mensaje
#   finito nunca da exactamente igual, por eso se usa una TOLERANCIA.
#   EN EL PARCIAL: decir qué tolerancia se usó y qué se comparó.


def es_cadena_ergodica(matriz_transicion, estocastica_por="filas"):
    """
    Decide si una fuente de Markov es ergódica: desde cualquier estado se puede
    llegar a cualquier otro (todos los estados son alcanzables entre sí).
    Solo en ese caso existe un vector estacionario único.
    """
    P = matriz_transicion
    if estocastica_por == "columnas":
        P = [list(col) for col in zip(*P)]
    n = len(P)
    
    for inicio in range(n):
        visitados = set()
        pila = [inicio]
        while pila:
            actual = pila.pop()
            if actual not in visitados:
                visitados.add(actual)
                for vecino in range(n):
                    if P[actual][vecino] > 1e-9 and vecino not in visitados:
                        pila.append(vecino)
        if len(visitados) < n:
            return False
    return True
# INTERPRETACIÓN:
#   Ergódica: todos los estados son alcanzables entre sí (y hay un conjunto finito de
#   estados). Una fuente ergódica, observada un tiempo suficientemente largo, emite
#   con probabilidad 1 una secuencia "típica", y tiene una distribución estacionaria
#   ÚNICA que no depende de las condiciones iniciales.
#   - NO ergódica: hay estados de los que no se puede salir (ej. TP2 17a: el estado 3
#     tiene un lazo con P = 1). Lo que pasa a largo plazo depende de dónde arranca, y
#     no se calcula vector estacionario ni entropía.


def vector_estacionario(matriz_transicion, estocastica_por="filas", n_iter=10000):
    """
    Vector estacionario V* de una fuente de Markov: la probabilidad de cada estado
    a largo plazo, cuando la fuente se estabiliza. Se obtiene resolviendo
    V* = M·V* junto con la condición Σ vi = 1.
    """
    P = matriz_transicion
    if estocastica_por == "columnas":
        P = [list(col) for col in zip(*P)]

    n = len(P)

    A = []
    for j in range(n):
        fila = [P[i][j] - (1.0 if i == j else 0.0) for i in range(n)]
        A.append(fila + [0.0])
    A[n - 1] = [1.0] * n + [1.0]

    unica = True
    for col in range(n):
        piv = max(range(col, n), key=lambda f: abs(A[f][col]))
        if abs(A[piv][col]) < 1e-12:
            unica = False
            break
        A[col], A[piv] = A[piv], A[col]
        for f in range(n):
            if f != col:
                factor = A[f][col] / A[col][col]
                A[f] = [a - factor * b for a, b in zip(A[f], A[col])]

    if unica:
        pi = [A[i][n] / A[i][i] for i in range(n)]
        return [max(0.0, x) for x in pi]

    pi = [1.0 / n] * n
    acumulado = [0.0] * n
    for _ in range(n_iter):
        nuevo = [0.0] * n
        for j in range(n):
            for i in range(n):
                nuevo[j] += pi[i] * P[i][j]
        pi = nuevo
        acumulado = [a + x for a, x in zip(acumulado, pi)]
    s = sum(acumulado)
    return [a / s for a in acumulado]
# INTERPRETACIÓN:
#   V* = distribución de probabilidades a la que se estabiliza la fuente después de
#   emitir muchos símbolos (estado estacionario). Es la proporción de veces que
#   aparece cada símbolo a largo plazo.
#   - Se obtiene de V* = M·V*, o sea (M - I)·V* = 0, junto con Σ vi = 1.
#   - Existe y es única si la fuente es ergódica, y es independiente de las
#     condiciones iniciales.
#   - Se usa para ponderar la entropía de cada estado en H1.


def entropia_markov(matriz_transicion, pi=None, estocastica_por="filas"):
    """
    Entropía de una fuente de Markov: H = Σ p*_i · H(estado i).
    A la entropía de lo que puede salir después de cada estado se la multiplica
    por la probabilidad estacionaria de estar en ese estado, y se suman todas.
    """
    P = matriz_transicion
    if estocastica_por == "columnas":
        P = [list(col) for col in zip(*P)]
        
    n = len(P)
    if pi is None:
        pi = vector_estacionario(P, estocastica_por="filas")
        
    h_fuente = 0.0
    for i in range(n):
        h_estado = 0.0
        for j in range(n):
            p_ij = P[i][j]
            if p_ij > 0:
                h_estado -= p_ij * math.log2(p_ij)
        h_fuente += pi[i] * h_estado
    return h_fuente
# INTERPRETACIÓN:
#   H1 = Σ_i p*_i · Σ_j p(j|i)·log(1/p(j|i)) (Unidad 2): la incertidumbre de lo que
#   sale después de cada estado, ponderada por la probabilidad estacionaria de estar
#   en ese estado. Es la información media por símbolo TENIENDO EN CUENTA la memoria.
#   Es menor o igual a la entropía calculada solo con las probabilidades de los
#   símbolos: conocer el símbolo anterior ayuda a predecir el siguiente, así que la
#   memoria REDUCE la incertidumbre.


def simular_cadena_markov(matriz_transicion, alfabeto, n, inicial=None, estocastica_por="filas"):
    """
    Genera un mensaje de n símbolos emitido por una fuente de Markov: cada símbolo
    se elige según las probabilidades condicionales del símbolo anterior.
    """
    P = matriz_transicion
    if estocastica_por == "columnas":
        P = [list(col) for col in zip(*P)]
    
    indice = {s: i for i, s in enumerate(alfabeto)}
    actual = inicial if inicial is not None else random.choice(alfabeto)
    resultado = [actual]
    
    for _ in range(n - 1):
        fila_prob = P[indice[actual]]
        siguiente = random.choices(alfabeto, weights=fila_prob)[0]
        resultado.append(siguiente)
        actual = siguiente
        
    return ''.join(resultado)
# INTERPRETACIÓN:
#   Fuente con memoria: la probabilidad de cada símbolo depende del anterior, así que
#   se elige según las probabilidades condicionales del estado actual. El mensaje
#   tiene patrones (el anterior condiciona al siguiente). Si la fuente es ergódica y
#   N es grande, las frecuencias se acercan al vector estacionario.


# ==============================================================================
# SECCIÓN 3: PROPIEDADES DE CÓDIGOS Y SARDINAS-PATTERSON (TP3 & Práctica 4)
# ==============================================================================

def obtener_alfabeto_codigo(codigos):
    """
    Alfabeto código X: los símbolos distintos con los que se forman las palabras
    código, y r = cantidad de símbolos de X (la base del código).
    """
    simbolos = sorted(set(''.join(codigos)))
    return simbolos, len(simbolos)
# INTERPRETACIÓN:
#   X = {x1, ..., xr} es el ALFABETO CÓDIGO: los símbolos con los que se arman las
#   palabras código (S es el alfabeto fuente). r = cantidad de símbolos de X, y es
#   la base del logaritmo en H_r(S) y de Kraft (Σ r^-Li).
#   EN EL PARCIAL: decir qué es X, cuáles son sus símbolos y cuánto vale r.
#   Ojo: si el enunciado da un alfabeto con símbolos que no aparecen en las
#   palabras, pasar r a mano.


def es_codigo_bloque(codigos):
    """
    Decide si todas las palabras código tienen la misma longitud.
    OJO: la cátedra llama "bloque" a todo código que asigna una palabra fija a cada
    símbolo fuente, así que para ella todo código es bloque.
    """
    if not codigos:
        return True
    longitud = len(codigos[0])
    return all(len(c) == longitud for c in codigos)
# INTERPRETACIÓN:
#   OJO: esta función usa "bloque = todas las palabras del mismo largo", que NO es la
#   definición de la cátedra. Cátedra (Unidad 3): código bloque = a cada símbolo fuente
#   se le asigna una secuencia FIJA de símbolos de X (la palabra código). Con esa
#   definición todo código es bloque. Permite codificar pero puede no permitir
#   decodificar (ej. si dos símbolos comparten la misma palabra).
#   En las respuestas, "Bloque" = singular (es la clase más amplia).


def es_no_singular(codigos):
    """
    Decide si el código es no singular: todas sus palabras código son distintas
    entre sí.
    """
    return len(set(codigos)) == len(codigos)
# INTERPRETACIÓN:
#   No singular = todas las palabras código son distintas, así que cada símbolo
#   suelto se identifica sin ambigüedad. NO alcanza para garantizar la decodificación
#   de una secuencia. Ej. de la teoría: {0, 11, 00, 01}: "0011" puede ser S3 S2 o
#   S1 S1 S2.


def es_instantaneo(codigos):
    """
    Decide si el código es instantáneo: ninguna palabra código es prefijo de otra.
    Devuelve también los pares (prefijo, palabra) que lo impiden.
    """
    conflictos = []
    n = len(codigos)
    for i in range(n):
        for j in range(n):
            if i != j and codigos[j].startswith(codigos[i]):
                conflictos.append((codigos[i], codigos[j]))
    return len(conflictos) == 0, conflictos
# INTERPRETACIÓN:
#   Instantáneo = permite recuperar las palabras de una secuencia sin conocer los
#   símbolos que vienen después (se reconoce cada palabra apenas termina).
#   Condición necesaria y suficiente: ninguna palabra es PREFIJO de otra.
#   Instantáneo => unívoco. Los conflictos listados son los pares
#   (prefijo, palabra más larga) que impiden que sea instantáneo.


def sardinas_patterson(codigos, verbose=False):
    """
    Algoritmo de Sardinas-Patterson: decide si el código es unívocamente
    decodificable buscando sufijos que coincidan con palabras del código.
    OJO: acá S1 son los primeros sufijos; la cátedra llama S1 = C
    (ver sardinas_patterson_catedra).
    """
    if len(codigos) != len(set(codigos)):
        if verbose:
            print("El código es singular (contiene palabras duplicadas) -> NO es UD.")
        return False, []

    C = set(codigos)
    historial = []
    
    S1 = set()
    for x in C:
        for y in C:
            if x != y and y.startswith(x):
                residuo = y[len(x):]
                if residuo:
                    S1.add(residuo)
                    
    historial.append(S1)
    if verbose:
        print(f"S_1 = {S1}")
        
    if not S1:
        return True, historial
    
    i = 0
    while True:
        Si = historial[i]
        
        interseccion = Si.intersection(C)
        if interseccion:
            if verbose:
                print(f"Conflicto en S_{i+1}: contiene palabras de C: {interseccion}")
            return False, historial
        
        if not Si:
            if verbose:
                print(f"S_{i+1} está vacío -> Es UD.")
            return True, historial
        
        if Si in historial[:i]:
            if verbose:
                print(f"Ciclo detectado en S_{i+1} -> Es UD.")
            return True, historial
            
        S_next = set()
        for u in Si:
            for c in C:
                if c.startswith(u) and c != u:
                    S_next.add(c[len(u):])
                if u.startswith(c) and u != c:
                    S_next.add(u[len(c):])
                if c == u:
                    if verbose:
                        print(f"Palabra de C coincide exactamente con residuo '{u}' -> NO es UD.")
                    return False, historial
                    
        historial.append(S_next)
        i += 1
        if verbose:
            print(f"S_{i+1} = {S_next}")
# INTERPRETACIÓN:
#   Verifica si el código es unívocamente decodificable (UD): genera los SUFIJOS que
#   sobran cuando una palabra es prefijo de otra, para detectar ambigüedades.
#   - Si aparece una palabra de C entre los sufijos -> NO es UD (hay una secuencia
#     que se puede leer de dos formas).
#   - Si un conjunto se vacía o se repite (ciclo seguro) -> ES UD.
#   OJO: acá S_1 son los primeros sufijos, pero la cátedra llama S1 = C. Para el
#   parcial usar sardinas_patterson_catedra.


def sumatoria_kraft(codigos, r=None):
    """
    Suma de Kraft-McMillan: Σ r^(-Li), donde Li es la longitud de cada palabra
    código y r la cantidad de símbolos del alfabeto código.
    """
    if r is None:
        _, r = obtener_alfabeto_codigo(codigos)
    if r <= 1:
        r = 2
    return sum(r ** (-len(c)) for c in codigos)
# INTERPRETACIÓN:
#   K = Σ r^(-Li): solo depende de las LONGITUDES de las palabras, no de las palabras
#   en sí. Mide cuánto del "espacio" de palabras posibles usa el código (las palabras
#   cortas ocupan mucho).


def cumple_kraft(codigos, r=None, tol=1e-9):
    """
    Verifica la inecuación de Kraft-McMillan: Σ r^(-Li) <= 1.
    Si se cumple, existe al menos un código instantáneo con esas longitudes; si no
    se cumple, no existe ningún código unívoco con esas longitudes.
    """
    k = sumatoria_kraft(codigos, r)
    return k <= (1.0 + tol), k
# INTERPRETACIÓN:
#   Kraft (Unidad 3): Σ r^-Li <= 1 es condición SUFICIENTE para que exista AL MENOS
#   UN código instantáneo con esas longitudes.
#   McMillan: también es condición NECESARIA y suficiente para que exista un código
#   unívoco con esas longitudes. Si el código es unívoco, cumple Kraft.
#   - K > 1 -> es imposible un código unívoco (ni instantáneo) con esas longitudes.
#   - K <= 1 -> NO asegura que ESTE código sea instantáneo: es una condición
#     cuantitativa. Hay que verificar la condición de prefijo o usar S-P.
#     Ej. de la teoría: {0, 100, 110, 11} da K = 1 pero no es instantáneo.


def longitud_media(codigos, probabilidades):
    """
    Longitud media del código: L = Σ Pi·Li.
    A la longitud de cada palabra código se la multiplica por la probabilidad de
    su símbolo y se suman todas.
    """
    if len(codigos) != len(probabilidades):
        raise ValueError("Las listas de códigos y probabilidades deben tener la misma longitud.")
    return sum(p * len(c) for p, c in zip(probabilidades, codigos))
# INTERPRETACIÓN:
#   L = Σ P(Si)·Li: promedio de las longitudes de las palabras ponderadas por sus
#   probabilidades. Es la cantidad media de símbolos de X que se usan por cada
#   símbolo de la fuente. Regla: "cuanto más breve, mejor", porque afecta al
#   almacenamiento y a la velocidad de transmisión.
#   Para todo código unívoco: H_r(S) <= L (la entropía es el piso).


def eficiencia_y_redundancia(codigos, probabilidades, r=None):
    """
    Eficiencia del código: η = H_r(S) / L, qué tan cerca está la longitud media
    del mínimo teórico H_r(S). Redundancia = 1 - η.
    """
    if r is None:
        _, r = obtener_alfabeto_codigo(codigos)
    if r <= 1:
        r = 2
        
    h_r = entropia_fuente(probabilidades, base=r)
    l_med = longitud_media(codigos, probabilidades)
    
    if l_med == 0:
        return 0.0, 0.0, h_r, l_med
        
    eta = h_r / l_med
    redundancia = 1.0 - eta
    return eta, redundancia, h_r, l_med
# INTERPRETACIÓN:
#   η = H_r(S) / L: qué tan cerca está L del límite teórico H_r(S).
#   - η = 1 (100%) solo si L = H_r(S), o sea Li = log_r(1/Pi), lo que exige que las
#     probabilidades sean potencias enteras de 1/r (ej. P = 1/4 con r = 2 -> Li = 2).
#   - Redundancia = 1 - η: la parte de la longitud que no lleva información.


# ==============================================================================
# SECCIÓN 4: ALGORITMO DE HUFFMAN Y CÓDIGOS COMPACTOS (TP3)
# ==============================================================================

class _NodoHuffman:
    def __init__(self, peso, simbolo=None, hijos=None):
        self.peso = peso
        self.simbolo = simbolo
        self.hijos = hijos or []

    def __lt__(self, other):
        return self.peso < other.peso


def huffman(probabilidades, simbolos=None, r=2, alfabeto_codigo=None):
    """
    Código de Huffman: construye un código instantáneo de longitud media mínima
    (compacto) juntando repetidamente los r símbolos menos probables. Los símbolos
    más probables quedan con las palabras más cortas.
    """
    n = len(probabilidades)
    if simbolos is None:
        simbolos = [f"s{i+1}" for i in range(n)]
        
    if alfabeto_codigo is None:
        alfabeto_codigo = [str(i) for i in range(r)]
    elif len(alfabeto_codigo) != r:
        raise ValueError(f"El alfabeto código debe tener exactamente {r} símbolos.")
        
    probs_trabajo = list(probabilidades)
    simbs_trabajo = list(simbolos)
    
    if r > 2 and (len(probs_trabajo) - r) % (r - 1) != 0:
        faltantes = (r - 1) - ((len(probs_trabajo) - r) % (r - 1))
        for k in range(faltantes):
            simbs_trabajo.append(f"_ficticio_{k}")
            probs_trabajo.append(0.0)
            
    nodos = [_NodoHuffman(p, s) for s, p in zip(simbs_trabajo, probs_trabajo)]
    
    while len(nodos) > 1:
        nodos.sort(key=lambda item: item.peso)
        tomar = min(r, len(nodos))
        grupo = [nodos.pop(0) for _ in range(tomar)]
        nuevo_peso = sum(nodo.peso for nodo in grupo)
        nuevo_nodo = _NodoHuffman(peso=nuevo_peso, hijos=grupo)
        nodos.append(nuevo_nodo)
        
    raiz = nodos[0]
    mapa_codigos = {}
    
    def recorrer(nodo, prefijo):
        if nodo.simbolo is not None and not str(nodo.simbolo).startswith("_ficticio_"):
            mapa_codigos[nodo.simbolo] = prefijo if prefijo else "0"
        for idx, hijo in enumerate(nodo.hijos):
            recorrer(hijo, prefijo + alfabeto_codigo[idx])
            
    recorrer(raiz, "")
    
    l_opt = sum(prob * len(mapa_codigos[s]) for s, prob in zip(simbolos, probabilidades))
    return mapa_codigos, l_opt
# INTERPRETACIÓN:
#   Construye un código INSTANTÁNEO de longitud media mínima (compacto) para esas
#   probabilidades, juntando repetidamente los r símbolos menos probables. Los más
#   probables quedan con palabras más cortas. El código no es único (se pueden
#   intercambiar ramas) pero la L sí.


def es_codigo_compacto(codigos, probabilidades, r=None, metodo="catedra", tol=1e-6):
    """
    Decide si el código es compacto.
    Criterio de la cátedra: es unívoco y cada palabra cumple Li <= techo(log_r(1/Pi)).
    Con metodo="huffman": es unívoco y su L es igual a la del código de Huffman.
    """
    if len(codigos) != len(probabilidades):
        raise ValueError("Las listas de códigos y probabilidades deben coincidir en longitud.")
        
    if r is None:
        _, r = obtener_alfabeto_codigo(codigos)
    if r <= 1:
        r = 2
        
    if not es_no_singular(codigos):
        return False, "No es compacto: el código es singular.", 0.0, 0.0
        
    es_ud, _ = sardinas_patterson(codigos)
    if not es_ud:
        return False, "No es compacto: no es unívocamente decodificable.", 0.0, 0.0
        
    l_actual = longitud_media(codigos, probabilidades)
    _, l_huffman = huffman(probabilidades, r=r)
    
    if metodo == "catedra":
        for idx, (palabra, p) in enumerate(zip(codigos, probabilidades)):
            cota = math.ceil(math.log(1.0 / p, r) - 1e-9)
            if len(palabra) > cota:
                return (
                    False,
                    f"No es compacto (Criterio Cátedra): palabra {idx+1} ('{palabra}', len={len(palabra)}) supera la cota ceil(log_{r}(1/p_{idx+1})) = {cota}.",
                    l_actual,
                    l_huffman
                )
        return (
            True,
            f"Es compacto (Criterio Cátedra): es unívoco y todas las palabras cumplen l_i <= ceil(log_{r}(1/p_i)).",
            l_actual,
            l_huffman
        )
    else:
        if abs(l_actual - l_huffman) <= tol:
            return True, f"Es compacto (Óptimo Huffman): su longitud media ({l_actual:.4f}) es mínima e igual a Huffman ({l_huffman:.4f}).", l_actual, l_huffman
        else:
            return False, f"No es compacto (Óptimo Huffman): su longitud media ({l_actual:.4f}) es mayor a la de Huffman ({l_huffman:.4f}).", l_actual, l_huffman
# INTERPRETACIÓN:
#   Compacto (Unidad 3): un código unívoco es compacto si su L es menor o igual que la
#   de cualquier otro código unívoco para la misma fuente y el mismo alfabeto X.
#   Criterio de la cátedra (teórico-práctica): unívoco y Li <= techo(log_r(1/Pi))
#   para CADA palabra, o sea que ninguna palabra es más larga de lo que "merece" según
#   su probabilidad. No hace falta que Li = log_r(1/Pi) exacto (eso casi nunca es entero).
#   Si no es unívoco, no puede ser compacto.
#   EN EL PARCIAL: mostrar la cota techo(log_r(1/Pi)) de cada palabra comparada con Li.


def simular_mensaje_codificado(codigos, probabilidades, n):
    """
    Genera un mensaje codificado: elige n símbolos de la fuente según sus
    probabilidades y concatena sus palabras código.
    """
    palabras_elegidas = random.choices(codigos, weights=probabilidades, k=n)
    return ''.join(palabras_elegidas)
# INTERPRETACIÓN:
#   Genera la tira de símbolos de código tal como se transmitiría (palabras pegadas,
#   sin separadores). Muestra por qué el objetivo es poder "reconstruir fielmente el
#   mensaje original a partir de la secuencia codificada": el receptor tiene que
#   poder cortarla en palabras sin ambigüedad.


# ==============================================================================
# SECCIÓN 5: REPORTE INTEGRAL RÁPIDO PARA EJERCICIOS DE PARCIAL
# ==============================================================================

def clasificar_codigo_completo(codigos, probabilidades=None, verbose=True):
    """
    Reporte completo de un código: alfabeto código X y r, si es bloque, no singular,
    instantáneo y unívoco, inecuación de Kraft y, si se dan probabilidades, longitud
    media, entropía H_r(S), eficiencia y si es compacto.
    """
    alfabeto_x, r = obtener_alfabeto_codigo(codigos)
    bloque = es_codigo_bloque(codigos)
    no_sing = es_no_singular(codigos)
    inst, conflictos = es_instantaneo(codigos)
    ud, hist_sp = sardinas_patterson(codigos)
    cumple_k, val_k = cumple_kraft(codigos, r)
    
    resultado = {
        "alfabeto_codigo": alfabeto_x,
        "r": r,
        "es_bloque": bloque,
        "es_no_singular": no_sing,
        "es_instantaneo": inst,
        "es_univoco": ud,
        "kraft_valor": val_k,
        "cumple_kraft": cumple_k
    }
    
    if probabilidades is not None:
        l_med = longitud_media(codigos, probabilidades)
        eta, red, h_r, _ = eficiencia_y_redundancia(codigos, probabilidades, r)
        compacto, motivo, _, l_opt = es_codigo_compacto(codigos, probabilidades, r)
        resultado.update({
            "longitud_media": l_med,
            "entropia_hr": h_r,
            "eficiencia": eta,
            "redundancia": red,
            "es_compacto": compacto,
            "longitud_optima": l_opt,
            "motivo_compacidad": motivo
        })
        
    if verbose:
        print("=" * 60)
        print("REPORTE DE CLASIFICACIÓN DE CÓDIGO")
        print("=" * 60)
        print(f"Palabras código: {codigos}")
        print(f"Alfabeto código X: {alfabeto_x}  (r = {r})")
        print(f"¿Es Bloque?: {'SÍ' if bloque else 'NO'}")
        print(f"¿Es No Singular?: {'SÍ' if no_sing else 'NO'}")
        print(f"¿Es Instantáneo?: {'SÍ' if inst else 'NO'}")
        if not inst:
            print(f"   Conflictos de prefijo: {conflictos}")
        print(f"¿Es Unívocamente Decodificable (Sardinas-Patterson)?: {'SÍ' if ud else 'NO'}")
        print(f"Inecuación de Kraft (Base {r}): {val_k:.4f} -> {'Cumple (<= 1)' if cumple_k else 'NO cumple (> 1)'}")
        
        if probabilidades is not None:
            print("-" * 60)
            print(f"Longitud Media (L): {resultado['longitud_media']:.4f}")
            print(f"Entropía H_{r}(S): {resultado['entropia_hr']:.4f}")
            print(f"Eficiencia (eta): {resultado['eficiencia'] * 100:.2f}%")
            print(f"Redundancia: {resultado['redundancia'] * 100:.2f}%")
            print(f"¿Es Compacto?: {'SÍ' if resultado['es_compacto'] else 'NO'}")
            print(f"Detalle compacidad: {resultado['motivo_compacidad']}")
        print("=" * 60)

    return resultado
# INTERPRETACIÓN:
#   Resumen de todas las propiedades del código. Árbol de la cátedra:
#   Bloque ⊃ No singular ⊃ Unívoco ⊃ Instantáneo -> se responde la clase MÁS restrictiva.
#   OJO: "bloque" acá es la definición de largo fijo, no la de la cátedra.


# ==============================================================================
# SECCIÓN 6: RESOLVER EJERCICIOS DE PARCIAL PASO A PASO (formato cátedra)
# ==============================================================================
# En el parcial del 30/09/2025 casi la mitad del puntaje fue "Explicar cómo se
# obtuvieron los resultados". Estas funciones imprimen cada paso con los datos
# concretos (tolerancia, r, sufijos de Sardinas-Patterson, cotas) para poder
# copiarlos en la explicación.
#
# CONVENCIÓN DE LA CÁTEDRA para la matriz de transición:
#   columna j = símbolo ANTERIOR (desde),  fila i = símbolo SIGUIENTE (hacia)
#   M[i][j] = P(sale i | antes salió j)  ->  cada COLUMNA suma 1.


def _fmt(x, dec=4):
    """
    Muestra un número sin ceros de más (0.1400 -> 0.14).
    """
    texto = f"{x:.{dec}f}".rstrip('0').rstrip('.')
    return texto if texto not in ("", "-0") else "0"


def _imprimir_matriz(alfabeto, M, dec=2):
    """
    Muestra una matriz de transición: columnas = símbolo anterior, filas = símbolo siguiente.
    """
    ancho = max(7, dec + 4)
    print("      desde->  " + "".join(f"{repr(s):>{ancho}}" for s in alfabeto))
    for i, s in enumerate(alfabeto):
        print(f"  hacia {repr(s):>5}  " + "".join(f"{M[i][j]:>{ancho}.{dec}f}" for j in range(len(alfabeto))))


def resolver_fuente(mensaje, tolerancia=0.05, dec=2):
    """
    Resuelve el ejercicio de fuentes a partir de un mensaje (TP2 ej. 16):
    probabilidades de los símbolos, matriz de transición, si la fuente tiene
    memoria o no (con tolerancia), entropía y, según el caso, la extensión de
    orden 2 (memoria nula) o el vector estacionario (con memoria).
    """
    print("=" * 70)
    print(f"MENSAJE ({len(mensaje)} símbolos): {mensaje}")
    print("=" * 70)

    alfabeto, probs = analizar_cadena_fuente(mensaje)
    n = len(alfabeto)
    print("\na) ALFABETO Y PROBABILIDADES  ->  P(s) = apariciones de s / largo del mensaje")
    print(f"   Alfabeto: {{{', '.join(repr(s) for s in alfabeto)}}}  ({n} símbolos)")
    for s, p in zip(alfabeto, probs):
        print(f"   P({s!r}) = {mensaje.count(s)}/{len(mensaje)} = {p:.{dec}f}"
              f"   ->  I({s!r}) = log2(1/P) = {cantidad_informacion(p):.{dec}f} bits")

    _, conteos, M = matriz_transicion(mensaje)
    print("\nb) MATRIZ DE TRANSICIÓN  (columna = símbolo anterior, fila = símbolo siguiente)")
    print(f"   Se recorren los {len(mensaje) - 1} pares consecutivos (anterior, siguiente) del mensaje.")
    print("   Cantidad de pares:")
    _imprimir_matriz(alfabeto, conteos, dec=0)
    print("   Cada columna se divide por su total (veces que ese símbolo fue seguido de otro):")
    print("   totales por columna: " + ", ".join(
        f"{s!r}={sum(conteos[i][j] for i in range(n))}" for j, s in enumerate(alfabeto)))
    _imprimir_matriz(alfabeto, M, dec=dec)

    print(f"\nc) MEMORIA  (tolerancia = {tolerancia})")
    print("   Si la fuente no tiene memoria, P(siguiente) no depende del anterior:")
    print("   cada FILA de la matriz debe tener todos sus valores iguales.")
    memoria_nula = True
    for i, s in enumerate(alfabeto):
        dif = max(M[i]) - min(M[i])
        ok = dif <= tolerancia
        memoria_nula = memoria_nula and ok
        print(f"   fila {s!r}: max - min = {max(M[i]):.{dec}f} - {min(M[i]):.{dec}f} = {dif:.{dec}f} "
              f"{'<=' if ok else '>'} {tolerancia}")
    print(f"   => FUENTE {'DE MEMORIA NULA' if memoria_nula else 'CON MEMORIA'}")

    print("\nd) ENTROPÍA")
    if memoria_nula:
        h = entropia_fuente(probs, 2)
        print("   Memoria nula: H(S) = Σ P(s) · log2(1/P(s))")
        for s, p in zip(alfabeto, probs):
            print(f"     {s!r}: {p:.4f} · log2(1/{p:.4f}) = {p * math.log2(1 / p):.4f}")
        print(f"   H(S) = {h:.{dec}f} bits")

        palabras, probs2, h2 = extension_fuente(alfabeto, probs, 2)
        print("\ne) EXTENSIÓN DE ORDEN 2  ->  P(ab) = P(a) · P(b)")
        for pal, p in zip(palabras, probs2):
            print(f"   P({pal!r}) = {p:.4f}")
        print(f"   H(S^2) = Σ P · log2(1/P) = {h2:.{dec}f} bits   (verifica 2 · H(S) = {2 * h:.{dec}f})")
        _, _, h3 = extension_fuente(alfabeto, probs, 3)
        print(f"   (extra) orden 3: {n ** 3} símbolos, H(S^3) = {h3:.{dec}f} bits   (verifica 3 · H(S) = {3 * h:.{dec}f})")
    else:
        ergodica = es_cadena_ergodica(M, estocastica_por="columnas")
        print(f"   Cadena ergódica (todos los estados se comunican): {'SÍ' if ergodica else 'NO'}")
        pi = vector_estacionario(M, estocastica_por="columnas")
        print("   Con memoria: H(S) = Σ_j π_j · H(columna j),  H(columna j) = Σ_i M[i][j] · log2(1/M[i][j])")
        h = 0.0
        for j, s in enumerate(alfabeto):
            h_col = entropia_fuente([M[i][j] for i in range(n)], 2)
            h += pi[j] * h_col
            print(f"     desde {s!r}: π = {pi[j]:.4f}, H(columna) = {h_col:.4f}, aporte = {pi[j] * h_col:.4f}")
        print(f"   H(S) = {h:.{dec}f} bits")
        h_sin = entropia_fuente(probs, 2)
        print(f"   (extra) si se ignorara la memoria: Σ P(s)·log2(1/P(s)) = {h_sin:.{dec}f} bits"
              f" -> la memoria la reduce en {h_sin - h:.{dec}f} bits")

        print("\nf) VECTOR ESTACIONARIO  ->  resolver π = M · π  con  Σ π = 1  (Gauss)")
        for s, p in zip(alfabeto, pi):
            print(f"   π({s!r}) = {p:.{dec}f}")
        print("   (a largo plazo, es la proporción de veces que sale cada símbolo)")
    print(f"\n(extra) ENTROPÍA MÁXIMA para {n} símbolos: log2({n}) = {math.log2(n):.{dec}f} bits"
          f"  ->  H(S) = {h:.{dec}f} queda {math.log2(n) - h:.{dec}f} bits abajo")
    print()
# INTERPRETACIÓN:
#   Conclusión según el resultado:
#   - MEMORIA NULA: los símbolos son estadísticamente independientes. H(S) sale solo
#     de las probabilidades y la extensión cumple H(S^2) = 2·H(S).
#   - CON MEMORIA: el símbolo anterior condiciona al siguiente (fuente de Markov de
#     orden 1). H = Σ πj·H(columna j), menor que la entropía calculada solo con las
#     probabilidades, porque la memoria hace más predecible a la fuente. π es la
#     proporción de cada símbolo a largo plazo.
#   EN EL PARCIAL: nombrar la tolerancia, cómo se armó la matriz y qué fila/columna
#   decidió la memoria.


def _fraccion(x, max_den=100):
    """
    Muestra un número como fracción si lo es (0.3636... -> 4/11), para comparar con
    los resultados de la cátedra.
    """
    for q in range(1, max_den + 1):
        p = round(x * q)
        if abs(p / q - x) < 1e-9:
            return str(p) if q == 1 else f"{p}/{q}"
    return f"{x:.4f}"


def matriz_desde_grafo(estados, flechas):
    """
    Matriz de transición (formato cátedra, por columnas) a partir del grafo de una
    fuente de Markov. Cada flecha va del estado anterior al siguiente y lleva la
    probabilidad de esa transición. Si una flecha no tiene probabilidad, se asume
    que todas las flechas que salen de ese estado son equiprobables.
    """
    n = len(estados)
    indice = {s: k for k, s in enumerate(estados)}
    M = [[0.0] * n for _ in range(n)]
    salientes = {s: [] for s in estados}
    for f in flechas:
        salientes[f[0]].append(f)
    for desde, lista in salientes.items():
        for f in lista:
            p = f[2] if len(f) > 2 and f[2] is not None else 1 / len(lista)
            M[indice[f[1]]][indice[desde]] = p
    return M
# INTERPRETACIÓN:
#   Leer el grafo: cada flecha "desde -> hacia" con probabilidad p va en la columna
#   del estado desde y la fila del estado hacia. Un lazo (flecha a sí mismo) va en la
#   diagonal. Las flechas que salen de un estado suman 1, por eso cada columna suma 1.
#   EN EL PARCIAL: si el grafo no trae probabilidades, decir que se asumió
#   equiprobabilidad entre las flechas que salen de cada estado.


def resolver_markov(M, estados=None, dec=2):
    """
    Resuelve el ejercicio de fuentes de Markov cuando dan la matriz o el grafo
    (TP2 ej. 13 y 17): matriz de transición, si la fuente es ergódica y, si lo es,
    el vector estacionario (π = M·π con Σπ = 1) y la entropía H = Σ πj·H(columna j).
    """
    n = len(M)
    if estados is None:
        estados = [str(k + 1) for k in range(n)]
    print("=" * 70)
    print(f"FUENTE DE MARKOV con {n} estados: {{{', '.join(estados)}}}")
    print("=" * 70)

    print("\na) MATRIZ DE TRANSICIÓN  (columna = estado anterior, fila = estado siguiente)")
    ancho = 7
    print("      desde->  " + "".join(f"{s:>{ancho}}" for s in estados))
    for i, s in enumerate(estados):
        print(f"  hacia {s:>5}  " + "".join(f"{_fraccion(M[i][j]):>{ancho}}" for j in range(n)))
    sumas = [sum(M[i][j] for i in range(n)) for j in range(n)]
    malas = [estados[j] for j in range(n) if abs(sumas[j] - 1) > 1e-6]
    if malas:
        print(f"   ATENCIÓN: las columnas {malas} no suman 1. ¿La cargaste por filas?"
              " En la cátedra cada COLUMNA suma 1.")
        return
    print("   Cada columna suma 1 (las transiciones que salen de cada estado).")

    print("\nb) ERGODICIDAD: todos los estados tienen que ser alcanzables entre sí")
    alcanzables = []
    for inicio in range(n):
        vistos = {inicio}
        pila = [inicio]
        while pila:
            j = pila.pop()
            for i in range(n):
                if M[i][j] > 1e-12 and i not in vistos:
                    vistos.add(i)
                    pila.append(i)
        alcanzables.append(vistos)
    ergodica = True
    for j in range(n):
        faltan = [estados[i] for i in range(n) if i not in alcanzables[j]]
        if faltan:
            ergodica = False
            print(f"   desde {estados[j]} NO se puede llegar a: {', '.join(faltan)}")
    for j in range(n):
        if abs(M[j][j] - 1) < 1e-12:
            print(f"   El estado {estados[j]} es absorbente: su única transición es a sí mismo (P = 1)")
    if not ergodica:
        print("   => NO ES ERGÓDICA: no se calculan vector estacionario ni entropía")
        print()
        return
    print("   Desde cualquier estado se llega a todos los demás => ES ERGÓDICA")

    print("\nc) VECTOR ESTACIONARIO: se resuelve π = M·π junto con Σ π = 1")
    for i, s in enumerate(estados):
        terminos = [f"{_fraccion(M[i][j])}·π{estados[j]}" for j in range(n) if M[i][j] > 1e-12]
        print(f"   π{s} = " + " + ".join(terminos))
    print("   " + " + ".join(f"π{s}" for s in estados) + " = 1")
    pi = vector_estacionario(M, estocastica_por="columnas")
    for s, p in zip(estados, pi):
        print(f"   π{s} = {p:.{dec}f}  ({_fraccion(p)})")

    print("\nd) ENTROPÍA: H = Σ πj · H(columna j),  H(columna j) = Σ Pi·log2(1/Pi)")
    h = 0.0
    for j, s in enumerate(estados):
        h_col = entropia_fuente([M[i][j] for i in range(n)], 2)
        h += pi[j] * h_col
        print(f"   desde {s}: π = {pi[j]:.4f}, H(columna) = {h_col:.4f}, aporte = {pi[j] * h_col:.4f}")
    print(f"   H = {h:.{dec}f} bits")
    print(f"   (extra) entropía máxima para {n} estados: log2({n}) = {math.log2(n):.{dec}f} bits")
    print()
    return pi, h
# INTERPRETACIÓN:
#   - Ergódica: desde cualquier estado se puede llegar a cualquier otro. Si hay un
#     estado absorbente o un grupo del que no se sale, no es ergódica: el
#     comportamiento a largo plazo depende de dónde arranca y no se informan π ni H.
#   - π: proporción del tiempo que la fuente pasa en cada estado a largo plazo. Los
#     estados con lazos o a los que llegan muchas flechas tienen π más alto.
#   - H: incertidumbre de cada estado (qué tan impredecible es el próximo salto),
#     ponderada por π. Un estado con una única salida (P = 1) aporta 0.
#   EN EL PARCIAL: decir cómo se armó la matriz (columna = desde), por qué es o no
#   ergódica (qué estado no se alcanza), el sistema de π y los aportes de H.


def sardinas_patterson_catedra(codigos):
    """
    Sardinas-Patterson con la numeración de la cátedra:
    S1 = C (las palabras código). Cada S(i+1) son los sufijos que sobran al comparar
    las palabras de C con las de Si cuando una es prefijo de la otra.
    Si algún Si contiene una palabra de C, el código no es unívoco; si un Si queda
    vacío o repite uno anterior, es unívoco.
    """
    C = set(codigos)
    conjuntos = [set(C)]
    while True:
        Si = conjuntos[-1]
        nuevo = set()
        for x in C:
            for y in Si:
                if len(conjuntos) == 1 and x == y:
                    continue
                if y.startswith(x) and y != x:
                    nuevo.add(y[len(x):])
                elif x.startswith(y) and x != y:
                    nuevo.add(x[len(y):])
        conjuntos.append(nuevo)
        k = len(conjuntos)
        if nuevo & C:
            return False, conjuntos, f"S{k} contiene palabras del código: {sorted(nuevo & C)}"
        if not nuevo:
            return True, conjuntos, f"S{k} es vacío"
        if nuevo in conjuntos[1:-1]:
            return True, conjuntos, f"S{k} ya apareció antes (ciclo)"
# INTERPRETACIÓN:
#   Numeración de la cátedra (teórico-práctica):
#   1. S1 = C (las palabras código).
#   2. Para cada par (x de S1, y de Si): si uno es prefijo del otro, el sufijo que
#      sobra va a S(i+1).
#   3. Si algún Si contiene una palabra de C -> NO es UD (una misma secuencia tiene
#      dos lecturas). Si se obtiene un Si que ya apareció antes (o vacío) -> ES UD.
#   Ejemplos de clase: {0, 01, 10} NO es UD y {0, 01, 11} SÍ es UD.
#   EN EL PARCIAL: escribir todos los Si y decir por qué se cortó.


def resolver_codigo(codigos, probabilidades, r=None, dec=2):
    """
    Resuelve el ejercicio de códigos (TP3 ej. 8): alfabeto código X y r, entropía
    H_r(S) y longitud media L, inecuación de Kraft, clasificación (Bloque / No
    singular / Unívoco / Instantáneo), si es compacto y los pasos de
    Sardinas-Patterson.
    """
    q = len(codigos)
    print("=" * 70)
    print("CÓDIGO:")
    for k, (c, p) in enumerate(zip(codigos, probabilidades), 1):
        print(f"   S{k}  P = {p:<6}  palabra = {c!r}  (largo {len(c)})")
    print("=" * 70)

    alfabeto_x, r_detectado = obtener_alfabeto_codigo(codigos)
    if r is None:
        r = r_detectado
    print(f"\na) ALFABETO CÓDIGO: X = {{{', '.join(alfabeto_x)}}}  ->  r = {r} símbolos")

    h_r = entropia_fuente(probabilidades, r)
    L = longitud_media(codigos, probabilidades)
    print(f"\nb) ENTROPÍA en base r = {r}: H{r}(S) = Σ Pi · log{r}(1/Pi)")
    for k, p in enumerate(probabilidades, 1):
        print(f"     S{k}: {p} · log{r}(1/{p}) = {p * math.log(1 / p, r):.4f}")
    print(f"   H{r}(S) = {h_r:.4f}")
    print("   LONGITUD MEDIA: L = Σ Pi · Li = " +
          " + ".join(f"{p}·{len(c)}" for c, p in zip(codigos, probabilidades)) + f" = {_fmt(L)}")
    print(f"   Se cumple H{r}(S) <= L: {h_r:.4f} <= {_fmt(L)}")
    print(f"   (extra) eficiencia η = H{r}(S)/L = {h_r / L:.4f} ({h_r / L * 100:.2f}%),"
          f"  redundancia = 1 - η = {1 - h_r / L:.4f}")

    kraft = sum(r ** (-len(c)) for c in codigos)
    print(f"\nc) KRAFT-McMILLAN: Σ r^(-Li) = " + " + ".join(f"{r}^-{len(c)}" for c in codigos) +
          f" = {kraft:.4f}  ->  {'CUMPLE (<= 1)' if kraft <= 1 + 1e-9 else 'NO CUMPLE (> 1): no puede ser unívoco'}")

    print("\nd) CLASIFICACIÓN  (Bloque ⊃ No singular ⊃ Unívoco ⊃ Instantáneo)")
    repetidas = [c for c in set(codigos) if codigos.count(c) > 1]
    if repetidas:
        for c in repetidas:
            simbolos = [f"S{k}" for k, x in enumerate(codigos, 1) if x == c]
            print(f"   {' y '.join(simbolos)} tienen la misma palabra {c!r} -> es SINGULAR")
        clase = "Bloque"
        es_ud = False
    else:
        print("   Todas las palabras son distintas -> es NO SINGULAR")
        prefijos = [(i, j) for i in range(q) for j in range(q)
                    if i != j and codigos[j].startswith(codigos[i])]
        if not prefijos:
            print("   Ninguna palabra es prefijo de otra -> es INSTANTÁNEO (y por lo tanto unívoco)")
            clase = "Instantáneo"
            es_ud = True
        else:
            for i, j in prefijos:
                print(f"   S{i + 1} ({codigos[i]!r}) es prefijo de S{j + 1} ({codigos[j]!r}) -> NO es instantáneo")
            es_ud, conjuntos, motivo = sardinas_patterson_catedra(codigos)
            print("\nf) SARDINAS-PATTERSON:")
            for k, S in enumerate(conjuntos, 1):
                print(f"   S{k} = {{{', '.join(repr(x) for x in sorted(S))}}}")
            print(f"   Fin: {motivo} -> {'ES' if es_ud else 'NO es'} unívocamente decodificable")
            clase = "Unívoco" if es_ud else "No singular"
    print(f"   => CÓDIGO {clase.upper()}")

    print("\ne) CÓDIGO COMPACTO: debe ser unívoco y cumplir Li <= techo(log_r(1/Pi)) para cada palabra")
    if not es_ud:
        print("   No es unívoco -> NO ES COMPACTO")
        compacto = False
    else:
        compacto = True
        for k, (c, p) in enumerate(zip(codigos, probabilidades), 1):
            cota = math.ceil(math.log(1 / p, r) - 1e-9)
            ok = len(c) <= cota
            compacto = compacto and ok
            print(f"   S{k}: L = {len(c)} {'<=' if ok else '>'} techo(log{r}(1/{p})) = "
                  f"techo({math.log(1 / p, r):.3f}) = {cota}  {'OK' if ok else 'NO'}")
        print(f"   => {'ES COMPACTO' if compacto else 'NO ES COMPACTO'}")
    print()
    return clase, compacto
# INTERPRETACIÓN:
#   Conclusión según el resultado:
#   - H_r(S) <= L siempre. Cuanto más cerca, más eficiente el código.
#   - Kraft > 1: no existe código unívoco con esas longitudes. Kraft <= 1: existe uno
#     instantáneo con esas longitudes, pero no asegura que ESTE lo sea.
#   - Clase (la más restrictiva): Instantáneo (decodifica sin mirar lo que viene),
#     Unívoco (sin ambigüedad pero hay que mirar adelante), No singular (palabras
#     distintas pero hay secuencias ambiguas), Bloque (hay palabras repetidas).
#   - Compacto: unívoco y ninguna Li supera techo(log_r(1/Pi)).
#   EN EL PARCIAL: decir qué es X y cuánto vale r, cómo se clasificó (qué palabra es
#   prefijo de cuál), los pasos de S-P y la cota de cada palabra para compacto.


if __name__ == "__main__":
    # Parcial 30/09/2025 (para practicar). Resultados oficiales en los comentarios.
    resolver_fuente(")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])")   # memoria nula, H=1.83, H(S2)=3.66
    resolver_fuente(".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::.")   # con memoria, H=1.57, pi=(.12,.24,.44,.18)
    resolver_codigo(["/+", "*", "+-", "-", "*/"], [0.15, 0.25, 0.05, 0.45, 0.10])  # H=0.98 L=1.3 K=0.687 no singular, no compacto
    resolver_codigo(["()", "]", "[)", ")", "(["], [0.15, 0.25, 0.05, 0.45, 0.10])  # instantáneo, compacto
