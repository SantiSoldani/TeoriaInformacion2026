'''
7. Implementar funciones en Python que reciban como parámetros: una cadena de
caracteres que contenga un alfabeto fuente y una lista de cadenas de caracteres que
almacena una codificación en el alfabeto binario, y resuelvan lo siguiente:
a. Dada una cadena de caracteres con un mensaje escrito en el alfabeto fuente,
devolver una secuencia de bytes (bytearray) que contenga el mensaje codificado.
b. Dada una secuencia de bytes, decodificar y retornar el mensaje original.
Sugerencia: manipular el mensaje codificado como una cadena de caracteres de unos y
ceros, tanto para codificar como para decodificar, y realizar las conversiones entre binarios
y enteros con las funciones de casteo correspondientes.
'''


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


if __name__ == "__main__":
    alfafuente = "ABCDE"
    codigo = ["0", "110", "100", "101", "111"]
    mensaje = "ABCDEECDBABCEDBDEABCACBDADBC"

    print("=== Alfabeto y Códigos ===")
    for s, c in zip(alfafuente, codigo):
        print(f"  '{s}' -> {c}")

    print("\n=== Mensaje Original ===")
    print("Texto:   ", mensaje)
    print("Longitud:", len(mensaje), "caracteres")

    # Codificamos
    codificado = codificar(mensaje, alfafuente, codigo)
    print("\n=== Codificación ===")
    print("Bytearray generado:", codificado)
    print("Tamaño en bytes:   ", len(codificado))
    print("Padding (bits):    ", codificado[0])
    print("Bytes (en binario):", " ".join(format(b, "08b") for b in codificado))

    # Decodificamos
    recuperado = decodificar(codificado, alfafuente, codigo)
    print("\n=== Decodificación ===")
    print("Recuperado:", recuperado)
    print("¿Coincide?:", mensaje == recuperado)


