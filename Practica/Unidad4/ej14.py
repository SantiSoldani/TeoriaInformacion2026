'''
14. Codificar funciones en Python que resuelvan lo siguiente:
a. Dada una cadena de caracteres, generar una secuencia de bytes (bytearray) que
contenga su representación con código ASCII y sus bits de paridad vertical,
longitudinal y cruzada.
b. Dada una secuencia de bytes que se obtuvo como resultado de la función anterior,
devolver el mensaje original o una cadena de caracteres vacía si no se pueden
corregir los errores.
'''


def caracter_a_byte_paridad(caracter: str, tipo_paridad: str = "par") -> int:
    """
    Convierte un carácter en un byte de 8 bits:
      - Bits 7 a 1: Código ASCII (7 bits).
      - Bit 0: Bit de paridad longitudinal (LRC).
    """
    if len(caracter) != 1:
        raise ValueError("Se debe ingresar exactamente un carácter.")

    codigo_ascii = ord(caracter)
    if codigo_ascii > 127:
        raise ValueError("El carácter debe pertenecer a la tabla ASCII estándar (0 a 127).")

    unos = bin(codigo_ascii).count("1")

    if tipo_paridad == "par":
        bit_paridad = 1 if (unos % 2 != 0) else 0
    else:
        bit_paridad = 1 if (unos % 2 == 0) else 0

    return (codigo_ascii << 1) | bit_paridad


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


def decodificar_mensaje(datos: bytearray) -> str:
    """
    b. Dada la secuencia de bytes con paridad vertical, longitudinal y cruzada:
       - Si no hay errores, devuelve el mensaje original.
       - Si hay un error simple (1 bit), lo detecta, lo corrige y devuelve el mensaje.
       - Si hay errores no corregibles, devuelve una cadena vacía "".
    """
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


if __name__ == "__main__":
    mensaje_original = "HOLA"
    print("=== Mensaje original ===")
    print("Texto:", mensaje_original)

    # Codificamos
    datos_codificados = codificar_mensaje(mensaje_original)
    print("\nBytes generados (Fila 0 paridad + datos):")
    for i, b in enumerate(datos_codificados):
        tipo = "VRC+Cruzada (Fila 0)" if i == 0 else f"Carácter '{mensaje_original[i-1]}'"
        print(f"  Byte {i}: {format(b, '08b')} ({tipo})")

    # 1. Decodificación limpia (sin ruido)
    recuperado = decodificar_mensaje(datos_codificados)
    print("\n1. Decodificación sin ruido:", recuperado)

    # 2. Simulamos 1 error (alteramos 1 bit en el carácter 'O', fila 2)
    datos_con_1_error = bytearray(datos_codificados)
    datos_con_1_error[2] ^= 0b00000100  # invertimos un bit
    print("\n2. Simulando 1 error aislado en la transmisión...")
    recuperado_corregido = decodificar_mensaje(datos_con_1_error)
    print("  -> Mensaje recuperado tras autocorrección:", recuperado_corregido)

    # 3. Simulamos 2 errores en la misma fila (no corregible)
    datos_con_2_errores = bytearray(datos_codificados)
    datos_con_2_errores[1] ^= 0b00000110  # invertimos dos bits
    print("\n3. Simulando 2 errores en un mismo carácter...")
    recuperado_fallido = decodificar_mensaje(datos_con_2_errores)
    print("  -> Mensaje recuperado (debe ser vacío):", repr(recuperado_fallido))
