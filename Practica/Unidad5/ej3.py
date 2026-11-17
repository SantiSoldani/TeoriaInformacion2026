'''
3. Desarrollar dos funciones en Python que reciban como parámetro una lista con la
distribución de probabilidades de una fuente de información y generen una lista de
cadenas de caracteres con codificaciones binarias de Huffman y de Shannon-Fano.
'''

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


# Alias para permitir llamar shannon(...) directamente
shannon = shannon_fano


if __name__ == "__main__":
    print("=== Ejemplo de la consigna / texto ===")
    p_ejemplo = [0.4, 0.3, 0.2, 0.1]
    cod_sf1 = shannon_fano(p_ejemplo)
    cod_huf1 = huffman(p_ejemplo)
    print("Probabilidades:", p_ejemplo)
    print("Shannon-Fano:  ", cod_sf1)
    print("Huffman:       ", cod_huf1)

    print("\n=== Ejemplo de la Figura 15 (Apunte) ===")
    # Símbolos: s1=0.1, s2=0.3, s3=0.25, s4=0.15, s5=0.2
    simbolos = ["s1", "s2", "s3", "s4", "s5"]
    probs = [0.1, 0.3, 0.25, 0.15, 0.2]
    cod_sf2 = shannon_fano(probs)
    cod_huf2 = huffman(probs)

    print(f"{'Símbolo':<8}{'Prob':<8}{'Shannon-Fano':<16}{'Huffman':<10}")
    print("-" * 42)
    for s, p, csf, chuf in zip(simbolos, probs, cod_sf2, cod_huf2):
        print(f"{s:<8}{p:<8.2f}{csf:<16}{chuf:<10}")
