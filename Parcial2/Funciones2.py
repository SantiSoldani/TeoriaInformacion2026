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


def distancia_hamming(codigo: list[str]) -> int:
    """
    Calcula la distancia de Hamming de un código binario (la distancia mínima
    entre todas las palabras código distintas).

    Exige que todas las palabras código tengan la misma longitud.
    Retorna únicamente la distancia de Hamming (int).
    """
    if not codigo or len(codigo) < 2:
        return 0

    longitud = len(codigo[0])
    if any(len(palabra) != longitud for palabra in codigo):
        raise ValueError("Todas las palabras código deben tener la misma longitud.")

    d_min = float('inf')

    # Comparamos todos los pares de palabras distintas (i < j)
    for i in range(len(codigo)):
        for j in range(i + 1, len(codigo)):
            d = sum(c1 != c2 for c1, c2 in zip(codigo[i], codigo[j]))
            if d < d_min:
                d_min = d

    return d_min if d_min != float('inf') else 0


def distancia_hamming_longitud_variable(codigo: list[str]) -> int:
    """
    Función anexa:
    Calcula la distancia mínima entre palabras código permitiendo diferentes longitudes.
    Por cada carácter de diferencia en la longitud entre dos palabras, la distancia aumenta en 1.
    """
    if not codigo or len(codigo) < 2:
        return 0

    d_min = float('inf')

    for i in range(len(codigo)):
        for j in range(i + 1, len(codigo)):
            p1 = codigo[i]
            p2 = codigo[j]
            d = sum(c1 != c2 for c1, c2 in zip(p1, p2)) + abs(len(p1) - len(p2))
            if d < d_min:
                d_min = d

    return d_min if d_min != float('inf') else 0


def errores_detectables(distancia: int) -> int:
    """Cantidad de errores que se pueden detectar con una distancia d: d - 1."""
    return max(0, distancia - 1)


def errores_corregibles(distancia: int) -> int:
    """Cantidad de errores que se pueden corregir con una distancia d: (d - 1) // 2."""
    return max(0, (distancia - 1) // 2)


def analizar_codigo_hamming(codigo: list[str]) -> tuple[int, int, int]:
    """
    Implementación del Ejercicio 10:
    Recibe una lista de cadenas de caracteres que representa una codificación binaria y
    devuelve una tupla con la distancia de Hamming, la cantidad de errores detectables y
    la cantidad de errores corregibles.

    Parámetros:
        codigo (list[str]): Lista de palabras código binarias de igual longitud.

    Formato de Salida:
        tuple[int, int, int]: (distancia_hamming, errores_detectables, errores_corregibles)
          - [0] distancia_hamming   : Distancia mínima de Hamming entre palabras distintas.
          - [1] errores_detectables : Cantidad máxima de errores detectables (d - 1).
          - [2] errores_corregibles : Cantidad máxima de errores corregibles ((d - 1) // 2).
    """
    d = distancia_hamming(codigo)
    detectables = errores_detectables(d)
    corregibles = errores_corregibles(d)
    return d, detectables, corregibles


# EJ 12

def caracter_a_byte_paridad(caracter: str, tipo_paridad: str = "par") -> int:
    """
    a. Dado un carácter, devuelve un byte (entero de 8 bits entre 0 y 255) que representa:
       - Bits 7 a 1: Los 7 bits del código ASCII del carácter.
       - Bit 0 (LSB, menos significativo): El bit de paridad ('par' o 'impar').

    Parámetros:
        caracter: Carácter de entrada (longitud 1).
        tipo_paridad: 'par' (por defecto) o 'impar'.

    Retorna:
        Un entero entre 0 y 255 que representa el byte resultante.
    """
    if len(caracter) != 1:
        raise ValueError("Se debe ingresar exactamente un carácter.")

    codigo_ascii = ord(caracter)
    if codigo_ascii > 127:
        raise ValueError("El carácter debe pertenecer a la tabla ASCII estándar (0 a 127).")

    # Contamos la cantidad de unos en la representación de 7 bits
    unos = bin(codigo_ascii).count("1")

    # Cálculo del bit de paridad
    if tipo_paridad == "par":
        # Paridad par: si la cantidad de 1s es impar, agregamos 1 para que el total sea par
        bit_paridad = 1 if (unos % 2 != 0) else 0
    elif tipo_paridad == "impar":
        # Paridad impar: si la cantidad de 1s es par, agregamos 1 para que el total sea impar
        bit_paridad = 1 if (unos % 2 == 0) else 0
    else:
        raise ValueError("tipo_paridad debe ser 'par' o 'impar'.")

    # Desplazamos 1 bit a la izquierda el código ASCII y colocamos la paridad en el LSB (bit 0)
    byte_con_paridad = (codigo_ascii << 1) | bit_paridad
    return byte_con_paridad


def verificar_byte(b: int, tipo_paridad: str = "par") -> bool:
    """
    b. Dado un byte generado por 'caracter_a_byte_paridad', verifica si es correcto
       o tiene errores de paridad.

    Parámetros:
        b: Entero de 8 bits (o byte) a verificar.
        tipo_paridad: 'par' (por defecto) o 'impar'.

    Retorna:
        True si la paridad es correcta, False si se detectó error.
    """
    if isinstance(b, (bytes, bytearray)):
        b = b[0]

    # Extraemos el código ASCII original (bits 7 a 1) y el bit de paridad recibido (bit 0)
    codigo_ascii = b >> 1
    bit_paridad_recibido = b & 1

    unos_ascii = bin(codigo_ascii).count("1")

    if tipo_paridad == "par":
        bit_paridad_esperado = 1 if (unos_ascii % 2 != 0) else 0
    elif tipo_paridad == "impar":
        bit_paridad_esperado = 1 if (unos_ascii % 2 == 0) else 0
    else:
        raise ValueError("tipo_paridad debe ser 'par' o 'impar'.")

    return bit_paridad_recibido == bit_paridad_esperado


def extraer_caracter(b: int, tipo_paridad: str = "par") -> str | None:
    """
    Función complementaria: Si el byte es válido, retorna el carácter original;
    si contiene error, retorna None.
    """
    if verificar_byte(b, tipo_paridad):
        return chr(b >> 1)
    return None


def bits_a_bytearray(cadena_bits: str) -> bytearray:
    """
    Función auxiliar: Convierte una cadena de bits binarios (ej. '1010000010101110...'
    o '10100000 10101110...' con espacios o saltos de línea) en un bytearray agrupando de a 8 bits.
    """
    limpia = cadena_bits.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    if len(limpia) == 0:
        return bytearray()
    if len(limpia) % 8 != 0:
        raise ValueError(f"La longitud de la cadena de bits ({len(limpia)}) debe ser múltiplo de 8.")
    return bytearray([int(limpia[i : i + 8], 2) for i in range(0, len(limpia), 8)])


def cadena_a_bytearray(cadena: str) -> bytearray:
    """
    Función auxiliar universal: Convierte una cadena a bytearray.
    - Si es una secuencia de bits binarios ('0', '1', espacios), agrupa de a 8 bits.
    - Si es texto estándar (ej. 'HOLA'), lo convierte a sus bytes correspondientes.
    """
    limpia = cadena.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    if limpia and all(c in "01" for c in limpia) and len(limpia) % 8 == 0:
        return bits_a_bytearray(limpia)
    return bytearray(cadena, "latin-1")


def codificar_mensaje(cadena: str) -> bytearray:
    """
    a. Genera una secuencia de bytes (bytearray) que contiene:
       - Fila 0: Byte con la paridad vertical (VRC) de cada columna y, en el bit 0 (arriba a la derecha),
         la paridad cruzada.
       - Filas 1 a N: Cada carácter de la cadena en 8 bits (7 bits ASCII + 1 bit paridad longitudinal LRC).
    """
    if not cadena:
        return bytearray()

    # 1. Creamos las filas correspondientes a cada carácter (filas de datos)
    matriz_datos = []
    for caracter in cadena:
        byte_val = caracter_a_byte_paridad(caracter, tipo_paridad="par")
        # Convertimos el byte en una lista de 8 bits [b7, b6, ..., b0]
        fila_bits = [int(b) for b in format(byte_val, "08b")]
        matriz_datos.append(fila_bits)

    # 2. Calculamos la Fila 0 (Paridad Vertical por cada columna)
    # Para cada columna (de 0 a 7), contamos cuántos 1s hay en matriz_datos
    fila_vrc = []
    for col in range(8):
        unos_col = sum(matriz_datos[fila][col] for fila in range(len(cadena)))
        bit_vrc = 1 if (unos_col % 2 != 0) else 0
        fila_vrc.append(bit_vrc)

    # 3. La matriz completa tiene en fila 0 la paridad vertical + cruzada, y luego los datos
    matriz_completa = [fila_vrc] + matriz_datos

    # 4. Transformamos cada fila de 8 bits en un byte y lo agregamos al bytearray
    resultado = bytearray()
    for fila in matriz_completa:
        byte_num = int("".join(map(str, fila)), 2)
        resultado.append(byte_num)

    return resultado


def decodificar_mensaje(datos: bytearray | str) -> str:
    """
    b. Dada la secuencia de bytes con paridad vertical, longitudinal y cruzada:
       - Si no hay errores, devuelve el mensaje original.
       - Si hay un error simple (1 bit), lo detecta, lo corrige y devuelve el mensaje.
       - Si hay errores no corregibles, devuelve una cadena vacía "".
       (Acepta tanto un bytearray como una cadena de texto con bits '0100...').
    """
    if isinstance(datos, str):
        datos = bits_a_bytearray(datos)

    if not datos or len(datos) < 2:
        return ""

    # Reconstruimos la matriz de bits a partir de los bytes recibidos
    matriz = []
    for b in datos:
        matriz.append([int(bit) for bit in format(b, "08b")])

    cant_filas = len(matriz)
    cant_cols = 8

    # 1. Verificamos paridad en cada fila (la suma total de bits en la fila debe ser par)
    filas_con_error = []
    for f in range(cant_filas):
        if sum(matriz[f]) % 2 != 0:
            filas_con_error.append(f)

    # 2. Verificamos paridad en cada columna (la suma total de bits en la columna debe ser par)
    cols_con_error = []
    for c in range(cant_cols):
        unos_col = sum(matriz[f][c] for f in range(cant_filas))
        if unos_col % 2 != 0:
            cols_con_error.append(c)

    # Caso 1: Sin errores
    if len(filas_con_error) == 0 and len(cols_con_error) == 0:
        pass  # La matriz está perfecta

    # Caso 2: Error simple corregible (exactamente 1 fila y 1 columna con error)
    elif len(filas_con_error) == 1 and len(cols_con_error) == 1:
        f_err = filas_con_error[0]
        c_err = cols_con_error[0]
        # Corregimos el bit invirtiéndolo (0 -> 1 ó 1 -> 0)
        matriz[f_err][c_err] ^= 1

    # Caso 3: Errores múltiples no corregibles
    else:
        return ""

    # 3. Reconstruimos los caracteres desde la fila 1 hasta el final
    caracteres = []
    for f in range(1, cant_filas):
        # Descartamos el bit de paridad (último bit, columna 7) y tomamos los 7 bits de ASCII
        bits_ascii = matriz[f][:7]
        codigo_ascii = int("".join(map(str, bits_ascii)), 2)
        caracteres.append(chr(codigo_ascii))

    return "".join(caracteres)





#---------------------------------------------------------------------------
# UNIDAD 5 ---------------






def huffman(probabilidades: list[float]) -> list[str]:
    """
    Construye un codigo compacto de Huffman a partir de una lista de probabilidades.

    Parámetros:
        - probabilidades (list[float]): Lista de probabilidades de los símbolos de la fuente.
    
    Retorna: lista paralela a 'probabilidades' con las palabras código generadas.
    """

    items = [[p, [i]] for i, p in enumerate(probabilidades)]
    codigos = [''] * len(probabilidades)
    while len(items) > 1:
        items = sorted(items, key=lambda x: x[0])
        menor1 = items.pop(0)
        menor2 = items.pop(0)
        for i in menor1[1]:
            codigos[i] = '0' + codigos[i]
        for i in menor2[1]:
            codigos[i] = '1' + codigos[i]
        items.append([menor1[0] + menor2[0], menor1[1] + menor2[1]])
    return codigos

def shannon_fano(probabilidades: list[float]) -> list[str]:
    """
    Construye un código binario de Shannon-Fano a partir de una lista de probabilidades.

    Parámetros:
        - probabilidades (list[float]): Lista de probabilidades de los símbolos de la fuente.

    Retorna:
        - list[str]: Lista paralela a 'probabilidades' con las palabras código generadas.
    """
    n = len(probabilidades)
    if n == 0:
        return []
    if n == 1:
        return ['0']

    # Guardamos (probabilidad, índice_original) y ordenamos de mayor a menor
    items = sorted([(p, i) for i, p in enumerate(probabilidades)], key=lambda x: x[0], reverse=True)
    codigos = [''] * n

    def paso_shannon_fano(subgrupo: list[tuple[float, int]]) -> None:
        # Caso base: si el subgrupo tiene 1 elemento, no se divide más
        if len(subgrupo) <= 1:
            return

        total = sum(p for p, i in subgrupo)
        mejor_k = 1
        menor_dif = float('inf')
        acumulado = 0.0

        # Buscamos el corte k tal que |acumulado - resto| sea mínimo
        for k in range(1, len(subgrupo)):
            acumulado += subgrupo[k - 1][0]
            resto = total - acumulado
            dif = round(abs(acumulado - resto), 9)
            if dif < menor_dif:
                menor_dif = dif
                mejor_k = k

        grupo_0 = subgrupo[:mejor_k]
        grupo_1 = subgrupo[mejor_k:]

        # Asignamos bit '0' al primer subgrupo y '1' al segundo subgrupo
        for p, i in grupo_0:
            codigos[i] += '0'
        for p, i in grupo_1:
            codigos[i] += '1'

        # Recursión sobre cada subgrupo
        paso_shannon_fano(grupo_0)
        paso_shannon_fano(grupo_1)

    paso_shannon_fano(items)
    return codigos


def codificar(mensaje: str, alfabeto_fuente: str | list[str], codificacion: list[str]) -> bytearray:
    """
    a. Codifica un mensaje escrito en el alfabeto fuente a una secuencia de bytes (bytearray).

    Parámetros:
        - mensaje (str): Cadena de texto a codificar.
        - alfabeto_fuente (str | list[str]): Símbolos del alfabeto de la fuente (ej. 'ABCDE' o ['A','B','C']).
        - codificacion (list[str]): Palabras código binarias paralelas al alfabeto fuente.

    Retorna:
        - bytearray: Secuencia de bytes con el mensaje codificado.
                     El primer byte (byte 0) almacena la cantidad de bits de relleno (padding) añadidos
                     al final para completar el último byte.
    """
    if not mensaje:
        return bytearray()

    if len(alfabeto_fuente) != len(codificacion):
        raise ValueError("El alfabeto fuente y la codificación deben tener la misma longitud.")

    # Mapeo símbolo -> código binario
    mapa_cod = {simbolo: cod for simbolo, cod in zip(alfabeto_fuente, codificacion)}

    # Construimos la secuencia completa de bits
    bits = []
    for s in mensaje:
        if s not in mapa_cod:
            raise ValueError(f"El símbolo {repr(s)} no pertenece al alfabeto fuente.")
        bits.append(mapa_cod[s])
    cadena_bits = "".join(bits)

    # Calculamos cuántos bits de relleno (padding) faltan para que sea múltiplo de 8
    # padding es un valor entre 0 y 7
    padding = (8 - (len(cadena_bits) % 8)) % 8
    cadena_bits += "0" * padding

    resultado = bytearray()
    # Guardamos en el primer byte la cantidad de bits de relleno (0 a 7)
    resultado.append(padding)

    # Agrupamos de a 8 bits y convertimos a enteros (bytes)
    for i in range(0, len(cadena_bits), 8):
        bloque = cadena_bits[i : i + 8]
        resultado.append(int(bloque, 2))

    return resultado


def decodificar(datos: bytearray, alfabeto_fuente: str | list[str], codificacion: list[str]) -> str:
    """
    b. Decodifica una secuencia de bytes generada por 'codificar' y retorna el mensaje original.

    Parámetros:
        - datos (bytearray): Secuencia de bytes a decodificar.
        - alfabeto_fuente (str | list[str]): Símbolos del alfabeto de la fuente.
        - codificacion (list[str]): Palabras código binarias paralelas al alfabeto fuente.

    Retorna:
        - str: Mensaje original decodificado.
    """
    if not datos:
        return ""

    if len(alfabeto_fuente) != len(codificacion):
        raise ValueError("El alfabeto fuente y la codificación deben tener la misma longitud.")

    # El primer byte indica cuántos bits del final son relleno (padding)
    padding = datos[0]
    if padding > 7:
        raise ValueError("Datos corruptos: el padding no puede ser mayor a 7 bits.")

    # Convertimos los bytes restantes a una cadena de bits continua de unos y ceros
    cadena_bits = "".join(format(b, "08b") for b in datos[1:])

    # Descartamos los bits de relleno añadidos al final
    if padding > 0:
        cadena_bits = cadena_bits[:-padding]

    # Diccionario inverso: código binario -> símbolo fuente
    mapa_decod = {cod: simbolo for simbolo, cod in zip(alfabeto_fuente, codificacion)}

    # Decodificación instantánea símbolo a símbolo
    mensaje_recuperado = []
    acumulador = ""
    for bit in cadena_bits:
        acumulador += bit
        if acumulador in mapa_decod:
            mensaje_recuperado.append(mapa_decod[acumulador])
            acumulador = ""

    if acumulador:
        raise ValueError(f"Error al decodificar: quedaron bits sobrantes que no forman ningún código ({acumulador}).")

    return "".join(mensaje_recuperado)


def tasa_compresion(mensaje: str, codificacion: bytearray) -> float:
    """
    Calcula la tasa de compresión N:1 (N = tamaño_original / tamaño_comprimido).

    Parámetros:
        - mensaje (str): Cadena original (en ASCII estándar, 1 byte por carácter).
        - codificacion (bytearray): Mensaje comprimido en bytes.

    Retorna:
        - float: Tasa de compresión.
    """
    if len(codificacion) == 0:
        raise ValueError("La secuencia codificada no puede estar vacía.")

    tamano_original = len(mensaje)
    tamano_comprimido = len(codificacion)
    tasa = tamano_original / tamano_comprimido
    return tasa

def comprimir_rlc(mensaje: str) -> bytearray:
    """
    Comprime un mensaje mediante Run-Length Coding (RLC).
    Almacena cada secuencia repetida en 2 bytes consecutivos:
      - Byte 1: Código ASCII del carácter.
      - Byte 2: Cantidad de repeticiones (número entero entre 1 y 255).
    """
    if not mensaje:
        return bytearray()

    comprimido = bytearray()
    caracter_actual = mensaje[0]
    contador = 0

    for caracter in mensaje:
        # Si el carácter es el mismo y no superamos el límite de 1 byte (255)
        if caracter == caracter_actual and contador < 255:
            contador += 1
        else:
            comprimido.append(ord(caracter_actual))
            comprimido.append(contador)
            caracter_actual = caracter
            contador = 1

    # Guardamos el último grupo
    if contador > 0:
        comprimido.append(ord(caracter_actual))
        comprimido.append(contador)

    return comprimido


def descomprimir_rlc(datos: bytearray) -> str:
    """
    Descomprime una secuencia de bytes generada con RLC y retorna el mensaje original.
    Lee pares de bytes: (código_ascii, cantidad_repeticiones).
    """
    if not datos:
        return ""

    if len(datos) % 2 != 0:
        raise ValueError("Formato RLC inválido: la secuencia debe tener una cantidad par de bytes (pares carácter-longitud).")

    partes = []
    for i in range(0, len(datos), 2):
        caracter = chr(datos[i])
        repeticiones = datos[i + 1]
        partes.append(caracter * repeticiones)

    return "".join(partes)

    



#---------------------------------------------------------------------------
# UNIDAD 6  ---------------




def matriz_canal(entrada: str, salida: str):
    # Convertimos las cadenas en listas de caracteres
    entrada = list(entrada)
    salida = list(salida)
    
    # Obtenemos los alfabetos únicos y ordenados
    alf_entrada = sorted(set(entrada))
    alf_salida = sorted(set(salida))
    
    # Creamos una matriz de ceros (conteo de transiciones)
    mat = [[0 for _ in alf_salida] for _ in alf_entrada]
    
    # Contamos cuántas veces ocurre cada par (entrada, salida)
    for e, s in zip(entrada, salida):
        i = alf_entrada.index(e)
        j = alf_salida.index(s)
        mat[i][j] += 1

    # Normalizamos por cada fila (para obtener probabilidades)
    for i in range(len(alf_entrada)):
        total = sum(mat[i])
        if total > 0:
            mat[i] = [round(x / total,4) for x in mat[i]]

    return mat


def probabilidad_a_priori(cadena: str, redondear: int = 4) -> list[float]:
    """
    Calcula la lista de probabilidades a priori P(X) a partir de una secuencia de símbolos.
    Sigue el orden de los símbolos únicos ordenados alfabéticamente (sorted(set(cadena))),
    de modo que coincide exactamente con el orden de las filas de 'matriz_canal'.
    """
    if not cadena:
        return []
    alfabeto = sorted(set(cadena))
    total = len(cadena)
    return [round(cadena.count(s) / total, redondear) for s in alfabeto]


def probabilidad_salida(p_x: list[float], canal: list[list[float]]) -> list[float]:
    """Calcula P(Y) = sum_x P(X) * P(Y|X)."""
    num_salidas = len(canal[0])
    num_entradas = len(p_x)
    p_y = [0.0] * num_salidas
    for j in range(num_salidas):
        for i in range(num_entradas):
            p_y[j] += p_x[i] * canal[i][j]
    return p_y


def probabilidad_a_posteriori(p_x: list[float], canal: list[list[float]]) -> list[list[float]]:
    """Calcula P(X|Y) = [P(Y|X) * P(X)] / P(Y)."""
    p_y = probabilidad_salida(p_x, canal)
    num_entradas = len(p_x)
    num_salidas = len(canal[0])
    p_x_dado_y = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]
    for j in range(num_salidas):
        for i in range(num_entradas):
            if p_y[j] > 0:
                p_x_dado_y[i][j] = (canal[i][j] * p_x[i]) / p_y[j]
    return p_x_dado_y


def entropias_a_posteriori(p_x: list[float], p_y_dado_x: list[list[float]]) -> list[float]:
    """
    Devuelve una lista con H(A|b_j) para cada símbolo de salida b_j:
      H(A|b_j) = sum_i P(a_i|b_j) * log2(1 / P(a_i|b_j))
    """
    p_x_dado_y = probabilidad_a_posteriori(p_x, p_y_dado_x)
    num_salidas = len(p_y_dado_x[0])
    h_posteriori = []

    for j in range(num_salidas):
        h = 0.0
        for i in range(len(p_x_dado_y)):
            p = p_x_dado_y[i][j]
            if p > 0:
                h -= p * math.log2(p)
        h_posteriori.append(round(h, 4))

    return h_posteriori



def es_canal_sin_ruido(matriz_canal: list[list[float]]) -> bool:
    """
    a. Devuelve True si cada columna de la matriz tiene a lo sumo o exactamente un valor distinto de 0.
    """
    filas = len(matriz_canal)
    columnas = len(matriz_canal[0]) if filas > 0 else 0

    for j in range(columnas):
        contador_no_cero = 0
        for i in range(filas):
            if matriz_canal[i][j] != 0:
                contador_no_cero += 1
            if contador_no_cero > 1:
                return False
        if contador_no_cero != 1:
            return False

    return True


def es_canal_determinante(matriz_canal: list[list[float]]) -> bool:
    """
    b. Devuelve True si cada fila tiene exactamente un valor distinto de 0.
    """
    for fila in matriz_canal:
        contador_no_cero = 0
        for v in fila:
            if v != 0:
                contador_no_cero += 1
            if contador_no_cero > 1:
                return False
        if contador_no_cero != 1:
            return False

    return True



def probabilidad_conjunta(p_x: list[float], canal: list[list[float]]) -> list[list[float]]:
    """Calcula P(X, Y) = P(X) * P(Y|X)."""
    num_entradas = len(p_x)
    num_salidas = len(canal[0])
    p_xy = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]
    for i in range(num_entradas):
        for j in range(num_salidas):
            p_xy[i][j] = p_x[i] * canal[i][j]
    return p_xy



def ruido(probs_a_priori: list[float], matriz: list[list[float]]) -> float:
    """
    a. Calcula la equivocación o ruido H(A/B) POR DEFINICIÓN:
       H(A/B) = sum_i sum_j P(a_i, b_j) * log2(1 / P(a_i/b_j))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, matriz)
    p_post = probabilidad_a_posteriori(probs_a_priori, matriz)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(matriz[0])):
            if p_xy[i][j] > 0 and p_post[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / p_post[i][j])
    return round(val, 4)


def perdida(probs_a_priori: list[float], matriz: list[list[float]]) -> float:
    """
    b. Calcula la pérdida H(B/A) POR DEFINICIÓN:
       H(B/A) = sum_i sum_j P(a_i, b_j) * log2(1 / P(b_j/a_i))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, matriz)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(matriz[0])):
            if p_xy[i][j] > 0 and matriz[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / matriz[i][j])
    return round(val, 4)


def entropia_afin(probs_a_priori: list[float], matriz: list[list[float]]) -> float:
    """
    c. Calcula la entropía afín H(A, B) POR DEFINICIÓN:
       H(A, B) = sum_i sum_j P(a_i, b_j) * log2(1 / P(a_i, b_j))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, matriz)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(matriz[0])):
            if p_xy[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / p_xy[i][j])
    return round(val, 4)


def informacion_mutua(probs_a_priori: list[float], matriz: list[list[float]]) -> float:
    """
    d. Calcula la información mutua I(A, B) POR DEFINICIÓN:
       I(A, B) = sum_i sum_j P(a_i, b_j) * log2(P(a_i, b_j) / (P(a_i) * P(b_j)))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, matriz)
    p_y = probabilidad_salida(probs_a_priori, matriz)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(p_y)):
            if p_xy[i][j] > 0:
                denominador = probs_a_priori[i] * p_y[j]
                if denominador > 0:
                    val += p_xy[i][j] * math.log2(p_xy[i][j] / denominador)
    return round(val, 4)



def get_matriz_compuesta(canal1: list[list[float]], canal2: list[list[float]]) -> list[list[float]]:
    """
    Calcula la matriz compuesta de dos canales (multiplicación de matrices).

    canal1: matriz de tamaño (n x m)
    canal2: matriz de tamaño (m x p)

    Retorna la matriz resultante (n x p).
    """
    
    # Dimensiones
    filas_1 = len(canal1)
    columnas_1 = len(canal1[0])
    filas_2 = len(canal2)
    columnas_2 = len(canal2[0])

    # Validación mínima
    if columnas_1 != filas_2:
        raise ValueError("Las dimensiones no son compatibles para la multiplicación.")

    # Crear matriz resultado con ceros
    resultado = [[0 for _ in range(columnas_2)] for _ in range(filas_1)]

    # Multiplicación matricial
    for i in range(filas_1):
        for j in range(columnas_2):
            suma = 0
            for k in range(columnas_1):  
                suma += canal1[i][k] * canal2[k][j]
            resultado[i][j] = round(suma, 4)

    return resultado


def se_pueden_reducir(matriz: list[list[float]], col1: int, col2: int) -> bool:
    """
    a. Verifica si las columnas col1 y col2 pueden combinarse en una reducción suficiente.
    Dos columnas son reducibles si son proporcionales en todas las filas (a_i * b_k == a_k * b_i).
    """
    filas = len(matriz)
    # Comprobación de proporcionalidad cruzada para evitar divisiones por cero
    for i in range(filas):
        for k in range(i + 1, filas):
            prod1 = matriz[i][col1] * matriz[k][col2]
            prod2 = matriz[k][col1] * matriz[i][col2]
            if not math.isclose(prod1, prod2, abs_tol=1e-6):
                return False
    return True


def generar_matriz_determinante(matriz: list[list[float]], col1: int, col2: int) -> list[list[int]]:
    """
    b. Genera la matriz del canal determinante necesaria para combinar las columnas col1 y col2.
    La matriz resultante tiene dimensiones: (columnas_originales) x (columnas_originales - 1).
    """
    c_min, c_max = min(col1, col2), max(col1, col2)
    columnas_original = len(matriz[0])
    columnas_nueva = columnas_original - 1

    # 1. Crear matriz identidad de tamaño (columnas_nueva) x (columnas_nueva)
    matriz_det = [[1 if i == j else 0 for j in range(columnas_nueva)]
                  for i in range(columnas_nueva)]

    # 2. Fila que combina la columna mayor en la menor
    fila_nueva = [0] * columnas_nueva
    fila_nueva[c_min] = 1

    # 3. Insertar la fila nueva en la posición c_max
    matriz_det.insert(c_max, fila_nueva)

    return matriz_det


def reducir_matriz(matriz: list[list[float]]) -> list[list[float]]:
    """
    Reduce una matriz de canal combinando columnas proporcionalmente equivalentes
    mediante la multiplicación iterativa por canales determinantes.
    Itera hasta que no queden columnas reducibles.
    """
    matriz_reducida = [fila[:] for fila in matriz]

    hubo_reduccion = True
    while hubo_reduccion:
        hubo_reduccion = False
        n_cols = len(matriz_reducida[0])

        for i in range(n_cols):
            for j in range(i + 1, n_cols):
                if se_pueden_reducir(matriz_reducida, i, j):
                    mat_det = generar_matriz_determinante(matriz_reducida, i, j)
                    matriz_reducida = get_matriz_compuesta(matriz_reducida, mat_det)
                    hubo_reduccion = True
                    break
            if hubo_reduccion:
                break

    return matriz_reducida


def capacidad_canal_determinante(matriz: list[list[float]]) -> float:
    """
    a. Capacidad de un canal determinante:
       C = log2(número de salidas alcanzables) bits.
    """
    columnas = len(matriz[0])
    return round(math.log2(columnas), 4)


def capacidad_canal_sin_ruido(matriz: list[list[float]]) -> float:
    """
    b. Capacidad de un canal sin ruido:
       C = log2(número de entradas) bits.
    """
    filas = len(matriz)
    return round(math.log2(filas), 4)


def es_simetrico(matriz: list[list[float]]) -> bool:
    """Un canal es simétrico si es uniforme y todas las columnas son permutaciones entre sí."""
    if not es_uniforme(matriz):
        return False
    filas = len(matriz)
    cols = len(matriz[0])
    primera_col = sorted([matriz[i][0] for i in range(filas)])
    for j in range(1, cols):
        col_j = sorted([matriz[i][j] for i in range(filas)])
        if col_j != primera_col:
            return False
    return True



def maximizar_informacion_mutua(canal: list[list[float]], h: float = 0.001) -> tuple[float, float]:
    """
    Estima la capacidad de un canal binario mediante barrido de la probabilidad a priori omega en [0, 1]
    con paso h, calculando el máximo de la información mutua:
        C = max_omega I(A, B)

    Retorna:
        tuple[float, float]: (probabilidad_asociada_optima, capacidad_estimada)
    """
    capacidad = -1.0
    prob_optima = 0.0

    omega = 0.0
    while omega <= 1.0000001:
        p_apriori = [omega, 1.0 - omega]
        info = informacion_mutua(p_apriori, canal)

        if info > capacidad:
            capacidad = info
            prob_optima = omega

        omega += h

    return round(prob_optima, 4), round(capacidad, 4)


def capacidad_canal(matriz: list[list[float]], paso_h: float = 0.001) -> float:
    """
    Calcula la capacidad del canal C = max_P(X) I(A, B):
      - Independiente: C = 0 bits
      - Determinante:  C = log2(columnas)
      - Sin ruido:     C = log2(filas)
      - Uniforme:      C = log2(columnas) - H(fila)
      - Binario general (no uniforme): Se calcula maximizando la información mutua
        con barrido de paso h.
    """
    if es_independiente(matriz):
        return 0.0

    if es_canal_determinante(matriz):
        return capacidad_canal_determinante(matriz)

    if es_canal_sin_ruido(matriz):
        return capacidad_canal_sin_ruido(matriz)

    if es_uniforme(matriz):
        columnas = len(matriz[0])
        return round(math.log2(columnas) - entropia(matriz[0]), 4)

    # Si es un canal binario general (2 entradas), se calcula por maximización de I(A, B)
    if len(matriz) == 2:
        _, c_opt = maximizar_informacion_mutua(matriz, paso_h)
        return c_opt

    raise ValueError("El canal no es determinante, ni sin ruido, ni uniforme, ni binario.")


def clasificar_canal(matriz: list[list[float]], imprimir: bool = True) -> dict:
    """
    Clasifica un canal según todas las categorías de la Unidad 6 de la cátedra:
      - Sin Ruido: H(A/B) = 0 (a lo sumo un valor distinto de cero por columna).
      - Determinante: H(B/A) = 0 (exactamente un valor distinto de cero por fila).
      - Sin Pérdida ni Ruido: Ambos a la vez (matriz cuadrada permutación/identidad).
      - Uniforme: Cada fila es una permutación de la primera fila.
      - Simétrico: Cada fila y cada columna son permutaciones entre sí.
      - Independiente: Todas las filas son iguales (I(A, B) = 0, canal inútil).

    Retorna un diccionario con los booleanos de cada tipo y la capacidad teórica si aplica.
    Si imprimir=True, muestra un informe claro en consola.
    """
    sin_ruido = es_canal_sin_ruido(matriz)
    determinante = es_canal_determinante(matriz)
    ambos = sin_ruido and determinante
    simetrico = es_simetrico(matriz)

    filas = len(matriz)
    cols = len(matriz[0])
    capacidad = None
    detalle_cap = ""

    if ambos:
        capacidad = round(math.log2(filas), 4)
        detalle_cap = f"log2(filas) = log2({filas}) = {capacidad} bits"
    elif determinante:
        capacidad = round(math.log2(cols), 4)
        detalle_cap = f"log2(salidas) = log2({cols}) = {capacidad} bits"
    elif sin_ruido:
        capacidad = round(math.log2(filas), 4)
        detalle_cap = f"log2(entradas) = log2({filas}) = {capacidad} bits"
    elif filas == 2:
        p_opt, cap_est = maximizar_informacion_mutua(matriz, 0.001)
        capacidad = cap_est
        detalle_cap = f"Canal binario general: C = {cap_est} bits (con P(X=0) = {p_opt})"
    else:
        detalle_cap = "Canal ruidoso general (más de 2 entradas)"

    resultado = {
        "sin_ruido": sin_ruido,
        "determinante": determinante,
        "ambos": ambos,
        "simetrico": simetrico,
        "capacidad": capacidad,
        "detalle_capacidad": detalle_cap,
    }

    if imprimir:
        print("=== CLASIFICACIÓN DEL CANAL (Unidad 6) ===")
        print(f"Dimensiones: {filas} entradas x {cols} salidas")
        print(f"  • Sin Ruido:        {'SÍ' if sin_ruido else 'NO'}  (H(A/B) = 0)")
        print(f"  • Determinante:     {'SÍ' if determinante else 'NO'}  (H(B/A) = 0)")
        if ambos:
            print("  • ¡Canal Ideal! Es simultáneamente Sin Ruido y Determinante.")
        print(f"  • Simétrico:        {'SÍ' if simetrico else 'NO'}")
        print(f"  -> Capacidad:       {detalle_cap}")

    return resultado




def prob_error_canal(probs_a_priori: list[float], canal: list[list[float]], condicional: bool = False) -> float:
    """
    Calcula la probabilidad de error del canal según la regla de decisión de máxima posibilidad.

    Convención de Cátedra (Apunte págs. 85-86 y TP6 Ej. 29):
      - Por defecto (condicional=False): "Regla de decisión de máxima posibilidad" (Maximum Likelihood),
        donde para cada símbolo de salida Y=y se elige la entrada X=x que maximiza el elemento de la
        columna de la matriz del canal: max_x P(Y=y | X=x).
      - Si condicional=True: "Regla de máxima posibilidad condicional" (MAP),
        donde se maximiza la probabilidad a posteriori: max_x P(X=x) * P(Y=y | X=x).

    Parámetros:
        probs_a_priori (list[float]): Probabilidades de los símbolos de entrada P(X=x).
        canal (list[list[float]]): Matriz del canal donde canal[x][y] = P(Y=y | X=x).
        condicional (bool): False para Máxima Posibilidad (ML de cátedra), True para MAP.

    Retorna:
        float: Probabilidad de error PE redondeada a 4 decimales.
    """
    filas = len(canal)        # cantidad de valores de entrada X
    columnas = len(canal[0])  # cantidad de valores de salida Y

    p_acierto_total = 0.0

    # Recorremos cada posible símbolo recibido Y = y
    for y in range(columnas):
        if condicional:
            # MAP: maximiza P(X=x, Y=y) = P(X=x) * P(Y=y|X=x)
            criterio = [probs_a_priori[x] * canal[x][y] for x in range(filas)]
        else:
            # Máxima Posibilidad estándar de la cátedra: maximiza P(Y=y | X=x)
            criterio = [canal[x][y] for x in range(filas)]

        # Decisión d(y): índice de la entrada x elegida
        x_decision = criterio.index(max(criterio))

        # Probabilidad de acierto para esta salida: P(X = x_decision, Y = y)
        p_acierto_total += probs_a_priori[x_decision] * canal[x_decision][y]

    # Probabilidad de error total: P(E) = 1 - P(acierto)
    prob_error = 1.0 - p_acierto_total
    return round(prob_error, 4)


# ===========================================================================
# ALIASES DE COMPATIBILIDAD (Para soportar diferentes enunciados de TP y parcial)
# ===========================================================================
calcular_probabilidad_salida = probabilidad_salida
distribucion_salida = probabilidad_salida
calcular_probabilidad_a_posteriori = probabilidad_a_posteriori
calcular_probabilidad_conjunta = probabilidad_conjunta
calcular_probabilidad_a_priori = probabilidad_a_priori
probabilidades_condicionales = matriz_canal


