'''
2. Codificar una función en Python que reciba como parámetros dos cadenas de caracteres
que contengan secuencias de entrada y de salida de un canal y retorne la matriz que
representa dicho canal.
'''

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

if __name__ == "__main__":
    # Prueba con datos del Ejercicio 1 del TP6:
    entrada = "abcacaabbcacaabcacaaabcaca"
    salida = "01010110011001000100010011"
    mat = matriz_canal(entrada, salida)
    print("=== Matriz del Canal (Ej 1 TP6) ===")
    print("Salidas: ['0', '1']")
    for fila, s in zip(mat, sorted(set(entrada))):
        print(f"  {s}: {fila}")
