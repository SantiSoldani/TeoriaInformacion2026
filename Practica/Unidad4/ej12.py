'''
12. Desarrollar funciones en Python que resuelvan lo siguiente:
a. Dado un carácter, devolver un byte que represente su código ASCII (7 bits) y utilice
el bit menos significativo para almacenar la paridad del código.
b. Dado un byte que se obtuvo como resultado de la función anterior, verificar si es
correcto o tiene errores.
'''


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


if __name__ == "__main__":
    print("=== Pruebas del Ejercicio 12 ===")

    caracteres = ['A', 'B', 'C', '1', ' ']

    for c in caracteres:
        byte_cod = caracter_a_byte_paridad(c, tipo_paridad="par")
        valido = verificar_byte(byte_cod, tipo_paridad="par")
        caracter_recuperado = extraer_caracter(byte_cod, tipo_paridad="par")

        print(f"Carácter: '{c}' (ASCII={ord(c)}, bin={format(ord(c), '07b')})")
        print(f"  -> Byte generado: {byte_cod} (binario: {format(byte_cod, '08b')})")
        print(f"  -> ¿Es válido?: {valido}")
        print(f"  -> Carácter recuperado: '{caracter_recuperado}'")

        # Simulamos un error invirtiendo el bit menos significativo
        byte_con_error = byte_cod ^ 1
        valido_error = verificar_byte(byte_con_error, tipo_paridad="par")
        print(f"  -> Simulando error (bit invertido): {format(byte_con_error, '08b')} -> ¿Es válido?: {valido_error}\n")
