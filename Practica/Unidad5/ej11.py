'''
11. Realizar una función en Python que reciba como parámetro una cadena de caracteres con
un mensaje y devuelva una secuencia de bytes (bytearray) que contenga el mensaje
comprimido con RLC, utilizando un byte para almacenar la representación en código ASCII
del carácter y otro byte para el número.
'''


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


# Aliases para compatibilidad con distintas convenciones de nombres
comprimirRLC = comprimir_rlc
descomprimirRLC = descomprimir_rlc


if __name__ == "__main__":
    ejemplos = [
        "XXXYZZZZ",
        "AAAABBBCCDAA",
        "UUOOOOAAAIEUUUU",
    ]

    print("=== Pruebas de Compresión y Descompresión RLC ===\n")
    for msg in ejemplos:
        comprimido = comprimir_rlc(msg)
        recuperado = descomprimir_rlc(comprimido)

        # Representamos los pares (carácter, cantidad)
        pares = [f"('{chr(comprimido[i])}', {comprimido[i+1]})" for i in range(0, len(comprimido), 2)]

        print(f"Original:     '{msg}' ({len(msg)} bytes)")
        print(f"Pares RLC:    {' '.join(pares)}")
        print(f"Bytearray:    {list(comprimido)} ({len(comprimido)} bytes)")
        print(f"Descomprimido:'{recuperado}'")
        print(f"¿Coincide?:   {msg == recuperado}\n")

