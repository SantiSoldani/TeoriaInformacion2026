'''
10. Implementar una función en Python que reciba una lista de cadenas de caracteres que
representa una codificación binaria y devuelva: la distancia de Hamming, la cantidad de
errores que se pueden detectar y la cantidad de errores que se pueden corregir.
'''


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


# Alias por comodidad
hamming = analizar_codigo_hamming



if __name__ == "__main__":
    print("=== Pruebas de Distancia de Hamming (Misma Longitud) ===")
    codigos_ej9 = {
        "Código 1": ['00', '01', '10', '11'],
        "Código 2": ['000', '100', '101', '111'],
        "Código 3": ['0000', '0011', '1010', '0101']
    }

    for nombre, c in codigos_ej9.items():
        d = distancia_hamming(c)
        print(f"{nombre}: palabras={c}")
        print(f"  -> Distancia de Hamming: {d}")
        print(f"  -> Errores detectables : {errores_detectables(d)}")
        print(f"  -> Errores corregibles : {errores_corregibles(d)}\n")

    print("=== Prueba Anexo: Distinta Longitud ===")
    codigo_mixto = ['01', '1010', '001']
    d_var = distancia_hamming_longitud_variable(codigo_mixto)
    print(f"Código con longitudes variadas: {codigo_mixto}")
    print(f"  -> Distancia calculada con caracteres extras: {d_var}")
