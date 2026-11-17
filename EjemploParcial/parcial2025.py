import math

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


def imprimirmatriz(matriz):
    for fila in matriz:
        print(fila)

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

def es_uniforme(matriz: list[list[float]]) -> bool:
    """Canal uniforme: todas las filas son permutaciones de la primera fila."""
    primera = sorted(matriz[0])
    for fila in matriz[1:]:
        if sorted(fila) != primera:
            return False
    return True

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


def es_independiente(matriz: list[list[float]]) -> bool:
    """Un canal es independiente si todas las filas son iguales (I(A, B) = 0)."""
    primera = matriz[0]
    for fila in matriz[1:]:
        for v1, v2 in zip(primera, fila):
            if not math.isclose(v1, v2, abs_tol=1e-5):
                return False
    return True


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
    uniforme = es_uniforme(matriz)
    simetrico = es_simetrico(matriz)
    indep = es_independiente(matriz)

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
    elif uniforme:
        h_fila = entropia(matriz[0])
        capacidad = round(math.log2(cols) - h_fila, 4)
        detalle_cap = f"log2(salidas) - H(fila) = {round(math.log2(cols), 4)} - {round(h_fila, 4)} = {capacidad} bits"
    elif indep:
        capacidad = 0.0
        detalle_cap = "Canal independiente: C = 0 bits"
    else:
        detalle_cap = "Canal ruidoso general (usar maximizar_informacion_mutua)"

    resultado = {
        "sin_ruido": sin_ruido,
        "determinante": determinante,
        "ambos": ambos,
        "uniforme": uniforme,
        "simetrico": simetrico,
        "independiente": indep,
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
        print(f"  • Uniforme:         {'SÍ' if uniforme else 'NO'}")
        print(f"  • Simétrico:        {'SÍ' if simetrico else 'NO'}")
        print(f"  • Independiente:    {'SÍ' if indep else 'NO'}  (I(A, B) = 0)")
        print(f"  -> Capacidad:       {detalle_cap}")

    return resultado

def ruido(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    a. Calcula la equivocación o ruido H(A/B) POR DEFINICIÓN:
       H(A/B) = sum_i sum_j P(a_i, b_j) * log2(1 / P(a_i/b_j))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    p_post = probabilidad_a_posteriori(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(probs_condicionales[0])):
            if p_xy[i][j] > 0 and p_post[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / p_post[i][j])
    return round(val, 4)


def perdida(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    b. Calcula la pérdida H(B/A) POR DEFINICIÓN:
       H(B/A) = sum_i sum_j P(a_i, b_j) * log2(1 / P(b_j/a_i))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(probs_condicionales[0])):
            if p_xy[i][j] > 0 and probs_condicionales[i][j] > 0:
                val += p_xy[i][j] * math.log2(1.0 / probs_condicionales[i][j])
    return round(val, 4)


def informacion_mutua(probs_a_priori: list[float], probs_condicionales: list[list[float]]) -> float:
    """
    d. Calcula la información mutua I(A, B) POR DEFINICIÓN:
       I(A, B) = sum_i sum_j P(a_i, b_j) * log2(P(a_i, b_j) / (P(a_i) * P(b_j)))
    """
    p_xy = probabilidad_conjunta(probs_a_priori, probs_condicionales)
    p_y = probabilidad_salida(probs_a_priori, probs_condicionales)
    val = 0.0
    for i in range(len(probs_a_priori)):
        for j in range(len(p_y)):
            if p_xy[i][j] > 0:
                denominador = probs_a_priori[i] * p_y[j]
                if denominador > 0:
                    val += p_xy[i][j] * math.log2(p_xy[i][j] / denominador)
    return round(val, 4)


def probabilidad_conjunta(p_x: list[float], canal: list[list[float]]) -> list[list[float]]:
    """Calcula P(X, Y) = P(X) * P(Y|X)."""
    num_entradas = len(p_x)
    num_salidas = len(canal[0])
    p_xy = [[0.0 for _ in range(num_salidas)] for _ in range(num_entradas)]
    for i in range(num_entradas):
        for j in range(num_salidas):
            p_xy[i][j] = p_x[i] * canal[i][j]
    return p_xy


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

def probabilidad_salida(p_x: list[float], canal: list[list[float]]) -> list[float]:
    """Calcula P(Y) = sum_x P(X) * P(Y|X)."""
    num_salidas = len(canal[0])
    num_entradas = len(p_x)
    p_y = [0.0] * num_salidas
    for j in range(num_salidas):
        for i in range(num_entradas):
            p_y[j] += p_x[i] * canal[i][j]
    return p_y


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
        c_opt = maximizar_informacion_mutua(matriz, paso_h)
        return c_opt

    raise ValueError("El canal no es determinante, ni sin ruido, ni uniforme, ni binario.")

if __name__ == "__main__": 
    entrada = "10100000101011101001111110011001"
    salida = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"
    mat = matriz_canal(entrada,salida)
    probs_a_priori = probabilidad_a_priori(entrada)
    print("Probabilidad a priori: ",probs_a_priori)
    imprimirmatriz(mat)
    clasificar_canal(mat)
    print("ruido: ", ruido(probs_a_priori, mat))
    print("perdida: ", perdida(probs_a_priori, mat))
    print("informacion mutua: ", informacion_mutua(probs_a_priori, mat))
    C = capacidad_canal(mat)
    print(C)



