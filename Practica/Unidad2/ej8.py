'''
8. Realizar una función en Python que reciba como parámetro el valor ω de una fuente
binaria de memoria nula y, utilizando las funciones desarrolladas en el ejercicio 1, calcule la
entropía de la fuente.
'''

from ej1 import entropia_fuente

def entropia_fuente_binaria(omega, r = 2):
    """
    Recibe el parámetro omega (probabilidad de uno de los símbolos) de una fuente binaria
    de memoria nula y, utilizando la función entropia_fuente del ejercicio 1, calcula su entropía.
    """
    probabilidades = [omega, 1 - omega]
    return entropia_fuente(probabilidades, r)

if __name__ == '__main__':
    omega = 0.7
    print(f"Entropia de la fuente con omega = {omega}: {entropia_fuente_binaria(omega)}")
    
    # Comprobación de los casos del ejercicio 9
    casos = [0.25, 0.75, 0.5, 1.0, 0.0]
    for w in casos:
        print(f"  omega = {w:4}: H(S) = {entropia_fuente_binaria(w):.4f} bits")
