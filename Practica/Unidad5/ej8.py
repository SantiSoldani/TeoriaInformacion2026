'''
8. Codificar una función en Python que reciba como parámetros: una cadena de caracteres
con un mensaje y una secuencia de bytes (bytearray) con ese mensaje codificado y calcule
la tasa de compresión.
'''


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


if __name__ == "__main__":
    # Prueba con datos del Ejercicio 10 y 12 del TP5:
    # "XXXYZZZZ" (8 bytes) -> comprimido RLC: [88, 3, 89, 1, 90, 4] (6 bytes) -> Tasa = 8/6 = 4/3 = 1.3333
    msg = "XXXYZZZZ"
    cod = bytearray([88, 3, 89, 1, 90, 4])
    print(f"Mensaje: '{msg}' ({len(msg)} bytes)")
    print(f"Codificación: {list(cod)} ({len(cod)} bytes)")
    print(f"Tasa de compresión: {tasa_compresion(msg, cod):.4f} (esperado 4/3 = 1.3333)")


